# 🗄️ Estrutura do Airtable e Sistema de Relatórios - PES v2.0

---

Este documento descreve a arquitetura do banco de dados no Airtable e a lógica dos workflows de automação no n8n, que juntos formam o sistema de relatórios de performance do indicador PES.

## 1. Visão Geral da Arquitetura

O sistema é composto por três partes principais:

1.  **Pine Script (TradingView):** Gera os sinais e envia webhooks com dados estruturados.
2.  **n8n (Automação):** Atua como o cérebro do sistema, recebendo os webhooks, processando os dados, interagindo com o Airtable e enviando relatórios para o Telegram.
3.  **Airtable (Banco de Dados):** Armazena permanentemente todos os dados dos trades e os resumos de performance em diferentes granularidades.

---

## 2. Estrutura da Base no Airtable

A base será chamada `[Crypto] PES Performance` e conterá 5 tabelas interligadas.

### Tabela 1: `Trades`

Esta é a tabela principal que registra cada operação individualmente, da abertura ao fechamento.

| Campo (Field) | Tipo (Type) | Descrição |
|---|---|---|
| `trade_id` | `Autonumber` | ID numérico sequencial e único para cada trade. |
| `signal_id` | `Single line text` | ID único gerado pelo Pine Script (`BTCUSDT_15_1737301200`) para ligar entrada e saída. **É a chave primária de fato.** |
| `status` | `Single select` | Estado atual do trade: `OPEN`, `CLOSED`, `CANCELLED`. |
| `symbol` | `Single line text` | O par de moedas negociado (ex: "BTCUSDT"). |
| `timeframe` | `Single select` | O timeframe em que o sinal foi gerado (ex: "5m", "15m", "1h"). |
| `direction` | `Single select` | A direção do trade: `LONG` ou `SHORT`. |
| `entry_price` | `Number` | Preço de entrada da operação. |
| `exit_price` | `Number` | Preço de saída da operação (preenchido no fechamento). |
| `entry_time_utc` | `Date` (com time) | Timestamp UTC exato da entrada. |
| `exit_time_utc` | `Date` (com time) | Timestamp UTC exato da saída. |
| `duration_minutes` | `Formula` | `DATETIME_DIFF({exit_time_utc}, {entry_time_utc}, 'minutes')`. |
| `quality` | `Single select` | Qualidade do sinal de entrada: `PREMIUM`, `CAUTELA`, `CONTRA`. |
| `mtf_trend` | `Single select` | Tendência do fractal superior no momento da entrada: `ALTA`, `BAIXA`, `NEUTRO`. |
| `result_percent` | `Percent` | `IF({direction} = 'LONG', ({exit_price} - {entry_price}) / {entry_price}, ({entry_price} - {exit_price}) / {entry_price})`. |
| `result_usd` | `Currency` | `result_percent * {trade_capital}` (se um capital for definido). |
| `crypto_date` | `Date` (sem time) | **Campo Chave.** A "data cripto" do trade, calculada pelo n8n para respeitar a virada das 21:00. |
| `crypto_week` | `Formula` | `YEAR({crypto_date}) & '-W' & WEEKNUM({crypto_date})`. |
| `crypto_month` | `Formula` | `YEAR({crypto_date}) & '-' & IF(MONTH({crypto_date}) < 10, '0', '') & MONTH({crypto_date})`. |
| `crypto_year` | `Formula` | `YEAR({crypto_date})`. |
| `link_to_daily` | `Link to another record` | Link para o registro correspondente na tabela `Daily_Summary`. |
| `link_to_weekly` | `Link to another record` | Link para o registro correspondente na tabela `Weekly_Summary`. |
| `link_to_monthly` | `Link to another record` | Link para o registro correspondente na tabela `Monthly_Summary`. |
| `link_to_annual` | `Link to another record` | Link para o registro correspondente na tabela `Annual_Summary`. |

---

### Tabelas 2, 3, 4, 5: `Daily_Summary`, `Weekly_Summary`, `Monthly_Summary`, `Annual_Summary`

Estas tabelas são de **agregação**. Elas não recebem dados diretos do webhook, mas são preenchidas e atualizadas pelos workflows agendados do n8n. A estrutura delas é similar, contendo campos de `Rollup` e `Count` baseados nos links da tabela `Trades`.

**Exemplo de Estrutura para `Daily_Summary`:**

| Campo (Field) | Tipo (Type) | Configuração / Descrição |
|---|---|---|
| `crypto_date` | `Date` | Chave primária da tabela. |
| `trades_linked` | `Link to another record` | Link para todos os trades daquele dia na tabela `Trades`. |
| `total_trades` | `Count` | Contagem dos `trades_linked`. |
| `total_profit_percent` | `Rollup` | `SUM(values)` do campo `result_percent` dos `trades_linked`. |
| `win_rate` | `Rollup` | `(COUNTIF(values, ">0") / COUNT(values))` do campo `result_percent`. |
| `winning_trades` | `Rollup` | `COUNTIF(values, ">0")` do campo `result_percent`. |
| `losing_trades` | `Rollup` | `COUNTIF(values, "<0")` do campo `result_percent`. |
| `best_trade_percent` | `Rollup` | `MAX(values)` do campo `result_percent`. |
| `worst_trade_percent` | `Rollup` | `MIN(values)` do campo `result_percent`. |
| `premium_profit` | `Rollup` | `SUM(values)` do campo `result_percent` com filtro `quality = PREMIUM`. |

As tabelas `Weekly`, `Monthly` e `Annual` seguem a mesma lógica, usando seus respectivos campos de data (`crypto_week`, `crypto_month`, `crypto_year`) como chave.

---

## 3. Workflows de Automação (n8n)

Serão criados 5 workflows principais.

### Workflow 1: `[PES] Trade Processor`

*   **Gatilho:** Webhook (escuta os sinais do TradingView).
*   **Lógica Principal:**
    1.  Recebe o JSON do `alert()`.
    2.  **Se for `ENTRY`:**
        a. Calcula a `crypto_date` baseada no timestamp (se hora < 21:00, usa D-1).
        b. Cria um novo registro na tabela `Trades` com status `OPEN`.
        c. Envia notificação de "NOVA ENTRADA" para o Telegram.
    3.  **Se for `EXIT`:**
        a. Busca na tabela `Trades` pelo `signal_id` correspondente com status `OPEN`.
        b. Atualiza o registro encontrado com `exit_price`, `exit_time_utc` e muda o status para `CLOSED`.
        c. Os campos de fórmula (`result_percent`, `duration_minutes`, etc.) serão calculados automaticamente pelo Airtable.
        d. Envia notificação de "TRADE FECHADO" para o Telegram, já incluindo o resultado.

### Workflow 2: `[PES] Daily Report`

*   **Gatilho:** Agendado (Cron Job).
*   **Horário:** `59 20 * * *` (20:59, todos os dias, no fuso `America/Sao_Paulo`).
*   **Lógica Principal:**
    1.  Calcula a `crypto_date` do dia que está fechando (hoje se hora >= 21:00, ontem se hora < 21:00).
    2.  Busca na tabela `Daily_Summary` pelo registro da `crypto_date` calculada.
    3.  Os campos de `Rollup` no Airtable já terão feito todos os cálculos automaticamente.
    4.  Lê os dados consolidados do registro (total de trades, win rate, lucro total, etc.).
    5.  Formata uma mensagem bonita e estruturada.
    6.  Envia o relatório diário para o Telegram.

### Workflows 3, 4, 5: `Weekly`, `Monthly`, `Annual` Reports

Seguem a mesma lógica do workflow diário, mas com gatilhos diferentes:

*   **Semanal:** `59 20 * * 0` (Domingo, 20:59).
*   **Mensal:** `59 20 L * *` (Último dia do mês, 20:59).
*   **Anual:** `59 20 31 12 *` (31 de Dezembro, 20:59).

Cada workflow buscará os dados na sua respectiva tabela de resumo (`Weekly_Summary`, etc.) e enviará o relatório consolidado para o Telegram.
