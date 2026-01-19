# 🚀 PES Tier 1 (MVP) - Especificações de Implementação

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

## 🎯 Objetivo do Tier 1 (MVP)

O objetivo do MVP (Produto Mínimo Viável) é criar um sistema **totalmente funcional** que gera sinais de entrada e saída, rastreia o resultado de cada operação individualmente e notifica no Telegram. O foco é na **validação da lógica central** e no fluxo de dados ponta a ponta, sem as camadas de qualificação (MTF) e relatórios agregados, que serão adicionadas nos Tiers 2 e 3.

Ao final desta fase, teremos um sistema que já pode ser usado para operar e coletar dados de performance, provando a viabilidade da estratégia.

---

## 1. Pine Script (v1.0)

O script inicial será focado na mecânica de sinais e na comunicação com o n8n.

### 1.1. Entradas do Usuário (Inputs)

```pinescript
// =================== INPUTS ===================
entry_len = input.int(20, "Período Canal de Entrada", minval=1)
exit_len = input.int(10, "Período Canal de Saída", minval=1)
show_channels = input.bool(true, "Mostrar Canais no Gráfico")
```

### 1.2. Lógica de Canais e Sinais

- **Canais:**
  - `entry_high = ta.highest(high, entry_len)[1]`
  - `entry_low = ta.lowest(low, entry_len)[1]`
  - `exit_high = ta.highest(high, exit_len)[1]`
  - `exit_low = ta.lowest(low, exit_len)[1]`

- **Sinais de Rompimento:**
  - `long_entry_signal = close > entry_high`
  - `short_entry_signal = close < entry_low`
  - `long_exit_signal = close < exit_low`
  - `short_exit_signal = close > exit_high`

### 1.3. Gestão de Posição e `signal_id`

Esta é a parte mais crítica do MVP. Usaremos variáveis `var` para manter o estado da posição e o `signal_id`.

```pinescript
// =================== STATE MANAGEMENT ===================
var bool in_long_position = false
var bool in_short_position = false
var string signal_id = na

// Gerar ID único para o sinal
generate_signal_id() =>
    str.tostring(syminfo.ticker) + "_" + timeframe.period + "_" + str.tostring(time_utc)

// Lógica de Entrada LONG
if long_entry_signal and not in_long_position and not in_short_position
    in_long_position := true
    signal_id := generate_signal_id()
    // Disparar alerta de LONG_ENTRY com o signal_id

// Lógica de Saída LONG
if long_exit_signal and in_long_position
    in_long_position := false
    // Disparar alerta de LONG_EXIT com o MESMO signal_id
    signal_id := na // Resetar ID

// Lógica de Entrada SHORT (similar)
if short_entry_signal and not in_short_position and not in_long_position
    in_short_position := true
    signal_id := generate_signal_id()
    // Disparar alerta de SHORT_ENTRY com o signal_id

// Lógica de Saída SHORT (similar)
if short_exit_signal and in_short_position
    in_short_position := false
    // Disparar alerta de SHORT_EXIT com o MESMO signal_id
    signal_id := na // Resetar ID
```

### 1.4. Webhook JSON (Simplificado)

O `alert()` no TradingView será configurado para enviar a seguinte estrutura JSON. Cada alerta terá uma mensagem específica.

**Alerta de `LONG_ENTRY`:**
```json
{
  "action": "PES_SIGNAL",
  "signal_id": "{{strategy.order.comment}}",
  "symbol": "{{ticker}}",
  "timeframe": "{{interval}}",
  "type": "LONG_ENTRY",
  "price": {{close}}
}
```
*Nota: Usaremos o campo `strategy.order.comment` para passar o `signal_id` para o alerta.*

**Alerta de `LONG_EXIT`:**
```json
{
  "action": "PES_SIGNAL",
  "signal_id": "{{strategy.order.comment}}",
  "symbol": "{{ticker}}",
  "timeframe": "{{interval}}",
  "type": "LONG_EXIT",
  "price": {{close}}
}
```

### 1.5. Visualização no Gráfico

- Plotar os canais de entrada e saída se `show_channels == true`.
- Plotar setas simples para cima (`shape.triangleup`) em `long_entry_signal` e para baixo (`shape.triangledown`) em `short_entry_signal`.
- Plotar cruzes (`shape.cross`) para os sinais de saída.

---

## 2. Airtable (MVP)

A estrutura inicial será a mais simples possível para validar o fluxo.

### Tabela: `Trades`

| Campo (Field) | Tipo (Type) | Descrição |
|---|---|---|
| `signal_id` | `Single line text` | **Chave Primária.** ID único vindo do Pine Script. |
| `status` | `Single select` | `OPEN`, `CLOSED`. |
| `symbol` | `Single line text` | O par de moedas (ex: "BTCUSDT"). |
| `timeframe` | `Single select` | O timeframe do sinal (ex: "15"). |
| `direction` | `Single select` | `LONG` ou `SHORT`. |
| `entry_price` | `Number` | Preço de entrada. |
| `exit_price` | `Number` | Preço de saída. |
| `entry_time_utc` | `Date` (com time) | Timestamp da entrada. |
| `exit_time_utc` | `Date` (com time) | Timestamp da saída. |
| `result_percent` | `Percent` | **Fórmula:** `IF({direction} = 'LONG', ({exit_price} - {entry_price}) / {entry_price}, ({entry_price} - {exit_price}) / {entry_price})`. |

*Nota: Campos como `duration`, `quality`, `mtf_trend` e as tabelas de resumo serão adicionados nos Tiers 2 e 3.*

---

## 3. n8n (MVP)

Um único workflow para processar os sinais.

### Workflow: `[PES] Trade Processor (v1)`

- **Gatilho:** `Webhook` - URL pública para receber os POST requests do TradingView.

- **Nó 1: `Switch` (Analisar `type`)**
  - Rota 1: `body.type` contém `ENTRY` (`LONG_ENTRY` ou `SHORT_ENTRY`).
  - Rota 2: `body.type` contém `EXIT` (`LONG_EXIT` ou `SHORT_EXIT`).

- **Lógica da Rota 1 (ENTRY):**
  1.  **`Airtable Node (Create)`:**
      - **Operação:** `Create`
      - **Tabela:** `Trades`
      - **Mapeamento de Campos:**
        - `signal_id` ← `body.signal_id`
        - `status` ← `OPEN`
        - `symbol` ← `body.symbol`
        - `timeframe` ← `body.timeframe`
        - `direction` ← (Extrair "LONG" ou "SHORT" do `body.type`)
        - `entry_price` ← `body.price`
        - `entry_time_utc` ← (Timestamp atual do n8n)
  2.  **`Telegram Node (Send Message)`:**
      - Enviar mensagem formatada de **NOVA ENTRADA**.
      - Exemplo: `"🟢 PES LONG ENTRY\n\nAtivo: {{body.symbol}}\nTimeframe: {{body.timeframe}}\nPreço Entrada: {{body.price}}"`

- **Lógica da Rota 2 (EXIT):**
  1.  **`Airtable Node (Find)`:**
      - **Operação:** `Find`
      - **Tabela:** `Trades`
      - **Campo de Busca:** `signal_id`
      - **Valor de Busca:** `body.signal_id`
      - **Filtro Adicional:** `status = 'OPEN'` (para garantir que estamos fechando um trade aberto).
  2.  **`IF Node` (Verificar se encontrou o trade)**
      - Se o nó anterior retornou 1 resultado, continuar.
      - Se não, parar (evita erros).
  3.  **`Airtable Node (Update)`:**
      - **Operação:** `Update`
      - **Tabela:** `Trades`
      - **Record ID:** (ID do registro encontrado no passo 1)
      - **Mapeamento de Campos:**
        - `status` ← `CLOSED`
        - `exit_price` ← `body.price`
        - `exit_time_utc` ← (Timestamp atual do n8n)
  4.  **`Telegram Node (Send Message)`:**
      - **Buscar dados do Airtable** (preço de entrada) para calcular o resultado na mensagem.
      - Enviar mensagem formatada de **TRADE FECHADO** com o resultado.
      - Exemplo: `"🔴 PES LONG EXIT\n\nAtivo: {{body.symbol}}\nEntrada: {{entry_price_from_airtable}}\nSaída: {{body.price}}\n\nResultado: {{calculo_do_resultado}}%"`

---

## 4. Entregáveis do Tier 1

1.  **Código `pes_v1.0.pine`** pronto para ser copiado e colado no TradingView.
2.  **Template da Base Airtable** com a tabela `Trades` e seus campos configurados.
3.  **JSON do Workflow `[PES] Trade Processor (v1)`** para ser importado diretamente no n8n.
4.  **Instruções claras** de como conectar as 3 partes (configurar alertas no TradingView, obter API keys do Airtable e Telegram, e ativar o workflow no n8n).
