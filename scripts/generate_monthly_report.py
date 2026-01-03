#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de Relatórios Mensais
Gera relatórios mensais com KPIs avançados e estatísticas
Executado automaticamente no último dia do mês às 21:15 BRT
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import pytz
import calendar

class MonthlyReportGenerator:
    """Gera relatórios mensais com KPIs avançados"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.absolute()
        self.data_dir = self.base_dir / "data"
        self.archive_dir = self.data_dir / "archive"
        self.current_dir = self.data_dir / "current"
        self.timezone = pytz.timezone('America/Sao_Paulo')
        
    def generate_report(self, year: int = None, month: int = None):
        """
        Gera relatório mensal
        
        Args:
            year: Ano (None = ano atual)
            month: Mês (None = mês atual)
        """
        print("📈 Gerando Relatório Mensal...")
        
        # Determinar período
        now = datetime.now(self.timezone)
        if year is None:
            year = now.year
        if month is None:
            month = now.month
        
        # Primeiro e último dia do mês
        first_day = datetime(year, month, 1, tzinfo=self.timezone)
        last_day_num = calendar.monthrange(year, month)[1]
        last_day = datetime(year, month, last_day_num, 23, 59, 59, tzinfo=self.timezone)
        
        month_name = first_day.strftime('%B')
        
        print(f"Período: {first_day.strftime('%d/%m/%Y')} a {last_day.strftime('%d/%m/%Y')}")
        print(f"Mês: {month_name} {year}")
        
        # Coletar análises do mês
        analyses = self._collect_month_analyses(year, month)
        
        if not analyses:
            print("⚠️ Nenhuma análise encontrada para este mês")
            return None
        
        print(f"✅ {len(analyses)} análises encontradas")
        
        # Calcular KPIs
        kpis = self._calculate_kpis(analyses)
        
        # Análise de tendências
        trends = self._analyze_trends(analyses)
        
        # Estatísticas avançadas
        advanced_stats = self._calculate_advanced_stats(analyses)
        
        # Comparação com mês anterior
        comparison = self._compare_with_previous_month(year, month)
        
        # Montar relatório
        report = {
            "timestamp": datetime.now(self.timezone).isoformat(),
            "report_type": "monthly",
            "year": year,
            "month": month,
            "month_name": month_name.lower(),
            "period": {
                "start": first_day.strftime('%Y-%m-%d'),
                "end": last_day.strftime('%Y-%m-%d'),
                "start_formatted": first_day.strftime('%d de %B de %Y'),
                "end_formatted": last_day.strftime('%d de %B de %Y')
            },
            "kpis": kpis,
            "trends": trends,
            "advanced_stats": advanced_stats,
            "comparison": comparison,
            "analyses_count": len(analyses)
        }
        
        # Salvar relatório
        self._save_report(report, year, month)
        
        print("✅ Relatório mensal gerado com sucesso!")
        
        return report
    
    def _collect_month_analyses(self, year: int, month: int) -> List[Dict]:
        """Coleta todas as análises do mês"""
        analyses = []
        
        year_str = str(year)
        month_str = f"{month:02d}"
        
        daily_dir = self.archive_dir / year_str / month_str / "daily"
        
        if not daily_dir.exists():
            return analyses
        
        # Iterar por todos os dias
        for day_dir in sorted(daily_dir.glob("*")):
            if not day_dir.is_dir():
                continue
            
            # Coletar análises de abertura
            for file in day_dir.glob("opening_*.json"):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    data['_type'] = 'opening'
                    data['_date'] = f"{year_str}-{month_str}-{day_dir.name}"
                    analyses.append(data)
                except Exception as e:
                    print(f"⚠️ Erro ao ler {file}: {e}")
            
            # Coletar relatórios de fechamento
            for file in day_dir.glob("closing_*.json"):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    data['_type'] = 'closing'
                    data['_date'] = f"{year_str}-{month_str}-{day_dir.name}"
                    analyses.append(data)
                except Exception as e:
                    print(f"⚠️ Erro ao ler {file}: {e}")
        
        return analyses
    
    def _calculate_kpis(self, analyses: List[Dict]) -> Dict:
        """Calcula KPIs do mês"""
        opening_analyses = [a for a in analyses if a.get('_type') == 'opening']
        
        total_setups = 0
        setups_by_asset = {}
        total_long = 0
        total_short = 0
        scores = []
        daily_setups = []
        
        for analysis in opening_analyses:
            day_setups = 0
            assets = analysis.get('analyses', {})
            
            for asset, data in assets.items():
                if data.get('has_setup'):
                    total_setups += 1
                    day_setups += 1
                    
                    # Contar por ativo
                    if asset not in setups_by_asset:
                        setups_by_asset[asset] = 0
                    setups_by_asset[asset] += 1
                    
                    # Contar LONG vs SHORT
                    setups = data.get('setups', {})
                    if setups.get('long'):
                        total_long += 1
                        if 'score' in setups['long']:
                            scores.append(setups['long']['score'])
                    if setups.get('short'):
                        total_short += 1
                        if 'score' in setups['short']:
                            scores.append(setups['short']['score'])
            
            daily_setups.append(day_setups)
        
        # Calcular médias
        avg_score = sum(scores) / len(scores) if scores else 0
        avg_daily_setups = sum(daily_setups) / len(daily_setups) if daily_setups else 0
        
        # Melhor e pior ativo
        best_asset = max(setups_by_asset.items(), key=lambda x: x[1]) if setups_by_asset else (None, 0)
        worst_asset = min(setups_by_asset.items(), key=lambda x: x[1]) if setups_by_asset else (None, 0)
        
        return {
            "total_setups": total_setups,
            "total_long": total_long,
            "total_short": total_short,
            "long_percentage": round((total_long / total_setups * 100) if total_setups > 0 else 0, 1),
            "short_percentage": round((total_short / total_setups * 100) if total_setups > 0 else 0, 1),
            "average_score": round(avg_score, 1),
            "average_daily_setups": round(avg_daily_setups, 1),
            "setups_by_asset": setups_by_asset,
            "best_asset": {
                "symbol": best_asset[0],
                "setups_count": best_asset[1]
            } if best_asset[0] else None,
            "worst_asset": {
                "symbol": worst_asset[0],
                "setups_count": worst_asset[1]
            } if worst_asset[0] else None,
            "trading_days": len(opening_analyses)
        }
    
    def _analyze_trends(self, analyses: List[Dict]) -> Dict:
        """Analisa tendências do mês"""
        opening_analyses = [a for a in analyses if a.get('_type') == 'opening']
        
        # Agrupar por semana
        weekly_data = {}
        
        for analysis in opening_analyses:
            date_str = analysis.get('_date')
            if not date_str:
                continue
            
            date = datetime.fromisoformat(date_str)
            week_num = date.isocalendar()[1]
            
            if week_num not in weekly_data:
                weekly_data[week_num] = {
                    'setups': 0,
                    'fear_greed': [],
                    'usdt_d': []
                }
            
            # Contar setups
            assets = analysis.get('analyses', {})
            for asset, data in assets.items():
                if data.get('has_setup'):
                    weekly_data[week_num]['setups'] += 1
            
            # Coletar Fear & Greed
            fg = analysis.get('fear_greed', {})
            if 'value' in fg:
                weekly_data[week_num]['fear_greed'].append(fg['value'])
            
            # Coletar USDT.D
            usdt_d = analysis.get('usdt_d', {})
            if 'dominance' in usdt_d:
                weekly_data[week_num]['usdt_d'].append(usdt_d['dominance'])
        
        # Calcular médias semanais
        weekly_summary = []
        for week, data in sorted(weekly_data.items()):
            avg_fg = sum(data['fear_greed']) / len(data['fear_greed']) if data['fear_greed'] else 0
            avg_usdt = sum(data['usdt_d']) / len(data['usdt_d']) if data['usdt_d'] else 0
            
            weekly_summary.append({
                "week": week,
                "setups": data['setups'],
                "avg_fear_greed": round(avg_fg, 1),
                "avg_usdt_d": round(avg_usdt, 3)
            })
        
        # Melhor semana
        best_week = max(weekly_summary, key=lambda x: x['setups']) if weekly_summary else None
        
        return {
            "weekly_summary": weekly_summary,
            "best_week": best_week,
            "total_weeks": len(weekly_summary)
        }
    
    def _calculate_advanced_stats(self, analyses: List[Dict]) -> Dict:
        """Calcula estatísticas avançadas"""
        # Por enquanto, retorna placeholder
        # Em produção, calcular Sharpe Ratio, Sortino, etc. com dados reais de performance
        
        return {
            "sharpe_ratio": None,
            "sortino_ratio": None,
            "max_drawdown": None,
            "recovery_factor": None,
            "note": "Estatísticas avançadas requerem dados de performance real"
        }
    
    def _compare_with_previous_month(self, year: int, month: int) -> Dict:
        """Compara com mês anterior"""
        # Calcular mês anterior
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1
        
        # Tentar carregar relatório do mês anterior
        prev_month_name = datetime(prev_year, prev_month, 1).strftime('%B').lower()
        prev_report_file = self.archive_dir / str(prev_year) / f"{prev_month:02d}" / "monthly" / f"{prev_month_name}.json"
        
        if not prev_report_file.exists():
            return {
                "available": False,
                "message": "Relatório do mês anterior não disponível"
            }
        
        try:
            with open(prev_report_file, 'r') as f:
                prev_report = json.load(f)
            
            prev_kpis = prev_report.get('kpis', {})
            
            return {
                "available": True,
                "previous_month": {
                    "year": prev_year,
                    "month": prev_month,
                    "name": prev_month_name
                },
                "comparison": {
                    "total_setups": {
                        "previous": prev_kpis.get('total_setups', 0),
                        "change": "N/A"  # Será calculado ao gerar relatório atual
                    },
                    "average_score": {
                        "previous": prev_kpis.get('average_score', 0),
                        "change": "N/A"
                    }
                }
            }
        except Exception as e:
            print(f"⚠️ Erro ao carregar relatório anterior: {e}")
            return {
                "available": False,
                "message": "Erro ao carregar relatório do mês anterior"
            }
    
    def _save_report(self, report: Dict, year: int, month: int):
        """Salva relatório mensal"""
        # Salvar em current/
        current_file = self.current_dir / "latest_monthly.json"
        with open(current_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Salvo em: {current_file}")
        
        # Arquivar usando archive_manager
        import sys
        sys.path.append(str(self.base_dir / "scripts"))
        from archive_manager import ArchiveManager
        
        manager = ArchiveManager()
        manager.archive_analysis('monthly', str(current_file))

def main():
    """Função principal"""
    generator = MonthlyReportGenerator()
    generator.generate_report()

if __name__ == "__main__":
    main()
