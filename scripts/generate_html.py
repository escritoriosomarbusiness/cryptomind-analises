#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de HTML
Gera a página HTML completa com análises de BTC + Altcoins
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import pytz


class HTMLGenerator:
    """Gera HTML da página de análises"""
    
    def __init__(self):
        self.timezone = pytz.timezone('America/Sao_Paulo')
        self.template_dir = "/home/ubuntu/cryptomind-analises"
        self.data_dir = "/home/ubuntu/cryptomind-analises/data"
        
    def load_analysis(self) -> Dict:
        """Carrega a análise mais recente"""
        latest_file = f"{self.data_dir}/latest_analysis.json"
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def format_price(self, price: float) -> str:
        """Formata preço para exibição"""
        if price >= 1000:
            return f"${price:,.0f}"
        elif price >= 1:
            return f"${price:,.2f}"
        else:
            return f"${price:.4f}"
    
    def generate_asset_nav(self, analyses: Dict) -> str:
        """Gera navegação de ativos"""
        nav_items = []
        for symbol in analyses.keys():
            nav_items.append(f'<a href="#{symbol.lower()}" class="asset-nav-link">{symbol}</a>')
        return '\n'.join(nav_items)
    
    def generate_asset_summary_table(self, analyses: Dict) -> str:
        """Gera tabela resumo de todos os ativos"""
        rows = []
        for symbol, data in analyses.items():
            change_class = "positive" if data['price_change'] >= 0 else "negative"
            bias_class = data['bias']['bias_class']
            
            # Setup status
            if data['setups']['long'] and data['setups']['short']:
                setup_status = '<span class="setup-badge both">LONG + SHORT</span>'
            elif data['setups']['long']:
                setup_status = '<span class="setup-badge long">LONG</span>'
            elif data['setups']['short']:
                setup_status = '<span class="setup-badge short">SHORT</span>'
            else:
                setup_status = '<span class="setup-badge notrade">NO TRADE</span>'
            
            rows.append(f'''
                <tr onclick="document.getElementById('{symbol.lower()}').scrollIntoView({{behavior: 'smooth'}})">
                    <td class="asset-symbol">{symbol}</td>
                    <td class="asset-price">{data['price_formatted']}</td>
                    <td class="asset-change {change_class}">{data['price_change_formatted']}</td>
                    <td class="asset-bias {bias_class}">{data['bias']['bias']}</td>
                    <td class="asset-setup">{setup_status}</td>
                </tr>
            ''')
        
        return '\n'.join(rows)
    
    def generate_metrics_section(self, data: Dict) -> str:
        """Gera seção de métricas para um ativo"""
        change_class = "positive" if data['price_change'] >= 0 else "negative"
        funding_class = "positive" if data['funding_rate'] < 0.01 else "negative" if data['funding_rate'] > 0.05 else "neutral"
        
        return f'''
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-icon blue">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                        </svg>
                    </div>
                    <div class="metric-info">
                        <span class="metric-label">Preço Atual</span>
                        <span class="metric-value">{data['price_formatted']}</span>
                    </div>
                    <span class="metric-badge {change_class}">{data['price_change_formatted']}</span>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon purple">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                        </svg>
                    </div>
                    <div class="metric-info">
                        <span class="metric-label">Funding Rate</span>
                        <span class="metric-value">{data['funding_formatted']}</span>
                    </div>
                    <span class="metric-badge {funding_class}">{"Bullish" if data['funding_rate'] < 0.01 else "Bearish" if data['funding_rate'] > 0.05 else "Neutro"}</span>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon orange">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 6v6l4 2"/>
                        </svg>
                    </div>
                    <div class="metric-info">
                        <span class="metric-label">RSI (14)</span>
                        <span class="metric-value">{data['rsi']:.1f}</span>
                    </div>
                    <span class="metric-badge {"negative" if data['rsi'] > 70 else "positive" if data['rsi'] < 30 else "neutral"}">{"Sobrecomprado" if data['rsi'] > 70 else "Sobrevendido" if data['rsi'] < 30 else "Neutro"}</span>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon red">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2a10 10 0 1 0 10 10H12V2z"/>
                        </svg>
                    </div>
                    <div class="metric-info">
                        <span class="metric-label">Long/Short</span>
                        <span class="metric-value">{data['long_percent']}/{data['short_percent']}</span>
                    </div>
                    <span class="metric-badge neutral">{"Long Heavy" if data['long_percent'] > 55 else "Short Heavy" if data['short_percent'] > 55 else "Equilibrado"}</span>
                </div>
            </div>
        '''
    
    def generate_levels_section(self, data: Dict) -> str:
        """Gera seção de níveis-chave"""
        sr = data['sr_levels']
        
        levels_html = f'''
            <div class="levels-section">
                <h3>Níveis-Chave do Dia</h3>
                <div class="levels-grid">
                    <div class="level-card resistance">
                        <span class="level-type">Resistência 2</span>
                        <span class="level-price">{self.format_price(sr["resistances"][1] if len(sr["resistances"]) > 1 else sr["pdh"])}</span>
                        <span class="level-note">Zona de liquidez</span>
                    </div>
                    <div class="level-card resistance">
                        <span class="level-type">Resistência 1</span>
                        <span class="level-price">{self.format_price(sr["pdh"])}</span>
                        <span class="level-note">High do dia (PDH)</span>
                    </div>
                    <div class="level-card current">
                        <span class="level-type">Preço Atual</span>
                        <span class="level-price">{data["price_formatted"]}</span>
                        <span class="level-note">{data["symbol"]}/USDT</span>
                    </div>
                    <div class="level-card support">
                        <span class="level-type">Suporte 1</span>
                        <span class="level-price">{self.format_price(sr["pdl"])}</span>
                        <span class="level-note">Low do dia (PDL)</span>
                    </div>
                    <div class="level-card support">
                        <span class="level-type">Suporte 2</span>
                        <span class="level-price">{self.format_price(sr["supports"][1] if len(sr["supports"]) > 1 and sr["supports"][1] > 0 else sr["pdl"] * 0.98)}</span>
                        <span class="level-note">Suporte forte</span>
                    </div>
                </div>
            </div>
        '''
        return levels_html
    
    def generate_setup_card(self, setup: Dict, setup_type: str) -> str:
        """Gera card de setup"""
        if not setup:
            return ''
        
        type_class = "long" if setup_type == "long" else "short"
        
        return f'''
            <div class="setup-card {type_class}">
                <div class="setup-header">
                    <span class="setup-type">{setup["type"]}</span>
                    <span class="setup-badge">{setup["style"]}</span>
                </div>
                <div class="setup-body">
                    <div class="setup-row">
                        <span class="setup-label">Entrada</span>
                        <span class="setup-value">{self.format_price(setup["entry_low"])} - {self.format_price(setup["entry_high"])}</span>
                    </div>
                    <div class="setup-row">
                        <span class="setup-label">Stop Loss</span>
                        <span class="setup-value stop">{self.format_price(setup["stop_loss"])}</span>
                    </div>
                    <div class="setup-row">
                        <span class="setup-label">Alvo 1</span>
                        <span class="setup-value target">{self.format_price(setup["target1"])} <small>(R/R {setup["rr1"]})</small></span>
                    </div>
                    <div class="setup-row">
                        <span class="setup-label">Alvo 2</span>
                        <span class="setup-value target">{self.format_price(setup["target2"])} <small>(R/R {setup["rr2"]})</small></span>
                    </div>
                    <div class="setup-trigger">
                        <strong>Gatilho:</strong> {setup["trigger"]}
                    </div>
                </div>
            </div>
        '''
    
    def generate_setups_section(self, data: Dict) -> str:
        """Gera seção de setups"""
        setups = data['setups']
        
        if not setups['long'] and not setups['short']:
            return f'''
                <div class="setups-section">
                    <h3>Setups do Dia</h3>
                    <div class="no-trade-zone">
                        <div class="no-trade-icon">⚠️</div>
                        <h4>NO TRADE ZONE</h4>
                        <p>Não há setups com boa relação risco/retorno no momento.</p>
                        <ul>
                            <li>RSI em zona de sobrecompra/sobrevenda extrema</li>
                            <li>Estrutura de mercado indefinida</li>
                            <li>Aguardar melhor oportunidade</li>
                        </ul>
                    </div>
                </div>
            '''
        
        setup_cards = ''
        if setups['long']:
            setup_cards += self.generate_setup_card(setups['long'], 'long')
        if setups['short']:
            setup_cards += self.generate_setup_card(setups['short'], 'short')
        
        return f'''
            <div class="setups-section">
                <h3>Setups do Dia</h3>
                <div class="setups-grid">
                    {setup_cards}
                </div>
            </div>
        '''
    
    def generate_bias_section(self, data: Dict) -> str:
        """Gera seção de viés"""
        bias = data['bias']
        
        positive_reasons = '\n'.join([
            f'<div class="reason positive"><span>✓</span> {r}</div>'
            for r in bias['bullish_factors']
        ])
        
        negative_reasons = '\n'.join([
            f'<div class="reason negative"><span>✗</span> {r}</div>'
            for r in bias['bearish_factors']
        ])
        
        return f'''
            <div class="bias-section">
                <h3>Viés do Dia</h3>
                <div class="bias-card-wrapper">
                    <div class="bias-indicator {bias["bias_class"]}">
                        <span class="bias-text">{bias["bias"]}</span>
                    </div>
                    <div class="bias-reasons">
                        {positive_reasons}
                        {negative_reasons}
                    </div>
                </div>
            </div>
        '''
    
    def generate_asset_section(self, symbol: str, data: Dict, is_first: bool = False) -> str:
        """Gera seção completa de um ativo"""
        
        section_class = "asset-section" + (" first" if is_first else "")
        
        return f'''
            <section class="{section_class}" id="{symbol.lower()}">
                <div class="container">
                    <div class="asset-header">
                        <h2>{symbol}/USDT</h2>
                        <div class="asset-price-display">
                            <span class="price">{data["price_formatted"]}</span>
                            <span class="change {"positive" if data["price_change"] >= 0 else "negative"}">{data["price_change_formatted"]}</span>
                        </div>
                    </div>
                    
                    {self.generate_metrics_section(data)}
                    {self.generate_levels_section(data)}
                    {self.generate_setups_section(data)}
                    {self.generate_bias_section(data)}
                </div>
            </section>
        '''
    
    def generate_usdt_d_section(self, usdt_d: Dict) -> str:
        """Gera seção do USDT.D - Indicador Macro"""
        if not usdt_d:
            return ''
        
        impact_class = usdt_d.get('crypto_impact_class', 'neutral')
        
        # Status das EMAs
        ema_9_status = '✅' if usdt_d.get('below_ema_9', False) else '❌'
        ema_21_status = '✅' if usdt_d.get('below_ema_21', False) else '❌'
        ema_200_status = '✅' if usdt_d.get('below_ema_200', False) else '❌'
        
        return f'''
            <div class="usdt-d-section">
                <div class="usdt-d-header">
                    <div class="usdt-d-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                        </svg>
                    </div>
                    <div class="usdt-d-title">
                        <h3>USDT.D - Indicador Macro</h3>
                        <span class="usdt-d-subtitle">Dominância do USDT no mercado</span>
                    </div>
                    <div class="usdt-d-impact {impact_class}">
                        <span class="impact-label">Impacto Cripto:</span>
                        <span class="impact-value">{usdt_d.get('crypto_impact', 'NEUTRO')}</span>
                    </div>
                </div>
                
                <div class="usdt-d-body">
                    <div class="usdt-d-metrics">
                        <div class="usdt-metric">
                            <span class="metric-label">Dominância Atual</span>
                            <span class="metric-value">{usdt_d.get('dominance_formatted', '0%')}</span>
                        </div>
                        <div class="usdt-metric">
                            <span class="metric-label">EMA 9</span>
                            <span class="metric-value">{usdt_d.get('ema_9', 0):.3f}%</span>
                            <span class="metric-status">{ema_9_status} Abaixo</span>
                        </div>
                        <div class="usdt-metric">
                            <span class="metric-label">EMA 21</span>
                            <span class="metric-value">{usdt_d.get('ema_21', 0):.3f}%</span>
                            <span class="metric-status">{ema_21_status} Abaixo</span>
                        </div>
                        <div class="usdt-metric">
                            <span class="metric-label">EMA 200</span>
                            <span class="metric-value">{usdt_d.get('ema_200', 0):.3f}%</span>
                            <span class="metric-status">{ema_200_status} Abaixo</span>
                        </div>
                        <div class="usdt-metric">
                            <span class="metric-label">RSI</span>
                            <span class="metric-value">{usdt_d.get('rsi', 0):.1f}</span>
                        </div>
                        <div class="usdt-metric">
                            <span class="metric-label">MACD</span>
                            <span class="metric-value">{usdt_d.get('macd', 0):.4f}%</span>
                        </div>
                    </div>
                    
                    <div class="usdt-d-levels">
                        <h4>Níveis de S/R</h4>
                        <div class="levels-mini">
                            <div class="level-item resistance">
                                <span>Resistência W1</span>
                                <span>{usdt_d.get('sr_levels', {}).get('resistance_w1', 0):.2f}%</span>
                            </div>
                            <div class="level-item resistance">
                                <span>Resistência D1</span>
                                <span>{usdt_d.get('sr_levels', {}).get('resistance_d1', 0):.2f}%</span>
                            </div>
                            <div class="level-item current">
                                <span>Atual</span>
                                <span>{usdt_d.get('dominance', 0):.3f}%</span>
                            </div>
                            <div class="level-item support">
                                <span>Suporte H4</span>
                                <span>{usdt_d.get('sr_levels', {}).get('support_h4', 0):.2f}%</span>
                            </div>
                            <div class="level-item support">
                                <span>Suporte W1</span>
                                <span>{usdt_d.get('sr_levels', {}).get('support_w1', 0):.2f}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="usdt-d-analysis">
                        <div class="analysis-item">
                            <span class="analysis-icon">📊</span>
                            <span class="analysis-text">{usdt_d.get('impact_reason', '')}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-icon">🎯</span>
                            <span class="analysis-text">Próximo nível: {usdt_d.get('next_level', '')}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-icon">⚠️</span>
                            <span class="analysis-text">Invalidação: {usdt_d.get('invalidation', '')}</span>
                        </div>
                    </div>
                </div>
            </div>
        '''
    
    def generate_fear_greed_section(self, fear_greed: Dict) -> str:
        """Gera seção de Fear & Greed"""
        value = fear_greed['value']
        classification = fear_greed['classification']
        
        # Determinar classe CSS
        if value <= 25:
            fg_class = "extreme-fear"
        elif value <= 45:
            fg_class = "fear"
        elif value <= 55:
            fg_class = "neutral"
        elif value <= 75:
            fg_class = "greed"
        else:
            fg_class = "extreme-greed"
        
        return f'''
            <div class="fear-greed-card">
                <h4>Fear & Greed Index</h4>
                <div class="gauge-container">
                    <div class="gauge">
                        <div class="gauge-fill" style="--value: {value};"></div>
                        <div class="gauge-center">
                            <span class="gauge-value">{value}</span>
                            <span class="gauge-label">{classification}</span>
                        </div>
                    </div>
                </div>
                <div class="sentiment-history">
                    <div class="history-item">
                        <span>Ontem</span>
                        <span class="{fg_class}">{fear_greed["yesterday"]}</span>
                    </div>
                    <div class="history-item">
                        <span>Semana passada</span>
                        <span class="{fg_class}">{fear_greed["week_ago"]}</span>
                    </div>
                </div>
            </div>
        '''
    
    def generate_html(self, analysis: Dict) -> str:
        """Gera HTML completo"""
        
        # Dados principais
        btc_data = analysis['analyses'].get('BTC', {})
        fear_greed = analysis['fear_greed']
        
        # Gerar navegação de ativos
        asset_nav = self.generate_asset_nav(analysis['analyses'])
        
        # Gerar tabela resumo
        summary_table = self.generate_asset_summary_table(analysis['analyses'])
        
        # Gerar seções de cada ativo
        asset_sections = ''
        for i, (symbol, data) in enumerate(analysis['analyses'].items()):
            asset_sections += self.generate_asset_section(symbol, data, is_first=(i==0))
        
        # Fear & Greed
        fear_greed_html = self.generate_fear_greed_section(fear_greed)
        
        # USDT.D - Indicador Macro
        usdt_d = analysis.get('usdt_d', {})
        usdt_d_html = self.generate_usdt_d_section(usdt_d)
        
        html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptoMind IA - Análises Diárias de Day Trade</title>
    <meta name="description" content="Análises diárias de criptomoedas com IA para Day Trade. BTC, ETH, SOL, BNB, XRP, ADA - Setups, níveis-chave e sentimento de mercado.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/png" href="images/favicon.png">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">
                        <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20 4L36 12V28L20 36L4 28V12L20 4Z" stroke="url(#gradient1)" stroke-width="2" fill="none"/>
                            <circle cx="20" cy="20" r="8" fill="url(#gradient1)"/>
                            <defs>
                                <linearGradient id="gradient1" x1="4" y1="4" x2="36" y2="36">
                                    <stop offset="0%" stop-color="#00D4FF"/>
                                    <stop offset="100%" stop-color="#7B2DFF"/>
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                    <div class="logo-text">
                        <span class="logo-name">CryptoMind</span>
                        <span class="logo-suffix">IA</span>
                    </div>
                </div>
                <nav class="nav">
                    <a href="#resumo" class="nav-link active">Resumo</a>
                    <a href="#btc" class="nav-link">BTC</a>
                    <a href="#eth" class="nav-link">ETH</a>
                    <a href="#sol" class="nav-link">SOL</a>
                    <a href="https://cryptomindia.com" class="nav-link btn-primary" target="_blank">Site Principal</a>
                </nav>
                <button class="mobile-menu-btn" aria-label="Menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="hero-badge">
                    <span class="pulse"></span>
                    <span>Atualizado às <span id="update-time">{analysis["time"]}</span> BRT</span>
                </div>
                <h1 class="hero-title">Análise Pré-Mercado</h1>
                <p class="hero-date" id="analysis-date">{analysis["date"]}</p>
                <div class="hero-stats">
                    <div class="stat-card">
                        <span class="stat-label">BTC/USDT</span>
                        <span class="stat-value">{btc_data.get("price_formatted", "$0")}</span>
                        <span class="stat-change {"positive" if btc_data.get("price_change", 0) >= 0 else "negative"}">{btc_data.get("price_change_formatted", "0%")}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-label">Fear & Greed</span>
                        <span class="stat-value">{fear_greed["value"]}</span>
                        <span class="stat-change {"negative" if fear_greed["value"] < 40 else "positive" if fear_greed["value"] > 60 else "neutral"}">{fear_greed["classification"]}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-label">Viés BTC</span>
                        <span class="stat-value">{btc_data.get("bias", {}).get("bias", "NEUTRO")}</span>
                        <span class="stat-change {btc_data.get("bias", {}).get("bias_class", "neutral")}">Day Trade</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="hero-bg"></div>
    </section>

    <!-- Asset Navigation -->
    <section class="asset-nav-section" id="resumo">
        <div class="container">
            <div class="asset-nav-wrapper">
                <h3>Navegação Rápida</h3>
                <div class="asset-nav">
                    {asset_nav}
                </div>
            </div>
            
            <!-- Summary Table -->
            <div class="summary-table-wrapper">
                <h3>Resumo dos Ativos</h3>
                <table class="summary-table">
                    <thead>
                        <tr>
                            <th>Ativo</th>
                            <th>Preço</th>
                            <th>24h</th>
                            <th>Viés</th>
                            <th>Setup</th>
                        </tr>
                    </thead>
                    <tbody>
                        {summary_table}
                    </tbody>
                </table>
            </div>
            
            <!-- USDT.D - Indicador Macro -->
            {usdt_d_html}
            
            <!-- Fear & Greed -->
            {fear_greed_html}
        </div>
    </section>

    <!-- Asset Sections -->
    {asset_sections}

    <!-- Disclaimer -->
    <section class="disclaimer">
        <div class="container">
            <div class="disclaimer-content">
                <p><strong>⚠️ Aviso:</strong> Esta análise não constitui recomendação de investimento. Trading de criptomoedas envolve riscos significativos. Faça sua própria pesquisa e opere com responsabilidade.</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <div class="logo">
                        <div class="logo-icon">
                            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M20 4L36 12V28L20 36L4 28V12L20 4Z" stroke="url(#gradient2)" stroke-width="2" fill="none"/>
                                <circle cx="20" cy="20" r="8" fill="url(#gradient2)"/>
                                <defs>
                                    <linearGradient id="gradient2" x1="4" y1="4" x2="36" y2="36">
                                        <stop offset="0%" stop-color="#00D4FF"/>
                                        <stop offset="100%" stop-color="#7B2DFF"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                        <span class="logo-name">CryptoMind <span class="logo-suffix">IA</span></span>
                    </div>
                    <p>Análises de criptomoedas com inteligência artificial</p>
                </div>
                <div class="footer-links">
                    <a href="https://cryptomindia.com" target="_blank">Site Principal</a>
                    <a href="#resumo">Resumo</a>
                    <a href="#btc">BTC</a>
                    <a href="#eth">ETH</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 CryptoMind IA. Todos os direitos reservados.</p>
                <p>Análises geradas por IA às {analysis["time"]} BRT</p>
            </div>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>'''
        
        return html
    
    def save_html(self, html: str, filename: str = "index.html"):
        """Salva o HTML gerado"""
        filepath = f"{self.template_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML salvo em: {filepath}")
        return filepath
    
    def run(self):
        """Executa a geração completa"""
        print("Carregando análise...")
        analysis = self.load_analysis()
        
        print("Gerando HTML...")
        html = self.generate_html(analysis)
        
        print("Salvando HTML...")
        self.save_html(html)
        
        print("Concluído!")
        return html


if __name__ == "__main__":
    generator = HTMLGenerator()
    generator.run()
