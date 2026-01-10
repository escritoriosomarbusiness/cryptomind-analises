# ⚡ Guia Rápido: Adicionar Timeframes (10 Minutos)

## 🎯 Objetivo
Adicionar opção de escolher timeframes (5min, 15min, 1h, 4h) no bot Telegram.

---

## 📋 PASSO 1: Airtable (2 minutos)

1. Acesse: https://airtable.com/appTIDQW6MXCYntnW/Preferencias

2. Clique em **"+"** (adicionar campo)

3. Configure:
   - Nome: `timeframe_preferido`
   - Tipo: **Single select**
   - Opções: `5min`, `15min`, `1h`, `4h`
   - Padrão: `1h`

4. **Salve**

✅ **Airtable pronto!**

---

## 📋 PASSO 2: Atualizar Menu Config (2 minutos)

1. Acesse: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. Duplo-clique no nó **"Enviar Menu Config"**

3. Localize o campo `reply_markup` → `inline_keyboard`

4. **Adicione** esta linha após os botões Moedas e USDT:

```json
[
  {
    "text": "🕒 Timeframe",
    "callback_data": "config_timeframe"
  }
]
```

**Resultado final:**
```json
"inline_keyboard": [
  [
    {"text": "💰 Moedas", "callback_data": "config_moedas"},
    {"text": "💵 USDT", "callback_data": "config_usdt"}
  ],
  [
    {"text": "🕒 Timeframe", "callback_data": "config_timeframe"}
  ]
]
```

5. **Salve** o nó

✅ **Menu atualizado!**

---

## 📋 PASSO 3: Criar Nó "Mostrar Menu Timeframes" (3 minutos)

1. No canvas, clique em **"+"** para adicionar nó

2. Selecione **"HTTP Request"**

3. Configure:
   - **Nome:** `Mostrar Menu Timeframes`
   - **Method:** POST
   - **URL:** `https://api.telegram.org/bot8437212177:AAEsm0d-ARdcj8zDGDqdpjeaSoQgsY-Byqc/sendMessage`
   - **Body Content Type:** JSON

4. **Body (copie e cole):**

```json
{
  "chat_id": "={{ $json.callback_query.from.id }}",
  "text": "🕒 Escolha o timeframe para receber alertas:",
  "reply_markup": {
    "inline_keyboard": [
      [
        {"text": "⚡ 5 minutos", "callback_data": "set_timeframe_5min"},
        {"text": "📊 15 minutos", "callback_data": "set_timeframe_15min"}
      ],
      [
        {"text": "🕐 1 hora", "callback_data": "set_timeframe_1h"},
        {"text": "🕓 4 horas", "callback_data": "set_timeframe_4h"}
      ]
    ]
  }
}
```

5. **Salve** o nó

✅ **Nó criado!**

---

## 📋 PASSO 4: Atualizar Switch Callback (2 minutos)

1. Duplo-clique no nó **"Switch Callback"**

2. Clique na aba **"JSON"**

3. Localize a seção `"rules": { "values": [ ... ] }`

4. **Adicione** estas 2 regras no final do array `values`:

```json
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "timeframe",
        "leftValue": "={{ $json.callback_query.data }}",
        "rightValue": "config_timeframe",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ],
    "combinator": "and"
  },
  "renameOutput": false
},
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "set_timeframe",
        "leftValue": "={{ $json.callback_query.data }}",
        "rightValue": "set_timeframe_",
        "operator": {
          "type": "string",
          "operation": "startsWith"
        }
      }
    ],
    "combinator": "and"
  },
  "renameOutput": false
}
```

5. **Salve** o nó

✅ **Switch atualizado! Agora tem 6 regras.**

---

## 📋 PASSO 5: Conectar Nós (1 minuto)

1. Localize o nó **"Switch Callback"**

2. Você verá agora **6 saídas** (0, 1, 2, 3, 4, 5)

3. **Conecte:**
   - **Saída 4** → **"Mostrar Menu Timeframes"** (nó que você criou)
   - **Saída 5** → **"Buscar Usuário Callback"** (nó existente)

✅ **Conexões feitas!**

---

## 📋 PASSO 6: Atualizar Lógica de Salvamento (2 minutos)

### 6.1: Atualizar "Preparar Update"

1. Duplo-clique no nó **"Preparar Update"**

2. Se for nó **Code/Function**, adicione este código:

```javascript
const data = $json.callback_query.data;
const recordId = $json.records[0].id;

// Timeframe
if (data.startsWith('set_timeframe_')) {
  const timeframe = data.replace('set_timeframe_', '');
  return {
    fields: { timeframe_preferido: timeframe },
    recordId: recordId,
    mensagem: `✅ Timeframe atualizado para ${timeframe}`
  };
}

// Moeda (código existente)
if (data.startsWith('set_moeda_')) {
  const moeda = data.replace('set_moeda_', '');
  return {
    fields: { moeda_preferida: moeda },
    recordId: recordId,
    mensagem: `✅ Moeda atualizada para ${moeda}`
  };
}

// USDT (código existente)
if (data.startsWith('set_usdt_')) {
  const usdt = data.replace('set_usdt_', '');
  return {
    fields: { usdt_preferido: usdt },
    recordId: recordId,
    mensagem: `✅ Valor USDT atualizado para ${usdt}`
  };
}

return $json;
```

3. **Salve**

### 6.2: Atualizar "Formatar Status"

1. Duplo-clique no nó **"Formatar Status"**

2. Adicione linha para timeframe:

```javascript
const record = $json.records[0].fields;
const moeda = record.moeda_preferida || 'Não definida';
const usdt = record.usdt_preferido || 'Não definido';
const timeframe = record.timeframe_preferido || 'Não definido';

return {
  chat_id: record.chat_id,
  text: `📊 *Suas Preferências*\n\n💰 *Moeda:* ${moeda}\n💵 *USDT:* ${usdt}\n🕒 *Timeframe:* ${timeframe}`,
  parse_mode: 'Markdown'
};
```

3. **Salve**

✅ **Lógica atualizada!**

---

## 📋 PASSO 7: Salvar Workflow

1. Clique no botão **"Save"** no topo da página

2. Aguarde confirmação

✅ **Workflow salvo!**

---

## 🧪 TESTE RÁPIDO

1. Abra o bot Telegram

2. Envie: **`/config`**

3. Verifique se aparece botão **"🕒 Timeframe"**

4. Clique em **"🕒 Timeframe"**

5. Verifique se aparece submenu: **[5min] [15min] [1h] [4h]**

6. Clique em **"1h"**

7. Verifique se recebe: **"✅ Timeframe atualizado para 1h"**

8. Envie: **`/status`**

9. Verifique se aparece: **"🕒 Timeframe: 1h"**

✅ **Se todos os testes passarem = IMPLEMENTAÇÃO COMPLETA!**

---

## 📊 Resumo Visual

```
Menu Config
    ↓
[Moedas] [USDT] [Timeframe] ← Novo botão
    ↓
Clica "Timeframe"
    ↓
Switch Callback (regra 4)
    ↓
Mostrar Menu Timeframes ← Novo nó
    ↓
[5min] [15min] [1h] [4h]
    ↓
Clica "1h"
    ↓
Switch Callback (regra 5)
    ↓
Buscar Usuário Callback
    ↓
Preparar Update (adiciona timeframe)
    ↓
Atualizar Preferência (Airtable)
    ↓
Confirmar: "✅ Timeframe atualizado para 1h"
```

---

## ✅ Checklist Final

- [ ] Airtable: Campo `timeframe_preferido` criado
- [ ] Menu Config: Botão "Timeframe" adicionado
- [ ] Nó "Mostrar Menu Timeframes" criado
- [ ] Switch Callback: 2 regras adicionadas (total 6)
- [ ] Conexões: Saídas 4 e 5 conectadas
- [ ] Preparar Update: Lógica de timeframe adicionada
- [ ] Formatar Status: Exibição de timeframe adicionada
- [ ] Workflow salvo
- [ ] Testes realizados e aprovados

---

**Tempo total: ~10 minutos**  
**Dificuldade: Média**  
**Resultado: Funcionalidade completa de timeframes** ✅
