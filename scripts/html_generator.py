#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de HTML
==============================
Gera relatório HTML com cards coloridos por Trading System.
"""

import os
import json
from datetime import datetime


def generate_html_report(result: dict) -> str:
    """Gera relatório HTML com cards coloridos por TS."""
    
    # Gerar cards macro
    macro = result.get('macro', {})
    fg = macro.get('fear_greed', {})
    dom = macro.get('dominance', {})
    summary = macro.get('market_summary', {})
    
    fg_class = 'bullish' if fg.get('value', 50) < 40 else 'bearish' if fg.get('value', 50) > 60 else 'neutral'
    btc_class = 'bullish' if dom.get('btc_d', {}).get('impact') == 'BULLISH' else 'bearish' if dom.get('btc_d', {}).get('impact') == 'BEARISH' else 'neutral'
    usdt_class = 'bullish' if dom.get('usdt_d', {}).get('impact') == 'BULLISH' else 'bearish' if dom.get('usdt_d', {}).get('impact') == 'BEARISH' else 'neutral'
    
    macro_cards = f'''
        <div class="macro-card">
            <h3>Fear & Greed</h3>
            <div class="macro-value {fg_class}">{fg.get('value', 'N/A')}</div>
            <div class="macro-label">{fg.get('classification', 'N/A')}</div>
        </div>
        <div class="macro-card">
            <h3>BTC Dominance</h3>
            <div class="macro-value {btc_class}">{dom.get('btc_d', {}).get('dominance', 'N/A')}%</div>
            <div class="macro-label">{dom.get('btc_d', {}).get('impact', 'N/A')}</div>
        </div>
        <div class="macro-card">
            <h3>USDT Dominance</h3>
            <div class="macro-value {usdt_class}">{dom.get('usdt_d', {}).get('dominance', 'N/A')}%</div>
            <div class="macro-label">{dom.get('usdt_d', {}).get('impact', 'N/A')}</div>
        </div>
        <div class="macro-card">
            <h3>Sentimento Geral</h3>
            <div class="macro-value">{summary.get('sentiment', 'N/A')}</div>
            <div class="macro-label">Baseado em múltiplos fatores</div>
        </div>
    '''
    
    # Gerar cards de setups
    setup_cards = ''
    all_setups = []
    for symbol, setups in result.get('setups', {}).items():
        for setup in setups:
            setup['_symbol'] = symbol
            all_setups.append(setup)
    
    # Ordenar por score
    all_setups.sort(key=lambda x: x.get('confidence_score', 0), reverse=True)
    
    if not all_setups:
        setup_cards = '<div class="no-setups"><p>Nenhum setup identificado no momento.</p></div>'
    else:
        for setup in all_setups:
            ts_class = setup['ts_type'].lower()
            score = setup.get('confidence_score', 0)
            conf_class = 'confidence-high' if score >= 8 else 'confidence-medium' if score >= 5 else 'confidence-low'
            
            risk_plan = setup.get('risk_plan', {})
            entry = risk_plan.get('entry', {})
            stop = risk_plan.get('stop_loss', {})
            rm = risk_plan.get('risk_management', {})
            partials = risk_plan.get('partials', [])
            
            partials_html = ''
            for p in partials:
                if p['target_price'] == 'TRAILING':
                    partials_html += f'<div class="partial-item"><span>Trailing Stop</span><span>{p["size_percent"]}%</span></div>'
                else:
                    partials_html += f'<div class="partial-item"><span>${p["target_price"]:.2f} ({p["rr_ratio"]}R)</span><span>{p["size_percent"]}%</span></div>'
            
            setup_cards += f'''
            <div class="setup-card">
                <div class="setup-header {ts_class}">
                    <span class="setup-title">{setup['direction']} {setup['_symbol']}</span>
                    <span class="setup-badge">{setup['ts_name']}</span>
                </div>
                <div class="setup-body">
                    <div class="setup-score">
                        <span class="score-value {conf_class}">{score}/10</span>
                        <span class="score-label">{setup.get('confidence_level', 'N/A')}</span>
                    </div>
                    <div class="setup-details">
                        <div class="detail-row">
                            <span class="detail-label">Entrada</span>
                            <span class="detail-value">${entry.get('min', 0):.2f} - ${entry.get('max', 0):.2f}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Stop Loss</span>
                            <span class="detail-value">${stop.get('price', 0):.2f} ({stop.get('distance_percent', 0):.2f}%)</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Risco</span>
                            <span class="detail-value">{rm.get('risk_percent', 0)}% da banca</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Alavancagem</span>
                            <span class="detail-value">{rm.get('suggested_leverage', 1)}x (máx: {rm.get('max_leverage', 1)}x)</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">R:R</span>
                            <span class="detail-value">{risk_plan.get('metrics', {}).get('risk_reward', 0):.1f}</span>
                        </div>
                    </div>
                    <div class="partials-section">
                        <div class="detail-label" style="margin-bottom: 10px;">Plano de Parciais</div>
                        {partials_html}
                    </div>
                </div>
            </div>
            '''
    
    timestamp = result.get('timestamp', datetime.now().isoformat())
    
    # Template HTML completo
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptoMind IA - Análise de Trading</title>
    <style>
        :root {{
            --bg-primary: #0f0f0f;
            --bg-secondary: #1a1a1a;
            --bg-card: #242424;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent-blue: #3B82F6;
            --accent-green: #22C55E;
            --accent-orange: #F97316;
            --accent-red: #EF4444;
            --accent-yellow: #EAB308;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 30px;
        }}
        
        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .timestamp {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .macro-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .macro-card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        
        .macro-card h3 {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .macro-value {{
            font-size: 2rem;
            font-weight: bold;
        }}
        
        .macro-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 5px;
        }}
        
        .bullish {{ color: var(--accent-green); }}
        .bearish {{ color: var(--accent-red); }}
        .neutral {{ color: var(--accent-yellow); }}
        
        .section-title {{
            font-size: 1.5rem;
            margin: 40px 0 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #333;
        }}
        
        .setups-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .setup-card {{
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.2s;
        }}
        
        .setup-card:hover {{
            transform: translateY(-5px);
        }}
        
        .setup-header {{
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .setup-header.ts1 {{ background: linear-gradient(135deg, #3B82F6, #1D4ED8); }}
        .setup-header.ts2 {{ background: linear-gradient(135deg, #22C55E, #15803D); }}
        .setup-header.ts3 {{ background: linear-gradient(135deg, #F97316, #C2410C); }}
        
        .setup-title {{
            font-size: 1.1rem;
            font-weight: bold;
        }}
        
        .setup-badge {{
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
        }}
        
        .setup-body {{
            padding: 20px;
        }}
        
        .setup-score {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .score-value {{
            font-size: 2rem;
            font-weight: bold;
        }}
        
        .score-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        .confidence-high {{ color: var(--accent-green); }}
        .confidence-medium {{ color: var(--accent-yellow); }}
        .confidence-low {{ color: var(--accent-red); }}
        
        .setup-details {{
            display: grid;
            gap: 10px;
        }}
        
        .detail-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #333;
        }}
        
        .detail-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .detail-value {{
            font-weight: 500;
        }}
        
        .partials-section {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #333;
        }}
        
        .partial-item {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 0.85rem;
        }}
        
        .no-setups {{
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }}
        
        .legend {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }}
        
        .legend-color.ts1 {{ background: var(--accent-blue); }}
        .legend-color.ts2 {{ background: var(--accent-green); }}
        .legend-color.ts3 {{ background: var(--accent-orange); }}
        
        footer {{
            text-align: center;
            padding: 40px 0;
            color: var(--text-secondary);
            font-size: 0.85rem;
            border-top: 1px solid #333;
            margin-top: 40px;
        }}
        
        @media (max-width: 768px) {{
            .setups-grid {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>CryptoMind IA</h1>
            <p class="timestamp">Análise gerada em {timestamp}</p>
        </header>
        
        <section class="macro-section">
            {macro_cards}
        </section>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color ts1"></div>
                <span>TS1 - Rompimento</span>
            </div>
            <div class="legend-item">
                <div class="legend-color ts2"></div>
                <span>TS2 - Continuação</span>
            </div>
            <div class="legend-item">
                <div class="legend-color ts3"></div>
                <span>TS3 - Reversão</span>
            </div>
        </div>
        
        <h2 class="section-title">Setups Identificados</h2>
        
        <div class="setups-grid">
            {setup_cards}
        </div>
        
        <footer>
            <p>CryptoMind IA - Sistema de Análise Automatizada</p>
            <p>Disclaimer: Esta análise não constitui recomendação de investimento.</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html


def main():
    """Teste do gerador HTML."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'full_analysis.json')
    
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        html = generate_html_report(result)
        
        output_path = os.path.join(script_dir, '..', 'index.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML gerado: {output_path}")
    else:
        print("Erro: Arquivo de análise não encontrado")


if __name__ == "__main__":
    main()
