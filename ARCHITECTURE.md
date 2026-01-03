# 🏗️ Arquitetura do Sistema CryptoMind IA

## 📋 Visão Geral

Sistema completo de análises automatizadas de criptomoedas com suporte a:
- ✅ Análises de abertura (diárias)
- ✅ Análises de fechamento (diárias)
- 🆕 Relatórios semanais com KPIs (domingos às 21:15)
- 🆕 Relatórios mensais com KPIs (último dia do mês às 21:15)
- 🆕 Interface web para navegação no histórico

---

## 📁 Estrutura de Diretórios

```
cryptomind-analises/
├── data/
│   ├── current/                          # Análises atuais (sempre atualizadas)
│   │   ├── latest_opening.json          # Última análise de abertura
│   │   ├── latest_closing.json          # Último relatório de fechamento
│   │   ├── latest_weekly.json           # Último relatório semanal
│   │   └── latest_monthly.json          # Último relatório mensal
│   │
│   ├── archive/                          # Histórico organizado
│   │   ├── 2026/
│   │   │   ├── 01/                      # Janeiro 2026
│   │   │   │   ├── daily/
│   │   │   │   │   ├── 02/              # 02/01/2026
│   │   │   │   │   │   ├── opening_11-04.json
│   │   │   │   │   │   └── closing_20-52.json
│   │   │   │   │   ├── 03/              # 03/01/2026
│   │   │   │   │   │   ├── opening_11-04.json
│   │   │   │   │   │   └── closing_21-15.json
│   │   │   │   ├── weekly/
│   │   │   │   │   ├── week_01.json     # Semana 1 (dom 05/01 21:15)
│   │   │   │   │   ├── week_02.json     # Semana 2 (dom 12/01 21:15)
│   │   │   │   │   └── week_03.json     # Semana 3 (dom 19/01 21:15)
│   │   │   │   └── monthly/
│   │   │   │       └── january.json     # Relatório mensal (31/01 21:15)
│   │   │   └── 02/                      # Fevereiro 2026
│   │   │       └── ...
│   │
│   ├── index/                            # Índices para navegação rápida
│   │   ├── master_index.json            # Índice geral de todas as análises
│   │   ├── daily_index.json             # Índice de análises diárias
│   │   ├── weekly_index.json            # Índice de relatórios semanais
│   │   └── monthly_index.json           # Índice de relatórios mensais
│   │
│   └── performance/                      # Dados de performance
│       ├── daily_performance.json       # Performance diária acumulada
│       ├── weekly_performance.json      # Performance semanal
│       └── monthly_performance.json     # Performance mensal
│
├── scripts/
│   ├── generate_analysis.py             # ✅ Análise de abertura (existente)
│   ├── generate_closing_report.py       # ✅ Relatório de fechamento (existente)
│   ├── generate_weekly_report.py        # 🆕 Relatório semanal + KPIs
│   ├── generate_monthly_report.py       # 🆕 Relatório mensal + KPIs
│   ├── archive_manager.py               # 🆕 Gerenciador de arquivamento
│   └── index_builder.py                 # 🆕 Construtor de índices
│
├── web/
│   ├── index.html                        # Página principal (análise atual)
│   ├── history.html                      # 🆕 Página de histórico
│   ├── weekly.html                       # 🆕 Relatórios semanais
│   ├── monthly.html                      # 🆕 Relatórios mensais
│   ├── css/
│   │   ├── style.css                    # ✅ Estilos principais
│   │   └── history.css                  # 🆕 Estilos do histórico
│   └── js/
│       ├── main.js                      # ✅ Script principal
│       ├── history.js                   # 🆕 Navegação no histórico
│       └── charts.js                    # 🆕 Gráficos de KPIs
│
└── .github/
    └── workflows/
        └── scheduled_reports.yml         # 🆕 Agendamento automático
```

---

## 📊 Tipos de Relatórios

### 1. **Análise de Abertura** (Diária)
- **Horário**: Variável (geralmente manhã)
- **Conteúdo**:
  - Análise técnica de BTC + Top 5 altcoins
  - Setups de LONG/SHORT
  - Níveis de entrada, stop e alvos
  - Viés do dia (BULLISH/BEARISH/NEUTRO)
  - Indicador macro USDT.D
  - Fear & Greed Index

### 2. **Relatório de Fechamento** (Diário)
- **Horário**: Variável (geralmente noite)
- **Conteúdo**:
  - Resumo do dia
  - Performance dos setups
  - Análise de acertos/erros
  - Lições aprendidas

### 3. **Relatório Semanal** (Domingos 21:15)
- **Conteúdo**:
  - **KPIs da Semana**:
    - Taxa de acerto (Win Rate %)
    - Total de setups gerados
    - Setups executados vs não executados
    - Profit Factor
    - Melhor ativo da semana
    - Pior ativo da semana
  - **Análise Macro**:
    - Tendência semanal do BTC
    - Comportamento do USDT.D
    - Fear & Greed médio
  - **Destaques**:
    - Melhor trade da semana
    - Trade mais arriscado
    - Oportunidades perdidas

### 4. **Relatório Mensal** (Último dia do mês 21:15)
- **Conteúdo**:
  - **KPIs do Mês**:
    - Taxa de acerto mensal (Win Rate %)
    - Total de setups gerados no mês
    - Profit Factor mensal
    - Drawdown máximo
    - Melhor semana do mês
    - Comparação com mês anterior
  - **Análise de Tendências**:
    - Gráfico de performance mensal
    - Ativos mais rentáveis
    - Padrões identificados
  - **Estatísticas Avançadas**:
    - Sharpe Ratio
    - Sortino Ratio
    - Maximum Drawdown
    - Recovery Factor

---

## 🔄 Fluxo de Dados

```
1. GERAÇÃO
   ├─ Script executa análise/relatório
   ├─ Salva em data/current/latest_*.json
   └─ Dispara archive_manager.py

2. ARQUIVAMENTO
   ├─ archive_manager.py lê latest_*.json
   ├─ Organiza em data/archive/YYYY/MM/tipo/
   └─ Dispara index_builder.py

3. INDEXAÇÃO
   ├─ index_builder.py varre data/archive/
   ├─ Gera/atualiza índices em data/index/
   └─ Calcula estatísticas de performance

4. EXIBIÇÃO
   ├─ Interface web lê data/current/ (página principal)
   ├─ Interface de histórico lê data/index/
   └─ Renderiza com filtros e busca
```

---

## 🎯 KPIs Rastreados

### Diários
- Número de setups gerados
- Setups LONG vs SHORT
- Ativos com setup vs NO TRADE ZONE
- Score médio dos setups

### Semanais
- Win Rate (%)
- Total de trades sugeridos
- Profit Factor
- Melhor/Pior ativo
- Volatilidade média

### Mensais
- Win Rate mensal (%)
- Profit Factor mensal
- Drawdown máximo
- Sharpe Ratio
- Sortino Ratio
- Comparação mês a mês

---

## 🕐 Agendamento

### GitHub Actions (Automático)
```yaml
# .github/workflows/scheduled_reports.yml

# Relatório Semanal - Domingos 21:15 BRT
- cron: '15 0 * * 0'  # 21:15 BRT = 00:15 UTC (segunda)

# Relatório Mensal - Último dia do mês 21:15 BRT
- cron: '15 0 L * *'  # 21:15 BRT do último dia
```

### Manual (via Manus)
```bash
# Semanal
python3 scripts/generate_weekly_report.py

# Mensal
python3 scripts/generate_monthly_report.py
```

---

## 🌐 Interface Web

### Página Principal (`index.html`)
- Exibe análise de abertura mais recente
- Card com USDT.D e Fear & Greed
- Setups destacados
- Botão "📊 Ver Histórico"

### Página de Histórico (`history.html`)
- **Filtros**:
  - Data (calendário)
  - Tipo (Abertura/Fechamento/Semanal/Mensal)
  - Ativo (BTC, ETH, SOL, etc.)
- **Visualização**:
  - Cards com preview
  - Modal com análise completa
  - Download JSON/PDF

### Página de Relatórios Semanais (`weekly.html`)
- Lista de todas as semanas
- Gráficos de KPIs
- Comparação semana a semana

### Página de Relatórios Mensais (`monthly.html`)
- Lista de todos os meses
- Gráficos de performance
- Estatísticas avançadas

---

## 🔧 Tecnologias

- **Backend**: Python 3.11
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Gráficos**: Chart.js
- **Hospedagem**: GitHub Pages
- **Automação**: GitHub Actions
- **Formato de Dados**: JSON

---

## 📝 Próximos Passos

1. ✅ Criar estrutura de pastas
2. ✅ Implementar archive_manager.py
3. ✅ Implementar index_builder.py
4. ✅ Criar generate_weekly_report.py
5. ✅ Criar generate_monthly_report.py
6. ✅ Desenvolver interface de histórico
7. ✅ Configurar GitHub Actions
8. ✅ Migrar análises existentes
9. ✅ Testar e publicar

---

**Última atualização**: 03/01/2026
