#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de Calls v2.0
Sistema integrado para geração de calls profissionais

Integra:
- Trading Systems v2 (TS1, TS2, TS3)
- Risk Management v2
- Score de Confiança
- Formatação para Telegram e HTML
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Importar módulos
from trading_systems_v2 import TradingSystemsV2
from risk_management_v2 import RiskManagerV2, RiskValidation
from confidence_score import ConfidenceScoreCalculator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CallGeneratorV2:
    """Gerador de calls profissionais v2.0"""
    
    def __init__(self, account_balance: float = 10000.0):
        self.risk_manager = RiskManagerV2(account_balance)
        self.score_calculator = ConfidenceScoreCalculator()
        
    def generate_calls(self, market_data: Dict, macro_data: Dict) -> List[Dict]:
        """
        Gera calls validadas a partir dos dados de mercado
        
        Args:
            market_data: Dados de preço e indicadores por ativo
            macro_data: Dados macro (Fear & Greed, BTC.D, USDT.D)
            
        Returns:
            Lista de calls validadas
        """
        # Detectar setups
        ts = TradingSystemsV2(market_data)
        raw_setups = ts.analyze_all()
        
        validated_calls = []
        
        for setup in raw_setups:
            # Validar risco
            validation = self.risk_manager.validate_setup(setup)
            
            if not validation.is_valid:
                print(f"❌ Setup rejeitado: {setup['symbol']} {setup['direction']} - {validation.rejection_reason}")
                continue
            
            # Calcular score de confiança
            score_data = self.score_calculator.calculate(setup, macro_data)
            
            # Filtrar por score mínimo (5)
            if score_data['score'] < 5:
                print(f"⚠️ Score baixo: {setup['symbol']} {setup['direction']} - Score {score_data['score']}/10")
                continue
            
            # Calcular tamanho da posição
            position = self.risk_manager.calculate_position_size(setup)
            
            # Montar call completa
            call = {
                **setup,
                'score': score_data['score'],
                'score_label': score_data['label'],
                'score_stars': score_data['stars'],
                'validation': {
                    'is_valid': validation.is_valid,
                    'real_risk_pct': validation.real_risk_pct,
                    'risk_level': validation.risk_level.value,
                    'warnings': validation.warnings
                },
                'position': position
            }
            
            validated_calls.append(call)
        
        # Ordenar por score (maior primeiro)
        validated_calls.sort(key=lambda x: x['score'], reverse=True)
        
        return validated_calls
    
    def format_call_telegram(self, call: Dict) -> str:
        """Formata call para Telegram"""
        lines = [
            f"{call['ts_color']} **{call['direction']} {call['symbol']}** - {call['ts_name']}",
            f"",
            f"📊 Score: {call['score']}/10 ({call['score_label']})",
            f"",
            f"📍 **Fundamento:**",
            f"{call['fundamento']}",
            f"⏱️ Timeframe: {call['timeframe']}",
            f"",
            f"🎯 **Entrada:** ${call['entry_low']:,.2f} - ${call['entry_high']:,.2f}",
            f"   Range: {call['entry_range_pct']:.2f}%",
            f"",
            f"🛑 **Stop Loss:** ${call['sl_price']:,.2f} ({call['sl_pct']:.1f}%)",
            f"",
            f"⚙️ **Gestão:**",
            f"• Risco: {call['risk_per_trade']:.1f}% da banca",
            f"• Alavancagem: {call['leverage']}x",
            f"• Risco Real: {call['validation']['real_risk_pct']:.1f}%",
            f"",
            f"📈 **Parciais:**"
        ]
        
        for i, target in enumerate(call['targets'], 1):
            if target['price'] == 'Trailing':
                lines.append(f"{i}. Trailing Stop {call['trailing_pct']}% → {target['size_pct']}%")
            else:
                lines.append(f"{i}. ${target['price']:,.2f} ({target['r']}R) → {target['size_pct']}%")
                lines.append(f"   {target['action']}")
        
        lines.extend([
            f"",
            f"❌ **Invalidação:** {call['invalidation']}",
            f"",
            f"⚠️ Não é recomendação de investimento"
        ])
        
        return "\n".join(lines)
    
    def format_call_html(self, call: Dict) -> str:
        """Formata call para HTML"""
        targets_html = ""
        for i, target in enumerate(call['targets'], 1):
            if target['price'] == 'Trailing':
                targets_html += f"""
                <div class="partial">
                    <span class="partial-num">{i}.</span>
                    <span>Trailing Stop {call['trailing_pct']}%</span>
                    <span class="partial-size">{target['size_pct']}%</span>
                </div>
                """
            else:
                targets_html += f"""
                <div class="partial">
                    <span class="partial-num">{i}.</span>
                    <span>${target['price']:,.2f} ({target['r']}R)</span>
                    <span class="partial-size">{target['size_pct']}%</span>
                </div>
                <div class="partial-action">{target['action']}</div>
                """
        
        return f"""
        <div class="call-card" style="border-left: 4px solid {call['ts_color_hex']};">
            <div class="call-header">
                <span class="call-direction {'long' if call['direction'] == 'LONG' else 'short'}">
                    {call['direction']} {call['symbol']}
                </span>
                <span class="call-ts">{call['ts_name']}</span>
            </div>
            
            <div class="call-score">
                <span class="score-value">{call['score']}/10</span>
                <span class="score-label">{call['score_label']}</span>
                <span class="score-stars">{call['score_stars']}</span>
            </div>
            
            <div class="call-fundamento">
                <strong>Fundamento:</strong> {call['fundamento']}
            </div>
            
            <div class="call-timeframe">
                <strong>Timeframe:</strong> {call['timeframe']}
            </div>
            
            <div class="call-entry">
                <div class="entry-label">Entrada</div>
                <div class="entry-value">${call['entry_low']:,.2f} - ${call['entry_high']:,.2f}</div>
                <div class="entry-range">Range: {call['entry_range_pct']:.2f}%</div>
            </div>
            
            <div class="call-sl">
                <div class="sl-label">Stop Loss</div>
                <div class="sl-value">${call['sl_price']:,.2f}</div>
                <div class="sl-pct">{call['sl_pct']:.1f}%</div>
            </div>
            
            <div class="call-risk">
                <div class="risk-item">
                    <span>Risco:</span>
                    <span>{call['risk_per_trade']:.1f}% da banca</span>
                </div>
                <div class="risk-item">
                    <span>Alavancagem:</span>
                    <span>{call['leverage']}x</span>
                </div>
                <div class="risk-item">
                    <span>Risco Real:</span>
                    <span class="risk-real">{call['validation']['real_risk_pct']:.1f}%</span>
                </div>
            </div>
            
            <div class="call-targets">
                <div class="targets-label">Parciais</div>
                {targets_html}
            </div>
            
            <div class="call-invalidation">
                <strong>Invalidação:</strong> {call['invalidation']}
            </div>
            
            <div class="call-disclaimer">
                ⚠️ Não é recomendação de investimento
            </div>
        </div>
        """


def test_call_generator():
    """Testa o gerador de calls"""
    # Dados de teste simulando mercado real
    market_data = {
        'BTC': {
            'prices': [94000, 94200, 94500, 94300, 94800, 95000, 95200, 94900, 
                      95100, 95300, 95500, 95200, 95400, 95600, 95800, 95500,
                      95700, 95900, 96000, 95800, 96100, 96300, 96500, 96200,
                      96400, 96600, 96800, 96500, 96700, 96900],
            'rsi': 58,
            'ema_9': 96500,
            'ema_21': 96000,
            'ema_200': 92000
        },
        'ETH': {
            'prices': [3000, 3020, 3050, 3030, 3080, 3100, 3120, 3090,
                      3110, 3130, 3150, 3120, 3140, 3160, 3180, 3150,
                      3170, 3190, 3200, 3180, 3210, 3230, 3250, 3220,
                      3240, 3260, 3280, 3250, 3270, 3290],
            'rsi': 62,
            'ema_9': 3250,
            'ema_21': 3200,
            'ema_200': 3000
        },
        'SOL': {
            'prices': [180, 178, 175, 177, 173, 170, 172, 169,
                      171, 168, 166, 169, 167, 164, 162, 165,
                      163, 160, 158, 161, 159, 156, 154, 157,
                      155, 152, 150, 153, 151, 148],
            'rsi': 28,
            'ema_9': 152,
            'ema_21': 158,
            'ema_200': 170
        }
    }
    
    macro_data = {
        'fear_greed': 35,
        'btc_d': {
            'value': 56.5,
            'trend': 'bullish'
        },
        'usdt_d': {
            'value': 5.8,
            'trend': 'bearish',
            'below_emas': True
        }
    }
    
    generator = CallGeneratorV2(account_balance=10000)
    calls = generator.generate_calls(market_data, macro_data)
    
    print("=" * 70)
    print("CALL GENERATOR V2.0 - TESTE")
    print("=" * 70)
    print(f"\nCalls geradas: {len(calls)}\n")
    
    for call in calls:
        print(generator.format_call_telegram(call))
        print("\n" + "-" * 70 + "\n")
    
    return calls


if __name__ == "__main__":
    test_call_generator()
