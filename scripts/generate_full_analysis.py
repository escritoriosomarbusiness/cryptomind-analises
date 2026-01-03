#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de Análise Completa
==========================================
Integra todos os módulos:
- Análise multi-timeframe
- Trading Systems
- Score de confiança
- Gestão de risco
- Geração de HTML
"""

import os
import sys
import json
from datetime import datetime
import pytz

# Adicionar diretório de scripts ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from multi_timeframe_analyzer import run_analysis as run_multi_timeframe
from trading_systems import detect_setups_for_all_assets, TSType
from confidence_score import calculate_confidence_for_setup
from risk_management import RiskManager
from html_generator import generate_html_report

BR_TZ = pytz.timezone('America/Sao_Paulo')


def generate_full_analysis():
    """Gera análise completa integrando todos os módulos."""
    print("=" * 60)
    print("CryptoMind IA - Análise Completa v2.0")
    print("=" * 60)
    
    # 1. Carregar dados multi-timeframe existentes (para evitar rate limit)
    print("\n[1/4] Carregando dados multi-timeframe...")
    mtf_path = os.path.join(script_dir, '..', 'data', 'multi_timeframe_analysis.json')
    
    if os.path.exists(mtf_path):
        with open(mtf_path, 'r', encoding='utf-8') as f:
            mtf_data = json.load(f)
        print("   Dados carregados do cache")
    else:
        print("   Cache não encontrado, executando análise...")
        try:
            mtf_data = run_multi_timeframe()
            if not mtf_data:
                print("Erro: Não foi possível obter dados multi-timeframe")
                return None
        except Exception as e:
            print(f"Erro na análise multi-timeframe: {e}")
            return None
    
    # 2. Detectar Trading Systems
    print("[2/4] Detectando Trading Systems...")
    ts_results = detect_setups_for_all_assets(mtf_data)
    
    # 3. Calcular scores de confiança e planos de risco
    print("[3/4] Calculando scores e planos de risco...")
    market_context = {
        'dominance': mtf_data.get('dominance', {}),
        'fear_greed': mtf_data.get('fear_greed', {}),
        'market_summary': mtf_data.get('market_summary', {})
    }
    
    enhanced_setups = {}
    for symbol, setups in ts_results.get('setups', {}).items():
        enhanced_setups[symbol] = []
        asset_data = mtf_data.get('assets', {}).get(symbol, {})
        
        for setup in setups:
            # Recalcular score com módulo dedicado
            score, level = calculate_confidence_for_setup(
                asset_data,
                market_context,
                setup['ts_type'],
                setup['direction']
            )
            setup['confidence_score'] = score
            setup['confidence_level'] = level
            
            # Criar plano de risco
            risk_manager = RiskManager(setup)
            risk_plan = risk_manager.create_risk_plan()
            setup['risk_plan'] = risk_plan.to_dict()
            
            enhanced_setups[symbol].append(setup)
    
    # 4. Compilar resultado final
    print("[4/4] Compilando resultado final...")
    
    final_result = {
        'timestamp': datetime.now(BR_TZ).isoformat(),
        'date': datetime.now(BR_TZ).strftime('%d/%m/%Y'),
        'time': datetime.now(BR_TZ).strftime('%H:%M'),
        'version': '2.0',
        
        # Contexto macro
        'macro': {
            'fear_greed': mtf_data.get('fear_greed', {}),
            'dominance': mtf_data.get('dominance', {}),
            'market_summary': mtf_data.get('market_summary', {})
        },
        
        # Análise por ativo
        'assets': mtf_data.get('assets', {}),
        
        # Setups com gestão de risco
        'setups': enhanced_setups,
        
        # Resumo
        'summary': {
            'total_setups': sum(len(s) for s in enhanced_setups.values()),
            'high_confidence': sum(1 for s in sum(enhanced_setups.values(), []) if s['confidence_score'] >= 8),
            'medium_confidence': sum(1 for s in sum(enhanced_setups.values(), []) if 5 <= s['confidence_score'] < 8),
            'low_confidence': sum(1 for s in sum(enhanced_setups.values(), []) if s['confidence_score'] < 5),
            'by_ts_type': {
                'TS1': sum(1 for s in sum(enhanced_setups.values(), []) if s['ts_type'] == 'TS1'),
                'TS2': sum(1 for s in sum(enhanced_setups.values(), []) if s['ts_type'] == 'TS2'),
                'TS3': sum(1 for s in sum(enhanced_setups.values(), []) if s['ts_type'] == 'TS3')
            },
            'by_direction': {
                'LONG': sum(1 for s in sum(enhanced_setups.values(), []) if s['direction'] == 'LONG'),
                'SHORT': sum(1 for s in sum(enhanced_setups.values(), []) if s['direction'] == 'SHORT')
            }
        }
    }
    
    # Salvar resultado
    output_path = os.path.join(script_dir, '..', 'data', 'full_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)
    
    # Também salvar como latest
    latest_path = os.path.join(script_dir, '..', 'data', 'latest_full_analysis.json')
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Análise salva em: {output_path}")
    
    # Exibir resumo
    print_summary(final_result)
    
    return final_result


def print_summary(result: dict):
    """Exibe resumo da análise."""
    print("\n" + "=" * 60)
    print("RESUMO DA ANÁLISE")
    print("=" * 60)
    
    # Macro
    macro = result.get('macro', {})
    fg = macro.get('fear_greed', {})
    dom = macro.get('dominance', {})
    
    print(f"\n📊 Contexto Macro:")
    print(f"   Fear & Greed: {fg.get('value', 'N/A')} ({fg.get('classification', 'N/A')})")
    print(f"   BTC.D: {dom.get('btc_d', {}).get('dominance', 'N/A')}% - {dom.get('btc_d', {}).get('impact', 'N/A')}")
    print(f"   USDT.D: {dom.get('usdt_d', {}).get('dominance', 'N/A')}% - {dom.get('usdt_d', {}).get('impact', 'N/A')}")
    
    # Setups
    summary = result.get('summary', {})
    print(f"\n📈 Setups Identificados: {summary.get('total_setups', 0)}")
    print(f"   Alta Confiança: {summary.get('high_confidence', 0)}")
    print(f"   Média Confiança: {summary.get('medium_confidence', 0)}")
    print(f"   Baixa Confiança: {summary.get('low_confidence', 0)}")
    
    print(f"\n🎯 Por Tipo:")
    by_ts = summary.get('by_ts_type', {})
    print(f"   TS1 (Rompimento): {by_ts.get('TS1', 0)}")
    print(f"   TS2 (Continuação): {by_ts.get('TS2', 0)}")
    print(f"   TS3 (Reversão): {by_ts.get('TS3', 0)}")
    
    print(f"\n📍 Por Direção:")
    by_dir = summary.get('by_direction', {})
    print(f"   LONG: {by_dir.get('LONG', 0)}")
    print(f"   SHORT: {by_dir.get('SHORT', 0)}")
    
    # Melhores setups
    print("\n" + "=" * 60)
    print("MELHORES SETUPS (Score >= 5)")
    print("=" * 60)
    
    all_setups = []
    for symbol, setups in result.get('setups', {}).items():
        for setup in setups:
            setup['_symbol'] = symbol
            all_setups.append(setup)
    
    # Ordenar por score
    all_setups.sort(key=lambda x: x.get('confidence_score', 0), reverse=True)
    
    for setup in all_setups[:5]:  # Top 5
        if setup.get('confidence_score', 0) >= 5:
            ts_emoji = "🟦" if setup['ts_type'] == 'TS1' else "🟩" if setup['ts_type'] == 'TS2' else "🟧"
            print(f"\n{ts_emoji} {setup['direction']} {setup['_symbol']} - {setup['ts_name']}")
            print(f"   Score: {setup['confidence_score']}/10 ({setup['confidence_level']})")
            
            risk_plan = setup.get('risk_plan', {})
            entry = risk_plan.get('entry', {})
            print(f"   Entrada: ${entry.get('min', 0):.2f} - ${entry.get('max', 0):.2f}")
            print(f"   Stop: ${risk_plan.get('stop_loss', {}).get('price', 0):.2f}")
            
            rm = risk_plan.get('risk_management', {})
            print(f"   Risco: {rm.get('risk_percent', 0)}% | Alavancagem: {rm.get('suggested_leverage', 1)}x")


def main():
    """Função principal."""
    # Gerar análise completa
    result = generate_full_analysis()
    
    if result:
        # Gerar HTML
        print("\n[+] Gerando relatório HTML...")
        html = generate_html_report(result)
        
        # Salvar HTML
        html_path = os.path.join(script_dir, '..', 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML salvo em: {html_path}")
        print("\n" + "=" * 60)
        print("ANÁLISE COMPLETA FINALIZADA")
        print("=" * 60)
    else:
        print("❌ Erro ao gerar análise")


if __name__ == "__main__":
    main()
