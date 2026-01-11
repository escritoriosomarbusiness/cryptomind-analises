# Sistema de Monitoramento Automático do Ecossistema CryptoMind IA

## 📋 Visão Geral

Sistema automatizado que verifica diariamente se todo o ecossistema está funcionando corretamente, incluindo:

- ✅ Geração de relatórios de abertura e fechamento
- ✅ Commits no GitHub
- ✅ Publicação no site https://analises.cryptomindia.com/

## 🔍 Script de Verificação

**Arquivo:** `scripts/health_check.py`

### O que verifica:

1. **Relatório de Abertura**
   - Verifica se foi gerado hoje (segunda a sexta)
   - Horário esperado: após 12:00 UTC (09:00 BRT)
   - Localização: `data/archive/YYYY/MM/daily/DD/opening_*.json`

2. **Relatório de Fechamento**
   - Verifica se foi gerado hoje
   - Horário esperado: após 00:00 UTC (21:00 BRT do dia anterior)
   - Localização: `data/closing_report_YYYYMMDD.json`

3. **Commits no GitHub**
   - Verifica se houve commits nas últimas 24 horas
   - Usa API do GitHub

4. **Site**
   - Verifica se está acessível
   - Verifica se contém conteúdo atualizado

### Como executar manualmente:

```bash
cd /home/ubuntu/cryptomind-analises
python3 scripts/health_check.py
```

## ⚙️ Workflow do GitHub Actions

**Arquivo:** `.github/workflows/health_check.yml`

### Agendamento:

O workflow executa **3 vezes ao dia**:

| Horário UTC | Horário BRT | Propósito |
|-------------|-------------|-----------|
| 13:00 | 10:00 | Após análise de abertura |
| 02:00 | 23:00 (dia anterior) | Após análise de fechamento |
| 18:00 | 15:00 | Verificação adicional |

### Dias de execução:

- **Verificação de abertura:** Segunda a sexta (1-5)
- **Verificação de fechamento:** Terça a sábado (2-6)

### Funcionalidades:

1. **Detecção Automática de Problemas**
   - Executa o script `health_check.py`
   - Identifica falhas automaticamente

2. **Criação de Issues**
   - Cria issue automaticamente quando detecta falha
   - Labels: `health-check`, `automated`, `bug`
   - Contém link direto para os logs

3. **Resolução Automática**
   - Fecha a issue automaticamente quando o problema é resolvido
   - Adiciona comentário confirmando a resolução

4. **Evita Duplicação**
   - Não cria múltiplas issues para o mesmo problema
   - Adiciona comentários na issue existente

## 📝 Como Adicionar o Workflow Manualmente

Devido a restrições de permissão do GitHub App, o workflow precisa ser adicionado manualmente:

### Opção 1: Via Interface do GitHub

1. Acesse: https://github.com/escritoriosomarbusiness/cryptomind-analises
2. Vá em **Actions** → **New workflow**
3. Clique em **set up a workflow yourself**
4. Cole o conteúdo do arquivo `.github/workflows/health_check.yml` (disponível localmente)
5. Commit com a mensagem: "🔍 Adiciona workflow de monitoramento automático"

### Opção 2: Via Git Local

```bash
# Clone o repositório (se ainda não tiver)
git clone https://github.com/escritoriosomarbusiness/cryptomind-analises.git
cd cryptomind-analises

# Copie o arquivo do workflow
# (o arquivo já está em .github/workflows/health_check.yml)

# Adicione e faça commit
git add .github/workflows/health_check.yml
git commit -m "🔍 Adiciona workflow de monitoramento automático"
git push
```

### Opção 3: Via GitHub CLI

```bash
cd /home/ubuntu/cryptomind-analises
gh workflow create
```

## 🚨 Notificações

Quando o sistema detecta um problema:

1. **Issue Criada**
   - Título: "🚨 Falha na Verificação de Saúde do Ecossistema"
   - Contém checklist de verificação
   - Link para os logs da execução

2. **Comentários Adicionais**
   - Se o problema persistir, adiciona comentários na issue
   - Timestamp de cada ocorrência

3. **Fechamento Automático**
   - Quando o problema é resolvido
   - Adiciona comentário confirmando

## 📊 Exemplo de Saída

```
🚀 Iniciando verificação de saúde do ecossistema CryptoMind IA

📊 Verificando relatório de abertura...
✅ OK: Relatório de abertura encontrado: opening_09-33.json

📊 Verificando relatório de fechamento...
✅ OK: Relatório de fechamento encontrado: closing_report_20260110.json

🔄 Verificando commits no GitHub...
✅ OK: Último commit há 12.0 horas: Relatório de fechamento - 10/01/2026 21:16

🌐 Verificando site...
✅ OK: Site acessível: https://analises.cryptomindia.com/
✅ OK: Site contém análise atualizada

============================================================
📋 RELATÓRIO DE VERIFICAÇÃO DO ECOSSISTEMA
============================================================

🕐 Data/Hora: 11/01/2026 09:15:46 -03

✅ Sucessos: 5
  ✅ OK: Relatório de abertura encontrado: opening_09-33.json
  ✅ OK: Relatório de fechamento encontrado: closing_report_20260110.json
  ✅ OK: Último commit há 12.0 horas: Relatório de fechamento - 10/01/2026 21:16
  ✅ OK: Site acessível: https://analises.cryptomindia.com/
  ✅ OK: Site contém análise atualizada

============================================================
✅ STATUS: TUDO OK!
```

## 🔧 Manutenção

### Ajustar horários de verificação

Edite o arquivo `.github/workflows/health_check.yml` e modifique as linhas de cron:

```yaml
schedule:
  - cron: '0 13 * * 1-5'  # 13:00 UTC = 10:00 BRT
```

### Adicionar novas verificações

Edite o arquivo `scripts/health_check.py` e adicione novos métodos:

```python
def check_nova_funcionalidade(self):
    """Verifica nova funcionalidade"""
    print("\n🔍 Verificando nova funcionalidade...")
    
    # Sua lógica aqui
    
    if sucesso:
        self.log_success("Nova funcionalidade OK")
        return True
    else:
        self.log_error("Problema na nova funcionalidade")
        return False
```

Depois adicione a chamada no método `run()`:

```python
def run(self):
    self.check_opening_report()
    self.check_closing_report()
    self.check_github_commits()
    self.check_website()
    self.check_nova_funcionalidade()  # Nova verificação
```

## 📞 Suporte

Em caso de dúvidas ou problemas:

1. Verifique os logs das execuções no GitHub Actions
2. Execute o script manualmente para debug
3. Verifique as issues criadas automaticamente

---

**Criado em:** 11/01/2026  
**Última atualização:** 11/01/2026
