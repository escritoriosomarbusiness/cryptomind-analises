# 🚀 Plano de Implementação Priorizado - TuTCI v2.0

---

Este documento divide o desenvolvimento do projeto TuTCI v2.0 em 3 Tiers (níveis) de prioridade, permitindo uma entrega incremental de valor, do MVP (Produto Mínimo Viável) à solução completa com relatórios avançados.

## Tier 1: MVP - Sinais e Rastreamento de Resultados

**Objetivo:** Ter um sistema funcional que gera sinais de entrada/saída, rastreia o resultado de cada trade individualmente e notifica no Telegram. O foco é validar a lógica central e o fluxo de dados.

### 1.1. Pine Script (TradingView)

*   [ ] **Lógica Central:** Implementar a estratégia base de Turtle Trading com canais duplos (entrada de 20 períodos, saída de 10 períodos).
*   [ ] **Gestão de Posição Básica:** Adicionar a lógica para não entrar `long` se já estiver `long`, e vice-versa.
*   [ ] **`signal_id` Único:** Criar o ID único no momento da entrada (`{ticker}_{timeframe}_{timestamp}`) e persistir esse ID até o sinal de saída.
*   [ ] **Webhook Simplificado:** Configurar o `alert()` para enviar um JSON contendo apenas os campos essenciais:
    *   `action`, `signal_id`, `symbol`, `timeframe`, `type` (`LONG_ENTRY`, `LONG_EXIT`, etc.), `price`.

### 1.2. Airtable

*   [ ] **Criar Base:** Configurar a base `[Crypto] TuTCI Performance`.
*   [ ] **Tabela `Trades`:** Criar apenas a tabela principal `Trades` com os campos essenciais para calcular o resultado de um trade (ex: `signal_id`, `status`, `entry_price`, `exit_price`, `result_percent`). As fórmulas e campos de data mais complexos podem ser deixados para o Tier 2.

### 1.3. n8n

*   [ ] **Workflow `[TUTCI] Trade Processor` (v1):**
    *   [ ] Criar o webhook para receber os alertas do TradingView.
    *   [ ] Lógica para `ENTRY`: Criar um novo registro na tabela `Trades` do Airtable com status `OPEN`.
    *   [ ] Lógica para `EXIT`: Buscar o registro correspondente pelo `signal_id`, atualizar com o `exit_price` e mudar o status para `CLOSED`.
    *   [ ] Enviar notificação simples para o Telegram para cada entrada e cada saída, já mostrando o resultado percentual no fechamento.

**Resultado ao Final do Tier 1:** Um indicador que opera e um bot que informa o resultado de cada operação fechada. Já é um sistema funcional e lucrativo (ou não), mas sem a inteligência de qualificação e sem relatórios agregados.

---

## Tier 2: Core Features - Qualificação MTF e Melhorias Visuais

**Objetivo:** Adicionar a camada de inteligência ao indicador, qualificando os sinais com base na tendência macro e melhorando a usabilidade no gráfico.

### 2.1. Pine Script (TradingView)

*   [ ] **Implementar Análise MTF:** Adicionar toda a lógica de busca de dados no fractal superior (mapeamento de TFs, EMAs 55 e 233).
*   [ ] **Classificação de Qualidade:** Implementar a lógica que classifica cada sinal de entrada como `PREMIUM`, `CAUTELA` ou `CONTRA`.
*   [ ] **Filtro de Terço de Candle:** Adicionar a validação que exige o fechamento no terço final do candle para entradas.
*   [ ] **Webhook Completo:** Expandir o JSON do webhook para incluir os novos campos: `quality`, `mtf_trend`, `entry_channel_price`, etc.
*   [ ] **Melhorias Visuais:**
    *   [ ] Implementar o Dashboard com status da tendência MTF.
    *   [ ] Adicionar as labels coloridas (Verde/Amarelo/Vermelho) para indicar a qualidade do sinal.
    *   [ ] Implementar o posicionamento dinâmico das labels para evitar sobreposição.

### 2.2. Airtable

*   [ ] **Adicionar Campos:** Adicionar os campos `quality` e `mtf_trend` na tabela `Trades` para armazenar os dados enriquecidos do Tier 2.

### 2.3. n8n

*   [ ] **Workflow `[TUTCI] Trade Processor` (v2):**
    *   [ ] Adaptar o workflow para receber e salvar os novos campos (`quality`, `mtf_trend`) no Airtable.
    *   [ ] **Melhorar Notificações:** Formatar as mensagens do Telegram para incluir a qualidade do sinal, usando emojis (🌟, ⚠️, 🚫) e destacando a informação.

**Resultado ao Final do Tier 2:** O sistema agora é "inteligente". O usuário recebe sinais qualificados, permitindo uma melhor gestão de risco, e a visualização no gráfico é muito mais rica e profissional.

---

## Tier 3: Advanced Reporting - Automação Completa de Performance

**Objetivo:** Construir o sistema de relatórios automáticos que fornece uma visão completa da performance do indicador em diferentes períodos, transformando dados brutos em insights acionáveis.

### 3.1. Airtable

*   [ ] **Tabelas de Resumo:** Criar as 4 tabelas de agregação: `Daily_Summary`, `Weekly_Summary`, `Monthly_Summary`, e `Annual_Summary`.
*   [ ] **Configurar Links e Rollups:** Implementar todos os campos de `Link`, `Count` e `Rollup` para que os cálculos de performance (win rate, lucro total, etc.) sejam feitos automaticamente pelo Airtable.
*   [ ] **Campos de Data Cripto:** Adicionar os campos de fórmula (`crypto_week`, `crypto_month`, `crypto_year`) e o campo `crypto_date` que será preenchido pelo n8n.

### 3.2. n8n

*   [ ] **Ajuste no Workflow Principal:** Atualizar o workflow `Trade Processor` para calcular e preencher corretamente o campo `crypto_date` (respeitando a virada das 21:00) em cada novo trade.
*   [ ] **Workflow `[TUTCI] Daily Report`:**
    *   [ ] Criar o workflow agendado para rodar às 20:59 (GMT-3).
    *   [ ] Implementar a lógica para ler os dados da tabela `Daily_Summary`.
    *   [ ] Formatar e enviar o relatório diário completo para o Telegram.
*   [ ] **Workflow `[TUTCI] Weekly Report`:** Criar e configurar o workflow para o relatório semanal.
*   [ ] **Workflow `[TUTCI] Monthly Report`:** Criar e configurar o workflow para o relatório mensal.
*   [ ] **Workflow `[TUTCI] Annual Report`:** Criar e configurar o workflow para o relatório anual.

### 3.3. Pine Script (TradingView)

*   [ ] **Revisão Final:** Fazer quaisquer ajustes finos no código e nos alertas para garantir integração perfeita com o sistema de backend.

**Resultado ao Final do Tier 3:** Um sistema de trading e análise de performance totalmente autônomo. O indicador opera, e o backend trabalha 24/7 para coletar, agregar e apresentar dados de performance, permitindo uma visão clara e objetiva da eficácia da estratégia ao longo do tempo.
