#!/usr/bin/env python3
"""
Script de Verificação de Saúde do Ecossistema CryptoMind IA

Verifica diariamente se:
1. Análises de abertura e fechamento foram geradas
2. Arquivos foram commitados no GitHub
3. Site está acessível e atualizado
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import pytz

# Configurações
GITHUB_REPO = "escritoriosomarbusiness/cryptomind-analises"
SITE_URL = "https://analises.cryptomindia.com/"
TIMEZONE = pytz.timezone('America/Sao_Paulo')

class HealthCheck:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []
        
    def log_error(self, message):
        """Registra um erro crítico"""
        self.errors.append(f"❌ ERRO: {message}")
        print(f"❌ ERRO: {message}")
        
    def log_warning(self, message):
        """Registra um aviso"""
        self.warnings.append(f"⚠️ AVISO: {message}")
        print(f"⚠️ AVISO: {message}")
        
    def log_success(self, message):
        """Registra um sucesso"""
        self.success.append(f"✅ OK: {message}")
        print(f"✅ OK: {message}")
    
    def check_opening_report(self):
        """Verifica se o relatório de abertura foi gerado hoje"""
        print("\n📊 Verificando relatório de abertura...")
        
        now = datetime.now(TIMEZONE)
        today = now.strftime("%Y-%m-%d")
        day = now.strftime("%d")
        
        # Verifica se é dia útil (segunda a sexta)
        if now.weekday() >= 5:  # 5 = sábado, 6 = domingo
            self.log_warning(f"Hoje é {now.strftime('%A')} - análise de abertura não esperada")
            return True
        
        # Verifica se já passou das 12:00 (horário da análise de abertura)
        if now.hour < 12:
            self.log_warning("Ainda não passou das 12:00 - análise de abertura ainda não deveria ter sido gerada")
            return True
        
        # Procura arquivo de abertura no diretório de arquivo
        opening_path = f"data/archive/2026/01/daily/{day}/opening_*.json"
        
        # Lista arquivos que correspondem ao padrão
        import glob
        opening_files = glob.glob(opening_path)
        
        if opening_files:
            # Pega o arquivo mais recente
            latest_file = max(opening_files, key=os.path.getmtime)
            file_time = datetime.fromtimestamp(os.path.getmtime(latest_file), tz=TIMEZONE)
            
            # Verifica se o arquivo é de hoje
            if file_time.date() == now.date():
                self.log_success(f"Relatório de abertura encontrado: {os.path.basename(latest_file)}")
                return True
            else:
                self.log_error(f"Relatório de abertura desatualizado (última modificação: {file_time.strftime('%d/%m/%Y %H:%M')})")
                return False
        else:
            self.log_error(f"Relatório de abertura não encontrado para hoje ({day}/01/2026)")
            return False
    
    def check_closing_report(self):
        """Verifica se o relatório de fechamento foi gerado"""
        print("\n📊 Verificando relatório de fechamento...")
        
        now = datetime.now(TIMEZONE)
        yesterday = now - timedelta(days=1)
        today_str = now.strftime("%Y%m%d")
        
        # Verifica se é dia útil (terça a sábado, pois o fechamento é do dia anterior)
        if now.weekday() == 6:  # Domingo
            self.log_warning("Hoje é domingo - análise de fechamento não esperada")
            return True
        
        # Verifica se já passou das 00:00 (horário da análise de fechamento)
        if now.hour < 1:
            self.log_warning("Ainda não passou das 01:00 - análise de fechamento ainda não deveria ter sido gerada")
            return True
        
        # Verifica arquivo de fechamento
        closing_file = f"data/closing_report_{today_str}.json"
        
        if os.path.exists(closing_file):
            file_time = datetime.fromtimestamp(os.path.getmtime(closing_file), tz=TIMEZONE)
            
            # Verifica se o arquivo foi modificado nas últimas 24 horas
            if (now - file_time).total_seconds() < 86400:  # 24 horas
                self.log_success(f"Relatório de fechamento encontrado: {os.path.basename(closing_file)}")
                return True
            else:
                self.log_error(f"Relatório de fechamento desatualizado (última modificação: {file_time.strftime('%d/%m/%Y %H:%M')})")
                return False
        else:
            self.log_error(f"Relatório de fechamento não encontrado: {closing_file}")
            return False
    
    def check_github_commits(self):
        """Verifica se houve commits recentes no GitHub"""
        print("\n🔄 Verificando commits no GitHub...")
        
        try:
            # API do GitHub para listar commits
            url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
            headers = {"Accept": "application/vnd.github.v3+json"}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            commits = response.json()
            
            if commits:
                latest_commit = commits[0]
                commit_date = datetime.strptime(
                    latest_commit['commit']['author']['date'], 
                    "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=pytz.UTC)
                
                now = datetime.now(pytz.UTC)
                hours_ago = (now - commit_date).total_seconds() / 3600
                
                if hours_ago < 24:
                    self.log_success(f"Último commit há {hours_ago:.1f} horas: {latest_commit['commit']['message'][:50]}")
                    return True
                else:
                    self.log_warning(f"Último commit há {hours_ago:.1f} horas (mais de 24h)")
                    return True
            else:
                self.log_error("Nenhum commit encontrado no repositório")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_error(f"Erro ao verificar GitHub: {str(e)}")
            return False
    
    def check_website(self):
        """Verifica se o site está acessível e atualizado"""
        print("\n🌐 Verificando site...")
        
        try:
            response = requests.get(SITE_URL, timeout=10)
            response.raise_for_status()
            
            # Verifica se a página contém conteúdo esperado
            content = response.text.lower()
            
            if "análise pré-mercado" in content or "cryptomind ia" in content:
                self.log_success(f"Site acessível: {SITE_URL}")
                
                # Verifica se há data de atualização recente
                now = datetime.now(TIMEZONE)
                today_str = now.strftime("%d de %B de %Y").lower()
                
                if today_str in content or "atualizado às" in content:
                    self.log_success("Site contém análise atualizada")
                    return True
                else:
                    self.log_warning("Site pode estar desatualizado (data não encontrada)")
                    return True
            else:
                self.log_error("Site não contém conteúdo esperado")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_error(f"Erro ao acessar site: {str(e)}")
            return False
    
    def generate_report(self):
        """Gera relatório final da verificação"""
        print("\n" + "="*60)
        print("📋 RELATÓRIO DE VERIFICAÇÃO DO ECOSSISTEMA")
        print("="*60)
        
        now = datetime.now(TIMEZONE)
        print(f"\n🕐 Data/Hora: {now.strftime('%d/%m/%Y %H:%M:%S %Z')}")
        
        print(f"\n✅ Sucessos: {len(self.success)}")
        for msg in self.success:
            print(f"  {msg}")
        
        if self.warnings:
            print(f"\n⚠️ Avisos: {len(self.warnings)}")
            for msg in self.warnings:
                print(f"  {msg}")
        
        if self.errors:
            print(f"\n❌ Erros: {len(self.errors)}")
            for msg in self.errors:
                print(f"  {msg}")
        
        print("\n" + "="*60)
        
        # Status final
        if self.errors:
            print("❌ STATUS: FALHA - Ação necessária!")
            return False
        elif self.warnings:
            print("⚠️ STATUS: ATENÇÃO - Verificar avisos")
            return True
        else:
            print("✅ STATUS: TUDO OK!")
            return True
    
    def run(self):
        """Executa todas as verificações"""
        print("🚀 Iniciando verificação de saúde do ecossistema CryptoMind IA\n")
        
        # Executa todas as verificações
        self.check_opening_report()
        self.check_closing_report()
        self.check_github_commits()
        self.check_website()
        
        # Gera relatório final
        success = self.generate_report()
        
        # Retorna código de saída apropriado
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    checker = HealthCheck()
    checker.run()
