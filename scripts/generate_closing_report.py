#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de Relatório de Fechamento
Avalia os setups do dia e gera KPIs de performance
Executado às 21:05 BRT (após fechamento do candle diário)
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pytz


class ClosingReportGenerator:
    """Gera relatório de fechamento com KPIs"""
    
    def __init__(self):
        self.timezone = pytz.timezone('America/Sao_Paulo')
        self.data_dir = str(Path(__file__).parent.parent / "data")
        self.assets = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA"]
        
    def get_current_prices(self) -> Dict[str, float]:
        """Obtém preços atuais de todos os ativos"""
        prices = {}
        for symbol in self.assets:
            try:
                response = requests.get(
                    f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT",
                    timeout=10
                )
                prices[symbol] = float(response.json()['price'])
            except Exception as e:
                print(f"Erro ao obter preço de {symbol}: {e}")
                prices[symbol] = 0
        return prices
    
    def get_price_history(self, symbol: str, hours: int = 24) -> List[Dict]:
        """Obtém histórico de preços das últimas horas"""
        try:
            response = requests.get(
                f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit={hours}",
                timeout=10
            )
            klines = response.json()
            
            history = []
            for k in klines:
                history.append({
                    "timestamp": k[0],
                    "open": float(k[1]),
                    "high": float(k[2]),
                    "low": float(k[3]),
                    "close": float(k[4])
                })
            return history
        except Exception as e:
            print(f"Erro ao obter histórico de {symbol}: {e}")
            return []
    
    def load_morning_analysis(self) -> Optional[Dict]:
        """Carrega a análise da manhã"""
        try:
            # Procurar análise mais recente do dia
            today = datetime.now(self.timezone).strftime('%Y%m%d')
            
            # Tentar carregar a análise das 11:00
            for hour in ['11', '10', '09', '08', '07', '06']:
                filename = f"{self.data_dir}/analysis_{today}_{hour}*.json"
                import glob
                files = glob.glob(filename.replace('*', '??'))
                if files:
                    with open(sorted(files)[-1], 'r', encoding='utf-8') as f:
                        return json.load(f)
            
            # Fallback para latest
            latest_file = f"{self.data_dir}/latest_analysis.json"
            if os.path.exists(latest_file):
                with open(latest_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
        except Exception as e:
            print(f"Erro ao carregar análise: {e}")
            return None
    
    def load_performance_history(self) -> Dict:
        """Carrega histórico de performance"""
        history_file = f"{self.data_dir}/performance_history.json"
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_setups": 0,
            "winning_setups": 0,
            "losing_setups": 0,
            "ongoing_setups": 0,
            "bias_correct": 0,
            "bias_total": 0,
            "daily_results": []
        }
    
    def save_performance_history(self, history: Dict):
        """Salva histórico de performance"""
        history_file = f"{self.data_dir}/performance_history.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def evaluate_setup(self, setup: Dict, price_history: List[Dict], setup_type: str) -> Dict:
        """Avalia se um setup foi vencedor, perdedor ou está em andamento"""
        
        if not setup or not price_history:
            return {"status": "not_evaluated", "result": None}
        
        entry_low = setup['entry_low']
        entry_high = setup['entry_high']
        stop_loss = setup['stop_loss']
        target1 = setup['target1']
        target2 = setup['target2']
        
        # Verificar se a entrada foi ativada
        entry_activated = False
        entry_price = None
        
        for candle in price_history:
            if setup_type == "long":
                if candle['low'] <= entry_high:
                    entry_activated = True
                    entry_price = min(candle['low'], entry_high)
                    break
            else:  # short
                if candle['high'] >= entry_low:
                    entry_activated = True
                    entry_price = max(candle['high'], entry_low)
                    break
        
        if not entry_activated:
            return {
                "status": "not_activated",
                "result": "⚪ NÃO ATIVADO",
                "description": "Preço não atingiu zona de entrada",
                "pnl": 0
            }
        
        # Verificar resultado após entrada
        entry_index = price_history.index(candle) if entry_activated else 0
        
        hit_stop = False
        hit_target1 = False
        hit_target2 = False
        
        for candle in price_history[entry_index:]:
            if setup_type == "long":
                if candle['low'] <= stop_loss:
                    hit_stop = True
                    break
                if candle['high'] >= target2:
                    hit_target2 = True
                    break
                if candle['high'] >= target1:
                    hit_target1 = True
            else:  # short
                if candle['high'] >= stop_loss:
                    hit_stop = True
                    break
                if candle['low'] <= target2:
                    hit_target2 = True
                    break
                if candle['low'] <= target1:
                    hit_target1 = True
        
        # Determinar resultado
        if hit_stop:
            pnl = ((stop_loss - entry_price) / entry_price * 100) if setup_type == "long" else ((entry_price - stop_loss) / entry_price * 100)
            return {
                "status": "stop_loss",
                "result": "❌ STOP LOSS",
                "description": f"Stop acionado em ${stop_loss:,.2f}",
                "pnl": round(pnl, 2)
            }
        elif hit_target2:
            pnl = ((target2 - entry_price) / entry_price * 100) if setup_type == "long" else ((entry_price - target2) / entry_price * 100)
            return {
                "status": "target2",
                "result": "✅ ALVO 2 ATINGIDO",
                "description": f"Alvo 2 atingido em ${target2:,.2f}",
                "pnl": round(pnl, 2)
            }
        elif hit_target1:
            pnl = ((target1 - entry_price) / entry_price * 100) if setup_type == "long" else ((entry_price - target1) / entry_price * 100)
            return {
                "status": "target1",
                "result": "✅ ALVO 1 ATINGIDO",
                "description": f"Alvo 1 atingido em ${target1:,.2f}",
                "pnl": round(pnl, 2)
            }
        else:
            # Ainda em andamento
            current_price = price_history[-1]['close']
            unrealized_pnl = ((current_price - entry_price) / entry_price * 100) if setup_type == "long" else ((entry_price - current_price) / entry_price * 100)
            return {
                "status": "ongoing",
                "result": "⏳ EM ANDAMENTO",
                "description": f"Posição aberta, preço atual ${current_price:,.2f}",
                "pnl": round(unrealized_pnl, 2)
            }
    
    def evaluate_bias(self, bias: str, open_price: float, close_price: float) -> Dict:
        """Avalia se o viés do dia estava correto"""
        price_change = ((close_price - open_price) / open_price) * 100
        
        if bias == "BULLISH":
            if price_change > 0.5:
                return {"correct": True, "result": "✅ ACERTO", "description": f"Viés bullish, mercado subiu {price_change:.2f}%"}
            elif price_change < -0.5:
                return {"correct": False, "result": "❌ ERRO", "description": f"Viés bullish, mas mercado caiu {price_change:.2f}%"}
            else:
                return {"correct": True, "result": "🟡 PARCIAL", "description": f"Viés bullish, mercado lateral ({price_change:.2f}%)"}
        
        elif bias == "BEARISH":
            if price_change < -0.5:
                return {"correct": True, "result": "✅ ACERTO", "description": f"Viés bearish, mercado caiu {price_change:.2f}%"}
            elif price_change > 0.5:
                return {"correct": False, "result": "❌ ERRO", "description": f"Viés bearish, mas mercado subiu {price_change:.2f}%"}
            else:
                return {"correct": True, "result": "🟡 PARCIAL", "description": f"Viés bearish, mercado lateral ({price_change:.2f}%)"}
        
        else:  # NEUTRO
            if abs(price_change) < 2:
                return {"correct": True, "result": "✅ ACERTO", "description": f"Viés neutro, mercado lateral ({price_change:.2f}%)"}
            else:
                return {"correct": False, "result": "🟡 PARCIAL", "description": f"Viés neutro, mas mercado moveu {price_change:.2f}%"}
    
    def generate_report(self) -> Dict:
        """Gera o relatório de fechamento completo"""
        now = datetime.now(self.timezone)
        
        # Carregar análise da manhã
        morning_analysis = self.load_morning_analysis()
        if not morning_analysis:
            return {"error": "Análise da manhã não encontrada"}
        
        # Carregar histórico de performance
        performance_history = self.load_performance_history()
        
        # Obter preços atuais
        current_prices = self.get_current_prices()
        
        # Avaliar cada ativo
        results = {}
        day_stats = {
            "total_setups": 0,
            "winning": 0,
            "losing": 0,
            "ongoing": 0,
            "not_activated": 0,
            "total_pnl": 0,
            "bias_correct": 0,
            "bias_total": 0
        }
        
        for symbol, analysis in morning_analysis.get('analyses', {}).items():
            price_history = self.get_price_history(symbol, 24)
            
            # Preço de abertura do dia (21:00 de ontem)
            open_price = price_history[0]['open'] if price_history else analysis['price']
            close_price = current_prices.get(symbol, analysis['price'])
            
            # Avaliar setups
            long_result = None
            short_result = None
            
            if analysis['setups']['long']:
                long_result = self.evaluate_setup(analysis['setups']['long'], price_history, 'long')
                day_stats['total_setups'] += 1
                
                if long_result['status'] in ['target1', 'target2']:
                    day_stats['winning'] += 1
                elif long_result['status'] == 'stop_loss':
                    day_stats['losing'] += 1
                elif long_result['status'] == 'ongoing':
                    day_stats['ongoing'] += 1
                else:
                    day_stats['not_activated'] += 1
                
                day_stats['total_pnl'] += long_result.get('pnl', 0)
            
            if analysis['setups']['short']:
                short_result = self.evaluate_setup(analysis['setups']['short'], price_history, 'short')
                day_stats['total_setups'] += 1
                
                if short_result['status'] in ['target1', 'target2']:
                    day_stats['winning'] += 1
                elif short_result['status'] == 'stop_loss':
                    day_stats['losing'] += 1
                elif short_result['status'] == 'ongoing':
                    day_stats['ongoing'] += 1
                else:
                    day_stats['not_activated'] += 1
                
                day_stats['total_pnl'] += short_result.get('pnl', 0)
            
            # Avaliar viés
            bias_result = self.evaluate_bias(analysis['bias']['bias'], open_price, close_price)
            day_stats['bias_total'] += 1
            if bias_result['correct']:
                day_stats['bias_correct'] += 1
            
            results[symbol] = {
                "symbol": symbol,
                "open_price": open_price,
                "close_price": close_price,
                "price_change": round(((close_price - open_price) / open_price) * 100, 2),
                "bias_morning": analysis['bias']['bias'],
                "bias_result": bias_result,
                "long_setup": analysis['setups']['long'],
                "long_result": long_result,
                "short_setup": analysis['setups']['short'],
                "short_result": short_result
            }
        
        # Atualizar histórico de performance
        performance_history['total_setups'] += day_stats['total_setups']
        performance_history['winning_setups'] += day_stats['winning']
        performance_history['losing_setups'] += day_stats['losing']
        performance_history['ongoing_setups'] = day_stats['ongoing']
        performance_history['bias_correct'] += day_stats['bias_correct']
        performance_history['bias_total'] += day_stats['bias_total']
        
        # Adicionar resultado do dia ao histórico
        performance_history['daily_results'].append({
            "date": now.strftime('%Y-%m-%d'),
            "stats": day_stats
        })
        
        # Manter apenas últimos 30 dias
        if len(performance_history['daily_results']) > 30:
            performance_history['daily_results'] = performance_history['daily_results'][-30:]
        
        # Salvar histórico
        self.save_performance_history(performance_history)
        
        # Calcular estatísticas gerais
        total_evaluated = performance_history['winning_setups'] + performance_history['losing_setups']
        win_rate = (performance_history['winning_setups'] / total_evaluated * 100) if total_evaluated > 0 else 0
        bias_accuracy = (performance_history['bias_correct'] / performance_history['bias_total'] * 100) if performance_history['bias_total'] > 0 else 0
        
        report = {
            "timestamp": now.isoformat(),
            "date": now.strftime("%d de %B de %Y").replace("January", "Janeiro").replace("February", "Fevereiro").replace("March", "Março").replace("April", "Abril").replace("May", "Maio").replace("June", "Junho").replace("July", "Julho").replace("August", "Agosto").replace("September", "Setembro").replace("October", "Outubro").replace("November", "Novembro").replace("December", "Dezembro"),
            "time": now.strftime("%H:%M"),
            "results": results,
            "day_stats": day_stats,
            "cumulative_stats": {
                "total_setups": performance_history['total_setups'],
                "winning_setups": performance_history['winning_setups'],
                "losing_setups": performance_history['losing_setups'],
                "ongoing_setups": performance_history['ongoing_setups'],
                "win_rate": round(win_rate, 1),
                "bias_accuracy": round(bias_accuracy, 1)
            }
        }
        
        # Salvar relatório
        report_file = f"{self.data_dir}/closing_report_{now.strftime('%Y%m%d')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Salvar como latest
        latest_file = f"{self.data_dir}/latest_closing_report.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Relatório de fechamento salvo em: {report_file}")
        return report


if __name__ == "__main__":
    generator = ClosingReportGenerator()
    report = generator.generate_report()
    print(json.dumps(report, indent=2, default=str))
