#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de Análises Automatizadas
Gera análises para BTC + Top 5 Altcoins no formato do site
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz

class CryptoAnalyzer:
    """Analisa criptomoedas e gera setups de day trade"""
    
    def __init__(self):
        self.assets = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA"]
        self.timezone = pytz.timezone('America/Sao_Paulo')
        self.data_dir = "/home/ubuntu/cryptomind-analises/data"
        
    def get_binance_data(self, symbol: str) -> Dict:
        """Obtém dados do Binance"""
        try:
            pair = f"{symbol}USDT"
            
            # Ticker 24h
            ticker = requests.get(
                f"https://api.binance.com/api/v3/ticker/24hr?symbol={pair}",
                timeout=10
            ).json()
            
            # Klines 4H para análise
            klines_4h = requests.get(
                f"https://api.binance.com/api/v3/klines?symbol={pair}&interval=4h&limit=210",
                timeout=10
            ).json()
            
            # Klines 1H para estrutura
            klines_1h = requests.get(
                f"https://api.binance.com/api/v3/klines?symbol={pair}&interval=1h&limit=50",
                timeout=10
            ).json()
            
            # Klines 15m para entrada
            klines_15m = requests.get(
                f"https://api.binance.com/api/v3/klines?symbol={pair}&interval=15m&limit=100",
                timeout=10
            ).json()
            
            return {
                "ticker": ticker,
                "klines_4h": klines_4h,
                "klines_1h": klines_1h,
                "klines_15m": klines_15m
            }
        except Exception as e:
            print(f"Erro Binance {symbol}: {e}")
            return None
    
    def get_futures_data(self, symbol: str) -> Dict:
        """Obtém dados de futuros (funding, OI, L/S)"""
        try:
            pair = f"{symbol}USDT"
            base_url = "https://fapi.binance.com"
            
            # Funding Rate
            funding = requests.get(
                f"{base_url}/fapi/v1/fundingRate?symbol={pair}&limit=1",
                timeout=10
            ).json()
            
            # Open Interest
            oi = requests.get(
                f"{base_url}/fapi/v1/openInterest?symbol={pair}",
                timeout=10
            ).json()
            
            # Long/Short Ratio
            ls_ratio = requests.get(
                f"{base_url}/futures/data/globalLongShortAccountRatio?symbol={pair}&period=1h&limit=1",
                timeout=10
            ).json()
            
            return {
                "funding_rate": float(funding[0]['fundingRate']) if funding else 0,
                "open_interest": float(oi['openInterest']) if oi else 0,
                "long_short_ratio": float(ls_ratio[0]['longShortRatio']) if ls_ratio else 1
            }
        except Exception as e:
            print(f"Erro Futures {symbol}: {e}")
            return {"funding_rate": 0, "open_interest": 0, "long_short_ratio": 1}
    
    def get_fear_greed(self) -> Dict:
        """Obtém Fear & Greed Index"""
        try:
            data = requests.get(
                "https://api.alternative.me/fng/?limit=7",
                timeout=10
            ).json()
            
            return {
                "value": int(data['data'][0]['value']),
                "classification": data['data'][0]['value_classification'],
                "yesterday": int(data['data'][1]['value']) if len(data['data']) > 1 else 0,
                "week_ago": int(data['data'][6]['value']) if len(data['data']) > 6 else 0
            }
        except Exception as e:
            print(f"Erro Fear & Greed: {e}")
            return {"value": 50, "classification": "Neutral", "yesterday": 50, "week_ago": 50}
    
    def calculate_ema(self, prices: List[float], period: int) -> float:
        """Calcula EMA"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return round(ema, 2)
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calcula RSI"""
        if len(prices) < period + 1:
            return 50
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)
    
    def analyze_structure(self, klines: List) -> Dict:
        """Analisa estrutura de mercado (HH/HL ou LH/LL)"""
        highs = [float(k[2]) for k in klines]
        lows = [float(k[3]) for k in klines]
        
        # Encontrar swing points
        swing_highs = []
        swing_lows = []
        
        for i in range(2, len(highs) - 2):
            if highs[i] > max(highs[i-2:i]) and highs[i] > max(highs[i+1:i+3]):
                swing_highs.append((i, highs[i]))
            if lows[i] < min(lows[i-2:i]) and lows[i] < min(lows[i+1:i+3]):
                swing_lows.append((i, lows[i]))
        
        structure = "consolidation"
        
        if len(swing_highs) >= 2 and len(swing_lows) >= 2:
            last_hh = swing_highs[-1][1] > swing_highs[-2][1] if len(swing_highs) >= 2 else False
            last_hl = swing_lows[-1][1] > swing_lows[-2][1] if len(swing_lows) >= 2 else False
            last_lh = swing_highs[-1][1] < swing_highs[-2][1] if len(swing_highs) >= 2 else False
            last_ll = swing_lows[-1][1] < swing_lows[-2][1] if len(swing_lows) >= 2 else False
            
            if last_hh and last_hl:
                structure = "bullish"
            elif last_lh and last_ll:
                structure = "bearish"
        
        return {
            "type": structure,
            "swing_highs": [sh[1] for sh in swing_highs[-3:]],
            "swing_lows": [sl[1] for sl in swing_lows[-3:]],
            "last_swing_high": swing_highs[-1][1] if swing_highs else highs[-1],
            "last_swing_low": swing_lows[-1][1] if swing_lows else lows[-1]
        }
    
    def calculate_sr_levels(self, klines: List, current_price: float) -> Dict:
        """Calcula níveis de suporte e resistência"""
        highs = [float(k[2]) for k in klines]
        lows = [float(k[3]) for k in klines]
        
        # PDH/PDL (últimas 6 velas de 4h = 24h)
        pdh = max(highs[-6:])
        pdl = min(lows[-6:])
        
        # Níveis psicológicos
        if current_price > 1000:
            round_level = round(current_price / 1000) * 1000
        elif current_price > 100:
            round_level = round(current_price / 100) * 100
        elif current_price > 10:
            round_level = round(current_price / 10) * 10
        else:
            round_level = round(current_price, 1)
        
        # Resistências
        resistances = sorted(set([
            pdh,
            round_level if round_level > current_price else round_level + (1000 if current_price > 1000 else 100 if current_price > 100 else 10)
        ]))
        
        # Suportes
        supports = sorted(set([
            pdl,
            round_level if round_level < current_price else round_level - (1000 if current_price > 1000 else 100 if current_price > 100 else 10)
        ]), reverse=True)
        
        return {
            "pdh": round(pdh, 2),
            "pdl": round(pdl, 2),
            "resistances": [round(r, 2) for r in resistances[:2]],
            "supports": [round(s, 2) for s in supports[:2]]
        }
    
    def generate_setup(self, symbol: str, data: Dict, structure: Dict, sr_levels: Dict, 
                       emas: Dict, rsi: float, futures: Dict) -> Dict:
        """Gera setups de trade baseado na análise"""
        
        current_price = data['price']
        setups = {"long": None, "short": None}
        
        # Análise para LONG
        long_score = 0
        long_reasons = []
        
        # Price Action - Estrutura bullish
        if structure['type'] == 'bullish':
            long_score += 3
            long_reasons.append("Estrutura HH + HL confirmada")
        elif structure['type'] == 'consolidation':
            long_score += 1
            long_reasons.append("Consolidação - aguardar confirmação")
        
        # Preço próximo a suporte
        nearest_support = sr_levels['supports'][0] if sr_levels['supports'] else sr_levels['pdl']
        distance_to_support = ((current_price - nearest_support) / current_price) * 100
        
        if distance_to_support < 1.5:  # Menos de 1.5% do suporte
            long_score += 2
            long_reasons.append(f"Preço próximo ao suporte ${nearest_support:,.0f}")
        
        # EMAs
        if current_price > emas['ema_200']:
            long_score += 1
            long_reasons.append("Preço acima da EMA 200")
        if emas['ema_9'] > emas['ema_21']:
            long_score += 1
            long_reasons.append("EMA 9 > EMA 21 (momentum bullish)")
        
        # RSI
        if rsi < 40:
            long_score += 1
            long_reasons.append(f"RSI sobrevendido ({rsi})")
        elif rsi < 50:
            long_score += 0.5
        
        # Funding Rate
        if futures['funding_rate'] < 0.0001:
            long_score += 1
            long_reasons.append("Funding Rate baixo/negativo")
        
        # Gerar setup LONG se score >= 4
        if long_score >= 4:
            entry_low = nearest_support * 1.001
            entry_high = nearest_support * 1.005
            stop_loss = nearest_support * 0.99
            
            risk = entry_low - stop_loss
            target1 = entry_low + (risk * 1.5)
            target2 = entry_low + (risk * 2.5)
            
            setups['long'] = {
                "type": "LONG",
                "style": "Conservador" if long_score >= 6 else "Moderado",
                "entry_low": round(entry_low, 2),
                "entry_high": round(entry_high, 2),
                "stop_loss": round(stop_loss, 2),
                "target1": round(target1, 2),
                "target2": round(target2, 2),
                "rr1": "1.5:1",
                "rr2": "2.5:1",
                "trigger": "Rejeição com volume no suporte",
                "score": long_score,
                "reasons": long_reasons
            }
        
        # Análise para SHORT
        short_score = 0
        short_reasons = []
        
        # Price Action - Estrutura bearish
        if structure['type'] == 'bearish':
            short_score += 3
            short_reasons.append("Estrutura LH + LL confirmada")
        elif structure['type'] == 'consolidation':
            short_score += 1
            short_reasons.append("Consolidação - aguardar confirmação")
        
        # Preço próximo a resistência
        nearest_resistance = sr_levels['resistances'][0] if sr_levels['resistances'] else sr_levels['pdh']
        distance_to_resistance = ((nearest_resistance - current_price) / current_price) * 100
        
        if distance_to_resistance < 1.5:
            short_score += 2
            short_reasons.append(f"Preço próximo à resistência ${nearest_resistance:,.0f}")
        
        # EMAs
        if current_price < emas['ema_200']:
            short_score += 1
            short_reasons.append("Preço abaixo da EMA 200")
        if emas['ema_9'] < emas['ema_21']:
            short_score += 1
            short_reasons.append("EMA 9 < EMA 21 (momentum bearish)")
        
        # RSI
        if rsi > 60:
            short_score += 1
            short_reasons.append(f"RSI sobrecomprado ({rsi})")
        elif rsi > 50:
            short_score += 0.5
        
        # Funding Rate alto
        if futures['funding_rate'] > 0.0005:
            short_score += 1
            short_reasons.append("Funding Rate muito positivo")
        
        # Gerar setup SHORT se score >= 4
        if short_score >= 4:
            entry_low = nearest_resistance * 0.995
            entry_high = nearest_resistance * 0.999
            stop_loss = nearest_resistance * 1.01
            
            risk = stop_loss - entry_high
            target1 = entry_high - (risk * 1.5)
            target2 = entry_high - (risk * 2.5)
            
            setups['short'] = {
                "type": "SHORT",
                "style": "Agressivo" if short_score < 6 else "Moderado",
                "entry_low": round(entry_low, 2),
                "entry_high": round(entry_high, 2),
                "stop_loss": round(stop_loss, 2),
                "target1": round(target1, 2),
                "target2": round(target2, 2),
                "rr1": "1.5:1",
                "rr2": "2.5:1",
                "trigger": "Rejeição com volume na resistência",
                "score": short_score,
                "reasons": short_reasons
            }
        
        return setups
    
    def determine_bias(self, structure: Dict, emas: Dict, rsi: float, 
                       futures: Dict, fear_greed: int) -> Dict:
        """Determina o viés do dia"""
        
        bullish_factors = []
        bearish_factors = []
        
        # Estrutura
        if structure['type'] == 'bullish':
            bullish_factors.append("Estrutura de alta (HH + HL)")
        elif structure['type'] == 'bearish':
            bearish_factors.append("Estrutura de baixa (LH + LL)")
        
        # EMAs
        if emas['price'] > emas['ema_200']:
            bullish_factors.append("Preço acima da EMA 200")
        else:
            bearish_factors.append("Preço abaixo da EMA 200")
        
        if emas['ema_9'] > emas['ema_21']:
            bullish_factors.append("EMA 9 > EMA 21")
        else:
            bearish_factors.append("EMA 9 < EMA 21")
        
        # RSI
        if rsi < 40:
            bullish_factors.append(f"RSI sobrevendido ({rsi})")
        elif rsi > 60:
            bearish_factors.append(f"RSI sobrecomprado ({rsi})")
        
        # Funding
        if futures['funding_rate'] < 0:
            bullish_factors.append("Funding Rate negativo")
        elif futures['funding_rate'] > 0.0005:
            bearish_factors.append("Funding Rate muito positivo")
        else:
            bullish_factors.append("Funding Rate saudável")
        
        # Fear & Greed
        if fear_greed < 30:
            bullish_factors.append(f"Fear extremo ({fear_greed}) - oportunidade")
        elif fear_greed > 70:
            bearish_factors.append(f"Greed extremo ({fear_greed}) - cautela")
        
        # Determinar viés
        bull_count = len(bullish_factors)
        bear_count = len(bearish_factors)
        
        if bull_count >= bear_count + 2:
            bias = "BULLISH"
            bias_class = "bullish"
        elif bear_count >= bull_count + 2:
            bias = "BEARISH"
            bias_class = "bearish"
        else:
            bias = "NEUTRO"
            bias_class = "neutral"
        
        return {
            "bias": bias,
            "bias_class": bias_class,
            "bullish_factors": bullish_factors,
            "bearish_factors": bearish_factors
        }
    
    def analyze_asset(self, symbol: str, fear_greed: Dict) -> Optional[Dict]:
        """Análise completa de um ativo"""
        print(f"Analisando {symbol}...")
        
        # Coleta de dados
        binance_data = self.get_binance_data(symbol)
        if not binance_data:
            return None
        
        futures_data = self.get_futures_data(symbol)
        
        ticker = binance_data['ticker']
        klines_4h = binance_data['klines_4h']
        
        # Preço e variação
        current_price = float(ticker['lastPrice'])
        price_change = float(ticker['priceChangePercent'])
        high_24h = float(ticker['highPrice'])
        low_24h = float(ticker['lowPrice'])
        volume = float(ticker['volume'])
        
        # Calcular indicadores
        closes_4h = [float(k[4]) for k in klines_4h]
        
        ema_9 = self.calculate_ema(closes_4h, 9)
        ema_21 = self.calculate_ema(closes_4h, 21)
        ema_200 = self.calculate_ema(closes_4h, 200)
        rsi = self.calculate_rsi(closes_4h)
        
        emas = {
            "price": current_price,
            "ema_9": ema_9,
            "ema_21": ema_21,
            "ema_200": ema_200
        }
        
        # Estrutura de mercado
        structure = self.analyze_structure(klines_4h[-30:])
        
        # Níveis S/R
        sr_levels = self.calculate_sr_levels(klines_4h, current_price)
        
        # Gerar setups
        setups = self.generate_setup(
            symbol, 
            {"price": current_price}, 
            structure, 
            sr_levels, 
            emas, 
            rsi, 
            futures_data
        )
        
        # Determinar viés
        bias_data = self.determine_bias(
            structure, 
            emas, 
            rsi, 
            futures_data, 
            fear_greed['value']
        )
        
        # Formatar funding rate
        funding_pct = futures_data['funding_rate'] * 100
        
        # Long/Short ratio
        ls_ratio = futures_data['long_short_ratio']
        long_pct = round(ls_ratio / (1 + ls_ratio) * 100, 1)
        short_pct = round(100 - long_pct, 1)
        
        return {
            "symbol": symbol,
            "price": current_price,
            "price_formatted": f"${current_price:,.2f}" if current_price > 100 else f"${current_price:.4f}",
            "price_change": price_change,
            "price_change_formatted": f"+{price_change:.2f}%" if price_change >= 0 else f"{price_change:.2f}%",
            "high_24h": high_24h,
            "low_24h": low_24h,
            "volume": volume,
            "emas": emas,
            "rsi": rsi,
            "structure": structure,
            "sr_levels": sr_levels,
            "funding_rate": funding_pct,
            "funding_formatted": f"{funding_pct:.4f}%",
            "open_interest": futures_data['open_interest'],
            "long_percent": long_pct,
            "short_percent": short_pct,
            "setups": setups,
            "bias": bias_data,
            "has_setup": setups['long'] is not None or setups['short'] is not None
        }
    
    def run_analysis(self) -> Dict:
        """Executa análise completa de todos os ativos"""
        now = datetime.now(self.timezone)
        
        # Fear & Greed (global)
        fear_greed = self.get_fear_greed()
        
        # Analisar cada ativo
        analyses = {}
        for symbol in self.assets:
            analysis = self.analyze_asset(symbol, fear_greed)
            if analysis:
                analyses[symbol] = analysis
        
        result = {
            "timestamp": now.isoformat(),
            "date": now.strftime("%d de %B de %Y").replace("January", "Janeiro").replace("February", "Fevereiro").replace("March", "Março").replace("April", "Abril").replace("May", "Maio").replace("June", "Junho").replace("July", "Julho").replace("August", "Agosto").replace("September", "Setembro").replace("October", "Outubro").replace("November", "Novembro").replace("December", "Dezembro"),
            "time": now.strftime("%H:%M"),
            "fear_greed": fear_greed,
            "analyses": analyses
        }
        
        # Salvar dados
        os.makedirs(self.data_dir, exist_ok=True)
        data_file = f"{self.data_dir}/analysis_{now.strftime('%Y%m%d_%H%M')}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Salvar também como latest
        latest_file = f"{self.data_dir}/latest_analysis.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Análise salva em: {data_file}")
        return result


if __name__ == "__main__":
    analyzer = CryptoAnalyzer()
    result = analyzer.run_analysis()
    print(json.dumps(result, indent=2, default=str))
