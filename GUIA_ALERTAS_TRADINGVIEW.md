# 📢 GUIA COMPLETO: CONFIGURAÇÃO DE ALERTAS - DNP v1.1

**Data:** 10 de Janeiro de 2026  
**Versão DNP:** 1.1  
**Integração:** TradingView → n8n → Telegram

---

## 📋 ÍNDICE

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Webhook n8n](#configuração-do-webhook-n8n)
3. [Criação de Alertas no TradingView](#criação-de-alertas-no-tradingview)
4. [Tipos de Alertas](#tipos-de-alertas)
5. [Formato JSON dos Alertas](#formato-json-dos-alertas)
6. [Testes e Validação](#testes-e-validação)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 PRÉ-REQUISITOS

### **1. TradingView**
- ✅ Conta TradingView (Pro, Pro+ ou Premium para alertas ilimitados)
- ✅ Indicador DNP v1.1 instalado e funcionando
- ✅ Gráfico configurado com criptomoeda desejada

### **2. n8n**
- ✅ Instância n8n rodando (local ou cloud)
- ✅ Workflow DNP importado e ativo
- ✅ URL do webhook acessível pela internet

### **3. Telegram**
- ✅ Bot Telegram criado (via @BotFather)
- ✅ Token do bot configurado no n8n
- ✅ Chat ID obtido

---

## 🌐 CONFIGURAÇÃO DO WEBHOOK N8N

### **PASSO 1: Acessar o Workflow DNP no n8n**

1. Abrir n8n: `http://seu-n8n-instance.com`
2. Localizar workflow: **"DNP - TradingView Alerts"**
3. Clicar no nó **"Webhook"** (primeiro nó)

### **PASSO 2: Obter URL do Webhook**

O nó Webhook mostrará uma URL similar a:

```
https://seu-n8n-instance.com/webhook/dnp-alerts
```

ou

```
https://seu-n8n-instance.com/webhook-test/dnp-alerts
```

**⚠️ IMPORTANTE:**
- **Webhook de Produção:** `/webhook/dnp-alerts` (usar este!)
- **Webhook de Teste:** `/webhook-test/dnp-alerts` (apenas para testes)

### **PASSO 3: Copiar URL do Webhook**

Copie a URL completa do webhook de **PRODUÇÃO**. Você usará esta URL nos alertas do TradingView.

**Exemplo:**
```
https://n8n.cryptomind.com/webhook/dnp-alerts
```

### **PASSO 4: Ativar o Workflow**

1. Clicar no botão **"Active"** no canto superior direito
2. Verificar se o status mudou para **"Active"** (verde)

---

## 🔔 CRIAÇÃO DE ALERTAS NO TRADINGVIEW

### **CONFIGURAÇÃO GERAL**

Você precisará criar **4 ALERTAS** por criptomoeda/timeframe:

1. **DNP LONG - TRIGGER**
2. **DNP LONG - CONFIRMED**
3. **DNP SHORT - TRIGGER**
4. **DNP SHORT - CONFIRMED**

---

### **ALERTA 1: DNP LONG - TRIGGER**

#### **PASSO 1: Abrir Configuração de Alerta**
1. No gráfico com DNP v1.1 ativo
2. Clicar no ícone de **"Relógio"** (Alertas) no menu superior
3. Clicar em **"Criar Alerta"** ou pressionar `Alt + A`

#### **PASSO 2: Configurar Condição**
- **Condição:** `DNP by CryptoMindIA`
- **Quando:** `alert() function call`
- **Opções:** (deixar padrão)

#### **PASSO 3: Configurar Mensagem**

**Nome do Alerta:**
```
DNP LONG TRIGGER - {{ticker}} - {{interval}}
```

**Mensagem:**
```json
{{plot_0}}
```

**⚠️ IMPORTANTE:** Use exatamente `{{plot_0}}` - o TradingView substituirá pelo JSON do alerta!

#### **PASSO 4: Configurar Webhook**

**URL do Webhook:**
```
https://seu-n8n-instance.com/webhook/dnp-alerts
```

**Método:** `POST` (padrão)

#### **PASSO 5: Configurar Frequência**

- **Opções:**
  - ✅ **"Once Per Bar Close"** (Recomendado)
  - ❌ "Only Once" (não usar - alerta expira)
  - ❌ "Once Per Bar" (pode gerar alertas falsos)

- **Validade:**
  - ✅ **"Open-ended"** (sem expiração)

#### **PASSO 6: Salvar**

Clicar em **"Criar"**

---

### **ALERTA 2: DNP LONG - CONFIRMED**

Repetir os mesmos passos do ALERTA 1, mas com:

**Nome do Alerta:**
```
DNP LONG CONFIRMED - {{ticker}} - {{interval}}
```

**Mensagem:**
```json
{{plot_0}}
```

**Webhook URL:** (mesma do ALERTA 1)

---

### **ALERTA 3: DNP SHORT - TRIGGER**

Repetir os mesmos passos, mas com:

**Nome do Alerta:**
```
DNP SHORT TRIGGER - {{ticker}} - {{interval}}
```

**Mensagem:**
```json
{{plot_0}}
```

**Webhook URL:** (mesma)

---

### **ALERTA 4: DNP SHORT - CONFIRMED**

Repetir os mesmos passos, mas com:

**Nome do Alerta:**
```
DNP SHORT CONFIRMED - {{ticker}} - {{interval}}
```

**Mensagem:**
```json
{{plot_0}}
```

**Webhook URL:** (mesma)

---

## 📊 TIPOS DE ALERTAS

### **1. TRIGGER (Gatilho)**

**Quando dispara:**
- Todas as condições do setup foram atendidas
- Setup formado, aguardando confirmação no próximo candle

**O que fazer:**
- 🔔 Receber notificação
- 👀 Observar o gráfico
- ⏳ Aguardar confirmação
- ❌ **NÃO ENTRAR** ainda!

**Informações recebidas:**
- Símbolo, direção, timeframe
- Preço atual
- Trigger level (HIGH para LONG, LOW para SHORT)
- ADX e REMI atuais

---

### **2. CONFIRMED (Confirmado)**

**Quando dispara:**
- Candle seguinte rompeu o trigger level
- Setup confirmado, entrada válida

**O que fazer:**
- ✅ **ENTRAR NA OPERAÇÃO**
- 📝 Configurar ordem com os parâmetros recebidos
- 🎯 Definir Stop Loss e Targets

**Informações recebidas:**
- Símbolo, direção, timeframe
- **Entry:** Preço de entrada
- **Stop Loss:** Preço do SL
- **Target 1:** Primeiro alvo (1R)
- **Target 2:** Segundo alvo (2R)
- **Risk:** Valor do risco (em pontos)
- **Risk %:** Percentual de risco
- **Trailing Distance:** Distância do trailing stop (0.5R)
- ADX e REMI atuais

---

## 📋 FORMATO JSON DOS ALERTAS

### **TRIGGER LONG:**

```json
{
  "symbol": "BTCUSDT",
  "action": "TRIGGER",
  "direction": "LONG",
  "setup": "DNP",
  "timeframe": "15",
  "price": "90907.39",
  "triggerHigh": "91050.00",
  "adx": "22.45",
  "remi": "1.85"
}
```

### **CONFIRMED LONG:**

```json
{
  "symbol": "BTCUSDT",
  "action": "CONFIRMED",
  "direction": "LONG",
  "setup": "DNP",
  "timeframe": "15",
  "price": "91100.00",
  "entry": "91050.00",
  "stopLoss": "90500.00",
  "risk": "550.00",
  "riskPercent": "0.60",
  "target1": "91600.00",
  "target2": "92150.00",
  "trailingDistance": "275.00",
  "triggerHigh": "91050.00",
  "adx": "23.10",
  "remi": "1.92"
}
```

### **TRIGGER SHORT:**

```json
{
  "symbol": "BTCUSDT",
  "action": "TRIGGER",
  "direction": "SHORT",
  "setup": "DNP",
  "timeframe": "15",
  "price": "90500.00",
  "triggerLow": "90400.00",
  "adx": "21.80",
  "remi": "1.75"
}
```

### **CONFIRMED SHORT:**

```json
{
  "symbol": "BTCUSDT",
  "action": "CONFIRMED",
  "direction": "SHORT",
  "setup": "DNP",
  "timeframe": "15",
  "price": "90300.00",
  "entry": "90400.00",
  "stopLoss": "90950.00",
  "risk": "550.00",
  "riskPercent": "0.61",
  "target1": "89850.00",
  "target2": "89300.00",
  "trailingDistance": "275.00",
  "triggerLow": "90400.00",
  "adx": "22.30",
  "remi": "1.80"
}
```

---

## 🧪 TESTES E VALIDAÇÃO

### **TESTE 1: Webhook n8n Funcionando**

1. Abrir n8n
2. Abrir workflow DNP
3. Clicar em **"Execute Workflow"**
4. Enviar JSON de teste manualmente
5. Verificar se mensagem chega no Telegram

**JSON de Teste:**
```json
{
  "symbol": "BTCUSDT",
  "action": "TRIGGER",
  "direction": "LONG",
  "setup": "DNP",
  "timeframe": "15",
  "price": "90000.00",
  "triggerHigh": "90100.00",
  "adx": "22.00",
  "remi": "1.80"
}
```

### **TESTE 2: Alerta TradingView → n8n**

1. Criar alerta de teste no TradingView
2. Forçar disparo (manualmente ou aguardar sinal)
3. Verificar logs do n8n
4. Confirmar recebimento do JSON
5. Verificar mensagem no Telegram

### **TESTE 3: Validação Completa**

1. Aplicar DNP v1.1 em gráfico de teste
2. Configurar os 4 alertas
3. Aguardar sinal real ou usar replay
4. Validar:
   - ✅ TRIGGER recebido
   - ✅ CONFIRMED recebido
   - ✅ Dados corretos no Telegram
   - ✅ Formatação legível

---

## 🔧 TROUBLESHOOTING

### **PROBLEMA 1: Alerta não dispara**

**Possíveis causas:**
- ❌ Alerta configurado como "Only Once" e já disparou
- ❌ Alerta expirou (validade limitada)
- ❌ Condição do indicador não foi atendida

**Solução:**
- ✅ Recriar alerta com "Open-ended"
- ✅ Usar "Once Per Bar Close"
- ✅ Verificar dashboard DNP (todas condições verdes?)

---

### **PROBLEMA 2: Webhook não recebe dados**

**Possíveis causas:**
- ❌ URL do webhook incorreta
- ❌ Workflow n8n inativo
- ❌ Firewall bloqueando TradingView

**Solução:**
- ✅ Verificar URL (copiar novamente do n8n)
- ✅ Ativar workflow no n8n
- ✅ Testar webhook com Postman/curl
- ✅ Verificar logs do n8n

---

### **PROBLEMA 3: JSON malformado**

**Possíveis causas:**
- ❌ Mensagem do alerta não usa `{{plot_0}}`
- ❌ Indicador enviando formato errado

**Solução:**
- ✅ Usar exatamente `{{plot_0}}` na mensagem
- ✅ Verificar código do indicador (linhas 412-426)
- ✅ Testar com JSON manual no n8n

---

### **PROBLEMA 4: Mensagem não chega no Telegram**

**Possíveis causas:**
- ❌ Token do bot incorreto
- ❌ Chat ID incorreto
- ❌ Bot bloqueado pelo usuário

**Solução:**
- ✅ Verificar token no n8n
- ✅ Obter Chat ID novamente (@userinfobot)
- ✅ Enviar `/start` para o bot
- ✅ Testar envio manual no n8n

---

## 📊 MONITORAMENTO

### **Logs n8n**

Acessar: `n8n → Executions`

**Verificar:**
- ✅ Status: Success (verde)
- ✅ Webhook recebido
- ✅ JSON parseado
- ✅ Mensagem enviada

**Erros comuns:**
- 🔴 `Invalid JSON` → Problema no formato do alerta
- 🔴 `Webhook timeout` → URL incorreta
- 🔴 `Telegram error` → Token/Chat ID incorreto

---

### **Alertas Ativos no TradingView**

Acessar: `TradingView → Alertas → Ativos`

**Verificar:**
- ✅ 4 alertas por cripto/timeframe
- ✅ Status: Ativo (verde)
- ✅ Validade: Open-ended
- ✅ Frequência: Once Per Bar Close

---

## 🎯 CHECKLIST FINAL

### **Antes de Operar:**

- [ ] DNP v1.1 instalado e testado
- [ ] Workflow n8n ativo e funcionando
- [ ] Bot Telegram respondendo
- [ ] 4 alertas criados por cripto/timeframe
- [ ] Alertas testados e validados
- [ ] Mensagens chegando corretamente no Telegram
- [ ] Parâmetros ajustados para o timeframe
- [ ] Dashboard DNP mostrando dados corretos

---

## 📝 EXEMPLO DE CONFIGURAÇÃO COMPLETA

### **Cenário: BTC 15min**

**Gráfico:**
- Par: BTCUSDT
- Timeframe: 15min
- Indicador: DNP v1.1

**Parâmetros DNP:**
- Didi Dist. Eixo: 0.20%
- ADX Mínimo: 20
- Inclinação ADX: 2.5
- REMI Mínimo: 1.5
- Pivot Breakout: Por Fechamento (Close)
- Stop Loss: 3 Candles Anteriores

**Alertas Criados:**
1. ✅ DNP LONG TRIGGER - BTCUSDT - 15
2. ✅ DNP LONG CONFIRMED - BTCUSDT - 15
3. ✅ DNP SHORT TRIGGER - BTCUSDT - 15
4. ✅ DNP SHORT CONFIRMED - BTCUSDT - 15

**Webhook:**
```
https://n8n.cryptomind.com/webhook/dnp-alerts
```

**Status:**
- TradingView: ✅ 4 alertas ativos
- n8n: ✅ Workflow ativo
- Telegram: ✅ Bot respondendo

---

## 🚀 PRÓXIMOS PASSOS

Após configurar os alertas:

1. **Testar com conta demo** (se disponível)
2. **Monitorar primeiros sinais** sem operar
3. **Validar qualidade dos setups** (taxa de acerto)
4. **Ajustar parâmetros** conforme necessário
5. **Começar operação real** com gestão de risco

---

**🎉 SISTEMA PRONTO PARA OPERAR!**

Qualquer dúvida, consulte a documentação ou entre em contato.
