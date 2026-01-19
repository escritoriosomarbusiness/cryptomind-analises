# 🤖 n8n - Configuração do Workflow do MVP (Tier 1)

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

## 🎯 Objetivo

Criar um workflow no n8n que atue como o cérebro do MVP do **PES (Price Expansion System)**. Este workflow será responsável por receber os sinais do TradingView, processá-los, registrar no Airtable e notificar no Telegram.

---

## 1. Pré-requisitos: Credenciais

Antes de começar, você precisará de duas credenciais configuradas no n8n:

1.  **Airtable API:**
    *   Vá em `Credentials` > `New`.
    *   Procure por `Airtable API`.
    *   Cole a `API Key` que você obteve do Airtable.
    *   Salve com um nome como `Airtable Crypto`.

2.  **Telegram Bot API:**
    *   Vá em `Credentials` > `New`.
    *   Procure por `Telegram Bot API`.
    *   Converse com o `BotFather` no Telegram para criar um novo bot e obter o `Access Token`.
    *   Cole o token no n8n.
    *   Salve com um nome como `Telegram Bot Principal`.
    *   Você também precisará do `Chat ID` do seu canal ou grupo do Telegram. Você pode obtê-lo com bots como o `@userinfobot`.

---

## 2. Visão Geral do Workflow

O workflow será nomeado `[PES] Trade Processor (v1)` e terá a seguinte estrutura lógica:

```
+-----------+
| Webhook   | Recebe o sinal do TradingView
+-----+-----+
      |
+-----v-----+
| Switch    | É um sinal de ENTRADA ou SAÍDA?
+-----+-----+
      |
      +------> [ROTA DE ENTRADA]
      |
      +------> [ROTA DE SAÍDA]
```

---

## 3. Detalhamento dos Nós

### Nó 1: `Webhook` (Gatilho)

*   **Tipo:** `Webhook`.
*   **Configuração:**
    *   Ao criar, o n8n gerará uma URL de teste e uma URL de produção.
    *   Use a **URL de Produção** para configurar o campo `Webhook URL` no alerta do TradingView.
    *   **HTTP Method:** `POST`.

### Nó 2: `Switch`

*   **Tipo:** `Switch`.
*   **Configuração:**
    *   **Mode:** `Rules`.
    *   **Routing Rules:**
        *   **Rule 1 (Entrada):**
            *   **Name:** `Entrada`
            *   **Conditions:** `{{ $json.body.type }}` `String` `Contains` `ENTRY`
        *   **Rule 2 (Saída):**
            *   **Name:** `Saída`
            *   **Conditions:** `{{ $json.body.type }}` `String` `Contains` `EXIT`

--- 

### Rota de Entrada (Conectada à saída "Entrada" do Switch)

#### Nó 3.1: `Set` (Preparar Dados)

*   **Tipo:** `Set`.
*   **Objetivo:** Extrair a direção (LONG/SHORT) do tipo de sinal.
*   **Configuração:**
    *   **Keep Only Set:** `true`
    *   **Values to Set:**
        *   **Name:** `direction`
        *   **Value:** `{{ $json.body.type.includes("LONG") ? "LONG" : "SHORT" }}`

#### Nó 3.2: `Airtable` (Criar Registro)

*   **Tipo:** `Airtable`.
*   **Configuração:**
    *   **Authentication:** `Airtable API` (selecione a credencial que você criou).
    *   **Operation:** `Create`.
    *   **Base ID:** ID da sua base `[Crypto] PES Performance`.
    *   **Table ID:** `Trades`.
    *   **Fields:**
        *   `signal_id` ← `{{ $json.body.signal_id }}`
        *   `status` ← `OPEN`
        *   `symbol` ← `{{ $json.body.symbol }}`
        *   `timeframe` ← `{{ $json.body.timeframe }}`
        *   `direction` ← `{{ $json.direction }}` (do nó `Set` anterior)
        *   `entry_price` ← `{{ $json.body.price }}`
        *   `entry_time_utc` ← `{{ $now.toISO() }}`

#### Nó 3.3: `Telegram` (Notificar Entrada)

*   **Tipo:** `Telegram`.
*   **Configuração:**
    *   **Authentication:** `Telegram Bot API` (selecione a credencial).
    *   **Chat ID:** O ID do seu canal/grupo.
    *   **Text:**
        ```
        🟢 PES {{ $json.direction }} ENTRY
        
        Ativo: {{ $json.body.symbol }}
        Timeframe: {{ $json.body.timeframe }}min
        Preço Entrada: ${{ $json.body.price.toFixed(2) }}
        
        ID: {{ $json.body.signal_id }}
        ```
    *   **Outras Opções:** `Disable Notification: false`, `Parse Mode: Markdown`.

--- 

### Rota de Saída (Conectada à saída "Saída" do Switch)

#### Nó 4.1: `Airtable` (Buscar Trade Aberto)

*   **Tipo:** `Airtable`.
*   **Configuração:**
    *   **Authentication:** `Airtable API`.
    *   **Operation:** `Find`.
    *   **Base ID / Table ID:** `[Crypto] PES Performance` / `Trades`.
    *   **Search Field:** `signal_id`.
    *   **Search Value:** `{{ $json.body.signal_id }}`.
    *   **Additional Filter Formula:** `{status} = "OPEN"`.

#### Nó 4.2: `IF` (Verificar se Encontrou)

*   **Tipo:** `IF`.
*   **Objetivo:** Garantir que o workflow só continue se o trade foi encontrado no Airtable.
*   **Configuração:**
    *   **Condition:** `{{ $json.fields }}` `Is Not Empty`.

#### Nó 4.3: `Airtable` (Atualizar Trade)

*   **Conectado à saída `true` do nó `IF`**.
*   **Tipo:** `Airtable`.
*   **Configuração:**
    *   **Authentication:** `Airtable API`.
    *   **Operation:** `Update`.
    *   **Base ID / Table ID:** `[Crypto] PES Performance` / `Trades`.
    *   **Record ID:** `{{ $items("Buscar Trade Aberto")[0].id }}`.
    *   **Fields:**
        *   `status` ← `CLOSED`
        *   `exit_price` ← `{{ $json.body.price }}`
        *   `exit_time_utc` ← `{{ $now.toISO() }}`

#### Nó 4.4: `Set` (Calcular Resultado para Mensagem)

*   **Tipo:** `Set`.
*   **Objetivo:** Calcular o resultado em % para usar na mensagem do Telegram.
*   **Configuração:**
    *   **Keep Only Set:** `false` (para manter os dados dos nós anteriores).
    *   **Values to Set:**
        *   **Name:** `result_percent`
        *   **Value (Expression):**
            ```javascript
            const entryPrice = {{ $items("Buscar Trade Aberto")[0].json.fields.entry_price }};
            const exitPrice = {{ $json.body.price }};
            const direction = {{ $items("Buscar Trade Aberto")[0].json.fields.direction }};
            let result = 0;
            if (direction === 'LONG') {
              result = ((exitPrice - entryPrice) / entryPrice) * 100;
            } else {
              result = ((entryPrice - exitPrice) / entryPrice) * 100;
            }
            return result.toFixed(2);
            ```
        *   **Name:** `result_emoji`
        *   **Value:** `{{ $json.result_percent >= 0 ? "✅" : "❌" }}`

#### Nó 4.5: `Telegram` (Notificar Saída)

*   **Tipo:** `Telegram`.
*   **Configuração:**
    *   **Authentication:** `Telegram Bot API`.
    *   **Chat ID:** O ID do seu canal/grupo.
    *   **Text:**
        ```
        🔴 PES {{ $items("Buscar Trade Aberto")[0].json.fields.direction }} EXIT
        
        Ativo: {{ $json.body.symbol }}
        
        📈 Entrada: ${{ $items("Buscar Trade Aberto")[0].json.fields.entry_price.toFixed(2) }}
        📉 Saída: ${{ $json.body.price.toFixed(2) }}
        
        💰 Resultado: {{ $json.result_percent }}% {{ $json.result_emoji }}
        
        ID: {{ $json.body.signal_id }}
        ```

---

## 4. Importação do Workflow

Um arquivo JSON (`PES_MVP_Workflow.json`) será fornecido. Você pode simplesmente importá-lo para o n8n:

1.  Vá para a sua lista de workflows.
2.  Clique em `New` > `Import from File`.
3.  Selecione o arquivo JSON.
4.  O workflow será criado. Você só precisará **conectar as credenciais corretas** nos nós do Airtable e Telegram.
