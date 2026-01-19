# 📥 Guia de Importação do Workflow n8n - PES Tier 2

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

## 🎯 Objetivo

Importar o workflow completo do PES Tier 2 no n8n e configurar as credenciais necessárias.

---

## 📋 Pré-requisitos

Antes de importar, tenha em mãos:

1. ✅ **API Key do Airtable**
2. ✅ **Token do Bot do Telegram**
3. ✅ **Chat ID do Telegram** (canal ou grupo)
4. ✅ **Base ID do Airtable** (ex: `appXXXXXXXXXXXXXX`)

---

## 📥 Passo 1: Importar o Workflow

1. Acesse seu n8n
2. Clique em **"Workflows"** no menu lateral
3. Clique em **"Import from File"** ou **"+"** > **"Import from File"**
4. Selecione o arquivo **`PES_Tier2_Workflow.json`**
5. O workflow será criado com o nome **"[PES] Trade Processor v2.0 (Tier 2)"**

---

## 🔧 Passo 2: Configurar Credenciais do Airtable

### 2.1. Criar Credencial

1. No n8n, vá em **"Credentials"** no menu lateral
2. Clique em **"New"**
3. Procure por **"Airtable API"**
4. Cole sua **API Key** do Airtable
5. Salve com o nome **"Airtable Crypto"**

### 2.2. Conectar nos Nós

O workflow tem 3 nós do Airtable:
- **"Airtable - Create Trade"** (linha 200)
- **"Airtable - Find Trade"** (linha 400)
- **"Airtable - Update Trade"** (linha 400)

Para cada um:
1. Clique no nó
2. Em **"Credential to connect with"**, selecione **"Airtable Crypto"**
3. Em **"Application"**, cole seu **Base ID** (ex: `appXXXXXXXXXXXXXX`)
4. Em **"Table"**, confirme que está **"Trades"**

---

## 📱 Passo 3: Configurar Credenciais do Telegram

### 3.1. Criar Credencial

1. No n8n, vá em **"Credentials"**
2. Clique em **"New"**
3. Procure por **"Telegram Bot API"**
4. Cole o **Access Token** do seu bot (obtido com o BotFather)
5. Salve com o nome **"Telegram Bot Principal"**

### 3.2. Conectar nos Nós e Configurar Chat ID

O workflow tem 2 nós do Telegram:
- **"Telegram - Notify Entry"** (linha 200)
- **"Telegram - Notify Exit"** (linha 400)

Para cada um:
1. Clique no nó
2. Em **"Credential to connect with"**, selecione **"Telegram Bot Principal"**
3. Em **"Chat ID"**, substitua `YOUR_CHAT_ID` pelo seu Chat ID real

**Como obter o Chat ID:**
- Use o bot `@userinfobot` no Telegram
- Ou adicione seu bot em um grupo e use `@RawDataBot` para obter o ID

---

## 🌐 Passo 4: Obter URL do Webhook

1. Clique no nó **"Webhook TradingView"** (primeiro nó)
2. Copie a **Production URL** que aparece
3. Essa URL será usada no TradingView para configurar os alertas

**Exemplo de URL:**
```
https://seu-n8n.app.n8n.cloud/webhook/pes-signals
```

---

## ✅ Passo 5: Ativar o Workflow

1. No canto superior direito, clique no botão **"Inactive"**
2. Ele mudará para **"Active"** (verde)
3. O workflow agora está rodando e pronto para receber sinais!

---

## 🧪 Passo 6: Testar o Workflow (Opcional)

Você pode testar manualmente enviando um POST request para o webhook:

### Teste de Entrada LONG:

```bash
curl -X POST https://seu-n8n.app.n8n.cloud/webhook/pes-signals \
  -H "Content-Type: application/json" \
  -d '{
    "action": "PES_SIGNAL",
    "signal_id": "TEST_15_1737301200",
    "symbol": "BTCUSDT",
    "timeframe": "15",
    "type": "LONG_ENTRY",
    "price": 93161.0,
    "quality": "PREMIUM",
    "mtf_trend": "ALTA",
    "entry_channel": 93500.0,
    "exit_channel": 92500.0
  }'
```

### Teste de Saída LONG:

```bash
curl -X POST https://seu-n8n.app.n8n.cloud/webhook/pes-signals \
  -H "Content-Type: application/json" \
  -d '{
    "action": "PES_SIGNAL",
    "signal_id": "TEST_15_1737301200",
    "symbol": "BTCUSDT",
    "timeframe": "15",
    "type": "LONG_EXIT",
    "price": 93850.0
  }'
```

Se tudo estiver correto:
1. Você verá um registro criado no Airtable
2. Receberá uma mensagem no Telegram
3. Na saída, o registro será atualizado e você receberá outra mensagem com o resultado

---

## 🔍 Troubleshooting

### Erro: "Credential not found"
- Certifique-se de que os nomes das credenciais são exatamente:
  - `Airtable Crypto`
  - `Telegram Bot Principal`

### Erro: "Table not found"
- Verifique se o **Base ID** está correto
- Verifique se a tabela se chama exatamente **"Trades"**

### Erro: "Invalid Chat ID"
- Certifique-se de que o Chat ID está correto
- Se for um grupo, o ID geralmente é negativo (ex: `-1001234567890`)

### Webhook não recebe dados
- Verifique se o workflow está **Active**
- Teste com curl para ver se o webhook responde
- Verifique se a URL está correta no TradingView

---

## 📚 Próximos Passos

Após configurar o n8n:

1. Configure o Airtable (adicione os 4 campos do Tier 2)
2. Configure o TradingView (adicione o indicador e crie o alerta)
3. Teste com um ativo de baixa volatilidade primeiro

---

## ✅ Checklist Final

- [ ] Workflow importado no n8n
- [ ] Credencial "Airtable Crypto" criada e conectada
- [ ] Credencial "Telegram Bot Principal" criada e conectada
- [ ] Base ID configurado nos 3 nós do Airtable
- [ ] Chat ID configurado nos 2 nós do Telegram
- [ ] URL do webhook copiada
- [ ] Workflow ativado (Active)
- [ ] Teste manual realizado (opcional)

---

**Pronto! Seu workflow está configurado e pronto para receber sinais do TradingView!** 🚀
