#!/usr/bin/env python3
"""
CryptoMind IA - Monitor de USDT.D
=================================
Monitora a dominância do USDT e envia alertas quando se aproximar de níveis S/R importantes.
100% automatizado - pode ser executado via cron ou GitHub Actions.
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, List
import pytz

# Configuração
BOT_TOKEN = "8437212177:AAEsm0d-ARdcj8zDGDqdpjeaSoQgsY-Byqc"
CHAT_ID = 1372841832
BR_TZ = pytz.timezone('America/Sao_Paulo')

# Diretórios
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
state_file = os.path.join(data_dir, 'usdt_d_monitor_state.json')

# Níveis de S/R do USDT.D (atualizado 03/01/2026)
# IMPORTANTE: USDT.D tem relação INVERSAMENTE PROPORCIONAL com o mercado cripto
SR_LEVELS = {
    "resistance_w1": {"price": 6.74, "name": "Resistência Semanal", "timeframe": "W1", "importance": "alta"},
    "resistance_d1": {"price": 6.53, "name": "Resistência Diária", "timeframe": "D1", "importance": "alta"},
    "resistance_h4": {"price": 6.17, "name": "EMA 200 / Resistência H4", "timeframe": "H4", "importance": "muito_alta"},
    "support_h4": {"price": 6.00, "name": "Suporte H4", "timeframe": "H4", "importance": "média"},
    "support_w1": {"price": 5.86, "name": "Suporte Semanal", "timeframe": "W1", "importance": "alta"},
}

# Tolerância para alertas (em %)
ALERT_TOLERANCE = 0.05  # 0.05% de distância do nível


class USDTDMonitor:
    """Monitor de USDT.D com alertas para níveis S/R."""
    
    def __init__(self):
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Carrega estado anterior do monitor."""
        if os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_check": None,
            "last_dominance": None,
            "alerts_sent": {},  # {level_name: timestamp}
            "cooldown_hours": 4  # Não repetir alerta do mesmo nível por X horas
        }
    
    def _save_state(self):
        """Salva estado do monitor."""
        os.makedirs(data_dir, exist_ok=True)
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def get_usdt_dominance(self) -> Optional[float]:
        """Obtém dominância atual do USDT."""
        try:
            global_data = requests.get(
                "https://api.coingecko.com/api/v3/global",
                timeout=10
            ).json()
            
            usdt_data = requests.get(
                "https://api.coingecko.com/api/v3/coins/tether",
                timeout=10
            ).json()
            
            total_market_cap = global_data['data']['total_market_cap']['usd']
            usdt_market_cap = usdt_data['market_data']['market_cap']['usd']
            
            return (usdt_market_cap / total_market_cap) * 100
            
        except Exception as e:
            print(f"Erro ao obter USDT.D: {e}")
            return None
    
    def send_telegram_alert(self, message: str) -> bool:
        """Envia alerta para o Telegram."""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            response = requests.post(url, json=data, timeout=30)
            return response.json().get('ok', False)
        except Exception as e:
            print(f"Erro ao enviar Telegram: {e}")
            return False
    
    def can_send_alert(self, level_name: str) -> bool:
        """Verifica se pode enviar alerta (cooldown)."""
        if level_name not in self.state['alerts_sent']:
            return True
        
        last_sent = datetime.fromisoformat(self.state['alerts_sent'][level_name])
        now = datetime.now(BR_TZ)
        hours_passed = (now - last_sent).total_seconds() / 3600
        
        return hours_passed >= self.state['cooldown_hours']
    
    def check_levels(self, dominance: float) -> List[Dict]:
        """Verifica se o preço está próximo de algum nível S/R."""
        alerts = []
        
        for level_key, level_info in SR_LEVELS.items():
            level_price = level_info['price']
            distance = abs(dominance - level_price)
            distance_percent = (distance / level_price) * 100
            
            if distance_percent <= ALERT_TOLERANCE:
                # Determinar se está se aproximando de suporte ou resistência
                if dominance > level_price:
                    direction = "descendo em direção ao"
                    crypto_impact = "BULLISH" if "support" in level_key else "possível reversão"
                else:
                    direction = "subindo em direção à"
                    crypto_impact = "BEARISH" if "resistance" in level_key else "possível reversão"
                
                alerts.append({
                    "level_key": level_key,
                    "level_name": level_info['name'],
                    "level_price": level_price,
                    "timeframe": level_info['timeframe'],
                    "importance": level_info['importance'],
                    "direction": direction,
                    "distance": distance,
                    "distance_percent": distance_percent,
                    "crypto_impact": crypto_impact
                })
        
        return alerts
    
    def format_alert_message(self, dominance: float, alert: Dict) -> str:
        """Formata mensagem de alerta."""
        now = datetime.now(BR_TZ)
        
        # Emoji baseado na importância
        importance_emoji = {
            "muito_alta": "🚨🚨",
            "alta": "🚨",
            "média": "⚠️"
        }.get(alert['importance'], "📊")
        
        # Emoji baseado no impacto
        if alert['crypto_impact'] == "BULLISH":
            impact_emoji = "🟢"
            impact_text = "BULLISH para Cripto"
        elif alert['crypto_impact'] == "BEARISH":
            impact_emoji = "🔴"
            impact_text = "BEARISH para Cripto"
        else:
            impact_emoji = "🟡"
            impact_text = "Possível reversão"
        
        message = f"""
{importance_emoji} <b>ALERTA USDT.D</b> {importance_emoji}

━━━━━━━━━━━━━━━━━━━━
📊 <b>USDT Dominance</b>
━━━━━━━━━━━━━━━━━━━━

💰 <b>Dominância Atual:</b> {dominance:.3f}%
📍 <b>Nível Próximo:</b> {alert['level_name']}
🎯 <b>Preço do Nível:</b> {alert['level_price']:.2f}%
📏 <b>Distância:</b> {alert['distance']:.3f}% ({alert['distance_percent']:.2f}%)
⏱️ <b>Timeframe:</b> {alert['timeframe']}

━━━━━━━━━━━━━━━━━━━━
{impact_emoji} <b>Impacto:</b> {impact_text}
━━━━━━━━━━━━━━━━━━━━

💡 <b>Contexto:</b>
USDT.D {alert['direction']} {alert['level_name']}.
{"Se romper para baixo, indica mais dinheiro entrando em cripto." if "support" in alert['level_key'] else "Se romper para cima, indica dinheiro saindo de cripto."}

⚠️ <i>Lembre-se: USDT.D é INVERSAMENTE proporcional ao mercado cripto.</i>

🕐 {now.strftime('%d/%m/%Y %H:%M')} BRT
"""
        return message.strip()
    
    def run(self) -> Dict:
        """Executa verificação e envia alertas se necessário."""
        now = datetime.now(BR_TZ)
        result = {
            "timestamp": now.isoformat(),
            "dominance": None,
            "alerts_checked": 0,
            "alerts_sent": 0,
            "details": []
        }
        
        # Obter dominância atual
        dominance = self.get_usdt_dominance()
        if dominance is None:
            result["error"] = "Não foi possível obter dominância do USDT"
            return result
        
        result["dominance"] = round(dominance, 3)
        
        # Verificar níveis
        alerts = self.check_levels(dominance)
        result["alerts_checked"] = len(alerts)
        
        for alert in alerts:
            level_key = alert['level_key']
            
            if self.can_send_alert(level_key):
                message = self.format_alert_message(dominance, alert)
                
                if self.send_telegram_alert(message):
                    self.state['alerts_sent'][level_key] = now.isoformat()
                    result["alerts_sent"] += 1
                    result["details"].append({
                        "level": alert['level_name'],
                        "status": "sent"
                    })
                    print(f"✅ Alerta enviado: {alert['level_name']}")
                else:
                    result["details"].append({
                        "level": alert['level_name'],
                        "status": "failed"
                    })
                    print(f"❌ Falha ao enviar alerta: {alert['level_name']}")
            else:
                result["details"].append({
                    "level": alert['level_name'],
                    "status": "cooldown"
                })
                print(f"⏳ Cooldown ativo: {alert['level_name']}")
        
        # Atualizar estado
        self.state['last_check'] = now.isoformat()
        self.state['last_dominance'] = dominance
        self._save_state()
        
        return result


def main():
    """Função principal."""
    print("=" * 50)
    print("CRYPTOMIND IA - MONITOR USDT.D")
    print("=" * 50)
    print(f"Horário: {datetime.now(BR_TZ).strftime('%d/%m/%Y %H:%M')} BRT")
    print()
    
    monitor = USDTDMonitor()
    result = monitor.run()
    
    print(f"Dominância atual: {result.get('dominance', 'N/A')}%")
    print(f"Alertas verificados: {result.get('alerts_checked', 0)}")
    print(f"Alertas enviados: {result.get('alerts_sent', 0)}")
    
    if result.get('error'):
        print(f"Erro: {result['error']}")
    
    print()
    print("=" * 50)
    
    return result


if __name__ == "__main__":
    main()
