#!/usr/bin/env python3
"""
CryptoMind IA - Ciclo Completo de Análise
==========================================
Script mestre que executa todo o ciclo de análise:
1. Análise multi-timeframe
2. Detecção de Trading Systems
3. Cálculo de scores
4. Gestão de risco
5. Geração de HTML
6. Arquivamento
7. Envio de alertas no Telegram
8. Rastreamento de performance

100% automatizado - pode ser executado via cron ou GitHub Actions.
"""

import os
import sys
import json
import time
from datetime import datetime
import pytz

# Adicionar diretório de scripts ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Configuração
BR_TZ = pytz.timezone('America/Sao_Paulo')
data_dir = os.path.join(script_dir, '..', 'data')


def log(message: str):
    """Log com timestamp."""
    timestamp = datetime.now(BR_TZ).strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def run_multi_timeframe_analysis():
    """Executa análise multi-timeframe ou usa cache."""
    log("Verificando análise multi-timeframe...")
    
    cache_path = os.path.join(data_dir, 'multi_timeframe_analysis.json')
    
    # Verificar se cache existe e é recente (menos de 1 hora)
    if os.path.exists(cache_path):
        cache_age = time.time() - os.path.getmtime(cache_path)
        if cache_age < 3600:  # 1 hora
            log("✅ Usando cache de análise multi-timeframe (< 1h)")
            return True
    
    # Tentar executar nova análise
    try:
        from multi_timeframe_analyzer import MultiTimeframeAnalyzer
        
        analyzer = MultiTimeframeAnalyzer()
        result = analyzer.run_full_analysis()
        
        if result:
            log("✅ Análise multi-timeframe concluída")
            return True
        else:
            log("⚠️ API indisponível, usando cache existente")
            return os.path.exists(cache_path)
    except Exception as e:
        log(f"⚠️ Erro na API ({e}), usando cache")
        return os.path.exists(cache_path)


def run_full_analysis():
    """Executa análise completa com TS e gestão de risco."""
    log("Executando análise completa...")
    
    try:
        from generate_full_analysis import generate_full_analysis
        from html_generator import generate_html_report
        
        result = generate_full_analysis()
        
        if result:
            # Gerar HTML
            html = generate_html_report(result)
            html_path = os.path.join(script_dir, '..', 'index.html')
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            log("✅ Análise completa e HTML gerados")
            return result
        else:
            log("❌ Erro ao gerar análise completa")
            return None
    except Exception as e:
        log(f"❌ Erro na análise completa: {e}")
        return None


def run_archive():
    """Arquiva a análise atual."""
    log("Arquivando análise...")
    
    try:
        from archive_manager import ArchiveManager
        
        manager = ArchiveManager()
        
        # Determinar tipo de análise
        hour = datetime.now(BR_TZ).hour
        analysis_type = 'opening' if hour < 14 else 'closing'
        
        # Usar método correto
        archived = manager.archive_analysis(analysis_type)
        
        if archived:
            log(f"✅ Análise arquivada")
        
        # Reconstruir índices
        from index_builder import IndexBuilder
        builder = IndexBuilder()
        builder.build_all_indexes()
        
        log("✅ Índices reconstruídos")
        return True
    except Exception as e:
        log(f"⚠️ Arquivamento ignorado: {e}")
        return True  # Não é crítico


def send_telegram_alerts(result: dict):
    """Envia alertas para o Telegram."""
    log("Enviando alertas para o Telegram...")
    
    try:
        from telegram_bot import TelegramBot, AlertFormatter
        
        BOT_TOKEN = "8437212177:AAEsm0d-ARdcj8zDGDqdpjeaSoQgsY-Byqc"
        bot = TelegramBot(BOT_TOKEN)
        formatter = AlertFormatter()
        
        # Verificar se há chats configurados
        if not bot.config.get('chat_ids'):
            log("⚠️ Nenhum chat configurado para alertas")
            return False
        
        # Enviar resumo diário
        summary_msg = formatter.format_daily_summary(result)
        bot.broadcast(summary_msg)
        log("✅ Resumo diário enviado")
        
        # Enviar setups de alta confiança
        min_score = bot.config.get('settings', {}).get('min_score_alert', 5)
        setups_sent = 0
        
        for symbol, setups in result.get('setups', {}).items():
            for setup in setups:
                if setup.get('confidence_score', 0) >= min_score:
                    setup_msg = formatter.format_setup_alert(setup, symbol)
                    bot.broadcast(setup_msg)
                    setups_sent += 1
                    time.sleep(1)  # Evitar rate limit
        
        log(f"✅ {setups_sent} alertas de setup enviados")
        return True
    except Exception as e:
        log(f"⚠️ Erro ao enviar alertas: {e}")
        return False


def run_performance_tracking():
    """Executa rastreamento de performance."""
    log("Rastreando performance...")
    
    try:
        from performance_tracker import PerformanceTracker
        
        tracker = PerformanceTracker()
        tracker.register_new_setups_from_analysis()
        tracker.update_all_setups()
        
        summary = tracker.get_summary()
        log(f"✅ Performance: {summary['wins']}W/{summary['losses']}L | WR: {summary['win_rate']}")
        return True
    except Exception as e:
        log(f"⚠️ Erro no rastreamento: {e}")
        return False


def main():
    """Executa ciclo completo."""
    print("=" * 60)
    print("CryptoMind IA - Ciclo Completo de Análise")
    print("=" * 60)
    print(f"Iniciado em: {datetime.now(BR_TZ).strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    start_time = time.time()
    
    # 1. Análise multi-timeframe
    log("\n[1/5] ANÁLISE MULTI-TIMEFRAME")
    mtf_ok = run_multi_timeframe_analysis()
    
    # 2. Análise completa
    log("\n[2/5] ANÁLISE COMPLETA")
    result = run_full_analysis()
    
    if not result:
        log("❌ Falha crítica na análise. Abortando.")
        return False
    
    # 3. Arquivamento
    log("\n[3/5] ARQUIVAMENTO")
    run_archive()
    
    # 4. Alertas Telegram
    log("\n[4/5] ALERTAS TELEGRAM")
    send_telegram_alerts(result)
    
    # 5. Rastreamento de performance
    log("\n[5/5] RASTREAMENTO DE PERFORMANCE")
    run_performance_tracking()
    
    # Resumo final
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("CICLO COMPLETO FINALIZADO")
    print("=" * 60)
    print(f"Tempo total: {elapsed:.1f}s")
    print(f"Finalizado em: {datetime.now(BR_TZ).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Resumo dos setups
    total_setups = result.get('summary', {}).get('total_setups', 0)
    high_conf = sum(1 for s in result.get('setups', {}).values() 
                    for setup in s if setup.get('confidence_score', 0) >= 8)
    
    print(f"\n📊 Setups identificados: {total_setups}")
    print(f"⭐ Alta confiança: {high_conf}")
    print(f"🌐 Site: https://analises.cryptomindia.com")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
