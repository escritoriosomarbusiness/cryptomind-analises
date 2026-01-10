# 📊 Setup TRS v6.1 - Trend Reversal Setup by CryptoMind IA

**Versão:** 6.1 Final  
**Data de Implementação:** 10/01/2026  
**Status:** ✅ Operacional

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Características Técnicas](#características-técnicas)
3. [Pine Script v6.1](#pine-script)
4. [Integração n8n](#integração-n8n)
5. [Configuração de Alertas](#configuração-alertas)
6. [Metodologia Operacional](#metodologia-operacional)
7. [Gestão de Risco](#gestão-de-risco)

---

## 🎯 VISÃO GERAL {#visão-geral}

O **Setup TRS (Trend Reversal Setup)** é um sistema automatizado de detecção de reversões de tendência baseado no cruzamento da EMA 9, validado por múltiplos métodos:

- **Pivots Multi-Timeframe** (Suporte/Resistência)
- **RSI** (Sobrecompra/Sobrevenda)
- **Fibonacci Golden Zone** (Retração 0.5-0.618)

### **Diferenciais:**

✅ **Sistema de Confirmação:** Gatilho + Rompimento  
✅ **Validação Tripla:** Híbrida (Pivots OU RSI OU Fibonacci)  
✅ **Detecção de Confluências:** Simples, Dupla (⭐), Tripla (🌟🌟)  
✅ **Cálculo Automático:** Entry, SL, Targets, Trailing Stop  
✅ **Gestão de Risco Integrada:** Alavancagem sugerida baseada em risco real  

---

## 🔧 CARACTERÍSTICAS TÉCNICAS {#características-técnicas}

### **Indicadores Base:**
- **EMA 9:** Média móvel exponencial de 9 períodos
- **RSI 14:** Índice de Força Relativa
- **Pivots MTF:** Pivots de timeframes estruturais superiores

### **Timeframes Estruturais (Automático):**
| TF Operacional | TF Estrutural |
|----------------|---------------|
| 1 min          | 15 min        |
| 5 min          | 1 hora        |
| 15 min         | 4 horas       |
| 1 hora         | Diário        |
| 4 horas        | Semanal       |
| Diário         | Mensal        |

### **Filtros de Qualidade:**
- **Mínimo 5 candles** do mesmo lado da EMA antes do cruzamento
- **Candle forte:** Fechamento no terço superior (LONG) ou inferior (SHORT)
- **Cooldown:** 5 candles entre sinais
- **Timeout:** Máximo 10 barras para confirmação

---

## 💻 PINE SCRIPT V6.1 {#pine-script}

**Arquivo:** `pinescript_setup_trs_v6.1.pine`

### **Principais Funções:**

#### **1. Detecção de Cruzamento EMA**
```pinescript
crossAboveEMA = close[1] < ema9[1] and close > ema9
crossBelowEMA = close[1] > ema9[1] and close < ema9
```

#### **2. Validação de Candle Forte**
```pinescript
// LONG: Fechamento no terço superior
upperThird = low + (candleRange * 0.66)
strongBullCandle = close >= upperThird and close > open

// SHORT: Fechamento no terço inferior
lowerThird = high - (candleRange * 0.66)
strongBearCandle = close <= lowerThird and close < open
```

#### **3. Cálculo de Entry, SL e Targets**
```pinescript
// LONG
tickSize = syminfo.mintick
entryPrice = triggerHighLong
stopLossPrice = triggerLowLong - tickSize
riskValue = entryPrice - stopLossPrice
riskPercent = (riskValue / entryPrice) * 100

target1 = entryPrice + riskValue      // 1R
target2 = entryPrice + (riskValue * 2) // 2R
trailingDistance = riskValue * 0.5     // 0.5R
```

### **Alertas JSON:**

#### **TRIGGER (Gatilho Armado):**
```json
{
  "symbol": "XRPUSDT",
  "action": "TRIGGER",
  "direction": "LONG",
  "setup": "9.1",
  "timeframe": "5",
  "price": "2.5432",
  "validation": "SR+RSI"
}
```

#### **CONFIRMED (Confirmado):**
```json
{
  "symbol": "XRPUSDT",
  "action": "CONFIRMED",
  "direction": "LONG",
  "setup": "TRS",
  "timeframe": "5",
  "price": "2.5455",
  "validation": "SR+RSI",
  "triggerHigh": "2.5450",
  "triggerLow": "2.5400",
  "entry": "2.5450",
  "stopLoss": "2.5399",
  "risk": "0.0051",
  "riskPercent": "0.20",
  "target1": "2.5501",
  "target2": "2.5552",
  "trailingDistance": "0.00255"
}
```

---

## ⚙️ INTEGRAÇÃO N8N {#integração-n8n}

### **Workflow:** Setup TRS - Alertas TradingView

**Arquivo:** `n8n_workflow_setup_trs.json`

### **Fluxo:**
```
Webhook TradingView → Alerta do processador (JS) → Telegram
```

### **Código JavaScript (Processador):**

```javascript
// Processar dados do TradingView - Setup TRS v6.1
const data = $input.first().json.body || $input.first().json;

// Extrair informações do alerta
const symbol = data.symbol || 'BTCUSDT';
const action = data.action || 'TRIGGER';
const direction = data.direction || 'LONG';
const setup = data.setup || 'TRS';
const timeframe = data.timeframe || '5';
const price = parseFloat(data.price) || 0;
const validation = data.validation || 'HYBRID';

// Dados do candle gatilho e cálculos (só para CONFIRMED)
const triggerHigh = parseFloat(data.triggerHigh) || 0;
const triggerLow = parseFloat(data.triggerLow) || 0;
const entry = parseFloat(data.entry) || 0;
const stopLoss = parseFloat(data.stopLoss) || 0;
const risk = parseFloat(data.risk) || 0;
const riskPercent = parseFloat(data.riskPercent) || 0;
const target1 = parseFloat(data.target1) || 0;
const target2 = parseFloat(data.target2) || 0;
const trailingDistance = parseFloat(data.trailingDistance) || 0;

// Determinar tipo de alerta
const isTrigger = action === 'TRIGGER';
const isConfirmed = action === 'CONFIRMED';

// Emojis baseados em validação
let validationEmoji = '🔔';
let validationText = validation;

// Confluências
if (validation.includes('+')) {
  const validators = validation.split('+');
  if (validators.length >= 3) {
    validationEmoji = '🌟🌟'; // Tripla
  } else if (validators.length === 2) {
    validationEmoji = '⭐'; // Dupla
  }
}

// Emoji de direção
const directionEmoji = direction === 'LONG' ? '🟢' : '🔴';

// Formatar preços
const formatPrice = (p) => {
  if (p === 0) return '0.00';
  if (p >= 1000) return p.toFixed(2);
  if (p >= 1) return p.toFixed(4);
  return p.toFixed(8);
};

// Calcular alavancagem sugerida
const maxRealRisk = 15;
const suggestedLeverage = riskPercent > 0 ? Math.min(10, Math.floor(maxRealRisk / riskPercent)) : 1;
const realRisk = riskPercent * suggestedLeverage;

return {
  json: {
    symbol,
    action,
    direction,
    directionEmoji,
    setup,
    timeframe,
    price: formatPrice(price),
    validation,
    validationText,
    validationEmoji,
    isTrigger,
    isConfirmed,
    triggerHigh: formatPrice(triggerHigh),
    triggerLow: formatPrice(triggerLow),
    entry: formatPrice(entry),
    stopLoss: formatPrice(stopLoss),
    risk: formatPrice(risk),
    riskPercent: riskPercent.toFixed(2),
    target1: formatPrice(target1),
    target2: formatPrice(target2),
    trailingDistance: formatPrice(trailingDistance),
    suggestedLeverage,
    realRisk: realRisk.toFixed(1),
    timestamp: new Date().toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' })
  }
};
```

### **Template Telegram:**

```
{{ $json.validationEmoji }} <b>{{ $json.directionEmoji }} {{ $json.direction }} {{ $json.symbol }}</b>

📊 <b>Setup TRS by CryptoMind IA</b>
⏱️ {{ $json.timeframe }}m • 🕐 {{ $json.timestamp }}

{{ $json.isTrigger ? '🔔 <b>GATILHO ARMADO</b>' : '✅ <b>CONFIRMADO POR ROMPIMENTO</b>' }}

🎯 <b>Validação:</b> {{ $json.validationText }}

💰 <b>Preço Atual:</b> ${{ $json.price }}

{{ $json.isTrigger ? '📍 <b>Aguardando Rompimento</b>\n\n⚠️ <i>Entrada será confirmada no rompimento do gatilho</i>' : '🚀 <b>Entrada Ativa</b>\n\n🎯 <b>Entrada:</b> ${{ $json.entry }}\n🛑 <b>Stop Loss:</b> ${{ $json.stopLoss }} ({{ $json.riskPercent }}%)\n\n⚙️ <b>Gestão de Risco:</b>\n• Risco: 1% da banca\n• Alavancagem: {{ $json.suggestedLeverage }}x\n• Risco Real: {{ $json.realRisk }}%\n\n📈 <b>Alvos:</b>\n1️⃣ ${{ $json.target1 }} (1R) → Realizar 40%\n   ⚡ Mover SL para entrada + Trailing {{ $json.riskPercent }}%\n2️⃣ ${{ $json.target2 }} (2R) → Ativar Trailing Stop (${{ $json.trailingDistance }})\n\n❌ <b>Invalidação:</b> Se EMA 9 virar antes da entrada' }}

⚠️ <i>Não é recomendação de investimento</i>
```

---

## 🔔 CONFIGURAÇÃO DE ALERTAS {#configuração-alertas}

### **TradingView:**

1. **Condição:** CryptoMind - Setup 9.1 v6.1
2. **Tipo:** Qualquer chamada de função de alerta
3. **Frequência:** Uma vez por barra
4. **Webhook URL:** `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
5. **Mensagem:** Deixar em branco (JSON enviado automaticamente)

### **Nome do Alerta:**
```
Setup TRS - {{ticker}} {{interval}}
```

---

## 📈 METODOLOGIA OPERACIONAL {#metodologia-operacional}

### **Ao Receber TRIGGER:**
1. ✅ Anotar o setup
2. ✅ Aguardar confirmação
3. ❌ NÃO entrar ainda

### **Ao Receber CONFIRMED:**
1. ✅ Entrar no preço de **Entrada** informado
2. ✅ Colocar Stop Loss no preço informado
3. ✅ Configurar alavancagem sugerida
4. ✅ Calcular tamanho da posição (1% de risco da banca)

### **Gestão de Alvos:**

#### **Target 1 (1R):**
- Realizar **40%** da posição
- Mover Stop Loss para o preço de entrada (breakeven)
- Ativar trailing stop de **0.5R**

#### **Target 2 (2R):**
- Ativar trailing stop na distância informada
- Deixar a posição correr até ser stopada

### **Invalidação:**
- ❌ Se o preço cruzar a EMA 9 antes da entrada, cancele o setup
- ❌ Se o Stop Loss for atingido, aceite a perda (1% da banca)

---

## 💰 GESTÃO DE RISCO {#gestão-de-risco}

### **Princípios:**
- **Risco por trade:** 1% da banca
- **Risco real máximo:** 15% (com alavancagem)
- **Alavancagem máxima:** 10x
- **Exposição máxima:** 5% da banca em risco simultâneo

### **Cálculo de Alavancagem:**
```javascript
suggestedLeverage = Math.min(10, Math.floor(15 / riskPercent))
realRisk = riskPercent * suggestedLeverage
```

### **Exemplo:**
- Risco do setup: 0.20%
- Alavancagem sugerida: 10x (15 / 0.20 = 75, limitado a 10x)
- Risco real: 2.0% (0.20% × 10)

---

## 📊 CONFIGURAÇÕES RECOMENDADAS

### **Para Timeframe 5 minutos:**
- Lookback Pivots: **5**
- Min. candles EMA: **5**
- Cooldown: **5**

### **Para Timeframe 15 minutos:**
- Lookback Pivots: **7**
- Min. candles EMA: **5**
- Cooldown: **5**

### **Para Timeframe 1 hora:**
- Lookback Pivots: **10**
- Min. candles EMA: **7**
- Cooldown: **7**

---

## ✅ STATUS DE IMPLEMENTAÇÃO

- ✅ Pine Script v6.1 completo e testado
- ✅ Integração n8n funcionando
- ✅ Alertas TradingView configurados
- ✅ Mensagens Telegram formatadas
- ✅ Gestão de risco implementada
- ✅ Sistema 100% automatizado

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 10/01/2026  
**Versão:** 6.1 Final
