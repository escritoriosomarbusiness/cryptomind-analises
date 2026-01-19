# 🤖 n8n - Workflow do Tier 2

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

## 🎯 Objetivo

Atualizar o workflow do n8n para processar os novos campos do **Tier 2** do PES, incluindo qualidade do sinal e tendência MTF.

---

## 📝 Mudanças no Workflow

### **Rota de Entrada (ENTRY)**

#### Nó 3.2: `Airtable` (Criar Registro) - ATUALIZADO

Adicione os seguintes campos ao mapeamento:

```
Fields:
  - signal_id ← {{ $json.body.signal_id }}
  - status ← OPEN
  - symbol ← {{ $json.body.symbol }}
  - timeframe ← {{ $json.body.timeframe }}
  - direction ← {{ $json.direction }}
  - entry_price ← {{ $json.body.price }}
  - entry_time_utc ← {{ $now.toISO() }}
  - quality ← {{ $json.body.quality }}              // NOVO
  - mtf_trend ← {{ $json.body.mtf_trend }}          // NOVO
  - entry_channel ← {{ $json.body.entry_channel }}  // NOVO
  - exit_channel ← {{ $json.body.exit_channel }}    // NOVO
```

#### Nó 3.3: `Telegram` (Notificar Entrada) - ATUALIZADO

Atualize a mensagem para incluir qualidade e tendência MTF:

```
🟢 PES {{ $json.direction }} ENTRY - {{ $json.body.quality }} {{ $json.body.quality == 'PREMIUM' ? '🌟' : $json.body.quality == 'CAUTELA' ? '⚠️' : '🚫' }}

Ativo: {{ $json.body.symbol }}
Timeframe: {{ $json.body.timeframe }}min
Preço Entrada: ${{ $json.body.price.toFixed(2) }}

📊 Canal Superior: ${{ $json.body.entry_channel.toFixed(2) }}
📊 Canal Inferior: ${{ $json.body.exit_channel.toFixed(2) }}

📈 Tendência Macro: {{ $json.body.mtf_trend }} {{ $json.body.mtf_trend == 'ALTA' ? '✅' : $json.body.mtf_trend == 'BAIXA' ? '❌' : '〰️' }}
🎯 Qualidade: {{ $json.body.quality }} {{ $json.body.quality == 'PREMIUM' ? '🌟' : $json.body.quality == 'CAUTELA' ? '⚠️' : '🚫' }}

{{ $json.body.quality == 'PREMIUM' ? '⚠️ Este é um sinal de alta qualidade, alinhado com a tendência macro!' : $json.body.quality == 'CAUTELA' ? '⚠️ Sinal em tendência neutra. Opere com gestão de risco reforçada.' : '⚠️ Sinal contra a tendência macro. Alto risco!' }}

ID: {{ $json.body.signal_id }}
```

---

### **Rota de Saída (EXIT)**

#### Nó 4.5: `Telegram` (Notificar Saída) - ATUALIZADO

Atualize a mensagem para incluir qualidade do setup:

```
🔴 PES {{ $items("Buscar Trade Aberto")[0].json.fields.direction }} EXIT

Ativo: {{ $json.body.symbol }}

📈 Entrada: ${{ $items("Buscar Trade Aberto")[0].json.fields.entry_price.toFixed(2) }}
📉 Saída: ${{ $json.body.price.toFixed(2) }}

💰 Resultado: {{ $json.result_percent }}% {{ $json.result_emoji }}

🎯 Qualidade do Setup: {{ $items("Buscar Trade Aberto")[0].json.fields.quality }} {{ $items("Buscar Trade Aberto")[0].json.fields.quality == 'PREMIUM' ? '🌟' : $items("Buscar Trade Aberto")[0].json.fields.quality == 'CAUTELA' ? '⚠️' : '🚫' }}
📊 Tendência Macro: {{ $items("Buscar Trade Aberto")[0].json.fields.mtf_trend }} {{ $items("Buscar Trade Aberto")[0].json.fields.mtf_trend == 'ALTA' ? '✅' : $items("Buscar Trade Aberto")[0].json.fields.mtf_trend == 'BAIXA' ? '❌' : '〰️' }}

ID: {{ $json.body.signal_id }}
```

---

## 📊 Exemplo de Webhook JSON (Tier 2)

### Entrada LONG:
```json
{
  "action": "PES_SIGNAL",
  "signal_id": "BTCUSDT_15_1737301200",
  "symbol": "BTCUSDT",
  "timeframe": "15",
  "type": "LONG_ENTRY",
  "price": 93161.0,
  "quality": "PREMIUM",
  "mtf_trend": "ALTA",
  "entry_channel": 93500.0,
  "exit_channel": 92500.0
}
```

### Saída LONG:
```json
{
  "action": "PES_SIGNAL",
  "signal_id": "BTCUSDT_15_1737301200",
  "symbol": "BTCUSDT",
  "timeframe": "15",
  "type": "LONG_EXIT",
  "price": 93850.0
}
```

---

## ✅ Workflow Atualizado

Com estas mudanças, o workflow do n8n está pronto para processar os dados enriquecidos do Tier 2, incluindo a classificação de qualidade dos sinais e a tendência MTF.
