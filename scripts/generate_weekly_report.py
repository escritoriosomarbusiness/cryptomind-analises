#!/usr/bin/env python3
"""
CryptoMind IA - Gerador de Relatórios Semanais
Gera relatórios semanais com KPIs e análise de performance
Executado automaticamente todo domingo às 21:15 BRT
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import pytz

class WeeklyReportGenerator:
    """Gera relatórios semanais com KPIs"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.absolute()
        self.data_dir = self.base_dir / "data"
        self.archive_dir = self.data_dir / "archive"
        self.current_dir = self.data_dir / "current"
        self.timezone = pytz.timezone('America/Sao_Paulo')
        
    def generate_report(self, week_start: datetime = None):
        """
        Gera relatório semanal
        
        Args:
            week_start: Data de início da semana (segunda-feira). Se None, usa semana atual.
        """
        print("📊 Gerando Relatório Semanal...")
        
        # Determinar período da semana
        if week_start is None:
            now = datetime.now(self.timezone)
            # Voltar para a segunda-feira da semana
            week_start = now - timedelta(days=now.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        week_num = week_start.isocalendar()[1]
        
        print(f"Período: {week_start.strftime('%d/%m/%Y')} a {week_end.strftime('%d/%m/%Y')}")
        print(f"Semana: {week_num}")
        
        # Coletar análises da semana
        analyses = self._collect_week_analyses(week_start, week_end)
        
        if not analyses:
            print("⚠️ Nenhuma análise encontrada para esta semana")
            return None
        
        print(f"✅ {len(analyses)} análises encontradas")
        
        # Calcular KPIs
        kpis = self._calculate_kpis(analyses)
        
        # Análise macro
        macro_analysis = self._analyze_macro(analyses)
        
        # Destaques
        highlights = self._extract_highlights(analyses)
        
        # Montar relatório
        report = {
            "timestamp": datetime.now(self.timezone).isoformat(),
            "report_type": "weekly",
            "week_number": week_num,
            "year": week_start.year,
            "period": {
                "start": week_start.strftime('%Y-%m-%d'),
                "end": week_end.strftime('%Y-%m-%d'),
                "start_formatted": week_start.strftime('%d de %B de %Y'),
                "end_formatted": week_end.strftime('%d de %B de %Y')
            },
            "kpis": kpis,
            "macro_analysis": macro_analysis,
            "highlights": highlights,
            "analyses_count": len(analyses)
        }
        
        # Salvar relatório
        self._save_report(report, week_start)
        
        print("✅ Relatório semanal gerado com sucesso!")
        
        return report
    
    def _collect_week_analyses(self, week_start: datetime, week_end: datetime) -> List[Dict]:
        """Coleta todas as análises da semana"""
        analyses = []
        
        # Iterar pelos dias da semana
        current_day = week_start
        while current_day <= week_end:
            year = current_day.strftime('%Y')
            month = current_day.strftime('%m')
            day = current_day.strftime('%d')
            
            day_dir = self.archive_dir / year / month / "daily" / day
            
            if day_dir.exists():
                # Coletar análises de abertura
                for file in day_dir.glob("opening_*.json"):
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                        data['_type'] = 'opening'
                        data['_date'] = current_day.strftime('%Y-%m-%d')
                        analyses.append(data)
                    except Exception as e:
                        print(f"⚠️ Erro ao ler {file}: {e}")
                
                # Coletar relatórios de fechamento
                for file in day_dir.glob("closing_*.json"):
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                        data['_type'] = 'closing'
                        data['_date'] = current_day.strftime('%Y-%m-%d')
                        analyses.append(data)
                    except Exception as e:
                        print(f"⚠️ Erro ao ler {file}: {e}")
            
            current_day += timedelta(days=1)
        
        return analyses
    
    def _calculate_kpis(self, analyses: List[Dict]) -> Dict:
        """Calcula KPIs da semana"""
        # Filtrar apenas análises de abertura
        opening_analyses = [a for a in analyses if a.get('_type') == 'opening']
        
        total_setups = 0
        setups_by_asset = {}
        total_long = 0
        total_short = 0
        scores = []
        
        for analysis in opening_analyses:
            assets = analysis.get('analyses', {})
            
            for asset, data in assets.items():
                if data.get('has_setup'):
                    total_setups += 1
                    
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
        
        # Calcular médias
        avg_score = sum(scores) / len(scores) if scores else 0
        
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
    
    def _analyze_macro(self, analyses: List[Dict]) -> Dict:
        """Analisa indicadores macro da semana"""
        opening_analyses = [a for a in analyses if a.get('_type') == 'opening']
        
        fear_greed_values = []
        usdt_d_values = []
        usdt_d_impacts = []
        
        for analysis in opening_analyses:
            # Fear & Greed
            fg = analysis.get('fear_greed', {})
            if 'value' in fg:
                fear_greed_values.append(fg['value'])
            
            # USDT.D
            usdt_d = analysis.get('usdt_d', {})
            if 'dominance' in usdt_d:
                usdt_d_values.append(usdt_d['dominance'])
            if 'crypto_impact' in usdt_d:
                usdt_d_impacts.append(usdt_d['crypto_impact'])
        
        # Calcular médias
        avg_fear_greed = sum(fear_greed_values) / len(fear_greed_values) if fear_greed_values else 0
        avg_usdt_d = sum(usdt_d_values) / len(usdt_d_values) if usdt_d_values else 0
        
        # Classificação Fear & Greed
        if avg_fear_greed < 25:
            fg_class = "Extreme Fear"
        elif avg_fear_greed < 45:
            fg_class = "Fear"
        elif avg_fear_greed < 55:
            fg_class = "Neutral"
        elif avg_fear_greed < 75:
            fg_class = "Greed"
        else:
            fg_class = "Extreme Greed"
        
        # Impacto dominante do USDT.D
        if usdt_d_impacts:
            bullish_count = usdt_d_impacts.count('BULLISH')
            bearish_count = usdt_d_impacts.count('BEARISH')
            
            if bullish_count > bearish_count:
                dominant_impact = "BULLISH"
            elif bearish_count > bullish_count:
                dominant_impact = "BEARISH"
            else:
                dominant_impact = "NEUTRO"
        else:
            dominant_impact = "N/A"
        
        return {
            "fear_greed": {
                "average": round(avg_fear_greed, 1),
                "classification": fg_class,
                "min": min(fear_greed_values) if fear_greed_values else 0,
                "max": max(fear_greed_values) if fear_greed_values else 0
            },
            "usdt_d": {
                "average": round(avg_usdt_d, 3),
                "dominant_impact": dominant_impact,
                "min": round(min(usdt_d_values), 3) if usdt_d_values else 0,
                "max": round(max(usdt_d_values), 3) if usdt_d_values else 0
            }
        }
    
    def _extract_highlights(self, analyses: List[Dict]) -> Dict:
        """Extrai destaques da semana"""
        opening_analyses = [a for a in analyses if a.get('_type') == 'opening']
        
        best_setup = None
        best_score = 0
        
        for analysis in opening_analyses:
            assets = analysis.get('analyses', {})
            date = analysis.get('_date')
            
            for asset, data in assets.items():
                if data.get('has_setup'):
                    setups = data.get('setups', {})
                    
                    # Verificar LONG
                    if setups.get('long'):
                        score = setups['long'].get('score', 0)
                        if score > best_score:
                            best_score = score
                            best_setup = {
                                "asset": asset,
                                "type": "LONG",
                                "score": score,
                                "date": date,
                                "entry": setups['long'].get('entry_low'),
                                "target": setups['long'].get('target1')
                            }
                    
                    # Verificar SHORT
                    if setups.get('short'):
                        score = setups['short'].get('score', 0)
                        if score > best_score:
                            best_score = score
                            best_setup = {
                                "asset": asset,
                                "type": "SHORT",
                                "score": score,
                                "date": date,
                                "entry": setups['short'].get('entry_low'),
                                "target": setups['short'].get('target1')
                            }
        
        return {
            "best_setup": best_setup,
            "total_trading_days": len(opening_analyses)
        }
    
    def _save_report(self, report: Dict, week_start: datetime):
        """Salva relatório semanal"""
        # Salvar em current/
        current_file = self.current_dir / "latest_weekly.json"
        with open(current_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Salvo em: {current_file}")
        
        # Arquivar usando archive_manager
        import sys
        sys.path.append(str(self.base_dir / "scripts"))
        from archive_manager import ArchiveManager
        
        manager = ArchiveManager()
        manager.archive_analysis('weekly', str(current_file))

def main():
    """Função principal"""
    generator = WeeklyReportGenerator()
    generator.generate_report()

if __name__ == "__main__":
    main()
