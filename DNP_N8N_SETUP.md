# 🔔 Setup DNP - Integração n8n

**Versão:** 1.0  
**Data:** 10/01/2026

---

## 📋 VISÃO GERAL

Este documento descreve como configurar o workflow n8n para receber alertas do **Setup DNP** do TradingView e enviar notificações formatadas para o Telegram.

---

## 🔧 ARQUITETURA

```
TradingView → Webhook n8n → Processador JS → Telegram
```

---

## ⚙️ CONFIGURAÇÃO

### **1. IMPORTAR WORKFLOW**

1. Acesse seu n8n
2. Clique em **"Import from File"**
3. Selecione o arquivo `n8n_workflow_dnp.json`
4. Clique em **"Import"**

---

### **2. CONFIGURAR WEBHOOK**

1. Abra o nó **"Webhook"**
2. Copie a **URL do webhook**
3. Exemplo: `https://seu-n8n.app.n8n.cloud/webhook/dnp-alert`

---

### **3. CONFIGURAR TELEGRAM**

1. Abra o nó **"Enviar Telegram"**
2. Configure suas credenciais do Telegram:
   - **Bot Token:** Obtido via @BotFather
   - **Chat ID:** Seu ID ou do grupo
3. Salve as credenciais

---

### **4. ATIVAR WORKFLOW**

1. Clique no botão **"Active"** no canto superior direito
2. O workflow agora está ativo e aguardando alertas

---

## 📊 CONFIGURAR ALERTAS NO TRADINGVIEW

### **Passo 1: Criar Alerta**

1. Abra o gráfico com o indicador **DNP v1.0**
2. Clique no ícone de **Alerta** (sino)
3. Configure:
   - **Condição:** DNP v1.0
   - **Opção:** Qualquer chamada de função de alerta
   - **Frequência:** Uma vez por barra

---

### **Passo 2: Configurar Webhook**

1. Em **"Notificações"**, marque **"Webhook URL"**
2. Cole a URL do webhook do n8n
3. **Deixe o campo "Mensagem" em branco** (JSON enviado automaticamente)

---

### **Passo 3: Nomear e Salvar**

- **Nome:** `Setup DNP - {{ticker}} {{interval}}`
- Clique em **"Criar"**

---

## 📨 FORMATO DOS ALERTAS

### **TRIGGER (Gatilho Armado):**

```json
{
  "symbol": "BTCUSDT",
  "action": "TRIGGER",
  "direction": "LONG",
  "setup": "DNP",
  "timeframe": "5",
  "price": "90454.97",
  "triggerHigh": "90454.97",
  "adx": "25.50",
  "remi": "1.85"
}
```

---

### **CONFIRMED (Confirmado):**

```json
{
  "symbol": "BTCUSDT",
  "action": "CONFIRMED",
  "direction": "LONG",
  "setup": "DNP",
  "timeframe": "5",
  "price": "90539.95",
  "entry": "90454.97",
  "stopLoss": "90300.00",
  "risk": "154.97",
  "riskPercent": "0.17",
  "target1": "90609.94",
  "target2": "90764.91",
  "trailingDistance": "77.49",
  "triggerHigh": "90454.97",
  "adx": "25.50",
  "remi": "1.85"
}
```

---

## 📱 MENSAGEM NO TELEGRAM

### **TRIGGER:**

```
🔔 🟢 LONG BTCUSDT

📊 Setup DNP by CryptoMind IA
⏱️ 5m • 🕐 10/01/2026 14:30:00

🔔 GATILHO ARMADO

🎯 Indicadores:
• ADX: 25.50
• REMI: 1.85

💰 Preço Atual: $90454.97

📍 Aguardando Rompimento

⚠️ Entrada será confirmada no rompimento do gatilho

⚠️ Não é recomendação de investimento
```

---

### **CONFIRMED:**

```
✅ 🟢 LONG BTCUSDT

📊 Setup DNP by CryptoMind IA
⏱️ 5m • 🕐 10/01/2026 14:35:00

✅ CONFIRMADO POR ROMPIMENTO

🎯 Indicadores:
• ADX: 25.50
• REMI: 1.85

💰 Preço Atual: $90539.95

🚀 Entrada Ativa

🎯 Entrada: $90454.97
🛑 Stop Loss: $90300.00 (0.17%)

⚙️ Gestão de Risco:
• Risco: 1% da banca
• Alavancagem: 10x
• Risco Real: 1.7%

📈 Alvos:
1️⃣ $90609.94 (1R) → Realizar 40%
   ⚡ Mover SL para entrada + Trailing 0.17%
2️⃣ $90764.91 (2R) → Ativar Trailing Stop ($77.49)

❌ Invalidação: Se não romper no próximo candle

⚠️ Não é recomendação de investimento
```

---

## 🔍 TESTE

### **Testar Webhook:**

1. No n8n, clique em **"Execute Workflow"**
2. No TradingView, force um alerta manual
3. Verifique se a mensagem chegou no Telegram

---

## 💡 DICAS

- ✅ Use um **grupo privado** no Telegram para receber alertas
- ✅ Configure **múltiplos alertas** para diferentes timeframes
- ✅ Monitore o **log do n8n** para debug
- ✅ Teste com **paper trading** antes de usar capital real

---

## ⚠️ IMPORTANTE

- **Não compartilhe** a URL do webhook publicamente
- **Não use** este sistema como única fonte de decisão
- **Sempre faça** sua própria análise antes de operar

---

**Desenvolvido por:** CryptoMind IA  
**Versão:** 1.0
