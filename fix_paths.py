#!/usr/bin/env python3
"""
Script para corrigir caminhos absolutos para relativos em todos os scripts
"""

import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.absolute()
SCRIPTS_DIR = BASE_DIR / "scripts"

# Mapeamento de substituições
replacements = {
    'Path("/home/ubuntu/cryptomind-analises")': 'Path(__file__).parent.parent.absolute()',
    '"/home/ubuntu/cryptomind-analises/data"': 'str(Path(__file__).parent.parent / "data")',
    '"/home/ubuntu/cryptomind-analises"': 'str(Path(__file__).parent.parent.absolute())',
    "'/home/ubuntu/cryptomind-analises/scripts'": "str(Path(__file__).parent.absolute())",
    '"/home/ubuntu/cryptomind-analises/index.html"': 'str(Path(__file__).parent.parent / "index.html")',
}

def fix_file(filepath):
    """Corrige caminhos absolutos em um arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Corrigido: {filepath.name}")
        return True
    else:
        print(f"⏭️  Sem alterações: {filepath.name}")
        return False

def main():
    """Corrige todos os scripts Python"""
    print("🔧 Corrigindo caminhos absolutos para relativos...\n")
    
    fixed_count = 0
    for script_file in SCRIPTS_DIR.glob("*.py"):
        if script_file.name == "__pycache__":
            continue
        if fix_file(script_file):
            fixed_count += 1
    
    print(f"\n✅ {fixed_count} arquivos corrigidos!")

if __name__ == "__main__":
    main()
