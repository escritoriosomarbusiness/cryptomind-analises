#!/usr/bin/env python3
"""
CryptoMind IA - Sistema de Trading Systems
Implementa os 3 tipos de Trading Systems:
- TS1: Rompimento (Breakout)
- TS2: Continuação (Pullback)
- TS3: Reversão (Top/Bottom Fishing)
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import pytz

BR_TZ = pytz.timezone('America/Sao_Paulo')


class TSType(Enum):
    """Tipos de Trading Systems."""
    BREAKOUT = "TS1"      # Rompimento
    CONTINUATION = "TS2"  # Continuação/Pullback
    REVERSAL = "TS3"      # Reversão


class Direction(Enum):
    """Direção do trade."""
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class SetupConfig:
    """Configuração de gestão de risco por tipo de TS."""
    ts_type: TSType
    risk_percent: float      # % da banca por operação
    max_leverage: int        # Alavancagem máxima
    min_rr: float           # Risco/Retorno mínimo
    expected_winrate: str   # Taxa de acerto esperada
    partial_1_pct: float    # % para realizar na parcial 1
    partial_2_pct: float    # % para realizar na parcial 2
    trailing_pct: float     # % do trailing stop
    color: str              # Cor do card


# Configurações de gestão por TS
TS_CONFIGS = {
    TSType.BREAKOUT: SetupConfig(
        ts_type=TSType.BREAKOUT,
        risk_percent=2.0,
        max_leverage=10,
        min_rr=2.0,
        expected_winrate="45-55%",
        partial_1_pct=50,
        partial_2_pct=30,
        trailing_pct=1.0,
        color="#3B82F6"  # Azul
    ),
    TSType.CONTINUATION: SetupConfig(
        ts_type=TSType.CONTINUATION,
        risk_percent=3.0,
        max_leverage=7,
        min_rr=1.5,
        expected_winrate="55-65%",
        partial_1_pct=60,
        partial_2_pct=30,
        trailing_pct=0.8,
        color="#22C55E"  # Verde
    ),
    TSType.REVERSAL: SetupConfig(
        ts_type=TSType.REVERSAL,
        risk_percent=1.0,
        max_leverage=5,
        min_rr=4.0,
        expected_winrate="30-40%",
        partial_1_pct=40,
        partial_2_pct=30,
        trailing_pct=1.5,
        color="#F97316"  # Laranja
    )
}


@dataclass
class Setup:
    """Representa um setup de trade identificado."""
    symbol: str
    ts_type: TSType
    direction: Direction
    entry_zone: Tuple[float, float]
    stop_loss: float
    targets: List[float]
    risk_reward: float
    confidence_score: int  # 0-10
    reasoning: str
    timestamp: str
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            'symbol': self.symbol,
            'ts_type': self.ts_type.value,
            'ts_name': self._get_ts_name(),
            'direction': self.direction.value,
            'entry_zone': {
                'min': self.entry_zone[0],
                'max': self.entry_zone[1]
            },
            'stop_loss': self.stop_loss,
            'targets': self.targets,
            'risk_reward': self.risk_reward,
            'confidence_score': self.confidence_score,
            'confidence_level': self._get_confidence_level(),
            'reasoning': self.reasoning,
            'timestamp': self.timestamp,
            'config': self._get_config_dict()
        }
    
    def _get_ts_name(self) -> str:
        names = {
            TSType.BREAKOUT: "Rompimento",
            TSType.CONTINUATION: "Continuação",
            TSType.REVERSAL: "Reversão"
        }
        return names.get(self.ts_type, "Desconhecido")
    
    def _get_confidence_level(self) -> str:
        if self.confidence_score >= 8:
            return "ALTA"
        elif self.confidence_score >= 5:
            return "MÉDIA"
        elif self.confidence_score >= 3:
            return "BAIXA"
        else:
            return "SEM SETUP"
    
    def _get_config_dict(self) -> Dict:
        config = TS_CONFIGS.get(self.ts_type)
        if config:
            return {
                'risk_percent': config.risk_percent,
                'max_leverage': config.max_leverage,
                'min_rr': config.min_rr,
                'expected_winrate': config.expected_winrate,
                'partial_1_pct': config.partial_1_pct,
                'partial_2_pct': config.partial_2_pct,
                'trailing_pct': config.trailing_pct,
                'color': config.color
            }
        return {}


class TradingSystemDetector:
    """Detecta setups baseados nos Trading Systems definidos."""
    
    def __init__(self, asset_data: Dict, market_context: Dict):
        """
        Inicializa o detector.
        
        Args:
            asset_data: Dados do ativo (preço, indicadores, SR, etc.)
            market_context: Contexto de mercado (dominância, fear/greed, etc.)
        """
        self.asset = asset_data
        self.context = market_context
        self.symbol = asset_data.get('symbol', 'UNKNOWN')
        
    def detect_all_setups(self) -> List[Setup]:
        """Detecta todos os setups possíveis para o ativo."""
        setups = []
        
        # Detectar setups LONG
        long_setups = self._detect_direction_setups(Direction.LONG)
        setups.extend(long_setups)
        
        # Detectar setups SHORT
        short_setups = self._detect_direction_setups(Direction.SHORT)
        setups.extend(short_setups)
        
        # Filtrar setups com score mínimo
        valid_setups = [s for s in setups if s.confidence_score >= 3]
        
        # Ordenar por score
        valid_setups.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return valid_setups
    
    def _detect_direction_setups(self, direction: Direction) -> List[Setup]:
        """Detecta setups para uma direção específica."""
        setups = []
        
        # TS1 - Rompimento
        breakout = self._detect_breakout(direction)
        if breakout:
            setups.append(breakout)
        
        # TS2 - Continuação
        continuation = self._detect_continuation(direction)
        if continuation:
            setups.append(continuation)
        
        # TS3 - Reversão
        reversal = self._detect_reversal(direction)
        if reversal:
            setups.append(reversal)
        
        return setups
    
    def _detect_breakout(self, direction: Direction) -> Optional[Setup]:
        """
        Detecta setup de rompimento (TS1).
        
        Critérios LONG:
        - Preço próximo de resistência
        - Volume acima da média
        - Tendência de curto prazo favorável
        - RSI não sobrecomprado
        
        Critérios SHORT:
        - Preço próximo de suporte
        - Volume acima da média
        - Tendência de curto prazo favorável
        - RSI não sobrevendido
        """
        price = self.asset.get('price', 0)
        sr_levels = self.asset.get('sr_levels', {})
        trend = self.asset.get('trend', {})
        indicators = self.asset.get('indicators', {})
        
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', {})
        
        supports = sr_levels.get('supports', [])
        resistances = sr_levels.get('resistances', [])
        
        if direction == Direction.LONG:
            # Verificar se há resistência próxima para romper
            if not resistances:
                return None
            
            nearest_resistance = resistances[0]
            distance_to_resistance = (nearest_resistance - price) / price * 100
            
            # Preço deve estar próximo da resistência (até 5%)
            if distance_to_resistance > 5 or distance_to_resistance < -1:
                return None
            
            # RSI não pode estar muito sobrecomprado
            if rsi > 75:
                return None
            
            # Calcular score
            score = self._calculate_breakout_score(direction, rsi, macd, trend)
            
            if score < 3:
                return None
            
            # Definir níveis
            entry_min = price
            entry_max = nearest_resistance * 1.002  # 0.2% acima da resistência
            stop_loss = supports[0] if supports else price * 0.98
            
            # Calcular alvos baseados em R:R
            risk = entry_max - stop_loss
            target_1 = entry_max + (risk * 2)  # 2R
            target_2 = entry_max + (risk * 3)  # 3R
            target_3 = entry_max + (risk * 4)  # 4R
            
            rr = (target_1 - entry_max) / (entry_max - stop_loss) if (entry_max - stop_loss) > 0 else 0
            
            reasoning = f"Rompimento de resistência em ${nearest_resistance:.2f}. "
            reasoning += f"RSI em {rsi:.0f}, MACD {macd.get('trend', 'neutro')}."
            
            return Setup(
                symbol=self.symbol,
                ts_type=TSType.BREAKOUT,
                direction=direction,
                entry_zone=(round(entry_min, 2), round(entry_max, 2)),
                stop_loss=round(stop_loss, 2),
                targets=[round(target_1, 2), round(target_2, 2), round(target_3, 2)],
                risk_reward=round(rr, 2),
                confidence_score=score,
                reasoning=reasoning,
                timestamp=datetime.now(BR_TZ).isoformat()
            )
        
        else:  # SHORT
            # Verificar se há suporte próximo para romper
            if not supports:
                return None
            
            nearest_support = supports[0]
            distance_to_support = (price - nearest_support) / price * 100
            
            # Preço deve estar próximo do suporte (até 5%)
            if distance_to_support > 5 or distance_to_support < -1:
                return None
            
            # RSI não pode estar muito sobrevendido
            if rsi < 25:
                return None
            
            # Calcular score
            score = self._calculate_breakout_score(direction, rsi, macd, trend)
            
            if score < 3:
                return None
            
            # Definir níveis
            entry_max = price
            entry_min = nearest_support * 0.998  # 0.2% abaixo do suporte
            stop_loss = resistances[0] if resistances else price * 1.02
            
            # Calcular alvos
            risk = stop_loss - entry_min
            target_1 = entry_min - (risk * 2)
            target_2 = entry_min - (risk * 3)
            target_3 = entry_min - (risk * 4)
            
            rr = (entry_min - target_1) / (stop_loss - entry_min) if (stop_loss - entry_min) > 0 else 0
            
            reasoning = f"Rompimento de suporte em ${nearest_support:.2f}. "
            reasoning += f"RSI em {rsi:.0f}, MACD {macd.get('trend', 'neutro')}."
            
            return Setup(
                symbol=self.symbol,
                ts_type=TSType.BREAKOUT,
                direction=direction,
                entry_zone=(round(entry_min, 2), round(entry_max, 2)),
                stop_loss=round(stop_loss, 2),
                targets=[round(target_1, 2), round(target_2, 2), round(target_3, 2)],
                risk_reward=round(rr, 2),
                confidence_score=score,
                reasoning=reasoning,
                timestamp=datetime.now(BR_TZ).isoformat()
            )
    
    def _detect_continuation(self, direction: Direction) -> Optional[Setup]:
        """
        Detecta setup de continuação/pullback (TS2).
        
        Critérios LONG:
        - Tendência de alta estabelecida
        - Pullback para EMA 21 ou EMA 9
        - RSI entre 40-60 (não em extremo)
        - Estrutura de alta (HH+HL)
        
        Critérios SHORT:
        - Tendência de baixa estabelecida
        - Pullback para EMA 21 ou EMA 9
        - RSI entre 40-60
        - Estrutura de baixa (LH+LL)
        """
        price = self.asset.get('price', 0)
        trend = self.asset.get('trend', {})
        structure = self.asset.get('structure', {})
        indicators = self.asset.get('indicators', {})
        sr_levels = self.asset.get('sr_levels', {})
        
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', {})
        
        ema_9 = trend.get('ema_9', price)
        ema_21 = trend.get('ema_21', price)
        ema_50 = trend.get('ema_50', price)
        
        supports = sr_levels.get('supports', [])
        resistances = sr_levels.get('resistances', [])
        
        if direction == Direction.LONG:
            # Verificar tendência de alta
            trend_direction = trend.get('trend', 'NEUTRO')
            struct = structure.get('structure', 'INDEFINIDA')
            
            # Precisa de tendência bullish ou estrutura de alta
            if trend_direction == 'BEARISH' or struct in ['BAIXA', 'BAIXA_FORMANDO']:
                return None
            
            # Verificar pullback para EMAs
            distance_to_ema21 = abs(price - ema_21) / price * 100
            distance_to_ema9 = abs(price - ema_9) / price * 100
            
            # Preço deve estar próximo da EMA (pullback)
            is_pullback = (distance_to_ema21 < 1.5 and price >= ema_21 * 0.99) or \
                         (distance_to_ema9 < 1 and price >= ema_9 * 0.99)
            
            if not is_pullback:
                return None
            
            # RSI em zona neutra
            if rsi < 35 or rsi > 70:
                return None
            
            # Calcular score
            score = self._calculate_continuation_score(direction, rsi, macd, trend, structure)
            
            if score < 3:
                return None
            
            # Definir níveis
            entry_min = min(ema_9, ema_21) * 0.998
            entry_max = price * 1.002
            stop_loss = supports[0] if supports else ema_50 * 0.99
            
            # Alvos
            risk = entry_max - stop_loss
            target_1 = entry_max + (risk * 1.5)
            target_2 = entry_max + (risk * 2.5)
            target_3 = resistances[0] if resistances else entry_max + (risk * 3.5)
            
            rr = (target_1 - entry_max) / (entry_max - stop_loss) if (entry_max - stop_loss) > 0 else 0
            
            reasoning = f"Pullback na EMA 21 (${ema_21:.2f}) em tendência de alta. "
            reasoning += f"Estrutura: {struct}. RSI: {rsi:.0f}."
            
            return Setup(
                symbol=self.symbol,
                ts_type=TSType.CONTINUATION,
                direction=direction,
                entry_zone=(round(entry_min, 2), round(entry_max, 2)),
                stop_loss=round(stop_loss, 2),
                targets=[round(target_1, 2), round(target_2, 2), round(target_3, 2)],
                risk_reward=round(rr, 2),
                confidence_score=score,
                reasoning=reasoning,
                timestamp=datetime.now(BR_TZ).isoformat()
            )
        
        else:  # SHORT
            trend_direction = trend.get('trend', 'NEUTRO')
            struct = structure.get('structure', 'INDEFINIDA')
            
            if trend_direction == 'BULLISH' or struct in ['ALTA', 'ALTA_FORMANDO']:
                return None
            
            distance_to_ema21 = abs(price - ema_21) / price * 100
            distance_to_ema9 = abs(price - ema_9) / price * 100
            
            is_pullback = (distance_to_ema21 < 1.5 and price <= ema_21 * 1.01) or \
                         (distance_to_ema9 < 1 and price <= ema_9 * 1.01)
            
            if not is_pullback:
                return None
            
            if rsi < 30 or rsi > 65:
                return None
            
            score = self._calculate_continuation_score(direction, rsi, macd, trend, structure)
            
            if score < 3:
                return None
            
            entry_max = max(ema_9, ema_21) * 1.002
            entry_min = price * 0.998
            stop_loss = resistances[0] if resistances else ema_50 * 1.01
            
            risk = stop_loss - entry_min
            target_1 = entry_min - (risk * 1.5)
            target_2 = entry_min - (risk * 2.5)
            target_3 = supports[0] if supports else entry_min - (risk * 3.5)
            
            rr = (entry_min - target_1) / (stop_loss - entry_min) if (stop_loss - entry_min) > 0 else 0
            
            reasoning = f"Pullback na EMA 21 (${ema_21:.2f}) em tendência de baixa. "
            reasoning += f"Estrutura: {struct}. RSI: {rsi:.0f}."
            
            return Setup(
                symbol=self.symbol,
                ts_type=TSType.CONTINUATION,
                direction=direction,
                entry_zone=(round(entry_min, 2), round(entry_max, 2)),
                stop_loss=round(stop_loss, 2),
                targets=[round(target_1, 2), round(target_2, 2), round(target_3, 2)],
                risk_reward=round(rr, 2),
                confidence_score=score,
                reasoning=reasoning,
                timestamp=datetime.now(BR_TZ).isoformat()
            )
    
    def _detect_reversal(self, direction: Direction) -> Optional[Setup]:
        """
        Detecta setup de reversão (TS3).
        
        Critérios LONG (Bottom Fishing):
        - RSI sobrevendido (<30)
        - Preço em suporte forte
        - Divergência de alta (opcional)
        - Candle de rejeição (opcional)
        
        Critérios SHORT (Top Fishing):
        - RSI sobrecomprado (>70)
        - Preço em resistência forte
        - Divergência de baixa (opcional)
        """
        price = self.asset.get('price', 0)
        indicators = self.asset.get('indicators', {})
        sr_levels = self.asset.get('sr_levels', {})
        
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', {})
        
        supports = sr_levels.get('supports', [])
        resistances = sr_levels.get('resistances', [])
        key_levels = sr_levels.get('key_levels', [])
        
        if direction == Direction.LONG:
            # RSI deve estar sobrevendido ou próximo
            if rsi > 45:
                return None
            
            # Verificar se está em suporte forte
            if not supports:
                return None
            
            nearest_support = supports[0]
            distance_to_support = (price - nearest_support) / price * 100
            
            # Preço deve estar próximo do suporte (até 3%)
            if distance_to_support > 3:
                return None
            
            # Verificar se é um nível chave
            is_key_level = any(abs(nearest_support - kl) / nearest_support < 0.01 for kl in key_levels)
            
            # Calcular score
            score = self._calculate_reversal_score(direction, rsi, macd, is_key_level)
            
            if score < 3:
                return None
            
            # Definir níveis (stop mais apertado para reversão)
            entry_min = nearest_support * 0.998
            entry_max = nearest_support * 1.005
            stop_loss = nearest_support * 0.985  # 1.5% abaixo do suporte
            
            # Alvos maiores para compensar menor win rate
            risk = entry_max - stop_loss
            target_1 = entry_max + (risk * 4)
            target_2 = entry_max + (risk * 6)
            target_3 = resistances[0] if resistances else entry_max + (risk * 8)
            
            rr = (target_1 - entry_max) / (entry_max - stop_loss) if (entry_max - stop_loss) > 0 else 0
            
            reasoning = f"Reversão em suporte forte ${nearest_support:.2f}. "
            reasoning += f"RSI sobrevendido em {rsi:.0f}. "
            if is_key_level:
                reasoning += "Nível chave histórico."
            
            return Setup(
                symbol=self.symbol,
                ts_type=TSType.REVERSAL,
                direction=direction,
                entry_zone=(round(entry_min, 2), round(entry_max, 2)),
                stop_loss=round(stop_loss, 2),
                targets=[round(target_1, 2), round(target_2, 2), round(target_3, 2)],
                risk_reward=round(rr, 2),
                confidence_score=score,
                reasoning=reasoning,
                timestamp=datetime.now(BR_TZ).isoformat()
            )
        
        else:  # SHORT
            if rsi < 55:
                return None
            
            if not resistances:
                return None
            
            nearest_resistance = resistances[0]
            distance_to_resistance = (nearest_resistance - price) / price * 100
            
            if distance_to_resistance > 3:
                return None
            
            is_key_level = any(abs(nearest_resistance - kl) / nearest_resistance < 0.01 for kl in key_levels)
            
            score = self._calculate_reversal_score(direction, rsi, macd, is_key_level)
            
            if score < 3:
                return None
            
            entry_max = nearest_resistance * 1.002
            entry_min = nearest_resistance * 0.995
            stop_loss = nearest_resistance * 1.015
            
            risk = stop_loss - entry_min
            target_1 = entry_min - (risk * 4)
            target_2 = entry_min - (risk * 6)
            target_3 = supports[0] if supports else entry_min - (risk * 8)
            
            rr = (entry_min - target_1) / (stop_loss - entry_min) if (stop_loss - entry_min) > 0 else 0
            
            reasoning = f"Reversão em resistência forte ${nearest_resistance:.2f}. "
            reasoning += f"RSI sobrecomprado em {rsi:.0f}. "
            if is_key_level:
                reasoning += "Nível chave histórico."
            
            return Setup(
                symbol=self.symbol,
                ts_type=TSType.REVERSAL,
                direction=direction,
                entry_zone=(round(entry_min, 2), round(entry_max, 2)),
                stop_loss=round(stop_loss, 2),
                targets=[round(target_1, 2), round(target_2, 2), round(target_3, 2)],
                risk_reward=round(rr, 2),
                confidence_score=score,
                reasoning=reasoning,
                timestamp=datetime.now(BR_TZ).isoformat()
            )
    
    def _calculate_breakout_score(self, direction: Direction, rsi: float, macd: Dict, trend: Dict) -> int:
        """Calcula score para setup de rompimento."""
        score = 0
        
        # Contexto macro (3 pontos)
        score += self._get_macro_score(direction)
        
        # Tendência alinhada (2 pontos)
        trend_dir = trend.get('trend', 'NEUTRO')
        if direction == Direction.LONG and trend_dir == 'BULLISH':
            score += 2
        elif direction == Direction.SHORT and trend_dir == 'BEARISH':
            score += 2
        elif trend_dir == 'NEUTRO':
            score += 1
        
        # RSI favorável (2 pontos)
        if direction == Direction.LONG:
            if 40 <= rsi <= 60:
                score += 2
            elif 30 <= rsi <= 70:
                score += 1
        else:
            if 40 <= rsi <= 60:
                score += 2
            elif 30 <= rsi <= 70:
                score += 1
        
        # MACD favorável (2 pontos)
        macd_trend = macd.get('trend', 'NEUTRO')
        if direction == Direction.LONG and macd_trend == 'BULLISH':
            score += 2
        elif direction == Direction.SHORT and macd_trend == 'BEARISH':
            score += 2
        elif macd_trend == 'NEUTRO':
            score += 1
        
        # EMA alignment (1 ponto)
        ema_align = trend.get('ema_alignment', 'MIXED')
        if direction == Direction.LONG and ema_align == 'BULLISH':
            score += 1
        elif direction == Direction.SHORT and ema_align == 'BEARISH':
            score += 1
        
        return min(score, 10)
    
    def _calculate_continuation_score(self, direction: Direction, rsi: float, macd: Dict, trend: Dict, structure: Dict) -> int:
        """Calcula score para setup de continuação."""
        score = 0
        
        # Contexto macro (3 pontos)
        score += self._get_macro_score(direction)
        
        # Tendência forte (2 pontos)
        trend_dir = trend.get('trend', 'NEUTRO')
        strength = trend.get('strength', 'FRACA')
        
        if direction == Direction.LONG and trend_dir == 'BULLISH':
            score += 2 if strength == 'FORTE' else 1
        elif direction == Direction.SHORT and trend_dir == 'BEARISH':
            score += 2 if strength == 'FORTE' else 1
        
        # Estrutura confirmada (2 pontos)
        struct = structure.get('structure', 'INDEFINIDA')
        if direction == Direction.LONG and struct == 'ALTA':
            score += 2
        elif direction == Direction.LONG and struct == 'ALTA_FORMANDO':
            score += 1
        elif direction == Direction.SHORT and struct == 'BAIXA':
            score += 2
        elif direction == Direction.SHORT and struct == 'BAIXA_FORMANDO':
            score += 1
        
        # RSI em zona ideal (2 pontos)
        if 40 <= rsi <= 55:
            score += 2
        elif 35 <= rsi <= 65:
            score += 1
        
        # MACD confirmando (1 ponto)
        macd_trend = macd.get('trend', 'NEUTRO')
        if direction == Direction.LONG and macd_trend == 'BULLISH':
            score += 1
        elif direction == Direction.SHORT and macd_trend == 'BEARISH':
            score += 1
        
        return min(score, 10)
    
    def _calculate_reversal_score(self, direction: Direction, rsi: float, macd: Dict, is_key_level: bool) -> int:
        """Calcula score para setup de reversão."""
        score = 0
        
        # Contexto macro (3 pontos)
        score += self._get_macro_score(direction)
        
        # RSI em extremo (3 pontos)
        if direction == Direction.LONG:
            if rsi < 25:
                score += 3
            elif rsi < 30:
                score += 2
            elif rsi < 35:
                score += 1
        else:
            if rsi > 75:
                score += 3
            elif rsi > 70:
                score += 2
            elif rsi > 65:
                score += 1
        
        # Nível chave (2 pontos)
        if is_key_level:
            score += 2
        
        # MACD divergência potencial (2 pontos)
        histogram = macd.get('histogram', 0)
        if direction == Direction.LONG and histogram > 0:
            score += 2  # Histograma subindo em zona de sobrevenda
        elif direction == Direction.SHORT and histogram < 0:
            score += 2  # Histograma caindo em zona de sobrecompra
        
        return min(score, 10)
    
    def _get_macro_score(self, direction: Direction) -> int:
        """Calcula pontuação do contexto macro."""
        score = 0
        
        # USDT.D
        usdt_d = self.context.get('dominance', {}).get('usdt_d', {})
        usdt_impact = usdt_d.get('impact', 'NEUTRO')
        
        if direction == Direction.LONG and usdt_impact == 'BULLISH':
            score += 1
        elif direction == Direction.SHORT and usdt_impact == 'BEARISH':
            score += 1
        
        # BTC.D (para altcoins)
        if self.symbol != 'BTC':
            btc_d = self.context.get('dominance', {}).get('btc_d', {})
            btc_impact = btc_d.get('impact', 'NEUTRO')
            
            if direction == Direction.LONG and btc_impact == 'BULLISH':
                score += 1
            elif direction == Direction.SHORT and btc_impact == 'BEARISH':
                score += 1
        else:
            score += 1  # BTC não é afetado por BTC.D da mesma forma
        
        # Fear & Greed
        fg = self.context.get('fear_greed', {})
        fg_value = fg.get('value', 50)
        
        if direction == Direction.LONG and fg_value < 30:
            score += 1  # Medo = oportunidade de compra
        elif direction == Direction.SHORT and fg_value > 70:
            score += 1  # Ganância = oportunidade de venda
        
        return score


def detect_setups_for_all_assets(analysis_data: Dict) -> Dict:
    """
    Detecta setups para todos os ativos.
    
    Args:
        analysis_data: Dados da análise multi-timeframe
    
    Returns:
        Dicionário com setups por ativo
    """
    results = {
        'timestamp': datetime.now(BR_TZ).isoformat(),
        'setups': {},
        'summary': {
            'total_setups': 0,
            'long_setups': 0,
            'short_setups': 0,
            'by_ts_type': {
                'TS1': 0,
                'TS2': 0,
                'TS3': 0
            }
        }
    }
    
    market_context = {
        'dominance': analysis_data.get('dominance', {}),
        'fear_greed': analysis_data.get('fear_greed', {}),
        'market_summary': analysis_data.get('market_summary', {})
    }
    
    for symbol, asset_data in analysis_data.get('assets', {}).items():
        detector = TradingSystemDetector(asset_data, market_context)
        setups = detector.detect_all_setups()
        
        results['setups'][symbol] = [s.to_dict() for s in setups]
        
        # Atualizar resumo
        for setup in setups:
            results['summary']['total_setups'] += 1
            if setup.direction == Direction.LONG:
                results['summary']['long_setups'] += 1
            else:
                results['summary']['short_setups'] += 1
            results['summary']['by_ts_type'][setup.ts_type.value] += 1
    
    return results


def main():
    """Função principal para teste."""
    # Carregar dados da análise multi-timeframe
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '..', 'data', 'multi_timeframe_analysis.json')
    
    if not os.path.exists(input_path):
        print("Erro: Execute primeiro o multi_timeframe_analyzer.py")
        return
    
    with open(input_path, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    print("=" * 60)
    print("CryptoMind IA - Detecção de Trading Systems")
    print("=" * 60)
    
    # Detectar setups
    results = detect_setups_for_all_assets(analysis_data)
    
    # Salvar resultados
    output_path = os.path.join(script_dir, '..', 'data', 'trading_setups.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSetups salvos em: {output_path}")
    
    # Exibir resumo
    summary = results['summary']
    print(f"\n{'=' * 60}")
    print("RESUMO DOS SETUPS")
    print(f"{'=' * 60}")
    print(f"Total de Setups: {summary['total_setups']}")
    print(f"Setups LONG: {summary['long_setups']}")
    print(f"Setups SHORT: {summary['short_setups']}")
    print(f"\nPor Tipo:")
    print(f"  TS1 (Rompimento): {summary['by_ts_type']['TS1']}")
    print(f"  TS2 (Continuação): {summary['by_ts_type']['TS2']}")
    print(f"  TS3 (Reversão): {summary['by_ts_type']['TS3']}")
    
    # Exibir setups por ativo
    print(f"\n{'=' * 60}")
    print("SETUPS POR ATIVO")
    print(f"{'=' * 60}")
    
    for symbol, setups in results['setups'].items():
        if setups:
            print(f"\n{symbol}:")
            for setup in setups:
                ts_name = setup['ts_name']
                direction = setup['direction']
                score = setup['confidence_score']
                level = setup['confidence_level']
                entry = setup['entry_zone']
                
                print(f"  {direction} - {ts_name} | Score: {score}/10 ({level})")
                print(f"    Entrada: ${entry['min']:.2f} - ${entry['max']:.2f}")
                print(f"    Stop: ${setup['stop_loss']:.2f}")
                print(f"    Alvos: {', '.join([f'${t:.2f}' for t in setup['targets']])}")
        else:
            print(f"\n{symbol}: Nenhum setup identificado")
    
    return results


if __name__ == "__main__":
    main()
