#!/usr/bin/env python3
"""
CryptoMind IA - Algoritmo de Score de Confiança
===============================================
MÓDULO INTERNO - ALGORITMO PROPRIETÁRIO
Os critérios e pesos são confidenciais e não devem ser expostos ao usuário final.
O usuário verá apenas o score final (0-10) e a classificação (Alta/Média/Baixa).
"""

from typing import Dict, Tuple
from enum import Enum


class ConfidenceLevel(Enum):
    """Níveis de confiança."""
    HIGH = "ALTA"
    MEDIUM = "MÉDIA"
    LOW = "BAIXA"
    NO_SETUP = "SEM SETUP"


class ConfidenceScoreCalculator:
    """
    Calculadora de Score de Confiança.
    
    ALGORITMO PROPRIETÁRIO - NÃO EXPOR DETALHES AO USUÁRIO
    
    O score é calculado com base em múltiplos fatores:
    - Contexto macro (USDT.D, BTC.D, Fear & Greed)
    - Alinhamento de tendência em múltiplos timeframes
    - Indicadores técnicos
    - Critérios específicos do tipo de Trading System
    """
    
    # Pesos internos (CONFIDENCIAL)
    _WEIGHTS = {
        'macro': {
            'usdt_d': 1.0,
            'btc_d': 1.0,
            'fear_greed': 1.0
        },
        'trend': {
            'd1_alignment': 1.0,
            'h4_alignment': 1.0
        },
        'ts_specific': {
            'TS1': {  # Rompimento
                'volume': 1.0,
                'candle_strength': 1.0,
                'sr_tested': 1.0,
                'clear_path': 1.0,
                'adx_dmi': 1.0
            },
            'TS2': {  # Continuação
                'trend_strength': 1.0,
                'structure_confirmed': 1.0,
                'pullback_quality': 1.0,
                'ema_respect': 1.0,
                'macd_confirmation': 1.0
            },
            'TS3': {  # Reversão
                'rsi_extreme': 1.5,  # Peso maior
                'key_level': 1.5,    # Peso maior
                'divergence': 1.0,
                'rejection_candle': 1.0,
                'exhaustion_volume': 1.0
            }
        }
    }
    
    def __init__(self, asset_data: Dict, market_context: Dict, ts_type: str, direction: str):
        """
        Inicializa a calculadora.
        
        Args:
            asset_data: Dados do ativo
            market_context: Contexto de mercado
            ts_type: Tipo do Trading System (TS1, TS2, TS3)
            direction: Direção (LONG, SHORT)
        """
        self.asset = asset_data
        self.context = market_context
        self.ts_type = ts_type
        self.direction = direction
        self._score_breakdown = {}  # Para debug interno apenas
    
    def calculate(self) -> Tuple[int, ConfidenceLevel]:
        """
        Calcula o score de confiança.
        
        Returns:
            Tuple com (score 0-10, nível de confiança)
        """
        total_score = 0
        max_possible = 10
        
        # Componente 1: Macro (3 pontos)
        macro_score = self._calculate_macro_score()
        total_score += macro_score
        self._score_breakdown['macro'] = macro_score
        
        # Componente 2: Tendência (2 pontos)
        trend_score = self._calculate_trend_score()
        total_score += trend_score
        self._score_breakdown['trend'] = trend_score
        
        # Componente 3: Específico do TS (5 pontos)
        ts_score = self._calculate_ts_specific_score()
        total_score += ts_score
        self._score_breakdown['ts_specific'] = ts_score
        
        # Normalizar para 0-10
        final_score = min(int(total_score), 10)
        
        # Determinar nível
        level = self._get_confidence_level(final_score)
        
        return final_score, level
    
    def _calculate_macro_score(self) -> float:
        """Calcula pontuação do contexto macro."""
        score = 0.0
        is_long = self.direction == "LONG"
        
        # USDT.D
        usdt_d = self.context.get('dominance', {}).get('usdt_d', {})
        usdt_impact = usdt_d.get('impact', 'NEUTRO')
        
        if is_long:
            if usdt_impact == 'BULLISH':
                score += self._WEIGHTS['macro']['usdt_d']
            elif usdt_impact == 'NEUTRO':
                score += self._WEIGHTS['macro']['usdt_d'] * 0.5
        else:
            if usdt_impact == 'BEARISH':
                score += self._WEIGHTS['macro']['usdt_d']
            elif usdt_impact == 'NEUTRO':
                score += self._WEIGHTS['macro']['usdt_d'] * 0.5
        
        # BTC.D (para altcoins)
        symbol = self.asset.get('symbol', '')
        if symbol != 'BTC':
            btc_d = self.context.get('dominance', {}).get('btc_d', {})
            btc_impact = btc_d.get('impact', 'NEUTRO')
            
            # Para altcoins: BTC.D caindo é bullish
            if is_long:
                if btc_impact == 'BEARISH':  # BTC.D caindo
                    score += self._WEIGHTS['macro']['btc_d']
                elif btc_impact == 'NEUTRO':
                    score += self._WEIGHTS['macro']['btc_d'] * 0.5
            else:
                if btc_impact == 'BULLISH':  # BTC.D subindo
                    score += self._WEIGHTS['macro']['btc_d']
                elif btc_impact == 'NEUTRO':
                    score += self._WEIGHTS['macro']['btc_d'] * 0.5
        else:
            # BTC não é afetado por BTC.D da mesma forma
            score += self._WEIGHTS['macro']['btc_d'] * 0.5
        
        # Fear & Greed
        fg = self.context.get('fear_greed', {})
        fg_value = fg.get('value', 50)
        
        if is_long:
            # Medo = oportunidade de compra
            if fg_value < 25:
                score += self._WEIGHTS['macro']['fear_greed']
            elif fg_value < 40:
                score += self._WEIGHTS['macro']['fear_greed'] * 0.7
            elif fg_value < 50:
                score += self._WEIGHTS['macro']['fear_greed'] * 0.5
        else:
            # Ganância = oportunidade de venda
            if fg_value > 75:
                score += self._WEIGHTS['macro']['fear_greed']
            elif fg_value > 60:
                score += self._WEIGHTS['macro']['fear_greed'] * 0.7
            elif fg_value > 50:
                score += self._WEIGHTS['macro']['fear_greed'] * 0.5
        
        return min(score, 3.0)
    
    def _calculate_trend_score(self) -> float:
        """Calcula pontuação do alinhamento de tendência."""
        score = 0.0
        is_long = self.direction == "LONG"
        
        trend = self.asset.get('trend', {})
        trend_direction = trend.get('trend', 'NEUTRO')
        ema_alignment = trend.get('ema_alignment', 'MIXED')
        strength = trend.get('strength', 'FRACA')
        
        # Tendência D1/H4 alinhada
        if is_long:
            if trend_direction == 'BULLISH':
                score += self._WEIGHTS['trend']['d1_alignment']
                if strength in ['FORTE', 'MODERADA']:
                    score += self._WEIGHTS['trend']['h4_alignment'] * 0.5
            elif trend_direction == 'NEUTRO':
                score += self._WEIGHTS['trend']['d1_alignment'] * 0.5
        else:
            if trend_direction == 'BEARISH':
                score += self._WEIGHTS['trend']['d1_alignment']
                if strength in ['FORTE', 'MODERADA']:
                    score += self._WEIGHTS['trend']['h4_alignment'] * 0.5
            elif trend_direction == 'NEUTRO':
                score += self._WEIGHTS['trend']['d1_alignment'] * 0.5
        
        # EMA alignment
        if is_long and ema_alignment == 'BULLISH':
            score += self._WEIGHTS['trend']['h4_alignment'] * 0.5
        elif not is_long and ema_alignment == 'BEARISH':
            score += self._WEIGHTS['trend']['h4_alignment'] * 0.5
        
        return min(score, 2.0)
    
    def _calculate_ts_specific_score(self) -> float:
        """Calcula pontuação específica do Trading System."""
        if self.ts_type == 'TS1':
            return self._calculate_breakout_specific()
        elif self.ts_type == 'TS2':
            return self._calculate_continuation_specific()
        elif self.ts_type == 'TS3':
            return self._calculate_reversal_specific()
        return 0.0
    
    def _calculate_breakout_specific(self) -> float:
        """Critérios específicos para rompimento."""
        score = 0.0
        weights = self._WEIGHTS['ts_specific']['TS1']
        is_long = self.direction == "LONG"
        
        indicators = self.asset.get('indicators', {})
        trend = self.asset.get('trend', {})
        sr_levels = self.asset.get('sr_levels', {})
        
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', {})
        
        # Volume implícito (baseado em momentum)
        macd_histogram = macd.get('histogram', 0)
        if is_long and macd_histogram > 0:
            score += weights['volume']
        elif not is_long and macd_histogram < 0:
            score += weights['volume']
        
        # Força do candle (RSI não em extremo)
        if 40 <= rsi <= 60:
            score += weights['candle_strength']
        elif 35 <= rsi <= 65:
            score += weights['candle_strength'] * 0.5
        
        # SR testada (baseado em key levels)
        key_levels = sr_levels.get('key_levels', [])
        if len(key_levels) >= 3:
            score += weights['sr_tested']
        elif len(key_levels) >= 1:
            score += weights['sr_tested'] * 0.5
        
        # Caminho livre (distância para próxima SR)
        resistances = sr_levels.get('resistances', [])
        supports = sr_levels.get('supports', [])
        price = self.asset.get('price', 0)
        
        if is_long and resistances:
            distance = (resistances[0] - price) / price * 100
            if distance > 3:
                score += weights['clear_path']
            elif distance > 1.5:
                score += weights['clear_path'] * 0.5
        elif not is_long and supports:
            distance = (price - supports[0]) / price * 100
            if distance > 3:
                score += weights['clear_path']
            elif distance > 1.5:
                score += weights['clear_path'] * 0.5
        
        # ADX/DMI (baseado em MACD trend)
        macd_trend = macd.get('trend', 'NEUTRO')
        if is_long and macd_trend == 'BULLISH':
            score += weights['adx_dmi']
        elif not is_long and macd_trend == 'BEARISH':
            score += weights['adx_dmi']
        
        return min(score, 5.0)
    
    def _calculate_continuation_specific(self) -> float:
        """Critérios específicos para continuação."""
        score = 0.0
        weights = self._WEIGHTS['ts_specific']['TS2']
        is_long = self.direction == "LONG"
        
        trend = self.asset.get('trend', {})
        structure = self.asset.get('structure', {})
        indicators = self.asset.get('indicators', {})
        
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', {})
        
        # Força da tendência
        strength = trend.get('strength', 'FRACA')
        if strength == 'FORTE':
            score += weights['trend_strength']
        elif strength == 'MODERADA':
            score += weights['trend_strength'] * 0.7
        elif strength == 'CONSOLIDAÇÃO':
            score += weights['trend_strength'] * 0.3
        
        # Estrutura confirmada
        struct = structure.get('structure', 'INDEFINIDA')
        if is_long:
            if struct == 'ALTA':
                score += weights['structure_confirmed']
            elif struct == 'ALTA_FORMANDO':
                score += weights['structure_confirmed'] * 0.5
        else:
            if struct == 'BAIXA':
                score += weights['structure_confirmed']
            elif struct == 'BAIXA_FORMANDO':
                score += weights['structure_confirmed'] * 0.5
        
        # Qualidade do pullback (RSI em zona ideal)
        if 40 <= rsi <= 55:
            score += weights['pullback_quality']
        elif 35 <= rsi <= 60:
            score += weights['pullback_quality'] * 0.5
        
        # Respeito às EMAs
        ema_9 = trend.get('ema_9', 0)
        ema_21 = trend.get('ema_21', 0)
        price = self.asset.get('price', 0)
        
        if is_long:
            if price >= ema_9 and price >= ema_21:
                score += weights['ema_respect']
            elif price >= ema_21:
                score += weights['ema_respect'] * 0.5
        else:
            if price <= ema_9 and price <= ema_21:
                score += weights['ema_respect']
            elif price <= ema_21:
                score += weights['ema_respect'] * 0.5
        
        # Confirmação MACD
        macd_trend = macd.get('trend', 'NEUTRO')
        if is_long and macd_trend == 'BULLISH':
            score += weights['macd_confirmation']
        elif not is_long and macd_trend == 'BEARISH':
            score += weights['macd_confirmation']
        
        return min(score, 5.0)
    
    def _calculate_reversal_specific(self) -> float:
        """Critérios específicos para reversão."""
        score = 0.0
        weights = self._WEIGHTS['ts_specific']['TS3']
        is_long = self.direction == "LONG"
        
        indicators = self.asset.get('indicators', {})
        sr_levels = self.asset.get('sr_levels', {})
        
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', {})
        
        # RSI em extremo (peso maior)
        if is_long:
            if rsi < 25:
                score += weights['rsi_extreme']
            elif rsi < 30:
                score += weights['rsi_extreme'] * 0.7
            elif rsi < 35:
                score += weights['rsi_extreme'] * 0.4
        else:
            if rsi > 75:
                score += weights['rsi_extreme']
            elif rsi > 70:
                score += weights['rsi_extreme'] * 0.7
            elif rsi > 65:
                score += weights['rsi_extreme'] * 0.4
        
        # Nível chave (peso maior)
        key_levels = sr_levels.get('key_levels', [])
        supports = sr_levels.get('supports', [])
        resistances = sr_levels.get('resistances', [])
        price = self.asset.get('price', 0)
        
        # Verificar se está em nível chave
        is_at_key_level = False
        for kl in key_levels:
            if abs(price - kl) / price < 0.02:  # 2% de tolerância
                is_at_key_level = True
                break
        
        if is_at_key_level:
            score += weights['key_level']
        elif is_long and supports:
            # Próximo de suporte
            if abs(price - supports[0]) / price < 0.03:
                score += weights['key_level'] * 0.5
        elif not is_long and resistances:
            # Próximo de resistência
            if abs(price - resistances[0]) / price < 0.03:
                score += weights['key_level'] * 0.5
        
        # Divergência potencial (baseado em MACD histogram)
        histogram = macd.get('histogram', 0)
        if is_long and histogram > 0:
            score += weights['divergence']  # Histograma subindo em zona de sobrevenda
        elif not is_long and histogram < 0:
            score += weights['divergence']  # Histograma caindo em zona de sobrecompra
        
        # Candle de rejeição (inferido pelo RSI não em extremo absoluto)
        if is_long and 25 <= rsi <= 35:
            score += weights['rejection_candle'] * 0.5
        elif not is_long and 65 <= rsi <= 75:
            score += weights['rejection_candle'] * 0.5
        
        # Volume de exaustão (inferido)
        # Se MACD está virando, pode indicar exaustão
        macd_trend = macd.get('trend', 'NEUTRO')
        if is_long and macd_trend == 'BULLISH':
            score += weights['exhaustion_volume'] * 0.5
        elif not is_long and macd_trend == 'BEARISH':
            score += weights['exhaustion_volume'] * 0.5
        
        return min(score, 5.0)
    
    def _get_confidence_level(self, score: int) -> ConfidenceLevel:
        """Determina o nível de confiança baseado no score."""
        if score >= 8:
            return ConfidenceLevel.HIGH
        elif score >= 5:
            return ConfidenceLevel.MEDIUM
        elif score >= 3:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.NO_SETUP
    
    def get_breakdown(self) -> Dict:
        """
        Retorna o breakdown do score.
        
        APENAS PARA DEBUG INTERNO - NÃO EXPOR AO USUÁRIO
        """
        return self._score_breakdown.copy()


def calculate_confidence_for_setup(asset_data: Dict, market_context: Dict, 
                                   ts_type: str, direction: str) -> Tuple[int, str]:
    """
    Função de conveniência para calcular score de confiança.
    
    Args:
        asset_data: Dados do ativo
        market_context: Contexto de mercado
        ts_type: Tipo do TS (TS1, TS2, TS3)
        direction: Direção (LONG, SHORT)
    
    Returns:
        Tuple com (score, nível como string)
    """
    calculator = ConfidenceScoreCalculator(asset_data, market_context, ts_type, direction)
    score, level = calculator.calculate()
    return score, level.value


# Teste do módulo
if __name__ == "__main__":
    # Dados de teste
    test_asset = {
        'symbol': 'BTC',
        'price': 90000,
        'trend': {
            'trend': 'BULLISH',
            'strength': 'MODERADA',
            'ema_9': 89000,
            'ema_21': 88000,
            'ema_alignment': 'BULLISH'
        },
        'structure': {
            'structure': 'ALTA_FORMANDO'
        },
        'indicators': {
            'rsi': 55,
            'macd': {
                'trend': 'BULLISH',
                'histogram': 100
            }
        },
        'sr_levels': {
            'supports': [87000, 85000],
            'resistances': [93000, 95000],
            'key_levels': [85000, 90000, 95000]
        }
    }
    
    test_context = {
        'dominance': {
            'usdt_d': {'impact': 'BULLISH'},
            'btc_d': {'impact': 'NEUTRO'}
        },
        'fear_greed': {'value': 35}
    }
    
    print("=" * 50)
    print("Teste do Algoritmo de Score de Confiança")
    print("=" * 50)
    
    for ts in ['TS1', 'TS2', 'TS3']:
        for direction in ['LONG', 'SHORT']:
            score, level = calculate_confidence_for_setup(
                test_asset, test_context, ts, direction
            )
            print(f"{ts} {direction}: Score {score}/10 - {level}")
    
    print("\n✅ Algoritmo funcionando corretamente")
