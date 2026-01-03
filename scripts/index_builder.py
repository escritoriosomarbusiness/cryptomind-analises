#!/usr/bin/env python3
"""
Index Builder - Constrói índices de navegação para análises arquivadas
Gera índices otimizados para busca rápida na interface web
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pytz

class IndexBuilder:
    """Constrói índices de análises"""
    
    def __init__(self):
        self.base_dir = Path("/home/ubuntu/cryptomind-analises")
        self.archive_dir = self.base_dir / "data" / "archive"
        self.index_dir = self.base_dir / "data" / "index"
        self.timezone = pytz.timezone('America/Sao_Paulo')
        
        # Criar diretório de índices
        self.index_dir.mkdir(exist_ok=True)
        
    def build_all_indexes(self):
        """Constrói todos os índices"""
        print("🔨 Construindo índices...")
        
        self.build_daily_index()
        self.build_weekly_index()
        self.build_monthly_index()
        self.build_master_index()
        
        print("✅ Todos os índices construídos!")
        
    def build_daily_index(self):
        """Constrói índice de análises diárias"""
        print("\n📅 Construindo índice diário...")
        
        daily_index = []
        
        # Varrer todos os arquivos diários
        for year_dir in sorted(self.archive_dir.glob("*")):
            if not year_dir.is_dir():
                continue
                
            for month_dir in sorted(year_dir.glob("*")):
                if not month_dir.is_dir():
                    continue
                    
                daily_dir = month_dir / "daily"
                if not daily_dir.exists():
                    continue
                    
                for day_dir in sorted(daily_dir.glob("*")):
                    if not day_dir.is_dir():
                        continue
                        
                    # Processar arquivos do dia
                    day_data = {
                        "date": f"{year_dir.name}-{month_dir.name}-{day_dir.name}",
                        "year": year_dir.name,
                        "month": month_dir.name,
                        "day": day_dir.name,
                        "analyses": []
                    }
                    
                    for file in sorted(day_dir.glob("*.json")):
                        try:
                            with open(file, 'r') as f:
                                data = json.load(f)
                            
                            analysis_type = "opening" if "opening" in file.name else "closing"
                            
                            entry = {
                                "type": analysis_type,
                                "filename": file.name,
                                "path": str(file.relative_to(self.base_dir)),
                                "timestamp": data.get('timestamp'),
                                "time": data.get('time', ''),
                                "summary": self._extract_summary(data, analysis_type)
                            }
                            
                            day_data["analyses"].append(entry)
                            
                        except Exception as e:
                            print(f"⚠️ Erro ao processar {file}: {e}")
                    
                    if day_data["analyses"]:
                        daily_index.append(day_data)
        
        # Salvar índice
        index_file = self.index_dir / "daily_index.json"
        with open(index_file, 'w') as f:
            json.dump({
                "generated_at": datetime.now(self.timezone).isoformat(),
                "total_days": len(daily_index),
                "days": daily_index
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Índice diário: {len(daily_index)} dias")
        
    def build_weekly_index(self):
        """Constrói índice de relatórios semanais"""
        print("\n📊 Construindo índice semanal...")
        
        weekly_index = []
        
        for year_dir in sorted(self.archive_dir.glob("*")):
            if not year_dir.is_dir():
                continue
                
            for month_dir in sorted(year_dir.glob("*")):
                if not month_dir.is_dir():
                    continue
                    
                weekly_dir = month_dir / "weekly"
                if not weekly_dir.exists():
                    continue
                    
                for file in sorted(weekly_dir.glob("week_*.json")):
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                        
                        entry = {
                            "year": year_dir.name,
                            "month": month_dir.name,
                            "week": file.stem.split('_')[1],
                            "filename": file.name,
                            "path": str(file.relative_to(self.base_dir)),
                            "timestamp": data.get('timestamp'),
                            "summary": self._extract_weekly_summary(data)
                        }
                        
                        weekly_index.append(entry)
                        
                    except Exception as e:
                        print(f"⚠️ Erro ao processar {file}: {e}")
        
        # Salvar índice
        index_file = self.index_dir / "weekly_index.json"
        with open(index_file, 'w') as f:
            json.dump({
                "generated_at": datetime.now(self.timezone).isoformat(),
                "total_weeks": len(weekly_index),
                "weeks": weekly_index
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Índice semanal: {len(weekly_index)} semanas")
        
    def build_monthly_index(self):
        """Constrói índice de relatórios mensais"""
        print("\n📈 Construindo índice mensal...")
        
        monthly_index = []
        
        for year_dir in sorted(self.archive_dir.glob("*")):
            if not year_dir.is_dir():
                continue
                
            for month_dir in sorted(year_dir.glob("*")):
                if not month_dir.is_dir():
                    continue
                    
                monthly_dir_path = month_dir / "monthly"
                if not monthly_dir_path.exists():
                    continue
                    
                for file in sorted(monthly_dir_path.glob("*.json")):
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                        
                        entry = {
                            "year": year_dir.name,
                            "month": month_dir.name,
                            "month_name": file.stem,
                            "filename": file.name,
                            "path": str(file.relative_to(self.base_dir)),
                            "timestamp": data.get('timestamp'),
                            "summary": self._extract_monthly_summary(data)
                        }
                        
                        monthly_index.append(entry)
                        
                    except Exception as e:
                        print(f"⚠️ Erro ao processar {file}: {e}")
        
        # Salvar índice
        index_file = self.index_dir / "monthly_index.json"
        with open(index_file, 'w') as f:
            json.dump({
                "generated_at": datetime.now(self.timezone).isoformat(),
                "total_months": len(monthly_index),
                "months": monthly_index
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Índice mensal: {len(monthly_index)} meses")
        
    def build_master_index(self):
        """Constrói índice mestre com estatísticas gerais"""
        print("\n🎯 Construindo índice mestre...")
        
        # Carregar índices individuais
        daily_index = self._load_index("daily_index.json")
        weekly_index = self._load_index("weekly_index.json")
        monthly_index = self._load_index("monthly_index.json")
        
        # Calcular estatísticas
        total_analyses = 0
        for day in daily_index.get("days", []):
            total_analyses += len(day.get("analyses", []))
        
        master_index = {
            "generated_at": datetime.now(self.timezone).isoformat(),
            "statistics": {
                "total_days": daily_index.get("total_days", 0),
                "total_weeks": weekly_index.get("total_weeks", 0),
                "total_months": monthly_index.get("total_months", 0),
                "total_analyses": total_analyses
            },
            "latest": {
                "daily": self._get_latest_from_index(daily_index),
                "weekly": self._get_latest_from_index(weekly_index),
                "monthly": self._get_latest_from_index(monthly_index)
            },
            "indexes": {
                "daily": "data/index/daily_index.json",
                "weekly": "data/index/weekly_index.json",
                "monthly": "data/index/monthly_index.json"
            }
        }
        
        # Salvar índice mestre
        index_file = self.index_dir / "master_index.json"
        with open(index_file, 'w') as f:
            json.dump(master_index, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Índice mestre: {total_analyses} análises totais")
        
    def _extract_summary(self, data: Dict, analysis_type: str) -> Dict:
        """Extrai resumo de uma análise"""
        if analysis_type == "opening":
            analyses = data.get("analyses", {})
            return {
                "assets": list(analyses.keys()),
                "setups_count": sum(1 for a in analyses.values() if a.get("has_setup")),
                "fear_greed": data.get("fear_greed", {}).get("value"),
                "usdt_d_impact": data.get("usdt_d", {}).get("crypto_impact")
            }
        else:  # closing
            return {
                "summary": data.get("summary", ""),
                "performance": data.get("performance", {})
            }
    
    def _extract_weekly_summary(self, data: Dict) -> Dict:
        """Extrai resumo de relatório semanal"""
        return {
            "win_rate": data.get("kpis", {}).get("win_rate"),
            "total_setups": data.get("kpis", {}).get("total_setups"),
            "best_asset": data.get("highlights", {}).get("best_asset")
        }
    
    def _extract_monthly_summary(self, data: Dict) -> Dict:
        """Extrai resumo de relatório mensal"""
        return {
            "win_rate": data.get("kpis", {}).get("win_rate"),
            "profit_factor": data.get("kpis", {}).get("profit_factor"),
            "total_setups": data.get("kpis", {}).get("total_setups")
        }
    
    def _load_index(self, filename: str) -> Dict:
        """Carrega um índice"""
        index_file = self.index_dir / filename
        if index_file.exists():
            with open(index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _get_latest_from_index(self, index_data: Dict) -> Dict:
        """Obtém última entrada de um índice"""
        if "days" in index_data and index_data["days"]:
            latest_day = index_data["days"][-1]
            if latest_day.get("analyses"):
                return latest_day["analyses"][-1]
        elif "weeks" in index_data and index_data["weeks"]:
            return index_data["weeks"][-1]
        elif "months" in index_data and index_data["months"]:
            return index_data["months"][-1]
        return {}

def main():
    """Função principal"""
    builder = IndexBuilder()
    builder.build_all_indexes()

if __name__ == "__main__":
    main()
