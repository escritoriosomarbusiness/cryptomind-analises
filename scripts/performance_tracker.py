#!/usr/bin/env python3
"""
CryptoMind IA - Rastreador de Performance
==========================================
Rastreia o resultado dos setups gerados para calcular KPIs reais.
100% automatizado - verifica se setups atingiram alvos ou stops.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz

# Configuração
BR_TZ = pytz.timezone('America/Sao_Paulo')
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
performance_dir = os.path.join(data_dir, 'performance')


class PerformanceTracker:
    """Rastreador de performance dos setups."""
    
    def __init__(self):
        os.makedirs(performance_dir, exist_ok=True)
        self.active_setups_file = os.path.join(performance_dir, 'active_setups.json')
        self.completed_setups_file = os.path.join(performance_dir, 'completed_setups.json')
        self.kpis_file = os.path.join(performance_dir, 'kpis.json')
        
        self.active_setups = self._load_json(self.active_setups_file, [])
        self.completed_setups = self._load_json(self.completed_setups_file, [])
        self.kpis = self._load_json(self.kpis_file, self._default_kpis())
    
    def _load_json(self, path: str, default) -> any:
        """Carrega arquivo JSON ou retorna default."""
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, path: str, data: any):
        """Salva dados em arquivo JSON."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _default_kpis(self) -> dict:
        """Retorna KPIs padrão."""
        return {
            'total_setups': 0,
            'wins': 0,
            'losses': 0,
            'breakeven': 0,
            'active': 0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'total_r_gained': 0.0,
            'total_r_lost': 0.0,
            'best_trade': None,
            'worst_trade': None,
            'by_ts_type': {
                'TS1': {'wins': 0, 'losses': 0, 'total_r': 0.0},
                'TS2': {'wins': 0, 'losses': 0, 'total_r': 0.0},
                'TS3': {'wins': 0, 'losses': 0, 'total_r': 0.0}
            },
            'by_asset': {},
            'by_direction': {
                'LONG': {'wins': 0, 'losses': 0, 'total_r': 0.0},
                'SHORT': {'wins': 0, 'losses': 0, 'total_r': 0.0}
            },
            'last_updated': None
        }
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Obtém preço atual de um ativo."""
        coin_ids = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana',
            'BNB': 'binancecoin',
            'XRP': 'ripple'
        }
        
        coin_id = coin_ids.get(symbol)
        if not coin_id:
            return None
        
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get(coin_id, {}).get('usd')
        except Exception as e:
            print(f"Erro ao obter preço de {symbol}: {e}")
        
        return None
    
    def register_setup(self, setup: dict, symbol: str):
        """Registra um novo setup para rastreamento."""
        risk_plan = setup.get('risk_plan', {})
        entry = risk_plan.get('entry', {})
        stop = risk_plan.get('stop_loss', {})
        partials = risk_plan.get('partials', [])
        
        # Calcular alvos
        targets = []
        for p in partials:
            if p['target_price'] != 'TRAILING':
                targets.append({
                    'price': p['target_price'],
                    'rr': p['rr_ratio'],
                    'size': p['size_percent'],
                    'hit': False
                })
        
        tracked_setup = {
            'id': f"{symbol}_{setup['ts_type']}_{setup['direction']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'symbol': symbol,
            'direction': setup['direction'],
            'ts_type': setup['ts_type'],
            'ts_name': setup['ts_name'],
            'confidence_score': setup.get('confidence_score', 0),
            'entry_min': entry.get('min', 0),
            'entry_max': entry.get('max', 0),
            'stop_loss': stop.get('price', 0),
            'targets': targets,
            'status': 'WAITING',  # WAITING, ACTIVE, WIN, LOSS, BREAKEVEN, EXPIRED
            'created_at': datetime.now(BR_TZ).isoformat(),
            'activated_at': None,
            'closed_at': None,
            'entry_price': None,
            'exit_price': None,
            'result_r': 0.0,
            'partial_hits': 0
        }
        
        self.active_setups.append(tracked_setup)
        self._save_json(self.active_setups_file, self.active_setups)
        
        print(f"Setup registrado: {tracked_setup['id']}")
        return tracked_setup['id']
    
    def check_setup_status(self, setup: dict, current_price: float) -> str:
        """Verifica o status de um setup baseado no preço atual."""
        direction = setup['direction']
        entry_min = setup['entry_min']
        entry_max = setup['entry_max']
        stop_loss = setup['stop_loss']
        targets = setup['targets']
        
        # Verificar se entrou na zona de entrada
        if setup['status'] == 'WAITING':
            if entry_min <= current_price <= entry_max:
                setup['status'] = 'ACTIVE'
                setup['activated_at'] = datetime.now(BR_TZ).isoformat()
                setup['entry_price'] = current_price
                return 'ACTIVATED'
        
        # Se está ativo, verificar stop e alvos
        if setup['status'] == 'ACTIVE':
            entry_price = setup['entry_price']
            
            # Verificar stop loss
            if direction == 'LONG' and current_price <= stop_loss:
                setup['status'] = 'LOSS'
                setup['exit_price'] = current_price
                setup['closed_at'] = datetime.now(BR_TZ).isoformat()
                setup['result_r'] = -1.0
                return 'STOPPED'
            
            if direction == 'SHORT' and current_price >= stop_loss:
                setup['status'] = 'LOSS'
                setup['exit_price'] = current_price
                setup['closed_at'] = datetime.now(BR_TZ).isoformat()
                setup['result_r'] = -1.0
                return 'STOPPED'
            
            # Verificar alvos
            for target in targets:
                if not target['hit']:
                    if direction == 'LONG' and current_price >= target['price']:
                        target['hit'] = True
                        setup['partial_hits'] += 1
                        setup['result_r'] += target['rr'] * (target['size'] / 100)
                    
                    if direction == 'SHORT' and current_price <= target['price']:
                        target['hit'] = True
                        setup['partial_hits'] += 1
                        setup['result_r'] += target['rr'] * (target['size'] / 100)
            
            # Verificar se todos os alvos foram atingidos
            all_hit = all(t['hit'] for t in targets if t['price'] != 'TRAILING')
            if all_hit and targets:
                setup['status'] = 'WIN'
                setup['exit_price'] = current_price
                setup['closed_at'] = datetime.now(BR_TZ).isoformat()
                return 'TARGET_HIT'
            
            # Verificar se pelo menos o primeiro alvo foi atingido (breakeven)
            if setup['partial_hits'] > 0:
                # Atualizar stop para entrada (breakeven)
                setup['stop_loss'] = setup['entry_price']
        
        return 'NO_CHANGE'
    
    def update_all_setups(self):
        """Atualiza o status de todos os setups ativos."""
        print("=" * 60)
        print("Atualizando status dos setups...")
        print("=" * 60)
        
        # Agrupar por símbolo para otimizar requisições
        symbols = set(s['symbol'] for s in self.active_setups)
        prices = {}
        
        for symbol in symbols:
            price = self.get_current_price(symbol)
            if price:
                prices[symbol] = price
                print(f"{symbol}: ${price:.2f}")
        
        # Atualizar cada setup
        completed = []
        for setup in self.active_setups:
            symbol = setup['symbol']
            if symbol not in prices:
                continue
            
            current_price = prices[symbol]
            status = self.check_setup_status(setup, current_price)
            
            if status != 'NO_CHANGE':
                print(f"  {setup['id']}: {status}")
            
            # Mover para completados se finalizado
            if setup['status'] in ['WIN', 'LOSS', 'BREAKEVEN']:
                completed.append(setup)
        
        # Mover setups completados
        for setup in completed:
            self.active_setups.remove(setup)
            self.completed_setups.append(setup)
        
        # Verificar setups expirados (mais de 24h sem ativar)
        now = datetime.now(BR_TZ)
        expired = []
        for setup in self.active_setups:
            if setup['status'] == 'WAITING':
                created = datetime.fromisoformat(setup['created_at'])
                if (now - created).total_seconds() > 86400:  # 24 horas
                    setup['status'] = 'EXPIRED'
                    expired.append(setup)
        
        for setup in expired:
            self.active_setups.remove(setup)
            self.completed_setups.append(setup)
            print(f"  {setup['id']}: EXPIRED")
        
        # Salvar
        self._save_json(self.active_setups_file, self.active_setups)
        self._save_json(self.completed_setups_file, self.completed_setups)
        
        # Recalcular KPIs
        self._recalculate_kpis()
        
        print(f"\nSetups ativos: {len(self.active_setups)}")
        print(f"Setups completados: {len(self.completed_setups)}")
    
    def _recalculate_kpis(self):
        """Recalcula todos os KPIs baseado nos setups completados."""
        kpis = self._default_kpis()
        
        kpis['total_setups'] = len(self.completed_setups) + len(self.active_setups)
        kpis['active'] = len(self.active_setups)
        
        for setup in self.completed_setups:
            status = setup['status']
            ts_type = setup['ts_type']
            symbol = setup['symbol']
            direction = setup['direction']
            result_r = setup.get('result_r', 0)
            
            # Contagem geral
            if status == 'WIN':
                kpis['wins'] += 1
                kpis['total_r_gained'] += result_r
            elif status == 'LOSS':
                kpis['losses'] += 1
                kpis['total_r_lost'] += abs(result_r)
            elif status == 'BREAKEVEN':
                kpis['breakeven'] += 1
            
            # Por tipo de TS
            if ts_type in kpis['by_ts_type']:
                if status == 'WIN':
                    kpis['by_ts_type'][ts_type]['wins'] += 1
                elif status == 'LOSS':
                    kpis['by_ts_type'][ts_type]['losses'] += 1
                kpis['by_ts_type'][ts_type]['total_r'] += result_r
            
            # Por ativo
            if symbol not in kpis['by_asset']:
                kpis['by_asset'][symbol] = {'wins': 0, 'losses': 0, 'total_r': 0.0}
            if status == 'WIN':
                kpis['by_asset'][symbol]['wins'] += 1
            elif status == 'LOSS':
                kpis['by_asset'][symbol]['losses'] += 1
            kpis['by_asset'][symbol]['total_r'] += result_r
            
            # Por direção
            if status == 'WIN':
                kpis['by_direction'][direction]['wins'] += 1
            elif status == 'LOSS':
                kpis['by_direction'][direction]['losses'] += 1
            kpis['by_direction'][direction]['total_r'] += result_r
            
            # Melhor e pior trade
            if kpis['best_trade'] is None or result_r > kpis['best_trade'].get('result_r', 0):
                kpis['best_trade'] = {
                    'id': setup['id'],
                    'symbol': symbol,
                    'direction': direction,
                    'result_r': result_r
                }
            
            if kpis['worst_trade'] is None or result_r < kpis['worst_trade'].get('result_r', 0):
                kpis['worst_trade'] = {
                    'id': setup['id'],
                    'symbol': symbol,
                    'direction': direction,
                    'result_r': result_r
                }
        
        # Calcular win rate
        total_closed = kpis['wins'] + kpis['losses']
        if total_closed > 0:
            kpis['win_rate'] = (kpis['wins'] / total_closed) * 100
        
        # Calcular profit factor
        if kpis['total_r_lost'] > 0:
            kpis['profit_factor'] = kpis['total_r_gained'] / kpis['total_r_lost']
        elif kpis['total_r_gained'] > 0:
            kpis['profit_factor'] = float('inf')
        
        kpis['last_updated'] = datetime.now(BR_TZ).isoformat()
        
        self.kpis = kpis
        self._save_json(self.kpis_file, kpis)
    
    def register_new_setups_from_analysis(self):
        """Registra novos setups da análise mais recente."""
        analysis_path = os.path.join(data_dir, 'full_analysis.json')
        
        if not os.path.exists(analysis_path):
            print("Análise não encontrada")
            return
        
        with open(analysis_path, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        # Verificar setups já registrados
        existing_ids = set()
        for setup in self.active_setups + self.completed_setups:
            # Criar ID simplificado para comparação
            simple_id = f"{setup['symbol']}_{setup['ts_type']}_{setup['direction']}"
            existing_ids.add(simple_id)
        
        # Registrar novos setups
        min_score = 5  # Score mínimo para rastrear
        
        for symbol, setups in analysis.get('setups', {}).items():
            for setup in setups:
                if setup.get('confidence_score', 0) >= min_score:
                    simple_id = f"{symbol}_{setup['ts_type']}_{setup['direction']}"
                    
                    if simple_id not in existing_ids:
                        self.register_setup(setup, symbol)
                        existing_ids.add(simple_id)
    
    def get_summary(self) -> dict:
        """Retorna resumo dos KPIs."""
        return {
            'total_setups': self.kpis['total_setups'],
            'active': self.kpis['active'],
            'wins': self.kpis['wins'],
            'losses': self.kpis['losses'],
            'win_rate': f"{self.kpis['win_rate']:.1f}%",
            'profit_factor': f"{self.kpis['profit_factor']:.2f}",
            'total_r': f"{self.kpis['total_r_gained'] - self.kpis['total_r_lost']:.2f}R",
            'last_updated': self.kpis['last_updated']
        }
    
    def print_report(self):
        """Imprime relatório de performance."""
        print("\n" + "=" * 60)
        print("RELATÓRIO DE PERFORMANCE")
        print("=" * 60)
        
        print(f"\n📊 Resumo Geral:")
        print(f"   Total de Setups: {self.kpis['total_setups']}")
        print(f"   Ativos: {self.kpis['active']}")
        print(f"   Wins: {self.kpis['wins']}")
        print(f"   Losses: {self.kpis['losses']}")
        print(f"   Breakeven: {self.kpis['breakeven']}")
        
        print(f"\n📈 KPIs:")
        print(f"   Win Rate: {self.kpis['win_rate']:.1f}%")
        print(f"   Profit Factor: {self.kpis['profit_factor']:.2f}")
        print(f"   Total R Ganho: {self.kpis['total_r_gained']:.2f}R")
        print(f"   Total R Perdido: {self.kpis['total_r_lost']:.2f}R")
        print(f"   Resultado Líquido: {self.kpis['total_r_gained'] - self.kpis['total_r_lost']:.2f}R")
        
        print(f"\n🎯 Por Tipo de Setup:")
        for ts_type, data in self.kpis['by_ts_type'].items():
            total = data['wins'] + data['losses']
            wr = (data['wins'] / total * 100) if total > 0 else 0
            print(f"   {ts_type}: {data['wins']}W / {data['losses']}L ({wr:.1f}%) | {data['total_r']:.2f}R")
        
        print(f"\n💰 Por Ativo:")
        for symbol, data in self.kpis.get('by_asset', {}).items():
            total = data['wins'] + data['losses']
            wr = (data['wins'] / total * 100) if total > 0 else 0
            print(f"   {symbol}: {data['wins']}W / {data['losses']}L ({wr:.1f}%) | {data['total_r']:.2f}R")
        
        print(f"\n📍 Por Direção:")
        for direction, data in self.kpis['by_direction'].items():
            total = data['wins'] + data['losses']
            wr = (data['wins'] / total * 100) if total > 0 else 0
            print(f"   {direction}: {data['wins']}W / {data['losses']}L ({wr:.1f}%) | {data['total_r']:.2f}R")
        
        if self.kpis['best_trade']:
            bt = self.kpis['best_trade']
            print(f"\n🏆 Melhor Trade: {bt['symbol']} {bt['direction']} ({bt['result_r']:.2f}R)")
        
        if self.kpis['worst_trade']:
            wt = self.kpis['worst_trade']
            print(f"💀 Pior Trade: {wt['symbol']} {wt['direction']} ({wt['result_r']:.2f}R)")


def main():
    """Função principal."""
    tracker = PerformanceTracker()
    
    print("=" * 60)
    print("CryptoMind IA - Rastreador de Performance")
    print("=" * 60)
    
    # Registrar novos setups da análise
    print("\n[1] Registrando novos setups...")
    tracker.register_new_setups_from_analysis()
    
    # Atualizar status dos setups ativos
    print("\n[2] Atualizando status dos setups...")
    tracker.update_all_setups()
    
    # Imprimir relatório
    tracker.print_report()
    
    print("\n✅ Rastreamento concluído")


if __name__ == "__main__":
    main()
