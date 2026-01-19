_# Template: Workflow de Processamento de Pagamento (n8n)

**Gatilho:** Webhook do Mercado Pago

**Objetivo:** Processar um pagamento aprovado, registrar o assinante no Airtable, gerar um link de convite para o Telegram e notificar o cliente.

## Estrutura do Workflow

```json
{
  "name": "CryptoMind - Processamento de Pagamento",
  "nodes": [
    {
      "parameters": {},
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "path": "mercadopago-cryptomind",
        "httpMethod": "POST"
      },
      "name": "Webhook MP",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [450, 300],
      "webhookId": "..."
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "{{$json.body.action}}",
              "operation": "equal",
              "value2": "payment.updated"
            },
            {
              "value1": "{{$json.body.data.status}}",
              "operation": "equal",
              "value2": "approved"
            }
          ]
        }
      },
      "name": "Filtro: Pagamento Aprovado",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 300]
    },
    {
      "parameters": {
        "operation": "search",
        "baseId": "YOUR_BASE_ID",
        "tableId": "Assinantes",
        "filterByFormula": "({Email} = '{{$json.body.data.payer.email}}')"
      },
      "name": "Buscar Assinante Airtable",
      "type": "n8n-nodes-airtable.node",
      "typeVersion": 1,
      "position": [850, 200]
    },
    {
      "parameters": {
        "operation": "create",
        "baseId": "YOUR_BASE_ID",
        "tableId": "Assinantes",
        "fields": {
          "Nome": "{{$json.body.data.payer.first_name}} {{$json.body.data.payer.last_name}}",
          "Email": "{{$json.body.data.payer.email}}",
          "Plano": "{{$json.body.external_reference.split('-')[1]}}",
          "Status": "active",
          "Data_Inicio": "{{$now.toISODate()}}",
          "Valor_Pago": "{{$json.body.data.transaction_amount}}",
          "MP_Payment_ID": "{{$json.body.data.id}}"
        }
      },
      "name": "Criar Assinante Airtable",
      "type": "n8n-nodes-airtable.node",
      "typeVersion": 1,
      "position": [1050, 400]
    },
    {
      "parameters": {
        "chatId": "YOUR_CHANNEL_ID",
        "expireDate": "{{$now.plus({days: 1}).toSeconds()}}",
        "memberLimit": 1
      },
      "name": "Gerar Link Telegram",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [1250, 300]
    },
    {
      "parameters": {
        "to": "{{$node[\'Buscar Assinante Airtable\'].json.Email}}",
        "subject": "🎉 Bem-vindo ao CryptoMind Alerts!",
        "html": "..."
      },
      "name": "Enviar Email Boas-vindas",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 1,
      "position": [1450, 300]
    }
  ],
  "connections": {
    "Webhook MP": { "main": [ [ { "node": "Filtro: Pagamento Aprovado", "type": "main", "index": 0 } ] ] },
    "Filtro: Pagamento Aprovado": {
      "main": [
        [ { "node": "Buscar Assinante Airtable", "type": "main", "index": 0 } ]
      ]
    },
    "Buscar Assinante Airtable": {
      "main": [
        [ { "node": "Criar Assinante Airtable", "type": "main", "index": 0 } ]
      ]
    },
    "Criar Assinante Airtable": {
      "main": [
        [ { "node": "Gerar Link Telegram", "type": "main", "index": 0 } ]
      ]
    },
    "Gerar Link Telegram": {
      "main": [
        [ { "node": "Enviar Email Boas-vindas", "type": "main", "index": 0 } ]
      ]
    }
  }
}
```

## Notas de Implementação

1.  **Credenciais:** As credenciais do Airtable, Telegram e do serviço de email precisam ser configuradas no n8n.
2.  **IDs:** Os IDs da base (`baseId`) e do canal (`chatId`) precisam ser substituídos pelos valores corretos.
3.  **Lógica de Atualização:** O fluxo acima cobre a criação de um novo assinante. Uma lógica adicional (com um nó `IF`) será necessária para lidar com a **atualização** de um assinante existente (renovação).
4.  **Template de Email:** O conteúdo do email de boas-vindas será carregado de um arquivo de template ou definido diretamente no nó `Enviar Email`.
