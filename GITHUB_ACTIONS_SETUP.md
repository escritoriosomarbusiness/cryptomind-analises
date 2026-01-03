# 🤖 Configuração do GitHub Actions

## 📋 Passo a Passo

### 1. Acessar o Repositório no GitHub
Acesse: https://github.com/escritoriosomarbusiness/cryptomind-analises

### 2. Criar o Arquivo de Workflow

#### Opção A: Via Interface Web (Recomendado)

1. No repositório, clique em **"Actions"** no menu superior
2. Clique em **"New workflow"**
3. Clique em **"set up a workflow yourself"**
4. Cole o conteúdo abaixo no editor
5. Nomeie o arquivo como: `scheduled_reports.yml`
6. Clique em **"Start commit"** → **"Commit new file"**

#### Opção B: Via Git Local (Requer Permissões)

```bash
# Criar diretório
mkdir -p .github/workflows

# Criar arquivo (copiar conteúdo abaixo)
nano .github/workflows/scheduled_reports.yml

# Commit e push
git add .github/workflows/scheduled_reports.yml
git commit -m "🤖 Adicionar workflow de relatórios automatizados"
git push
```

---

## 📄 Conteúdo do Arquivo `scheduled_reports.yml`

```yaml
name: Relatórios Automatizados CryptoMind IA

on:
  schedule:
    # Relatório Semanal - Domingos às 21:15 BRT (00:15 UTC Segunda)
    - cron: '15 0 * * 1'
    
    # Relatório Mensal - Último dia do mês às 21:15 BRT (00:15 UTC)
    # Nota: GitHub Actions não suporta 'L' (último dia), então usamos dia 28-31
    - cron: '15 0 28-31 * *'
  
  workflow_dispatch:  # Permite execução manual

jobs:
  weekly_report:
    name: Gerar Relatório Semanal
    runs-on: ubuntu-latest
    # Executar apenas às segundas-feiras (relatório semanal)
    if: github.event.schedule == '15 0 * * 1' || github.event_name == 'workflow_dispatch'
    
    steps:
      - name: Checkout repositório
        uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Instalar dependências
        run: |
          pip install pytz requests
      
      - name: Gerar relatório semanal
        run: |
          python3 scripts/generate_weekly_report.py
      
      - name: Reconstruir índices
        run: |
          python3 scripts/index_builder.py
      
      - name: Commit e push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/
          git commit -m "📊 Relatório Semanal - $(date +'%d/%m/%Y %H:%M')" || echo "Nada para commitar"
          git push
  
  monthly_report:
    name: Gerar Relatório Mensal
    runs-on: ubuntu-latest
    # Executar apenas no último dia do mês
    if: github.event.schedule == '15 0 28-31 * *' || github.event_name == 'workflow_dispatch'
    
    steps:
      - name: Checkout repositório
        uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Instalar dependências
        run: |
          pip install pytz requests
      
      - name: Verificar se é último dia do mês
        id: check_last_day
        run: |
          TOMORROW=$(date -d "tomorrow" +%d)
          if [ "$TOMORROW" == "01" ]; then
            echo "is_last_day=true" >> $GITHUB_OUTPUT
          else
            echo "is_last_day=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Gerar relatório mensal
        if: steps.check_last_day.outputs.is_last_day == 'true'
        run: |
          python3 scripts/generate_monthly_report.py
      
      - name: Reconstruir índices
        if: steps.check_last_day.outputs.is_last_day == 'true'
        run: |
          python3 scripts/index_builder.py
      
      - name: Commit e push
        if: steps.check_last_day.outputs.is_last_day == 'true'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/
          git commit -m "📈 Relatório Mensal - $(date +'%B %Y')" || echo "Nada para commitar"
          git push
```

---

## ✅ Verificação

### 1. Confirmar que o Workflow foi Criado
1. Acesse: https://github.com/escritoriosomarbusiness/cryptomind-analises/actions
2. Você deve ver o workflow **"Relatórios Automatizados CryptoMind IA"** listado

### 2. Testar Execução Manual
1. Clique no workflow
2. Clique em **"Run workflow"** (botão no canto direito)
3. Selecione a branch **main**
4. Clique em **"Run workflow"**
5. Aguarde a execução (leva ~1-2 minutos)

### 3. Verificar Resultado
- ✅ Status verde = Sucesso
- ❌ Status vermelho = Erro (clique para ver logs)

---

## 📅 Agendamento

### Relatório Semanal
- **Quando**: Toda segunda-feira às 00:15 UTC (Domingos 21:15 BRT)
- **Frequência**: Semanal
- **Job**: `weekly_report`

### Relatório Mensal
- **Quando**: Dias 28-31 às 00:15 UTC (21:15 BRT)
- **Frequência**: Mensal (apenas no último dia)
- **Job**: `monthly_report`

---

## 🔧 Troubleshooting

### Erro: "refusing to allow a GitHub App to create or update workflow"
**Solução**: Criar o workflow via interface web do GitHub (Opção A)

### Workflow não executa automaticamente
**Verificar**:
1. Workflow está na branch **main**
2. Arquivo está em `.github/workflows/`
3. Sintaxe YAML está correta
4. Actions está habilitado no repositório

### Erro de permissão no push
**Solução**: Verificar se `GITHUB_TOKEN` tem permissão de escrita
1. Settings → Actions → General
2. Workflow permissions → **Read and write permissions**
3. Salvar

---

## 📝 Notas

- O timezone do GitHub Actions é **UTC**
- BRT = UTC-3
- Para executar às 21:15 BRT, usar 00:15 UTC (próximo dia)
- O workflow mensal verifica se é o último dia do mês antes de executar

---

## 🎯 Resultado Esperado

Após configuração:
- ✅ Relatórios semanais gerados automaticamente todo domingo às 21:15 BRT
- ✅ Relatórios mensais gerados automaticamente no último dia do mês às 21:15 BRT
- ✅ Commits automáticos com os relatórios
- ✅ Site atualizado automaticamente
- ✅ Histórico sempre atualizado

---

**Última atualização**: 03/01/2026
