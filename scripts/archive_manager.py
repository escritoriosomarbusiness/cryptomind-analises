#!/usr/bin/env python3
"""
Archive Manager - Gerencia o arquivamento automático de análises
Organiza análises por data e tipo em estrutura hierárquica
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import pytz

class ArchiveManager:
    """Gerencia arquivamento de análises"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.absolute()
        self.data_dir = self.base_dir / "data"
        self.archive_dir = self.data_dir / "archive"
        self.current_dir = self.data_dir / "current"
        self.timezone = pytz.timezone('America/Sao_Paulo')
        
    def archive_analysis(self, analysis_type: str, source_file: str = None):
        """
        Arquiva uma análise
        
        Args:
            analysis_type: 'opening', 'closing', 'weekly', 'monthly'
            source_file: Caminho do arquivo fonte (opcional, usa latest se None)
        """
        # Determinar arquivo fonte
        if source_file is None:
            if analysis_type == 'opening':
                source_file = self.data_dir / "latest_analysis.json"
            elif analysis_type == 'closing':
                source_file = self.data_dir / "latest_closing_report.json"
            elif analysis_type == 'weekly':
                source_file = self.current_dir / "latest_weekly.json"
            elif analysis_type == 'monthly':
                source_file = self.current_dir / "latest_monthly.json"
        else:
            source_file = Path(source_file)
            
        if not source_file.exists():
            print(f"❌ Arquivo fonte não encontrado: {source_file}")
            return False
            
        # Ler dados
        with open(source_file, 'r') as f:
            data = json.load(f)
            
        # Extrair timestamp
        timestamp_str = data.get('timestamp')
        if not timestamp_str:
            print(f"❌ Timestamp não encontrado no arquivo")
            return False
            
        # Parse timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = self.timezone.localize(dt)
        else:
            dt = dt.astimezone(self.timezone)
            
        # Determinar destino
        year = dt.strftime('%Y')
        month = dt.strftime('%m')
        day = dt.strftime('%d')
        time = dt.strftime('%H-%M')
        
        if analysis_type in ['opening', 'closing']:
            dest_dir = self.archive_dir / year / month / "daily" / day
            filename = f"{analysis_type}_{time}.json"
        elif analysis_type == 'weekly':
            week_num = dt.isocalendar()[1]
            dest_dir = self.archive_dir / year / month / "weekly"
            filename = f"week_{week_num:02d}.json"
        elif analysis_type == 'monthly':
            dest_dir = self.archive_dir / year / month / "monthly"
            month_name = dt.strftime('%B').lower()
            filename = f"{month_name}.json"
        else:
            print(f"❌ Tipo de análise inválido: {analysis_type}")
            return False
            
        # Criar diretório se não existir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar arquivo
        dest_file = dest_dir / filename
        shutil.copy2(source_file, dest_file)
        
        print(f"✅ Arquivado: {dest_file}")
        
        # Atualizar current/
        self._update_current(analysis_type, source_file)
        
        return True
        
    def _update_current(self, analysis_type: str, source_file: Path):
        """Atualiza diretório current/ com última análise"""
        self.current_dir.mkdir(exist_ok=True)
        
        dest_map = {
            'opening': 'latest_opening.json',
            'closing': 'latest_closing.json',
            'weekly': 'latest_weekly.json',
            'monthly': 'latest_monthly.json'
        }
        
        if analysis_type in dest_map:
            dest = self.current_dir / dest_map[analysis_type]
            # Evitar copiar o mesmo arquivo
            if source_file.resolve() != dest.resolve():
                shutil.copy2(source_file, dest)
                print(f"✅ Atualizado: {dest}")
            else:
                print(f"ℹ️ Arquivo já está em current: {dest}")
            
    def migrate_existing_files(self):
        """Migra arquivos existentes para nova estrutura"""
        print("\n🔄 Migrando arquivos existentes...")
        
        # Migrar análises de abertura
        for file in self.data_dir.glob("analysis_*.json"):
            if file.name.startswith("analysis_202"):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    # Adicionar timestamp se não existir
                    if 'timestamp' not in data:
                        # Extrair data do nome do arquivo
                        parts = file.stem.split('_')
                        if len(parts) >= 3:
                            date_str = parts[1]  # YYYYMMDD
                            time_str = parts[2]  # HHMM
                            dt_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}T{time_str[:2]}:{time_str[2:]}:00-03:00"
                            data['timestamp'] = dt_str
                            
                            # Salvar com timestamp
                            with open(file, 'w') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    # Arquivar
                    self.archive_analysis('opening', str(file))
                    
                except Exception as e:
                    print(f"⚠️ Erro ao migrar {file.name}: {e}")
                    
        # Migrar relatórios de fechamento
        for file in self.data_dir.glob("closing_report_*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                if 'timestamp' not in data:
                    # Extrair data do nome do arquivo
                    parts = file.stem.split('_')
                    if len(parts) >= 3:
                        date_str = parts[2]  # YYYYMMDD
                        dt_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}T21:15:00-03:00"
                        data['timestamp'] = dt_str
                        
                        with open(file, 'w') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.archive_analysis('closing', str(file))
                
            except Exception as e:
                print(f"⚠️ Erro ao migrar {file.name}: {e}")
                
        print("✅ Migração concluída!")
        
    def cleanup_old_files(self):
        """Remove arquivos antigos após migração (opcional)"""
        print("\n🧹 Limpando arquivos antigos...")
        
        patterns = [
            "analysis_202*.json",
            "closing_report_202*.json"
        ]
        
        for pattern in patterns:
            for file in self.data_dir.glob(pattern):
                if file.name not in ['latest_analysis.json', 'latest_closing_report.json']:
                    print(f"🗑️ Removendo: {file.name}")
                    # file.unlink()  # Descomente para remover de fato
                    
        print("✅ Limpeza concluída!")

def main():
    """Função principal"""
    import sys
    
    manager = ArchiveManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'migrate':
            manager.migrate_existing_files()
        elif command == 'cleanup':
            manager.cleanup_old_files()
        elif command == 'archive':
            if len(sys.argv) < 3:
                print("Uso: archive_manager.py archive <tipo> [arquivo]")
                print("Tipos: opening, closing, weekly, monthly")
                sys.exit(1)
            
            analysis_type = sys.argv[2]
            source_file = sys.argv[3] if len(sys.argv) > 3 else None
            manager.archive_analysis(analysis_type, source_file)
        else:
            print(f"Comando desconhecido: {command}")
            print("Comandos: migrate, cleanup, archive")
    else:
        print("Uso: archive_manager.py <comando>")
        print("Comandos:")
        print("  migrate  - Migra arquivos existentes")
        print("  cleanup  - Remove arquivos antigos")
        print("  archive  - Arquiva uma análise")

if __name__ == "__main__":
    main()
