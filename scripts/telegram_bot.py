#!/usr/bin/env python3
"""
CryptoMind IA - Bot do Telegram
================================
Bot para enviar alertas de setups e análises.
100% automatizado - não requer interação manual.
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, List, Dict
import pytz

# Configuração
BOT_TOKEN = "8437212177:AAEsm0d-ARdcj8zDGDqdpjeaSoQgsY-Byqc"
BR_TZ = pytz.timezone('America/Sao_Paulo')

# Diretório base
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
config_file = os.path.join(data_dir, 'telegram_config.json')


class TelegramBot:
    """Bot do Telegram para envio de alertas."""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Carrega configuração do bot."""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'chat_ids': [],  # IDs dos chats/grupos para enviar alertas
            'admin_ids': [],  # IDs dos administradores
            'settings': {
                'send_daily_analysis': True,
                'send_setups': True,
                'send_weekly_report': True,
                'send_monthly_report': True,
                'min_score_alert': 5  # Score mínimo para enviar alerta
            }
        }
    
    def _save_config(self):
        """Salva configuração do bot."""
        os.makedirs(data_dir, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _api_request(self, method: str, data: dict = None) -> Optional[dict]:
        """Faz requisição à API do Telegram."""
        try:
            url = f"{self.base_url}/{method}"
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                return result.get('result')
            else:
                print(f"Erro na API do Telegram: {result.get('description')}")
                return None
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def get_me(self) -> Optional[dict]:
        """Obtém informações do bot."""
        return self._api_request('getMe')
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = 'HTML') -> Optional[dict]:
        """Envia mensagem para um chat."""
        return self._api_request('sendMessage', {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        })
    
    def broadcast(self, text: str) -> List[dict]:
        """Envia mensagem para todos os chats configurados."""
        results = []
        for chat_id in self.config.get('chat_ids', []):
            result = self.send_message(chat_id, text)
            if result:
                results.append(result)
        return results
    
    def add_chat(self, chat_id: int):
        """Adiciona chat à lista de destinatários."""
        if chat_id not in self.config['chat_ids']:
            self.config['chat_ids'].append(chat_id)
            self._save_config()
            print(f"Chat {chat_id} adicionado")
    
    def remove_chat(self, chat_id: int):
        """Remove chat da lista de destinatários."""
        if chat_id in self.config['chat_ids']:
            self.config['chat_ids'].remove(chat_id)
            self._save_config()
            print(f"Chat {chat_id} removido")
    
    def get_updates(self, offset: int = None) -> List[dict]:
        """Obtém atualizações (mensagens recebidas)."""
        data = {'timeout': 30}
        if offset:
            data['offset'] = offset
        result = self._api_request('getUpdates', data)
        return result if result else []


class AlertFormatter:
    """Formatador de alertas para o Telegram."""
    
    @staticmethod
    def format_setup_alert(setup: dict, symbol: str) -> str:
        """Formata alerta de setup."""
        ts_emoji = {
            'TS1': '🟦',
            'TS2': '🟩', 
            'TS3': '🟧'
        }
        
        ts_name = {
            'TS1': 'Rompimento',
            'TS2': 'Continuação',
            'TS3': 'Reversão'
        }
        
        direction_emoji = '📈' if setup['direction'] == 'LONG' else '📉'
        score = setup.get('confidence_score', 0)
        conf_level = setup.get('confidence_level', 'N/A')
        
        risk_plan = setup.get('risk_plan', {})
        entry = risk_plan.get('entry', {})
        stop = risk_plan.get('stop_loss', {})
        rm = risk_plan.get('risk_management', {})
        partials = risk_plan.get('partials', [])
        
        # Formatar parciais
        partials_text = ""
        for i, p in enumerate(partials, 1):
            if p['target_price'] == 'TRAILING':
                partials_text += f"   └─ Trailing Stop: {p['size_percent']}%\n"
            else:
                partials_text += f"   {i}. ${p['target_price']:.2f} ({p['rr_ratio']}R) → {p['size_percent']}%\n"
        
        ts_type = setup.get('ts_type', 'TS1')
        emoji = ts_emoji.get(ts_type, '🔷')
        name = ts_name.get(ts_type, 'Setup')
        
        message = f"""
{emoji} <b>{setup['direction']} {symbol}</b> - {name}

{direction_emoji} <b>Score: {score}/10</b> ({conf_level})

📍 <b>Entrada:</b> ${entry.get('min', 0):.2f} - ${entry.get('max', 0):.2f}
🛑 <b>Stop Loss:</b> ${stop.get('price', 0):.2f} ({stop.get('distance_percent', 0):.2f}%)

⚙️ <b>Gestão:</b>
   • Risco: {rm.get('risk_percent', 0)}% da banca
   • Alavancagem: {rm.get('suggested_leverage', 1)}x

📊 <b>Parciais:</b>
{partials_text}
⚠️ <i>Não é recomendação de investimento</i>
"""
        return message.strip()
    
    @staticmethod
    def format_daily_summary(result: dict) -> str:
        """Formata resumo diário."""
        macro = result.get('macro', {})
        fg = macro.get('fear_greed', {})
        dom = macro.get('dominance', {})
        summary = result.get('summary', {})
        
        # Contar setups por tipo
        setups_by_type = {'TS1': 0, 'TS2': 0, 'TS3': 0}
        setups_long = 0
        setups_short = 0
        high_conf = 0
        
        for symbol, setups in result.get('setups', {}).items():
            for setup in setups:
                ts_type = setup.get('ts_type', 'TS1')
                setups_by_type[ts_type] = setups_by_type.get(ts_type, 0) + 1
                
                if setup['direction'] == 'LONG':
                    setups_long += 1
                else:
                    setups_short += 1
                
                if setup.get('confidence_score', 0) >= 8:
                    high_conf += 1
        
        timestamp = datetime.now(BR_TZ).strftime('%d/%m/%Y %H:%M')
        
        message = f"""
📊 <b>CryptoMind IA - Análise Diária</b>
🕐 {timestamp}

━━━━━━━━━━━━━━━━━━━━━━

📈 <b>Contexto Macro:</b>
   • Fear & Greed: {fg.get('value', 'N/A')} ({fg.get('classification', 'N/A')})
   • BTC.D: {dom.get('btc_d', {}).get('dominance', 'N/A')}% - {dom.get('btc_d', {}).get('impact', 'N/A')}
   • USDT.D: {dom.get('usdt_d', {}).get('dominance', 'N/A')}% - {dom.get('usdt_d', {}).get('impact', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━

🎯 <b>Setups Identificados:</b> {summary.get('total_setups', 0)}
   • Alta Confiança: {high_conf}
   • LONG: {setups_long} | SHORT: {setups_short}

📋 <b>Por Tipo:</b>
   🟦 Rompimento: {setups_by_type.get('TS1', 0)}
   🟩 Continuação: {setups_by_type.get('TS2', 0)}
   🟧 Reversão: {setups_by_type.get('TS3', 0)}

━━━━━━━━━━━━━━━━━━━━━━

🌐 <a href="https://analises.cryptomindia.com">Ver análise completa</a>

⚠️ <i>Não é recomendação de investimento</i>
"""
        return message.strip()
    
    @staticmethod
    def format_weekly_report(report: dict) -> str:
        """Formata relatório semanal."""
        kpis = report.get('kpis', {})
        period = report.get('period', {})
        
        message = f"""
📊 <b>CryptoMind IA - Relatório Semanal</b>
📅 Semana {period.get('week', 'N/A')}/{period.get('year', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━

📈 <b>KPIs da Semana:</b>
   • Total de Setups: {kpis.get('total_setups', 0)}
   • Win Rate: {kpis.get('win_rate', 0):.1f}%
   • Profit Factor: {kpis.get('profit_factor', 0):.2f}

🏆 <b>Destaques:</b>
   • Melhor Ativo: {kpis.get('best_asset', 'N/A')}
   • Melhor Setup: {kpis.get('best_setup', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━

🌐 <a href="https://analises.cryptomindia.com/history.html">Ver histórico completo</a>

⚠️ <i>Não é recomendação de investimento</i>
"""
        return message.strip()


def send_daily_analysis():
    """Envia análise diária para todos os chats configurados."""
    bot = TelegramBot(BOT_TOKEN)
    formatter = AlertFormatter()
    
    # Carregar análise
    analysis_path = os.path.join(data_dir, 'full_analysis.json')
    if not os.path.exists(analysis_path):
        print("Análise não encontrada")
        return
    
    with open(analysis_path, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    # Enviar resumo diário
    summary_msg = formatter.format_daily_summary(result)
    bot.broadcast(summary_msg)
    print("Resumo diário enviado")
    
    # Enviar setups de alta confiança
    min_score = bot.config.get('settings', {}).get('min_score_alert', 5)
    
    for symbol, setups in result.get('setups', {}).items():
        for setup in setups:
            if setup.get('confidence_score', 0) >= min_score:
                setup_msg = formatter.format_setup_alert(setup, symbol)
                bot.broadcast(setup_msg)
                print(f"Setup {symbol} enviado")


def send_weekly_report():
    """Envia relatório semanal."""
    bot = TelegramBot(BOT_TOKEN)
    formatter = AlertFormatter()
    
    # Carregar relatório semanal mais recente
    weekly_dir = os.path.join(data_dir, 'archive', str(datetime.now().year), 
                              f"{datetime.now().month:02d}", 'weekly')
    
    if os.path.exists(weekly_dir):
        files = sorted(os.listdir(weekly_dir), reverse=True)
        if files:
            report_path = os.path.join(weekly_dir, files[0])
            with open(report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            msg = formatter.format_weekly_report(report)
            bot.broadcast(msg)
            print("Relatório semanal enviado")


def register_chat_from_message():
    """Registra chats que enviarem /start ao bot."""
    bot = TelegramBot(BOT_TOKEN)
    
    print("Aguardando mensagens... (Ctrl+C para parar)")
    print("Envie /start para o bot para registrar seu chat")
    
    offset = None
    while True:
        try:
            updates = bot.get_updates(offset)
            
            for update in updates:
                offset = update['update_id'] + 1
                
                message = update.get('message', {})
                chat_id = message.get('chat', {}).get('id')
                text = message.get('text', '')
                
                if text == '/start':
                    bot.add_chat(chat_id)
                    bot.send_message(chat_id, """
🤖 <b>CryptoMind IA - Bot de Alertas</b>

✅ Seu chat foi registrado com sucesso!

Você receberá:
📊 Análises diárias de abertura e fechamento
🎯 Alertas de setups de alta confiança
📈 Relatórios semanais e mensais

🌐 <a href="https://analises.cryptomindia.com">Acesse o site completo</a>

⚠️ <i>Não é recomendação de investimento</i>
""")
                    print(f"Chat {chat_id} registrado")
                
                elif text == '/status':
                    bot.send_message(chat_id, "✅ Bot está funcionando!")
                
                elif text == '/help':
                    bot.send_message(chat_id, """
📋 <b>Comandos disponíveis:</b>

/start - Registrar para receber alertas
/status - Verificar se o bot está funcionando
/help - Ver esta mensagem

🌐 <a href="https://analises.cryptomindia.com">Site CryptoMind IA</a>
""")
        
        except KeyboardInterrupt:
            print("\nParando...")
            break
        except Exception as e:
            print(f"Erro: {e}")


def main():
    """Função principal - testa o bot."""
    bot = TelegramBot(BOT_TOKEN)
    
    # Verificar bot
    me = bot.get_me()
    if me:
        print(f"✅ Bot conectado: @{me.get('username')}")
        print(f"   Nome: {me.get('first_name')}")
        print(f"   ID: {me.get('id')}")
    else:
        print("❌ Erro ao conectar ao bot")
        return
    
    print("\n" + "=" * 50)
    print("Para registrar seu chat, envie /start para o bot")
    print("=" * 50)
    
    # Iniciar loop de registro
    register_chat_from_message()


if __name__ == "__main__":
    main()
