#!/usr/bin/env python3
"""
CryptoMind IA - Script Principal de Automação
Executa análise, gera HTML e publica no GitHub Pages
"""

import subprocess
import os
import sys
from datetime import datetime
import pytz

# Adicionar diretório de scripts ao path
sys.path.insert(0, '/home/ubuntu/cryptomind-analises/scripts')

from generate_analysis import CryptoAnalyzer
from generate_html import HTMLGenerator


def run_morning_analysis():
    """Executa análise da manhã (11:00 BRT)"""
    print("=" * 50)
    print("CRYPTOMIND IA - ANÁLISE DE ABERTURA")
    print("=" * 50)
    
    timezone = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(timezone)
    print(f"Data/Hora: {now.strftime('%d/%m/%Y %H:%M')} BRT")
    print()
    
    # 1. Executar análise
    print("[1/3] Coletando dados e gerando análises...")
    analyzer = CryptoAnalyzer()
    analysis = analyzer.run_analysis()
    print(f"✓ Análise concluída para {len(analysis['analyses'])} ativos")
    print()
    
    # 2. Gerar HTML
    print("[2/3] Gerando página HTML...")
    html_generator = HTMLGenerator()
    html_generator.run()
    print("✓ HTML gerado com sucesso")
    print()
    
    # 2.5. Arquivar análise
    print("[2.5/3] Arquivando análise...")
    from archive_manager import ArchiveManager
    manager = ArchiveManager()
    manager.archive_analysis('opening')
    print("✓ Análise arquivada")
    print()
    
    # 2.6. Reconstruir índices
    print("[2.6/3] Reconstruindo índices...")
    from index_builder import IndexBuilder
    builder = IndexBuilder()
    builder.build_all_indexes()
    print("✓ Índices atualizados")
    print()
    
    # 3. Publicar no GitHub
    print("[3/3] Publicando no GitHub Pages...")
    publish_to_github("Análise de abertura - " + now.strftime('%d/%m/%Y %H:%M'))
    print()
    
    print("=" * 50)
    print("ANÁLISE DE ABERTURA CONCLUÍDA!")
    print("=" * 50)
    
    return analysis


def run_closing_report():
    """Executa relatório de fechamento (21:05 BRT)"""
    print("=" * 50)
    print("CRYPTOMIND IA - RELATÓRIO DE FECHAMENTO")
    print("=" * 50)
    
    timezone = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(timezone)
    print(f"Data/Hora: {now.strftime('%d/%m/%Y %H:%M')} BRT")
    print()
    
    # 1. Gerar relatório de fechamento
    print("[1/3] Avaliando setups e gerando KPIs...")
    from generate_closing_report import ClosingReportGenerator
    report_generator = ClosingReportGenerator()
    report = report_generator.generate_report()
    print("✓ Relatório de fechamento gerado")
    print()
    
    # 2. Atualizar HTML com seção de fechamento
    print("[2/3] Atualizando página HTML com resultados...")
    update_html_with_closing(report)
    print("✓ HTML atualizado com KPIs")
    print()
    
    # 2.5. Arquivar relatório
    print("[2.5/3] Arquivando relatório...")
    from archive_manager import ArchiveManager
    manager = ArchiveManager()
    manager.archive_analysis('closing')
    print("✓ Relatório arquivado")
    print()
    
    # 2.6. Reconstruir índices
    print("[2.6/3] Reconstruindo índices...")
    from index_builder import IndexBuilder
    builder = IndexBuilder()
    builder.build_all_indexes()
    print("✓ Índices atualizados")
    print()
    
    # 3. Publicar no GitHub
    print("[3/3] Publicando no GitHub Pages...")
    publish_to_github("Relatório de fechamento - " + now.strftime('%d/%m/%Y %H:%M'))
    print()
    
    # Exibir resumo
    print_closing_summary(report)
    
    print("=" * 50)
    print("RELATÓRIO DE FECHAMENTO CONCLUÍDO!")
    print("=" * 50)
    
    return report


def update_html_with_closing(report):
    """Atualiza o HTML com a seção de fechamento"""
    import json
    
    # Gerar HTML da seção de fechamento
    closing_html = generate_closing_section_html(report)
    
    # Ler HTML atual
    html_path = "/home/ubuntu/cryptomind-analises/index.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Inserir seção de fechamento antes do disclaimer
    if '<!-- CLOSING_REPORT_SECTION -->' in html:
        # Substituir seção existente
        import re
        html = re.sub(
            r'<!-- CLOSING_REPORT_SECTION -->.*?<!-- /CLOSING_REPORT_SECTION -->',
            closing_html,
            html,
            flags=re.DOTALL
        )
    else:
        # Inserir nova seção
        html = html.replace(
            '<!-- Disclaimer -->',
            closing_html + '\n\n    <!-- Disclaimer -->'
        )
    
    # Salvar HTML atualizado
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_closing_section_html(report):
    """Gera HTML da seção de fechamento"""
    
    results = report.get('results', {})
    day_stats = report.get('day_stats', {})
    cumulative = report.get('cumulative_stats', {})
    
    # Gerar linhas da tabela de resultados
    result_rows = []
    for symbol, data in results.items():
        bias_result = data.get('bias_result', {}).get('result', '-')
        
        long_result = data.get('long_result', {}).get('result', '-') if data.get('long_result') else '-'
        long_pnl = data.get('long_result', {}).get('pnl', 0) if data.get('long_result') else 0
        
        short_result = data.get('short_result', {}).get('result', '-') if data.get('short_result') else '-'
        short_pnl = data.get('short_result', {}).get('pnl', 0) if data.get('short_result') else 0
        
        price_change = data.get('price_change', 0)
        change_class = 'positive' if price_change >= 0 else 'negative'
        
        result_rows.append(f'''
            <tr>
                <td class="asset-symbol">{symbol}</td>
                <td class="asset-change {change_class}">{price_change:+.2f}%</td>
                <td>{bias_result}</td>
                <td>{long_result} {f"({long_pnl:+.2f}%)" if long_pnl != 0 else ""}</td>
                <td>{short_result} {f"({short_pnl:+.2f}%)" if short_pnl != 0 else ""}</td>
            </tr>
        ''')
    
    # Calcular totais do dia
    total_pnl = day_stats.get('total_pnl', 0)
    pnl_class = 'positive' if total_pnl >= 0 else 'negative'
    
    html = f'''<!-- CLOSING_REPORT_SECTION -->
    <section class="closing-report" id="fechamento">
        <div class="container">
            <div class="section-header">
                <h2>📊 Balanço do Dia</h2>
                <p>Resultados das análises e setups - {report.get('date', '')} às {report.get('time', '')} BRT</p>
            </div>
            
            <!-- KPIs do Dia -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <span class="kpi-value">{day_stats.get('winning', 0)}/{day_stats.get('total_setups', 0)}</span>
                    <span class="kpi-label">Setups Vencedores</span>
                </div>
                <div class="kpi-card">
                    <span class="kpi-value {pnl_class}">{total_pnl:+.2f}%</span>
                    <span class="kpi-label">P&L do Dia</span>
                </div>
                <div class="kpi-card">
                    <span class="kpi-value">{day_stats.get('bias_correct', 0)}/{day_stats.get('bias_total', 0)}</span>
                    <span class="kpi-label">Viés Correto</span>
                </div>
                <div class="kpi-card">
                    <span class="kpi-value">{day_stats.get('ongoing', 0)}</span>
                    <span class="kpi-label">Em Andamento</span>
                </div>
            </div>
            
            <!-- Tabela de Resultados -->
            <div class="results-table-wrapper">
                <h3>Resultados por Ativo</h3>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Ativo</th>
                            <th>Variação</th>
                            <th>Viés</th>
                            <th>Long</th>
                            <th>Short</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(result_rows)}
                    </tbody>
                </table>
            </div>
            
            <!-- Performance Acumulada -->
            <div class="cumulative-stats">
                <h3>Performance Acumulada</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-value">{cumulative.get('win_rate', 0):.1f}%</span>
                        <span class="stat-label">Taxa de Acerto</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{cumulative.get('winning_setups', 0)}/{cumulative.get('total_setups', 0)}</span>
                        <span class="stat-label">Setups Vencedores</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{cumulative.get('bias_accuracy', 0):.1f}%</span>
                        <span class="stat-label">Precisão do Viés</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- /CLOSING_REPORT_SECTION -->'''
    
    return html


def print_closing_summary(report):
    """Imprime resumo do fechamento"""
    day_stats = report.get('day_stats', {})
    cumulative = report.get('cumulative_stats', {})
    
    print()
    print("📊 RESUMO DO DIA:")
    print(f"   Setups: {day_stats.get('winning', 0)} vencedores / {day_stats.get('losing', 0)} perdedores / {day_stats.get('ongoing', 0)} em andamento")
    print(f"   P&L Total: {day_stats.get('total_pnl', 0):+.2f}%")
    print(f"   Viés: {day_stats.get('bias_correct', 0)}/{day_stats.get('bias_total', 0)} corretos")
    print()
    print("📈 PERFORMANCE ACUMULADA:")
    print(f"   Taxa de Acerto: {cumulative.get('win_rate', 0):.1f}%")
    print(f"   Precisão do Viés: {cumulative.get('bias_accuracy', 0):.1f}%")
    print()


def publish_to_github(commit_message):
    """Publica alterações no GitHub Pages"""
    repo_dir = "/home/ubuntu/cryptomind-analises"
    
    try:
        # Adicionar alterações
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
        
        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
        
        # Push
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=repo_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        print("✓ Publicado no GitHub Pages com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠ Erro ao publicar: {e}")
        if "nothing to commit" in str(e.stderr):
            print("  (Nenhuma alteração para publicar)")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='CryptoMind IA - Automação de Análises')
    parser.add_argument('--mode', choices=['morning', 'closing', 'both'], default='morning',
                        help='Modo de execução: morning (11:00), closing (21:05), both (ambos)')
    
    args = parser.parse_args()
    
    if args.mode in ['morning', 'both']:
        run_morning_analysis()
    
    if args.mode in ['closing', 'both']:
        run_closing_report()
