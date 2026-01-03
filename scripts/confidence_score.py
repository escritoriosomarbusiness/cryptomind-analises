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
            'TS1': {
                'volume': 1.0,
                'candle_strength': 1.0,
                'sr_tested': 1.0,
                'clear_path': 1.0,
                'adx': 1.0
            },
            'TS2': {
                'ema_touch': 1.0,
                'trend_strength': 1.0,
                'pullback_depth': 1.0,
                'volume_dry': 1.0,
                'higher_tf_support': 1.0
            },
            'TS3': {
                'divergence': 1.5,
                'extreme_rsi': 1.0,
                'sr_rejection': 1.0,
                'reversal_candle': 1.0,
                'volume_spike': 0.5
            }
        }
    }
    
    def __init__(self):
        """Inicializa a calculadora de score"""
        pass
    
    def calculate(self, setup: Dict, macro_data: Dict) -> Dict:
        """
        Calcula o score de confiança para um setup.
        
        Args:
            setup: Dicionário com dados do setup
            macro_data: Dados macro (Fear & Greed, BTC.D, USDT.D)
            
        Returns:
            Dicionário com score, label e stars
        """
        total_score = 0.0
        
        direction = setup.get('direction', 'LONG')
        ts = setup.get('ts', 'TS1')
        symbol = setup.get('symbol', '')
        is_long = direction == 'LONG'
        
        # Componente 1: Macro (3 pontos)
        macro_score = self._calc_macro(macro_data, is_long, symbol)
        total_score += macro_score
        
        # Componente 2: Tendência (2 pontos)
        trend_score = self._calc_trend(setup, is_long)
        total_score += trend_score
        
        # Componente 3: Específico do TS (5 pontos)
        ts_score = self._calc_ts_specific(setup, ts)
        total_score += ts_score
        
        # Normalizar para 0-10
        final_score = min(int(round(total_score)), 10)
        
        # Determinar nível e estrelas
        if final_score >= 8:
            level = ConfidenceLevel.HIGH
            stars = "⭐⭐⭐"
        elif final_score >= 5:
            level = ConfidenceLevel.MEDIUM
            stars = "⭐⭐"
        elif final_score >= 3:
            level = ConfidenceLevel.LOW
            stars = "⭐"
        else:
            level = ConfidenceLevel.NO_SETUP
            stars = "❌"
        
        return {
            'score': final_score,
            'label': level.value,
            'stars': stars
        }
    
    def _calc_macro(self, macro_data: Dict, is_long: bool, symbol: str) -> float:
        """Calcula pontuação do contexto macro (máx 3 pontos)"""
        score = 0.0
        
        # Fear & Greed (1 ponto)
        fg = macro_data.get('fear_greed', 50)
        if is_long:
            # Para LONG: medo (< 40) é bom, ganância (> 60) é ruim
            if fg < 30:
                score += 1.0
            elif fg < 45:
                score += 0.7
            elif fg < 55:
                score += 0.5
            elif fg < 70:
                score += 0.3
            # > 70: 0 pontos
        else:
            # Para SHORT: ganância é bom
            if fg > 70:
                score += 1.0
            elif fg > 55:
                score += 0.7
            elif fg > 45:
                score += 0.5
            elif fg > 30:
                score += 0.3
        
        # USDT.D (1 ponto)
        usdt_d = macro_data.get('usdt_d', {})
        usdt_below_emas = usdt_d.get('below_emas', False)
        usdt_trend = usdt_d.get('trend', 'neutral')
        
        if is_long:
            # USDT.D caindo = bullish para cripto
            if usdt_below_emas and usdt_trend == 'bearish':
                score += 1.0
            elif usdt_below_emas:
                score += 0.5
        else:
            # USDT.D subindo = bearish para cripto
            if not usdt_below_emas and usdt_trend == 'bullish':
                score += 1.0
            elif not usdt_below_emas:
                score += 0.5
        
        # BTC.D (1 ponto) - apenas para altcoins
        if symbol != 'BTC':
            btc_d = macro_data.get('btc_d', {})
            btc_trend = btc_d.get('trend', 'neutral')
            
            if is_long:
                # BTC.D caindo = bullish para altcoins
                if btc_trend == 'bearish':
                    score += 1.0
                elif btc_trend == 'neutral':
                    score += 0.5
            else:
                # BTC.D subindo = bearish para altcoins
                if btc_trend == 'bullish':
                    score += 1.0
                elif btc_trend == 'neutral':
                    score += 0.5
        else:
            # Para BTC, dar ponto neutro
            score += 0.5
        
        return min(score, 3.0)
    
    def _calc_trend(self, setup: Dict, is_long: bool) -> float:
        """Calcula pontuação de alinhamento de tendência (máx 2 pontos)"""
        score = 0.0
        
        # Verificar se preço está acima/abaixo das EMAs
        current_price = setup.get('current_price', 0)
        ema_9 = setup.get('ema_9', 0)
        ema_21 = setup.get('ema_21', 0)
        ema_200 = setup.get('ema_200', 0)
        
        if is_long:
            # Para LONG: preço acima das EMAs
            if current_price > ema_200:
                score += 0.5
            if current_price > ema_21:
                score += 0.5
            if ema_9 > ema_21:
                score += 0.5
            if ema_21 > ema_200:
                score += 0.5
        else:
            # Para SHORT: preço abaixo das EMAs
            if current_price < ema_200:
                score += 0.5
            if current_price < ema_21:
                score += 0.5
            if ema_9 < ema_21:
                score += 0.5
            if ema_21 < ema_200:
                score += 0.5
        
        return min(score, 2.0)
    
    def _calc_ts_specific(self, setup: Dict, ts: str) -> float:
        """Calcula pontuação específica do Trading System (máx 5 pontos)"""
        score = 0.0
        
        rsi = setup.get('rsi', 50)
        volume_above_avg = setup.get('volume_above_avg', False)
        sr_tested = setup.get('sr_tested', 1)
        candle_strength = setup.get('candle_strength', 0.5)
        
        if ts == 'TS1':  # Rompimento
            # Volume no rompimento
            if volume_above_avg:
                score += 1.0
            
            # Força do candle de rompimento
            if candle_strength > 0.7:
                score += 1.0
            elif candle_strength > 0.5:
                score += 0.5
            
            # SR testada múltiplas vezes
            if sr_tested >= 3:
                score += 1.0
            elif sr_tested >= 2:
                score += 0.5
            
            # RSI não em extremo
            if 40 <= rsi <= 60:
                score += 1.0
            elif 30 <= rsi <= 70:
                score += 0.5
            
            # Espaço para movimento
            score += 1.0  # Assumir que já foi validado
            
        elif ts == 'TS2':  # Continuação
            # Pullback tocou EMA
            if setup.get('touched_ema', False):
                score += 1.0
            
            # Tendência forte
            if setup.get('trend_strong', False):
                score += 1.0
            
            # Profundidade do pullback adequada
            pullback_depth = setup.get('pullback_depth', 0)
            if 0.3 <= pullback_depth <= 0.6:
                score += 1.0
            elif 0.2 <= pullback_depth <= 0.7:
                score += 0.5
            
            # Volume secando no pullback
            if setup.get('volume_dry', False):
                score += 1.0
            
            # Suporte em timeframe maior
            if setup.get('higher_tf_support', False):
                score += 1.0
            else:
                score += 0.5  # Dar meio ponto por padrão
            
        elif ts == 'TS3':  # Reversão
            # Divergência (peso maior)
            if setup.get('divergence', False):
                score += 1.5
            
            # RSI em extremo
            if rsi < 25 or rsi > 75:
                score += 1.0
            elif rsi < 30 or rsi > 70:
                score += 0.5
            
            # Rejeição de SR
            if setup.get('sr_rejection', False):
                score += 1.0
            
            # Candle de reversão
            if setup.get('reversal_candle', False):
                score += 1.0
            
            # Volume spike
            if volume_above_avg:
                score += 0.5
        
        return min(score, 5.0)


def test_score_calculator():
    """Testa a calculadora de score"""
    calc = ConfidenceScoreCalculator()
    
    # Setup de teste
    setup = {
        'symbol': 'ETH',
        'direction': 'LONG',
        'ts': 'TS2',
        'current_price': 3250,
        'ema_9': 3240,
        'ema_21': 3200,
        'ema_200': 3000,
        'rsi': 55,
        'volume_above_avg': False,
        'touched_ema': True,
        'trend_strong': True,
        'pullback_depth': 0.4,
        'volume_dry': True
    }
    
    macro = {
        'fear_greed': 35,
        'btc_d': {'trend': 'neutral'},
        'usdt_d': {'below_emas': True, 'trend': 'bearish'}
    }
    
    result = calc.calculate(setup, macro)
    
    print("=" * 50)
    print("CONFIDENCE SCORE CALCULATOR - TESTE")
    print("=" * 50)
    print(f"Score: {result['score']}/10")
    print(f"Label: {result['label']}")
    print(f"Stars: {result['stars']}")


if __name__ == "__main__":
    test_score_calculator()
