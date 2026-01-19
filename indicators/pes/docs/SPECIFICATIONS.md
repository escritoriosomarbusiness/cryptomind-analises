# ⚙️ Especificações Técnicas - PES v2.0

---

Este documento detalha a lógica interna, os cálculos e as regras do indicador **Price Expansion System (PES) v2.0**.

## 1. Lógica Central: Donchian Channels com Canais Duplos

O indicador utiliza dois conjuntos de Donchian Channels para operar rompimentos de preço.

*   **Canal de Entrada (Lento):**
    *   **Período:** `input.int(20, "Período Canal de Entrada")`
    *   **Canal Superior (Long Entry):** `ta.highest(high, 20)[1]`
    *   **Canal Inferior (Short Entry):** `ta.lowest(low, 20)[1]`

*   **Canal de Saída (Rápido):**
    *   **Período:** `input.int(10, "Período Canal de Saída")`
    *   **Canal Superior (Short Exit):** `ta.highest(high, 10)[1]`
    *   **Canal Inferior (Long Exit):** `ta.lowest(low, 10)[1]`

### Regras de Sinal:

*   **`long_entry_signal`:** `close > ta.highest(high, 20)[1]`
*   **`short_entry_signal`:** `close < ta.lowest(low, 20)[1]`
*   **`long_exit_signal`:** `close < ta.lowest(low, 10)[1]`
*   **`short_exit_signal`:** `close > ta.highest(high, 10)[1]`

---

## 2. Análise Multi-Timeframe (MTF) Orientativa

A análise MTF serve para qualificar o sinal, não para filtrá-lo. A lógica é baseada nos indicadores DNP e TRS.

### Mapeamento de Timeframe (Fractal Superior):

| Timeframe de Operação | Timeframe de Análise (MTF) |
|-----------------------|----------------------------|
| 1m                    | 15m                        |
| 5m                    | 60m (H1)                   |
| 15m                   | 240m (H4)                  |
| 60m (H1)              | D (Daily)                  |
| 240m (H4)             | W (Weekly)                 |
| D (Daily)             | M (Monthly)                |

### Lógica de Tendência no Fractal Superior:

Utiliza duas EMAs (Médias Móveis Exponenciais) no timeframe de análise.

*   **EMA Lenta:** `ta.ema(close, 233)`
*   **EMA Rápida:** `ta.ema(close, 55)`

**Condições de Tendência:**

*   **Tendência de ALTA (`htf_trendUp`):**
    1.  `EMA 55 > EMA 233`
    2.  `EMA 55 > EMA 55[1]` (EMA 55 está subindo)
    3.  `close > EMA 55` (Preço está acima da EMA 55)

*   **Tendência de BAIXA (`htf_trendDown`):**
    1.  `EMA 55 < EMA 233`
    2.  `EMA 55 < EMA 55[1]` (EMA 55 está caindo)
    3.  `close < EMA 55` (Preço está abaixo da EMA 55)

*   **Tendência NEUTRA (`htf_trendNeutral`):**
    *   Qualquer cenário que não se encaixe nas condições de alta ou baixa.

### Classificação de Qualidade do Sinal:

| Tipo de Sinal   | Tendência MTF | Qualidade do Sinal |
|-----------------|---------------|--------------------|
| **Long Entry**  | ALTA          | 🌟 **PREMIUM**     |
| **Long Entry**  | NEUTRA        | ⚠️ **CAUTELA**     |
| **Long Entry**  | BAIXA         | 🚫 **CONTRA**      |
| **Short Entry** | BAIXA         | 🌟 **PREMIUM**     |
| **Short Entry** | NEUTRA        | ⚠️ **CAUTELA**     |
| **Short Entry** | ALTA          | 🚫 **CONTRA**      |

---

## 3. Filtros de Qualidade e Gestão

### Filtro de Fechamento no Terço do Candle:

Para um sinal de entrada ser válido, o candle de rompimento deve demonstrar força.

*   **Cálculo do Terço:**
    *   `candle_range = high - low`
    *   `upper_third = high - (candle_range / 3)`
    *   `lower_third = low + (candle_range / 3)`

*   **Condições de Validação:**
    *   **Long Entry:** `close >= upper_third`
    *   **Short Entry:** `close <= lower_third`

### Gestão de Posição:

Evita sinais redundantes.

*   Não gerar `long_entry_signal` se já estiver em uma posição `long`.
*   Não gerar `short_entry_signal` se já estiver em uma posição `short`.

### Distância Mínima Entre Sinais:

*   Um novo sinal de entrada (long ou short) só pode ser gerado após **5 candles** do sinal anterior para evitar ruído.

---

## 4. Webhook Unificado para Automação (JSON)

Todos os sinais (entrada e saída) enviam uma mensagem via `alert()` para um webhook, contendo um JSON estruturado.

### Geração do `signal_id`:

Um ID único é gerado no momento da **ENTRADA** e reutilizado na **SAÍDA** para permitir o rastreamento.

*   **Formato:** `{ticker}_{timeframe}_{timestamp_entrada}`
*   **Exemplo:** `BTCUSDT_15_1737301200`

### Estrutura do JSON:

```json
{
  "action": "PES_SIGNAL",
  "signal_id": "{string}", // ID único da operação
  "symbol": "{string}", // Ex: "BTCUSDT"
  "timeframe": "{string}", // Ex: "15"
  "type": "{string}", // "LONG_ENTRY", "LONG_EXIT", "SHORT_ENTRY", "SHORT_EXIT"
  "price": {float}, // Preço do evento (close do candle)
  "entry_channel_price": {float}, // Preço do canal de entrada no momento
  "exit_channel_price": {float}, // Preço do canal de saída no momento
  "quality": "{string}", // "PREMIUM", "CAUTELA", "CONTRA" (apenas para ENTRADA)
  "mtf_trend": "{string}", // "ALTA", "BAIXA", "NEUTRO" (apenas para ENTRADA)
  "timestamp_utc": "{string}" // Timestamp UTC do evento (YYYY-MM-DDTHH:mm:ssZ)
}
```

---

## 5. Visualização no Gráfico

### Labels de Sinais:

As labels são posicionadas dinamicamente para evitar sobreposição, usando o ATR (Average True Range) como referência de offset.

*   **Long Entry:** Label abaixo do `low` do candle (`low - ATR * 0.5`).
*   **Short Entry:** Label acima do `high` do candle (`high + ATR * 0.5`).
*   **Long Exit:** Label acima do `high` do candle (`high + ATR`).
*   **Short Exit:** Label abaixo do `low` do candle (`low - ATR`).

### Cores das Labels de Entrada:

*   **Verde:** Sinal PREMIUM
*   **Amarelo:** Sinal de CAUTELA
*   **Vermelho:** Sinal CONTRA

### Dashboard:

Uma tabela no canto do gráfico exibirá:

*   **Tendência MTF:** `ALTA`, `BAIXA` ou `NEUTRA`.
*   **Qualidade do Último Sinal:** `PREMIUM`, `CAUTELA` ou `CONTRA`.
*   **Status da Posição:** `Em Posição LONG`, `Em Posição SHORT` ou `Aguardando Sinal`.
