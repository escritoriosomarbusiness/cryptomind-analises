#!/usr/bin/env python3
"""
CryptoMind IA - Analisador Multi-Timeframe
Analisa ativos em múltiplos timeframes (W1, D1, H4, H1)
Inclui análise de BTC.D e USDT.D
Usa CoinGecko como fonte de dados principal
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz
import time

# Configuração de timezone
BR_TZ = pytz.timezone('America/Sao_Paulo')

class MultiTimeframeAnalyzer:
    """Analisador de múltiplos timeframes para criptomoedas."""
    
    # Ativos para análise
    ASSETS = {
        'BTC': {'id': 'bitcoin', 'name': 'Bitcoin'},
        'ETH': {'id': 'ethereum', 'name': 'Ethereum'},
        'SOL': {'id': 'solana', 'name': 'Solana'},
        'BNB': {'id': 'binancecoin', 'name': 'BNB'},
        'XRP': {'id': 'ripple', 'name': 'XRP'}
    }
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'CryptoMind-IA/2.0'
        })
    
    def _api_request(self, endpoint: str, params: dict = None) -> Optional[Dict]:
        """Faz requisição à API com tratamento de erros."""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Rate limit atingido, aguardando...")
                time.sleep(60)
                return self._api_request(endpoint, params)
            else:
                print(f"Erro na API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def get_market_data(self, coin_id: str, days: int = 90) -> Optional[Dict]:
        """Obtém dados de mercado históricos."""
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily' if days > 1 else 'hourly'
        }
        return self._api_request(f"coins/{coin_id}/market_chart", params)
    
    def get_ohlc(self, coin_id: str, days: int = 90) -> Optional[List]:
        """Obtém dados OHLC."""
        params = {
            'vs_currency': 'usd',
            'days': days
        }
        return self._api_request(f"coins/{coin_id}/ohlc", params)
    
    def get_current_price(self, coin_id: str) -> Optional[Dict]:
        """Obtém preço atual e dados de mercado."""
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_market_cap': 'true'
        }
        return self._api_request("simple/price", params)
    
    def get_global_data(self) -> Optional[Dict]:
        """Obtém dados globais do mercado."""
        return self._api_request("global")
    
    def get_fear_greed_index(self) -> Optional[Dict]:
        """Obtém Fear & Greed Index."""
        try:
            response = self.session.get(
                "https://api.alternative.me/fng/",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    return data['data'][0]
            return None
        except Exception as e:
            print(f"Erro ao obter Fear & Greed: {e}")
            return None
    
    def calculate_ema(self, prices: List[float], period: int) -> List[float]:
        """Calcula EMA (Exponential Moving Average)."""
        if len(prices) < period:
            return [prices[-1]] if prices else []
        
        multiplier = 2 / (period + 1)
        ema = [sum(prices[:period]) / period]
        
        for price in prices[period:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        
        return ema
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calcula RSI (Relative Strength Index)."""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    def calculate_macd(self, prices: List[float]) -> Dict:
        """Calcula MACD."""
        if len(prices) < 26:
            return {'macd': 0, 'signal': 0, 'histogram': 0, 'trend': 'NEUTRO'}
        
        ema_12 = self.calculate_ema(prices, 12)
        ema_26 = self.calculate_ema(prices, 26)
        
        min_len = min(len(ema_12), len(ema_26))
        ema_12 = ema_12[-min_len:]
        ema_26 = ema_26[-min_len:]
        
        macd_line = [e12 - e26 for e12, e26 in zip(ema_12, ema_26)]
        signal_line = self.calculate_ema(macd_line, 9)
        
        if not signal_line:
            return {'macd': 0, 'signal': 0, 'histogram': 0, 'trend': 'NEUTRO'}
        
        histogram = macd_line[-1] - signal_line[-1]
        
        # Determinar tendência do MACD
        if histogram > 0 and macd_line[-1] > macd_line[-2]:
            trend = 'BULLISH'
        elif histogram < 0 and macd_line[-1] < macd_line[-2]:
            trend = 'BEARISH'
        else:
            trend = 'NEUTRO'
        
        return {
            'macd': round(macd_line[-1], 4),
            'signal': round(signal_line[-1], 4),
            'histogram': round(histogram, 4),
            'trend': trend
        }
    
    def identify_trend(self, prices: List[float]) -> Dict:
        """Identifica tendência baseada nas EMAs."""
        if len(prices) < 50:
            return {
                'trend': 'INDEFINIDO',
                'strength': 'FRACA',
                'ema_alignment': 'INDEFINIDO'
            }
        
        current_price = prices[-1]
        
        ema_9 = self.calculate_ema(prices, 9)[-1]
        ema_21 = self.calculate_ema(prices, 21)[-1]
        ema_50 = self.calculate_ema(prices, 50)[-1]
        
        # Posição do preço
        above_ema_9 = current_price > ema_9
        above_ema_21 = current_price > ema_21
        above_ema_50 = current_price > ema_50
        
        # Alinhamento das EMAs
        emas_bullish = ema_9 > ema_21 > ema_50
        emas_bearish = ema_9 < ema_21 < ema_50
        
        # Direção das EMAs
        ema_9_list = self.calculate_ema(prices, 9)
        ema_21_list = self.calculate_ema(prices, 21)
        
        ema_9_rising = ema_9_list[-1] > ema_9_list[-3] if len(ema_9_list) >= 3 else False
        ema_21_rising = ema_21_list[-1] > ema_21_list[-3] if len(ema_21_list) >= 3 else False
        
        # Determinar tendência
        if emas_bullish and above_ema_50:
            trend = "BULLISH"
            strength = "FORTE" if above_ema_9 and ema_9_rising else "MODERADA"
        elif emas_bearish and not above_ema_50:
            trend = "BEARISH"
            strength = "FORTE" if not above_ema_9 and not ema_9_rising else "MODERADA"
        else:
            trend = "NEUTRO"
            strength = "CONSOLIDAÇÃO"
        
        return {
            'trend': trend,
            'strength': strength,
            'price': round(current_price, 2),
            'ema_9': round(ema_9, 2),
            'ema_21': round(ema_21, 2),
            'ema_50': round(ema_50, 2),
            'above_ema_9': above_ema_9,
            'above_ema_21': above_ema_21,
            'above_ema_50': above_ema_50,
            'ema_9_rising': ema_9_rising,
            'ema_21_rising': ema_21_rising,
            'ema_alignment': 'BULLISH' if emas_bullish else ('BEARISH' if emas_bearish else 'MIXED')
        }
    
    def identify_structure(self, prices: List[float], window: int = 5) -> Dict:
        """Identifica estrutura de mercado."""
        if len(prices) < window * 4:
            return {'structure': 'INDEFINIDA', 'description': 'Dados insuficientes'}
        
        # Encontrar swings (máximas e mínimas locais)
        highs = []
        lows = []
        
        for i in range(window, len(prices) - window):
            # Máxima local
            if prices[i] == max(prices[i-window:i+window+1]):
                highs.append((i, prices[i]))
            # Mínima local
            if prices[i] == min(prices[i-window:i+window+1]):
                lows.append((i, prices[i]))
        
        if len(highs) < 2 or len(lows) < 2:
            return {'structure': 'INDEFINIDA', 'description': 'Swings insuficientes'}
        
        # Analisar últimos swings
        last_highs = [h[1] for h in highs[-3:]]
        last_lows = [l[1] for l in lows[-3:]]
        
        # Higher Highs e Higher Lows
        hh = len(last_highs) >= 2 and last_highs[-1] > last_highs[-2]
        hl = len(last_lows) >= 2 and last_lows[-1] > last_lows[-2]
        
        # Lower Highs e Lower Lows
        lh = len(last_highs) >= 2 and last_highs[-1] < last_highs[-2]
        ll = len(last_lows) >= 2 and last_lows[-1] < last_lows[-2]
        
        if hh and hl:
            structure = "ALTA"
            description = "Higher Highs + Higher Lows confirmados"
        elif lh and ll:
            structure = "BAIXA"
            description = "Lower Highs + Lower Lows confirmados"
        elif hh or hl:
            structure = "ALTA_FORMANDO"
            description = "Estrutura de alta em formação"
        elif lh or ll:
            structure = "BAIXA_FORMANDO"
            description = "Estrutura de baixa em formação"
        else:
            structure = "CONSOLIDAÇÃO"
            description = "Mercado em range/consolidação"
        
        return {
            'structure': structure,
            'description': description,
            'last_high': round(last_highs[-1], 2) if last_highs else 0,
            'last_low': round(last_lows[-1], 2) if last_lows else 0,
            'hh': hh,
            'hl': hl,
            'lh': lh,
            'll': ll
        }
    
    def find_support_resistance(self, prices: List[float]) -> Dict:
        """Encontra níveis de suporte e resistência."""
        if len(prices) < 20:
            return {'supports': [], 'resistances': [], 'key_levels': []}
        
        current_price = prices[-1]
        
        # Encontrar pivots
        window = 5
        supports = []
        resistances = []
        
        for i in range(window, len(prices) - window):
            local_min = min(prices[i-window:i+window+1])
            local_max = max(prices[i-window:i+window+1])
            
            if prices[i] == local_min:
                supports.append(prices[i])
            if prices[i] == local_max:
                resistances.append(prices[i])
        
        # Filtrar níveis relevantes
        valid_supports = sorted(set([s for s in supports if s < current_price]), reverse=True)[:3]
        valid_resistances = sorted(set([r for r in resistances if r > current_price]))[:3]
        
        # Níveis chave (mais tocados)
        all_levels = supports + resistances
        level_counts = {}
        tolerance = current_price * 0.01  # 1% de tolerância
        
        for level in all_levels:
            found = False
            for key in level_counts:
                if abs(level - key) < tolerance:
                    level_counts[key] += 1
                    found = True
                    break
            if not found:
                level_counts[level] = 1
        
        key_levels = sorted(level_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        key_levels = [round(k[0], 2) for k in key_levels]
        
        return {
            'supports': [round(s, 2) for s in valid_supports],
            'resistances': [round(r, 2) for r in valid_resistances],
            'key_levels': key_levels,
            'nearest_support': round(valid_supports[0], 2) if valid_supports else None,
            'nearest_resistance': round(valid_resistances[0], 2) if valid_resistances else None
        }
    
    def analyze_asset(self, symbol: str) -> Optional[Dict]:
        """Analisa um ativo completo."""
        asset_info = self.ASSETS.get(symbol)
        if not asset_info:
            return None
        
        coin_id = asset_info['id']
        
        # Obter dados históricos (90 dias para análise diária)
        market_data = self.get_market_data(coin_id, 90)
        if not market_data:
            return None
        
        prices = [p[1] for p in market_data.get('prices', [])]
        
        if len(prices) < 50:
            return None
        
        # Obter preço atual
        current_data = self.get_current_price(coin_id)
        current_price = current_data.get(coin_id, {}).get('usd', prices[-1]) if current_data else prices[-1]
        change_24h = current_data.get(coin_id, {}).get('usd_24h_change', 0) if current_data else 0
        
        # Calcular indicadores
        trend = self.identify_trend(prices)
        structure = self.identify_structure(prices)
        sr_levels = self.find_support_resistance(prices)
        rsi = self.calculate_rsi(prices)
        macd = self.calculate_macd(prices)
        
        # Determinar viés
        bullish_factors = 0
        bearish_factors = 0
        
        if trend['trend'] == 'BULLISH':
            bullish_factors += 2
        elif trend['trend'] == 'BEARISH':
            bearish_factors += 2
        
        if structure['structure'] in ['ALTA', 'ALTA_FORMANDO']:
            bullish_factors += 1
        elif structure['structure'] in ['BAIXA', 'BAIXA_FORMANDO']:
            bearish_factors += 1
        
        if rsi < 30:
            bullish_factors += 1  # Sobrevendido = oportunidade de compra
        elif rsi > 70:
            bearish_factors += 1  # Sobrecomprado = oportunidade de venda
        
        if macd['trend'] == 'BULLISH':
            bullish_factors += 1
        elif macd['trend'] == 'BEARISH':
            bearish_factors += 1
        
        if bullish_factors > bearish_factors + 1:
            bias = 'BULLISH'
        elif bearish_factors > bullish_factors + 1:
            bias = 'BEARISH'
        else:
            bias = 'NEUTRO'
        
        return {
            'symbol': symbol,
            'name': asset_info['name'],
            'price': round(current_price, 2),
            'change_24h': round(change_24h, 2),
            'trend': trend,
            'structure': structure,
            'sr_levels': sr_levels,
            'indicators': {
                'rsi': rsi,
                'rsi_status': 'SOBRECOMPRADO' if rsi > 70 else ('SOBREVENDIDO' if rsi < 30 else 'NEUTRO'),
                'macd': macd
            },
            'bias': bias,
            'bullish_factors': bullish_factors,
            'bearish_factors': bearish_factors
        }
    
    def analyze_dominance(self) -> Dict:
        """Analisa dominância do BTC e USDT."""
        global_data = self.get_global_data()
        
        if not global_data:
            return {
                'btc_d': {'dominance': 0, 'impact': 'INDEFINIDO'},
                'usdt_d': {'dominance': 0, 'impact': 'INDEFINIDO'}
            }
        
        data = global_data.get('data', {})
        market_cap_pct = data.get('market_cap_percentage', {})
        
        btc_dominance = market_cap_pct.get('btc', 0)
        usdt_dominance = market_cap_pct.get('usdt', 0)
        
        # Análise BTC.D
        # BTC.D alto (>55%) = capital concentrado em BTC = bearish para alts
        # BTC.D baixo (<45%) = capital fluindo para alts = bullish para alts
        if btc_dominance > 55:
            btc_d_impact = 'BEARISH'
            btc_d_analysis = f"BTC.D em {btc_dominance:.2f}% - Alta dominância, capital concentrado em BTC"
        elif btc_dominance < 45:
            btc_d_impact = 'BULLISH'
            btc_d_analysis = f"BTC.D em {btc_dominance:.2f}% - Baixa dominância, capital fluindo para altcoins"
        else:
            btc_d_impact = 'NEUTRO'
            btc_d_analysis = f"BTC.D em {btc_dominance:.2f}% - Dominância neutra"
        
        # Análise USDT.D
        # USDT.D alto (>6%) = dinheiro em stablecoins = bearish para cripto
        # USDT.D baixo (<4%) = dinheiro em cripto = bullish para cripto
        if usdt_dominance > 6:
            usdt_d_impact = 'BEARISH'
            usdt_d_analysis = f"USDT.D em {usdt_dominance:.2f}% - Dinheiro em stablecoins, mercado cauteloso"
        elif usdt_dominance < 4:
            usdt_d_impact = 'BULLISH'
            usdt_d_analysis = f"USDT.D em {usdt_dominance:.2f}% - Dinheiro saindo de stablecoins para cripto"
        else:
            usdt_d_impact = 'NEUTRO'
            usdt_d_analysis = f"USDT.D em {usdt_dominance:.2f}% - Fluxo neutro"
        
        return {
            'btc_d': {
                'dominance': round(btc_dominance, 2),
                'impact': btc_d_impact,
                'analysis': btc_d_analysis
            },
            'usdt_d': {
                'dominance': round(usdt_dominance, 2),
                'impact': usdt_d_impact,
                'analysis': usdt_d_analysis
            }
        }
    
    def run_full_analysis(self) -> Dict:
        """Executa análise completa."""
        timestamp = datetime.now(BR_TZ)
        
        result = {
            'timestamp': timestamp.isoformat(),
            'date': timestamp.strftime('%d/%m/%Y'),
            'time': timestamp.strftime('%H:%M'),
            'assets': {},
            'dominance': {},
            'fear_greed': {},
            'market_summary': {}
        }
        
        # Fear & Greed Index
        print("Obtendo Fear & Greed Index...")
        fg = self.get_fear_greed_index()
        if fg:
            result['fear_greed'] = {
                'value': int(fg.get('value', 50)),
                'classification': fg.get('value_classification', 'Neutral'),
                'timestamp': fg.get('timestamp', '')
            }
        
        # Dominância
        print("Analisando dominância...")
        result['dominance'] = self.analyze_dominance()
        time.sleep(1)  # Rate limiting
        
        # Ativos
        for symbol in self.ASSETS.keys():
            print(f"Analisando {symbol}...")
            analysis = self.analyze_asset(symbol)
            if analysis:
                result['assets'][symbol] = analysis
            time.sleep(1)  # Rate limiting
        
        # Resumo do mercado
        result['market_summary'] = self._generate_summary(result)
        
        return result
    
    def _generate_summary(self, data: Dict) -> Dict:
        """Gera resumo do mercado."""
        bullish_assets = []
        bearish_assets = []
        neutral_assets = []
        
        for symbol, asset in data['assets'].items():
            bias = asset.get('bias', 'NEUTRO')
            if bias == 'BULLISH':
                bullish_assets.append(symbol)
            elif bias == 'BEARISH':
                bearish_assets.append(symbol)
            else:
                neutral_assets.append(symbol)
        
        # Fatores macro
        btc_d_impact = data['dominance'].get('btc_d', {}).get('impact', 'NEUTRO')
        usdt_d_impact = data['dominance'].get('usdt_d', {}).get('impact', 'NEUTRO')
        fg_value = data['fear_greed'].get('value', 50)
        
        # Calcular sentimento geral
        bullish_score = len(bullish_assets)
        bearish_score = len(bearish_assets)
        
        if btc_d_impact == 'BULLISH':
            bullish_score += 1
        elif btc_d_impact == 'BEARISH':
            bearish_score += 1
        
        if usdt_d_impact == 'BULLISH':
            bullish_score += 1
        elif usdt_d_impact == 'BEARISH':
            bearish_score += 1
        
        # Fear & Greed
        if fg_value < 25:
            bullish_score += 1  # Medo extremo = oportunidade
            fg_signal = 'BULLISH'
        elif fg_value > 75:
            bearish_score += 1  # Ganância extrema = cautela
            fg_signal = 'BEARISH'
        else:
            fg_signal = 'NEUTRO'
        
        # Determinar sentimento
        if bullish_score > bearish_score + 2:
            sentiment = 'BULLISH'
        elif bearish_score > bullish_score + 2:
            sentiment = 'BEARISH'
        else:
            sentiment = 'NEUTRO'
        
        # Recomendação
        if sentiment == 'BULLISH' and usdt_d_impact != 'BEARISH':
            recommendation = "Contexto favorável para operações LONG. Priorizar setups de continuação e rompimento."
        elif sentiment == 'BEARISH' and usdt_d_impact != 'BULLISH':
            recommendation = "Contexto favorável para operações SHORT ou proteção. Cautela com posições compradas."
        else:
            recommendation = "Mercado misto. Operar com tamanho reduzido e priorizar setups de alta confluência."
        
        return {
            'sentiment': sentiment,
            'bullish_score': bullish_score,
            'bearish_score': bearish_score,
            'bullish_assets': bullish_assets,
            'bearish_assets': bearish_assets,
            'neutral_assets': neutral_assets,
            'btc_d_impact': btc_d_impact,
            'usdt_d_impact': usdt_d_impact,
            'fear_greed_signal': fg_signal,
            'recommendation': recommendation
        }


def main():
    """Função principal."""
    analyzer = MultiTimeframeAnalyzer()
    
    print("=" * 60)
    print("CryptoMind IA - Análise Multi-Timeframe v2.0")
    print("=" * 60)
    
    result = analyzer.run_full_analysis()
    
    # Salvar resultado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '..', 'data', 'multi_timeframe_analysis.json')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nAnálise salva em: {output_path}")
    
    # Exibir resumo
    summary = result.get('market_summary', {})
    fg = result.get('fear_greed', {})
    dom = result.get('dominance', {})
    
    print(f"\n{'=' * 60}")
    print("RESUMO DO MERCADO")
    print(f"{'=' * 60}")
    print(f"Data/Hora: {result.get('date')} {result.get('time')}")
    print(f"\nFear & Greed: {fg.get('value', 'N/A')} ({fg.get('classification', 'N/A')})")
    print(f"BTC.D: {dom.get('btc_d', {}).get('dominance', 'N/A')}% - {dom.get('btc_d', {}).get('impact', 'N/A')}")
    print(f"USDT.D: {dom.get('usdt_d', {}).get('dominance', 'N/A')}% - {dom.get('usdt_d', {}).get('impact', 'N/A')}")
    print(f"\nSentimento Geral: {summary.get('sentiment', 'N/A')}")
    print(f"Ativos Bullish: {', '.join(summary.get('bullish_assets', [])) or 'Nenhum'}")
    print(f"Ativos Bearish: {', '.join(summary.get('bearish_assets', [])) or 'Nenhum'}")
    print(f"\nRecomendação: {summary.get('recommendation', 'N/A')}")
    
    return result





def run_analysis() -> Optional[Dict]:
    """Executa análise e retorna resultado."""
    analyzer = MultiTimeframeAnalyzer()
    return analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
