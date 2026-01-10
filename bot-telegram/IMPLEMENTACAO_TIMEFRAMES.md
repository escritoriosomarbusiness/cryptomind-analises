# 🕒 Implementação de Timeframes - Bot Telegram

## 📋 Visão Geral

Adicionar funcionalidade para usuários escolherem os timeframes (tempos gráficos) para receber alertas:
- **5min** - 5 minutos
- **15min** - 15 minutos  
- **1h** - 1 hora
- **4h** - 4 horas

---

## 🎯 Arquitetura da Solução

### Fluxo do Usuário
```
1. Usuário: /config
2. Bot: Menu com botões [Moedas] [USDT] [Timeframe]
3. Usuário: Clica em [Timeframe]
4. Bot: Submenu [5min] [15min] [1h] [4h]
5. Usuário: Clica em [1h]
6. Bot: "✅ Timeframe atualizado para 1h"
7. Airtable: Campo timeframe_preferido = "1h"
```

### Componentes Necessários

1. **Airtable:** Adicionar campo `timeframe_preferido`
2. **Menu Config:** Adicionar botão "Timeframe"
3. **Switch Callback:** Adicionar 2 novas regras
4. **Nó Mostrar Menu Timeframes:** Exibir opções
5. **Nó Atualizar Timeframe:** Salvar no Airtable

---

## 📦 PARTE 1: Atualizar Airtable

### Passo 1.1: Adicionar Campo

1. Acesse: https://airtable.com/appTIDQW6MXCYntnW/Preferencias

2. Clique em **"+"** para adicionar novo campo

3. Configure:
   - **Nome:** `timeframe_preferido`
   - **Tipo:** Single select
   - **Opções:**
     - `5min`
     - `15min`
     - `1h`
     - `4h`
   - **Valor padrão:** `1h`

4. Salve o campo

### Passo 1.2: Atualizar Registros Existentes

Execute este comando para definir valor padrão para usuários existentes:

```
Valor padrão: 1h
```

---

## 📦 PARTE 2: Atualizar Menu de Configuração

### Passo 2.1: Modificar Nó "Enviar Menu Config"

1. Acesse o workflow: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. Duplo-clique no nó **"Enviar Menu Config"**

3. Localize o campo `reply_markup` no JSON

4. Substitua por:

```json
{
  "chat_id": "={{ $json.callback_query.from.id }}",
  "text": "⚙️ Configurações\n\nEscolha o que deseja configurar:",
  "reply_markup": {
    "inline_keyboard": [
      [
        {
          "text": "💰 Moedas",
          "callback_data": "config_moedas"
        },
        {
          "text": "💵 USDT",
          "callback_data": "config_usdt"
        }
      ],
      [
        {
          "text": "🕒 Timeframe",
          "callback_data": "config_timeframe"
        }
      ]
    ]
  }
}
```

5. Salve o nó

---

## 📦 PARTE 3: Criar Nó "Mostrar Menu Timeframes"

### Passo 3.1: Adicionar Novo Nó HTTP Request

1. No canvas do workflow, clique em **"+"** para adicionar nó

2. Selecione **"HTTP Request"**

3. Configure:
   - **Nome:** `Mostrar Menu Timeframes`
   - **Method:** POST
   - **URL:** `https://api.telegram.org/bot8437212177:AAEsm0d-ARdcj8zDGDqdpjeaSoQgsY-Byqc/sendMessage`
   - **Authentication:** None
   - **Body Content Type:** JSON

4. **Body (JSON):**

```json
{
  "chat_id": "={{ $json.callback_query.from.id }}",
  "text": "🕒 Escolha o timeframe para alertas:",
  "reply_markup": {
    "inline_keyboard": [
      [
        {
          "text": "5 minutos",
          "callback_data": "set_timeframe_5min"
        },
        {
          "text": "15 minutos",
          "callback_data": "set_timeframe_15min"
        }
      ],
      [
        {
          "text": "1 hora",
          "callback_data": "set_timeframe_1h"
        },
        {
          "text": "4 horas",
          "callback_data": "set_timeframe_4h"
        }
      ]
    ]
  }
}
```

5. Salve o nó

---

## 📦 PARTE 4: Conectar Switch Callback

### Passo 4.1: Adicionar Conexão

1. Localize o nó **"Switch Callback"**

2. Conecte a **saída 4** (nova regra `config_timeframe`) ao nó **"Mostrar Menu Timeframes"**

3. Conecte a **saída 5** (nova regra `set_timeframe_*`) ao nó **"Buscar Usuário Callback"** (mesmo destino das moedas)

---

## 📦 PARTE 5: Atualizar Lógica de Salvamento

### Passo 5.1: Modificar Nó "Preparar Update"

1. Duplo-clique no nó **"Preparar Update"**

2. Adicione lógica para extrair timeframe:

```javascript
// Código existente
const data = $json.callback_query.data;

// Adicionar lógica de timeframe
if (data.startsWith('set_timeframe_')) {
  const timeframe = data.replace('set_timeframe_', '');
  return {
    fields: {
      timeframe_preferido: timeframe
    },
    recordId: $json.records[0].id,
    timeframe: timeframe
  };
}

// Resto do código existente para moedas e USDT
```

3. Salve o nó

### Passo 5.2: Modificar Nó "Confirmar Atualização"

1. Duplo-clique no nó **"Confirmar Atualização"**

2. Adicione lógica para mensagem de timeframe:

```json
{
  "chat_id": "={{ $json.callback_query.from.id }}",
  "text": "={{ $json.timeframe ? '✅ Timeframe atualizado para ' + $json.timeframe : '✅ Configuração atualizada!' }}"
}
```

3. Salve o nó

---

## 📦 PARTE 6: Atualizar Comando /status

### Passo 6.1: Modificar Nó "Formatar Status"

1. Duplo-clique no nó **"Formatar Status"**

2. Adicione timeframe na mensagem:

```javascript
const moeda = $json.records[0].fields.moeda_preferida || 'Não definida';
const usdt = $json.records[0].fields.usdt_preferido || 'Não definido';
const timeframe = $json.records[0].fields.timeframe_preferido || 'Não definido';

return {
  text: `📊 Suas Preferências:\n\n💰 Moeda: ${moeda}\n💵 USDT: ${usdt}\n🕒 Timeframe: ${timeframe}`
};
```

3. Salve o nó

---

## 📦 PARTE 7: Importar Workflow Atualizado (Alternativa Rápida)

### Opção A: Importação Automática

1. Acesse: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. Menu **⋮** → **"Importar de arquivo..."**

3. Selecione: **`workflow_v3_com_timeframes.json`**

4. **IMPORTANTE:** Após importar, você ainda precisa:
   - Criar manualmente o nó "Mostrar Menu Timeframes"
   - Atualizar o nó "Enviar Menu Config"
   - Conectar as novas saídas do Switch Callback

### Opção B: Implementação Manual (Recomendado)

Siga os passos 1-6 acima para implementação completa e controlada.

---

## ✅ Checklist de Implementação

- [ ] **Airtable:** Campo `timeframe_preferido` criado
- [ ] **Menu Config:** Botão "Timeframe" adicionado
- [ ] **Switch Callback:** 2 novas regras adicionadas (config_timeframe, set_timeframe_*)
- [ ] **Nó Mostrar Menu Timeframes:** Criado e configurado
- [ ] **Conexões:** Saídas 4 e 5 do Switch Callback conectadas
- [ ] **Preparar Update:** Lógica de timeframe adicionada
- [ ] **Confirmar Atualização:** Mensagem de timeframe adicionada
- [ ] **Formatar Status:** Exibição de timeframe adicionada
- [ ] **Workflow:** Salvo no n8n

---

## 🧪 Testes de Validação

### Teste 1: Menu Timeframe
```
Ação: /config → Clicar "Timeframe"
Esperado: Submenu [5min] [15min] [1h] [4h]
Status: ⬜
```

### Teste 2: Seleção de Timeframe
```
Ação: Clicar em "1h"
Esperado: "✅ Timeframe atualizado para 1h"
Status: ⬜
```

### Teste 3: Persistência no Airtable
```
Ação: Verificar Airtable
Esperado: Campo timeframe_preferido = "1h"
Status: ⬜
```

### Teste 4: Exibição no Status
```
Ação: /status
Esperado: Mensagem inclui "🕒 Timeframe: 1h"
Status: ⬜
```

---

## 📊 Estrutura de Dados

### Airtable - Tabela Preferencias

| Campo | Tipo | Valores | Padrão |
|-------|------|---------|--------|
| chat_id | Number | - | - |
| username | Text | - | - |
| moeda_preferida | Single select | BTC, ETH, etc. | BTC |
| usdt_preferido | Single select | 100, 500, 1000 | 500 |
| **timeframe_preferido** | **Single select** | **5min, 15min, 1h, 4h** | **1h** |

### Callback Data

| Ação | Callback Data | Destino |
|------|---------------|---------|
| Clicar "Timeframe" | `config_timeframe` | Mostrar Menu Timeframes |
| Clicar "5min" | `set_timeframe_5min` | Buscar Usuário → Atualizar |
| Clicar "15min" | `set_timeframe_15min` | Buscar Usuário → Atualizar |
| Clicar "1h" | `set_timeframe_1h` | Buscar Usuário → Atualizar |
| Clicar "4h" | `set_timeframe_4h` | Buscar Usuário → Atualizar |

---

## 🚀 Implementação Rápida (10 Minutos)

1. **Airtable (2 min):** Adicionar campo `timeframe_preferido`
2. **Menu Config (2 min):** Adicionar botão "Timeframe"
3. **Novo Nó (3 min):** Criar "Mostrar Menu Timeframes"
4. **Conexões (1 min):** Conectar saídas do Switch Callback
5. **Lógica (2 min):** Atualizar Preparar Update e Confirmar Atualização

**Total: ~10 minutos de implementação**

---

## 📞 Suporte

**Workflow ID:** `7V9SZdSeSfZELZ3l`  
**Airtable Base:** `appTIDQW6MXCYntnW`  
**Tabela:** `Preferencias`  

---

**Status:** ✅ Especificação completa pronta para implementação
