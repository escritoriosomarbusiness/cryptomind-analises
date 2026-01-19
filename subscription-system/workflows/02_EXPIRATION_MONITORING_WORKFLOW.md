# Template: Workflow de Monitoramento de Vencimentos (n8n)

**Gatilho:** Cron Job (execução diária)

**Objetivo:** Verificar assinaturas expiradas, remover os membros do Telegram e atualizar seu status no Airtable.

## Estrutura do Workflow

```json
{
  "name": "CryptoMind - Monitoramento de Vencimentos",
  "nodes": [
    {
      "parameters": {
        "rule": "0 9 * * *" 
      },
      "name": "Cron Diário (9h)",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "operation": "list",
        "baseId": "YOUR_BASE_ID",
        "tableId": "Assinantes",
        "filterByFormula": "AND(IS_BEFORE({Data_Vencimento}, TODAY()), {Status} = 'active')"
      },
      "name": "Buscar Assinantes Vencidos",
      "type": "n8n-nodes-airtable.node",
      "typeVersion": 1,
      "position": [450, 300]
    },
    {
      "parameters": {},
      "name": "Loop Over Expired",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 1,
      "position": [650, 300]
    },
    {
      "parameters": {
        "chatId": "YOUR_CHANNEL_ID",
        "userId": "{{$json.Telegram_ID}}"
      },
      "name": "Remover do Telegram",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [850, 300]
    },
    {
      "parameters": {
        "operation": "update",
        "baseId": "YOUR_BASE_ID",
        "tableId": "Assinantes",
        "recordId": "{{$json.id}}",
        "fields": {
          "Status": "expired"
        }
      },
      "name": "Atualizar Status Airtable",
      "type": "n8n-nodes-airtable.node",
      "typeVersion": 1,
      "position": [1050, 300]
    },
    {
      "parameters": {
        "to": "{{$json.Email}}",
        "subject": "❌ Sua assinatura do CryptoMind Alerts expirou",
        "html": "..."
      },
      "name": "Enviar Email de Expiração",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 1,
      "position": [1250, 300]
    }
  ],
  "connections": {
    "Cron Diário (9h)": { "main": [ [ { "node": "Buscar Assinantes Vencidos", "type": "main", "index": 0 } ] ] },
    "Buscar Assinantes Vencidos": { "main": [ [ { "node": "Loop Over Expired", "type": "main", "index": 0 } ] ] },
    "Loop Over Expired": { "main": [ [ { "node": "Remover do Telegram", "type": "main", "index": 0 } ] ] },
    "Remover do Telegram": { "main": [ [ { "node": "Atualizar Status Airtable", "type": "main", "index": 0 } ] ] },
    "Atualizar Status Airtable": { "main": [ [ { "node": "Enviar Email de Expiração", "type": "main", "index": 0 } ] ] }
  }
}
```

## Notas de Implementação

1.  **Fórmula de Filtro:** A fórmula `IS_BEFORE({Data_Vencimento}, TODAY())` é crucial para selecionar apenas os registros cuja data de vencimento já passou.
2.  **Loop:** O nó `SplitInBatches` (configurado para `batchSize: 1`) garante que cada assinante vencido seja processado individualmente no loop.
3.  **Telegram ID:** É fundamental que o campo `Telegram_ID` no Airtable contenha o ID numérico do usuário para que o nó `Remover do Telegram` funcione corretamente.
4.  **Lembretes:** Um workflow similar pode ser criado para enviar lembretes, alterando a fórmula do filtro para `IS_SAME(DATEADD(TODAY(), 3, 'days'), {Data_Vencimento})` para notificar usuários 3 dias antes do vencimento.
