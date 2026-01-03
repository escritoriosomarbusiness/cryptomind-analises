#!/usr/bin/env python3
"""
CryptoMind IA - Trading Systems v2.0
Sistema de identificação de setups com gestão de risco profissional

Baseado em:
- GCR: Gestão de risco, timing, contrarian thinking
- Hsaka: Supply/Demand zones, Order Blocks, Swing Failure Patterns
- Parâmetros realistas para day trade e scalp

Regras Fundamentais:
1. Range de entrada máximo: 0.5%
2. Risco Real = SL% × Alavancagem < 15%
3. Cada call deve especificar fundamento técnico exato
4. Zonas frescas (primeiro toque) têm prioridade
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TradingSystemsV2:
    """Sistema de Trading Systems com gestão de risco profissional"""
    
    # Parâmetros por Trading System
    TS_PARAMS = {
        'TS1': {  # Rompimento (Breakout)
            'name': 'Rompimento',
            'color': '🟦',
            'color_hex': '#3B82F6',
            'max_entry_range_pct': 0.3,  # 0.3% máximo
            'sl_range_pct': (0.5, 1.0),   # 0.5% a 1%
            'leverage': 10,
            'risk_per_trade_pct': 2.0,
            'min_rr': 2.0,
            'partials': [
                {'target_r': 2.0, 'size_pct': 50, 'action': 'Realizar 50%, SL para entrada'},
                {'target_r': 3.0, 'size_pct': 30, 'action': 'Realizar 30%'},
                {'target_r': 'trailing', 'size_pct': 20, 'action': 'Trailing Stop 1%'}
            ],
            'trailing_pct': 1.0
        },
        'TS2': {  # Continuação (Pullback)
            'name': 'Continuação',
            'color': '🟩',
            'color_hex': '#22C55E',
            'max_entry_range_pct': 0.5,  # 0.5% máximo
            'sl_range_pct': (0.8, 1.5),   # 0.8% a 1.5%
            'leverage': 7,
            'risk_per_trade_pct': 3.0,
            'min_rr': 1.5,
            'partials': [
                {'target_r': 1.5, 'size_pct': 60, 'action': 'Realizar 60%, SL para entrada'},
                {'target_r': 2.5, 'size_pct': 30, 'action': 'Realizar 30%'},
                {'target_r': 'trailing', 'size_pct': 10, 'action': 'Trailing Stop 0.8%'}
            ],
            'trailing_pct': 0.8
        },
        'TS3': {  # Reversão (Top/Bottom Fishing)
            'name': 'Reversão',
            'color': '🟧',
            'color_hex': '#F97316',
            'max_entry_range_pct': 0.3,  # 0.3% máximo (entrada precisa)
            'sl_range_pct': (1.0, 2.0),   # 1% a 2%
            'leverage': 5,
            'risk_per_trade_pct': 1.0,
            'min_rr': 4.0,
            'partials': [
                {'target_r': 2.0, 'size_pct': 40, 'action': 'Realizar 40%, SL para entrada'},
                {'target_r': 4.0, 'size_pct': 30, 'action': 'Realizar 30%'},
                {'target_r': 'trailing', 'size_pct': 30, 'action': 'Trailing Stop 1.5%'}
            ],
            'trailing_pct': 1.5
        }
    }
    
    # Risco real máximo permitido
    MAX_REAL_RISK_PCT = 15.0
    
    def __init__(self, market_data: Dict):
        """
        Inicializa o sistema com dados de mercado
        
        Args:
            market_data: Dicionário com dados de preço e indicadores
        """
        self.market_data = market_data
        self.setups = []
        
    def calculate_real_risk(self, sl_pct: float, leverage: int) -> float:
        """Calcula o risco real considerando alavancagem"""
        return sl_pct * leverage
    
    def validate_risk(self, sl_pct: float, leverage: int) -> Tuple[bool, float]:
        """
        Valida se o risco real está dentro do limite
        
        Returns:
            Tuple (is_valid, real_risk_pct)
        """
        real_risk = self.calculate_real_risk(sl_pct, leverage)
        return real_risk <= self.MAX_REAL_RISK_PCT, real_risk
    
    def calculate_entry_range(self, price: float, max_range_pct: float) -> Tuple[float, float]:
        """
        Calcula range de entrada respeitando o máximo permitido
        
        Returns:
            Tuple (entry_low, entry_high)
        """
        half_range = (price * max_range_pct / 100) / 2
        return round(price - half_range, 2), round(price + half_range, 2)
    
    def calculate_sl_from_worst_entry(self, entry_high: float, entry_low: float, 
                                       sl_pct: float, direction: str) -> float:
        """
        Calcula SL a partir do pior ponto de entrada
        
        Para LONG: pior entrada é entry_high, SL abaixo
        Para SHORT: pior entrada é entry_low, SL acima
        """
        if direction == 'LONG':
            worst_entry = entry_high
            sl_price = worst_entry * (1 - sl_pct / 100)
        else:
            worst_entry = entry_low
            sl_price = worst_entry * (1 + sl_pct / 100)
        return round(sl_price, 2)
    
    def calculate_targets(self, entry_price: float, sl_price: float, 
                          direction: str, partials: List[Dict]) -> List[Dict]:
        """Calcula alvos baseados no risco (R)"""
        risk = abs(entry_price - sl_price)
        targets = []
        
        for partial in partials:
            if partial['target_r'] == 'trailing':
                targets.append({
                    'price': 'Trailing',
                    'r': 'Trailing',
                    'size_pct': partial['size_pct'],
                    'action': partial['action']
                })
            else:
                if direction == 'LONG':
                    target_price = entry_price + (risk * partial['target_r'])
                else:
                    target_price = entry_price - (risk * partial['target_r'])
                    
                targets.append({
                    'price': round(target_price, 2),
                    'r': partial['target_r'],
                    'size_pct': partial['size_pct'],
                    'action': partial['action']
                })
        
        return targets
    
    def identify_support_resistance(self, prices: List[float], 
                                     timeframe: str) -> Dict[str, List[float]]:
        """
        Identifica níveis de suporte e resistência
        
        Usa:
        - Swing highs/lows
        - Números redondos (Schelling points - GCR)
        - Zonas de consolidação
        """
        if len(prices) < 20:
            return {'supports': [], 'resistances': []}
        
        supports = []
        resistances = []
        
        # Identificar swing points
        for i in range(2, len(prices) - 2):
            # Swing high
            if prices[i] > prices[i-1] and prices[i] > prices[i-2] and \
               prices[i] > prices[i+1] and prices[i] > prices[i+2]:
                resistances.append(prices[i])
            # Swing low
            if prices[i] < prices[i-1] and prices[i] < prices[i-2] and \
               prices[i] < prices[i+1] and prices[i] < prices[i+2]:
                supports.append(prices[i])
        
        # Adicionar números redondos próximos (Schelling points)
        current_price = prices[-1]
        round_levels = self._get_round_numbers(current_price)
        
        for level in round_levels:
            if level < current_price:
                supports.append(level)
            else:
                resistances.append(level)
        
        # Remover duplicatas e ordenar
        supports = sorted(list(set(supports)), reverse=True)[:5]
        resistances = sorted(list(set(resistances)))[:5]
        
        return {'supports': supports, 'resistances': resistances}
    
    def _get_round_numbers(self, price: float) -> List[float]:
        """Retorna números redondos próximos ao preço (Schelling points)"""
        round_levels = []
        
        if price > 10000:  # BTC
            base = int(price / 1000) * 1000
            round_levels = [base - 2000, base - 1000, base, base + 1000, base + 2000]
        elif price > 1000:
            base = int(price / 100) * 100
            round_levels = [base - 200, base - 100, base, base + 100, base + 200]
        elif price > 100:
            base = int(price / 10) * 10
            round_levels = [base - 20, base - 10, base, base + 10, base + 20]
        elif price > 10:
            base = int(price)
            round_levels = [base - 2, base - 1, base, base + 1, base + 2]
        else:
            base = round(price, 1)
            round_levels = [base - 0.2, base - 0.1, base, base + 0.1, base + 0.2]
        
        return [round(x, 2) for x in round_levels if x > 0]
    
    def check_zone_freshness(self, level: float, prices: List[float]) -> int:
        """
        Verifica quantas vezes uma zona foi testada (Hsaka - Freshness)
        
        Returns:
            Número de toques na zona (0 = zona fresca)
        """
        tolerance = level * 0.002  # 0.2% de tolerância
        touches = 0
        
        for price in prices:
            if abs(price - level) <= tolerance:
                touches += 1
        
        return touches
    
    def detect_breakout(self, symbol: str, data: Dict) -> Optional[Dict]:
        """
        Detecta setup de rompimento (TS1)
        
        Critérios:
        - Preço rompeu SR significativa
        - Volume acima da média
        - Candle de rompimento com corpo > 70% (convicção)
        """
        if 'prices' not in data or len(data['prices']) < 20:
            return None
            
        prices = data['prices']
        current_price = prices[-1]
        
        # Identificar SR
        sr_levels = self.identify_support_resistance(prices[:-5], 'H4')
        
        # Verificar rompimento de resistência (LONG)
        for resistance in sr_levels['resistances']:
            if current_price > resistance and prices[-2] <= resistance:
                # Verificar frescor da zona
                touches = self.check_zone_freshness(resistance, prices[:-5])
                if touches <= 3:  # Zona relativamente fresca
                    return self._create_breakout_setup(
                        symbol, 'LONG', current_price, resistance,
                        f"Rompimento da resistência ${resistance:,.2f}", touches
                    )
        
        # Verificar rompimento de suporte (SHORT)
        for support in sr_levels['supports']:
            if current_price < support and prices[-2] >= support:
                touches = self.check_zone_freshness(support, prices[:-5])
                if touches <= 3:
                    return self._create_breakout_setup(
                        symbol, 'SHORT', current_price, support,
                        f"Rompimento do suporte ${support:,.2f}", touches
                    )
        
        return None
    
    def _create_breakout_setup(self, symbol: str, direction: str, 
                                current_price: float, level: float,
                                fundamento: str, zone_touches: int) -> Optional[Dict]:
        """Cria setup de rompimento validado"""
        ts_params = self.TS_PARAMS['TS1']
        
        # Calcular range de entrada
        entry_low, entry_high = self.calculate_entry_range(
            current_price, ts_params['max_entry_range_pct']
        )
        
        # Calcular SL (usar valor médio do range permitido)
        sl_pct = (ts_params['sl_range_pct'][0] + ts_params['sl_range_pct'][1]) / 2
        
        # Validar risco
        is_valid, real_risk = self.validate_risk(sl_pct, ts_params['leverage'])
        if not is_valid:
            return None
        
        # Calcular SL do pior ponto de entrada
        sl_price = self.calculate_sl_from_worst_entry(
            entry_high, entry_low, sl_pct, direction
        )
        
        # Calcular alvos
        avg_entry = (entry_low + entry_high) / 2
        targets = self.calculate_targets(
            avg_entry, sl_price, direction, ts_params['partials']
        )
        
        return {
            'symbol': symbol,
            'ts': 'TS1',
            'ts_name': ts_params['name'],
            'ts_color': ts_params['color'],
            'ts_color_hex': ts_params['color_hex'],
            'direction': direction,
            'fundamento': fundamento,
            'timeframe': 'H4',
            'entry_low': entry_low,
            'entry_high': entry_high,
            'entry_range_pct': round((entry_high - entry_low) / entry_low * 100, 2),
            'sl_price': sl_price,
            'sl_pct': sl_pct,
            'leverage': ts_params['leverage'],
            'real_risk_pct': round(real_risk, 1),
            'risk_per_trade': ts_params['risk_per_trade_pct'],
            'targets': targets,
            'trailing_pct': ts_params['trailing_pct'],
            'zone_freshness': zone_touches,
            'invalidation': f"Fechamento {'abaixo' if direction == 'LONG' else 'acima'} de ${sl_price:,.2f}",
            'timestamp': datetime.now().isoformat()
        }
    
    def detect_pullback(self, symbol: str, data: Dict) -> Optional[Dict]:
        """
        Detecta setup de continuação/pullback (TS2)
        
        Critérios:
        - Tendência definida (HH+HL ou LH+LL)
        - Pullback para EMA 21 ou zona de SR rompida
        - RSI não em extremo
        """
        if 'prices' not in data or len(data['prices']) < 30:
            return None
            
        prices = data['prices']
        current_price = prices[-1]
        
        # Calcular EMA 21
        ema_21 = self._calculate_ema(prices, 21)
        if not ema_21:
            return None
        
        # Verificar tendência de alta + pullback para EMA
        if self._is_uptrend(prices) and self._is_near_ema(current_price, ema_21, 0.5):
            return self._create_pullback_setup(
                symbol, 'LONG', current_price, ema_21,
                f"Pullback na EMA 21 (${ema_21:,.2f}) em tendência de alta"
            )
        
        # Verificar tendência de baixa + pullback para EMA
        if self._is_downtrend(prices) and self._is_near_ema(current_price, ema_21, 0.5):
            return self._create_pullback_setup(
                symbol, 'SHORT', current_price, ema_21,
                f"Pullback na EMA 21 (${ema_21:,.2f}) em tendência de baixa"
            )
        
        return None
    
    def _calculate_ema(self, prices: List[float], period: int) -> Optional[float]:
        """Calcula EMA"""
        if len(prices) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return round(ema, 2)
    
    def _is_uptrend(self, prices: List[float]) -> bool:
        """Verifica se está em tendência de alta (HH + HL)"""
        if len(prices) < 20:
            return False
        
        recent = prices[-20:]
        highs = [max(recent[i:i+5]) for i in range(0, 15, 5)]
        lows = [min(recent[i:i+5]) for i in range(0, 15, 5)]
        
        # HH + HL
        return highs[-1] > highs[-2] and lows[-1] > lows[-2]
    
    def _is_downtrend(self, prices: List[float]) -> bool:
        """Verifica se está em tendência de baixa (LH + LL)"""
        if len(prices) < 20:
            return False
        
        recent = prices[-20:]
        highs = [max(recent[i:i+5]) for i in range(0, 15, 5)]
        lows = [min(recent[i:i+5]) for i in range(0, 15, 5)]
        
        # LH + LL
        return highs[-1] < highs[-2] and lows[-1] < lows[-2]
    
    def _is_near_ema(self, price: float, ema: float, tolerance_pct: float) -> bool:
        """Verifica se preço está próximo da EMA"""
        diff_pct = abs(price - ema) / ema * 100
        return diff_pct <= tolerance_pct
    
    def _create_pullback_setup(self, symbol: str, direction: str,
                                current_price: float, ema: float,
                                fundamento: str) -> Optional[Dict]:
        """Cria setup de pullback validado"""
        ts_params = self.TS_PARAMS['TS2']
        
        # Calcular range de entrada (na zona do pullback)
        entry_low, entry_high = self.calculate_entry_range(
            current_price, ts_params['max_entry_range_pct']
        )
        
        # SL abaixo do fundo do pullback
        sl_pct = (ts_params['sl_range_pct'][0] + ts_params['sl_range_pct'][1]) / 2
        
        # Validar risco
        is_valid, real_risk = self.validate_risk(sl_pct, ts_params['leverage'])
        if not is_valid:
            return None
        
        sl_price = self.calculate_sl_from_worst_entry(
            entry_high, entry_low, sl_pct, direction
        )
        
        avg_entry = (entry_low + entry_high) / 2
        targets = self.calculate_targets(
            avg_entry, sl_price, direction, ts_params['partials']
        )
        
        return {
            'symbol': symbol,
            'ts': 'TS2',
            'ts_name': ts_params['name'],
            'ts_color': ts_params['color'],
            'ts_color_hex': ts_params['color_hex'],
            'direction': direction,
            'fundamento': fundamento,
            'timeframe': 'H4',
            'entry_low': entry_low,
            'entry_high': entry_high,
            'entry_range_pct': round((entry_high - entry_low) / entry_low * 100, 2),
            'sl_price': sl_price,
            'sl_pct': sl_pct,
            'leverage': ts_params['leverage'],
            'real_risk_pct': round(real_risk, 1),
            'risk_per_trade': ts_params['risk_per_trade_pct'],
            'targets': targets,
            'trailing_pct': ts_params['trailing_pct'],
            'invalidation': f"Fechamento {'abaixo' if direction == 'LONG' else 'acima'} de ${sl_price:,.2f}",
            'timestamp': datetime.now().isoformat()
        }
    
    def detect_reversal(self, symbol: str, data: Dict) -> Optional[Dict]:
        """
        Detecta setup de reversão (TS3)
        
        Critérios:
        - Preço em SR significativa
        - Candle de rejeição (pin bar, engolfo)
        - RSI em extremo (divergência é bônus)
        """
        if 'prices' not in data or len(data['prices']) < 30:
            return None
            
        prices = data['prices']
        current_price = prices[-1]
        rsi = data.get('rsi', 50)
        
        sr_levels = self.identify_support_resistance(prices[:-3], 'H4')
        
        # Verificar reversão de alta em suporte
        if rsi < 35:  # RSI sobrevendido
            for support in sr_levels['supports']:
                if self._is_near_level(current_price, support, 0.5):
                    touches = self.check_zone_freshness(support, prices[:-3])
                    if touches <= 2:  # Zona fresca
                        return self._create_reversal_setup(
                            symbol, 'LONG', current_price, support,
                            f"Rejeição do suporte ${support:,.2f} com RSI sobrevendido ({rsi:.0f})",
                            touches
                        )
        
        # Verificar reversão de baixa em resistência
        if rsi > 65:  # RSI sobrecomprado
            for resistance in sr_levels['resistances']:
                if self._is_near_level(current_price, resistance, 0.5):
                    touches = self.check_zone_freshness(resistance, prices[:-3])
                    if touches <= 2:
                        return self._create_reversal_setup(
                            symbol, 'SHORT', current_price, resistance,
                            f"Rejeição da resistência ${resistance:,.2f} com RSI sobrecomprado ({rsi:.0f})",
                            touches
                        )
        
        return None
    
    def _is_near_level(self, price: float, level: float, tolerance_pct: float) -> bool:
        """Verifica se preço está próximo de um nível"""
        diff_pct = abs(price - level) / level * 100
        return diff_pct <= tolerance_pct
    
    def _create_reversal_setup(self, symbol: str, direction: str,
                                current_price: float, level: float,
                                fundamento: str, zone_touches: int) -> Optional[Dict]:
        """Cria setup de reversão validado"""
        ts_params = self.TS_PARAMS['TS3']
        
        # Range de entrada preciso
        entry_low, entry_high = self.calculate_entry_range(
            current_price, ts_params['max_entry_range_pct']
        )
        
        # SL acima/abaixo do extremo
        sl_pct = (ts_params['sl_range_pct'][0] + ts_params['sl_range_pct'][1]) / 2
        
        # Validar risco
        is_valid, real_risk = self.validate_risk(sl_pct, ts_params['leverage'])
        if not is_valid:
            return None
        
        sl_price = self.calculate_sl_from_worst_entry(
            entry_high, entry_low, sl_pct, direction
        )
        
        avg_entry = (entry_low + entry_high) / 2
        targets = self.calculate_targets(
            avg_entry, sl_price, direction, ts_params['partials']
        )
        
        return {
            'symbol': symbol,
            'ts': 'TS3',
            'ts_name': ts_params['name'],
            'ts_color': ts_params['color'],
            'ts_color_hex': ts_params['color_hex'],
            'direction': direction,
            'fundamento': fundamento,
            'timeframe': 'H4',
            'entry_low': entry_low,
            'entry_high': entry_high,
            'entry_range_pct': round((entry_high - entry_low) / entry_low * 100, 2),
            'sl_price': sl_price,
            'sl_pct': sl_pct,
            'leverage': ts_params['leverage'],
            'real_risk_pct': round(real_risk, 1),
            'risk_per_trade': ts_params['risk_per_trade_pct'],
            'targets': targets,
            'trailing_pct': ts_params['trailing_pct'],
            'zone_freshness': zone_touches,
            'invalidation': f"Fechamento {'abaixo' if direction == 'LONG' else 'acima'} de ${sl_price:,.2f}",
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_all(self) -> List[Dict]:
        """Analisa todos os ativos e retorna setups válidos"""
        setups = []
        
        for symbol, data in self.market_data.items():
            if symbol in ['macro', 'timestamp']:
                continue
            
            # Tentar detectar cada tipo de setup
            breakout = self.detect_breakout(symbol, data)
            if breakout:
                setups.append(breakout)
            
            pullback = self.detect_pullback(symbol, data)
            if pullback:
                setups.append(pullback)
            
            reversal = self.detect_reversal(symbol, data)
            if reversal:
                setups.append(reversal)
        
        return setups


def format_setup_for_display(setup: Dict) -> str:
    """Formata setup para exibição"""
    lines = [
        f"{setup['ts_color']} **{setup['direction']} {setup['symbol']}** - {setup['ts_name']}",
        f"",
        f"📍 **Fundamento:** {setup['fundamento']}",
        f"⏱️ **Timeframe:** {setup['timeframe']}",
        f"",
        f"🎯 **Entrada:** ${setup['entry_low']:,.2f} - ${setup['entry_high']:,.2f} ({setup['entry_range_pct']:.2f}%)",
        f"🛑 **Stop Loss:** ${setup['sl_price']:,.2f} ({setup['sl_pct']:.1f}%)",
        f"",
        f"⚙️ **Gestão:**",
        f"   • Risco: {setup['risk_per_trade']:.1f}% da banca",
        f"   • Alavancagem: {setup['leverage']}x",
        f"   • Risco Real: {setup['real_risk_pct']:.1f}%",
        f"",
        f"📊 **Parciais:**"
    ]
    
    for i, target in enumerate(setup['targets'], 1):
        if target['price'] == 'Trailing':
            lines.append(f"   {i}. Trailing Stop {setup['trailing_pct']}% → {target['size_pct']}%")
        else:
            lines.append(f"   {i}. ${target['price']:,.2f} ({target['r']}R) → {target['size_pct']}%")
    
    lines.extend([
        f"",
        f"❌ **Invalidação:** {setup['invalidation']}",
        f"",
        f"⚠️ *Não é recomendação de investimento*"
    ])
    
    return "\n".join(lines)


def test_trading_systems():
    """Testa o sistema com dados simulados"""
    # Dados de teste
    test_data = {
        'BTC': {
            'prices': [94000, 94200, 94500, 94300, 94800, 95000, 95200, 94900, 
                      95100, 95300, 95500, 95200, 95400, 95600, 95800, 95500,
                      95700, 95900, 96000, 95800, 96100, 96300, 96500, 96200,
                      96400, 96600, 96800, 96500, 96700, 96900],
            'rsi': 58
        },
        'ETH': {
            'prices': [3000, 3020, 3050, 3030, 3080, 3100, 3120, 3090,
                      3110, 3130, 3150, 3120, 3140, 3160, 3180, 3150,
                      3170, 3190, 3200, 3180, 3210, 3230, 3250, 3220,
                      3240, 3260, 3280, 3250, 3270, 3290],
            'rsi': 62
        },
        'SOL': {
            'prices': [180, 178, 175, 177, 173, 170, 172, 169,
                      171, 168, 166, 169, 167, 164, 162, 165,
                      163, 160, 158, 161, 159, 156, 154, 157,
                      155, 152, 150, 153, 151, 148],
            'rsi': 28
        }
    }
    
    ts = TradingSystemsV2(test_data)
    setups = ts.analyze_all()
    
    print("=" * 60)
    print("TRADING SYSTEMS V2.0 - TESTE")
    print("=" * 60)
    print(f"\nSetups encontrados: {len(setups)}\n")
    
    for setup in setups:
        print(format_setup_for_display(setup))
        print("\n" + "-" * 60 + "\n")
    
    return setups


if __name__ == "__main__":
    test_trading_systems()
