# 📚 Documentação do Sistema CryptoMind IA

## 🎯 Visão Geral

Sistema automatizado de análises técnicas de criptomoedas com geração de relatórios diários, semanais e mensais, incluindo interface web profissional para navegação no histórico.

---

## 📁 Estrutura do Sistema

```
cryptomind-analises/
├── data/
│   ├── current/              # Análises mais recentes
│   │   ├── latest_opening.json
│   │   ├── latest_closing.json
│   │   ├── latest_weekly.json
│   │   └── latest_monthly.json
│   │
│   ├── archive/              # Histórico organizado
│   │   └── YYYY/
│   │       └── MM/
│   │           ├── daily/
│   │           │   └── DD/
│   │           │       ├── opening_HH-MM.json
│   │           │       └── closing_HH-MM.json
│   │           ├── weekly/
│   │           │   └── week_NN.json
│   │           └── monthly/
│   │               └── month_name.json
│   │
│   ├── index/                # Índices para navegação
│   │   ├── master_index.json
│   │   ├── daily_index.json
│   │   ├── weekly_index.json
│   │   └── monthly_index.json
│   │
│   └── performance/          # Métricas de performance
│
├── scripts/
│   ├── generate_analysis.py          # Análise de abertura
│   ├── generate_closing_report.py    # Relatório de fechamento
│   ├── generate_weekly_report.py     # Relatório semanal
│   ├── generate_monthly_report.py    # Relatório mensal
│   ├── archive_manager.py            # Gerenciador de arquivamento
│   ├── index_builder.py              # Construtor de índices
│   ├── generate_html.py              # Gerador de HTML
│   └── run_daily_analysis.py         # Orquestrador principal
│
├── index.html                # Página principal
├── history.html              # Página de histórico
└── ARCHITECTURE.md           # Documentação da arquitetura
```

---

## 🔄 Tipos de Relatórios

### 1. Análise de Abertura (Diária)
**Horário**: Variável (geralmente manhã)  
**Comando**: `python3 scripts/run_daily_analysis.py --mode morning`

**Conteúdo**:
- Análise técnica de BTC + Top 5 altcoins
- Setups de LONG/SHORT com níveis de entrada, stop e alvos
- Viés do dia (BULLISH/BEARISH/NEUTRO)
- Indicadores macro (USDT.D, Fear & Greed)
- Score de qualidade dos setups (0-10)

**Arquivos Gerados**:
- `data/current/latest_opening.json`
- `data/archive/YYYY/MM/daily/DD/opening_HH-MM.json`
- `index.html` (atualizado)

---

### 2. Relatório de Fechamento (Diário)
**Horário**: Variável (geralmente noite)  
**Comando**: `python3 scripts/run_daily_analysis.py --mode closing`

**Conteúdo**:
- Performance dos setups do dia
- KPIs: Win Rate, P&L, Viés correto
- Análise de acertos e erros
- Performance acumulada

**Arquivos Gerados**:
- `data/current/latest_closing.json`
- `data/archive/YYYY/MM/daily/DD/closing_HH-MM.json`
- `index.html` (atualizado com seção de fechamento)

---

### 3. Relatório Semanal
**Horário**: Domingos às 21:15 BRT  
**Comando**: `python3 scripts/generate_weekly_report.py`

**Conteúdo**:
- **KPIs da Semana**:
  - Total de setups gerados
  - Distribuição LONG vs SHORT
  - Score médio dos setups
  - Melhor e pior ativo
  - Dias de trading
  
- **Análise Macro**:
  - Fear & Greed médio da semana
  - USDT.D médio e impacto dominante
  - Ranges de variação
  
- **Destaques**:
  - Melhor setup da semana
  - Total de dias analisados

**Arquivos Gerados**:
- `data/current/latest_weekly.json`
- `data/archive/YYYY/MM/weekly/week_NN.json`

---

### 4. Relatório Mensal
**Horário**: Último dia do mês às 21:15 BRT  
**Comando**: `python3 scripts/generate_monthly_report.py`

**Conteúdo**:
- **KPIs do Mês**:
  - Total de setups gerados
  - Distribuição LONG vs SHORT
  - Score médio
  - Média de setups por dia
  - Melhor e pior ativo
  - Dias de trading
  
- **Análise de Tendências**:
  - Resumo semanal (setups, Fear & Greed, USDT.D)
  - Melhor semana do mês
  
- **Estatísticas Avançadas**:
  - Placeholder para Sharpe Ratio, Sortino, etc.
  
- **Comparação**:
  - Comparação com mês anterior (se disponível)

**Arquivos Gerados**:
- `data/current/latest_monthly.json`
- `data/archive/YYYY/MM/monthly/month_name.json`

---

## 🛠️ Scripts Principais

### `archive_manager.py`
Gerencia o arquivamento automático de análises.

**Comandos**:
```bash
# Migrar arquivos existentes
python3 scripts/archive_manager.py migrate

# Arquivar uma análise específica
python3 scripts/archive_manager.py archive <tipo> [arquivo]

# Limpar arquivos antigos
python3 scripts/archive_manager.py cleanup
```

---

### `index_builder.py`
Constrói índices de navegação para a interface web.

**Comando**:
```bash
python3 scripts/index_builder.py
```

**Índices Gerados**:
- `daily_index.json` - Todas as análises diárias
- `weekly_index.json` - Todos os relatórios semanais
- `monthly_index.json` - Todos os relatórios mensais
- `master_index.json` - Estatísticas gerais + referências

---

### `run_daily_analysis.py`
Orquestrador principal que executa análise + HTML + arquivamento + push.

**Comandos**:
```bash
# Análise de abertura
python3 scripts/run_daily_analysis.py --mode morning

# Relatório de fechamento
python3 scripts/run_daily_analysis.py --mode closing

# Ambos
python3 scripts/run_daily_analysis.py --mode both
```

**Fluxo de Execução**:
1. Coleta dados e gera análise
2. Gera HTML
3. **Arquiva análise** (novo!)
4. **Reconstrói índices** (novo!)
5. Faz commit e push para GitHub

---

## 🌐 Interface Web

### Página Principal (`index.html`)
- Exibe análise de abertura mais recente
- Indicadores macro (USDT.D, Fear & Greed)
- Setups destacados por ativo
- Seção de fechamento (quando disponível)
- **Botão "📊 Histórico"** para acessar histórico completo

### Página de Histórico (`history.html`)
- **Estatísticas Gerais**:
  - Total de dias analisados
  - Total de análises
  - Total de relatórios semanais
  - Total de relatórios mensais
  
- **Filtros**:
  - Todas
  - Abertura
  - Fechamento
  - Semanais
  - Mensais
  
- **Timeline**:
  - Organizada por data (mais recente primeiro)
  - Cards clicáveis para cada análise
  - Preview com informações resumidas
  - Link direto para o JSON completo

---

## 🤖 Automação

### Análises Diárias
Executadas manualmente ou via cron/scheduler externo:

```bash
# Crontab exemplo
0 11 * * * cd /home/ubuntu/cryptomind-analises && python3 scripts/run_daily_analysis.py --mode morning
5 21 * * * cd /home/ubuntu/cryptomind-analises && python3 scripts/run_daily_analysis.py --mode closing
```

### Relatórios Semanais e Mensais
**GitHub Actions** (requer configuração manual):

1. Criar arquivo `.github/workflows/scheduled_reports.yml` no repositório
2. Conteúdo disponível em: `/home/ubuntu/cryptomind-analises/.github/workflows/scheduled_reports.yml` (local)
3. Adicionar via interface do GitHub ou com permissões adequadas

**Horários**:
- **Semanal**: Domingos às 21:15 BRT (00:15 UTC Segunda)
- **Mensal**: Último dia do mês às 21:15 BRT (00:15 UTC)

---

## 📊 KPIs Rastreados

### Diários
- Número de setups gerados
- Setups LONG vs SHORT
- Ativos com setup vs NO TRADE ZONE
- Score médio dos setups
- Performance dos setups (Win/Loss/Ongoing)
- P&L do dia
- Viés correto

### Semanais
- Total de setups da semana
- Distribuição LONG/SHORT
- Score médio
- Melhor/Pior ativo
- Fear & Greed médio
- USDT.D médio e impacto
- Melhor setup da semana

### Mensais
- Total de setups do mês
- Distribuição LONG/SHORT
- Score médio
- Média de setups por dia
- Melhor/Pior ativo
- Análise semanal (4-5 semanas)
- Melhor semana do mês
- Comparação com mês anterior

---

## 🔧 Manutenção

### Reconstruir Índices Manualmente
```bash
python3 scripts/index_builder.py
```

### Migrar Análises Antigas
```bash
python3 scripts/archive_manager.py migrate
```

### Gerar Relatório Semanal Manualmente
```bash
python3 scripts/generate_weekly_report.py
```

### Gerar Relatório Mensal Manualmente
```bash
python3 scripts/generate_monthly_report.py
```

### Verificar Estrutura
```bash
tree data -L 4
```

---

## 🚀 Próximas Melhorias

- [ ] Adicionar GitHub Actions workflow (requer permissão)
- [ ] Implementar estatísticas avançadas (Sharpe Ratio, Sortino, etc.)
- [ ] Criar gráficos interativos de performance
- [ ] Adicionar exportação de relatórios em PDF
- [ ] Implementar sistema de notificações (Telegram/Discord)
- [ ] Adicionar comparação entre ativos
- [ ] Criar dashboard de performance em tempo real

---

## 📝 Notas Importantes

1. **Arquivamento Automático**: Todas as análises diárias agora são automaticamente arquivadas após geração
2. **Índices Automáticos**: Os índices são reconstruídos automaticamente após cada análise
3. **Histórico Completo**: Todas as análises desde o início estão disponíveis na página de histórico
4. **GitHub Actions**: O workflow está pronto mas precisa ser adicionado manualmente devido a restrições de permissão
5. **Timezone**: Todos os horários são em BRT (America/Sao_Paulo)

---

## 🆘 Troubleshooting

### Erro ao arquivar
```bash
# Verificar permissões
ls -la data/

# Recriar estrutura
mkdir -p data/{current,archive,index,performance}
```

### Índices não atualizam
```bash
# Reconstruir manualmente
python3 scripts/index_builder.py
```

### Página de histórico vazia
```bash
# Verificar se índices existem
ls -la data/index/

# Reconstruir índices
python3 scripts/index_builder.py
```

---

**Última atualização**: 03/01/2026  
**Versão do Sistema**: 2.0
