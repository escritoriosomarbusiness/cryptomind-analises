# 🔄 TRS v6.1 - Trend Reversal Setup (COM MTF)

**Sistema de detecção de reversões de tendência com validação tripla e análise macro**

---

## 📊 VISÃO GERAL

O **TRS (Trend Reversal Setup)** é um sistema especializado em detectar reversões de tendência baseado em EMA 9 com validação tripla e análise de múltiplos timeframes (MTF).

**Status:** ✅ Operacional com MTF  
**Versão:** 6.1  
**Última Atualização:** 10/01/2026

---

## ✨ CARACTERÍSTICAS

### **Detecção de Reversões:**
- ✅ **EMA 9:** Base para detecção de reversões
- ✅ **Validação Tripla:** Pivots MTF + RSI + Fibonacci Golden Zone
- ✅ **Confluências:** Simples, Dupla (⭐), Tripla (🌟🌟)
- ✅ **Sistema de Confirmação:** Gatilho + Rompimento

### **Análise MTF (Multi-Timeframe):**
- ✅ **Detecção de Tendência HTF:** EMA 55 vs EMA 233
- ✅ **Classificação Automática:** PREMIUM/CAUTELA/CONTRA
- ✅ **Hierarquia de Timeframes:** 1m→15m, 5m→H1, 15m→H4, H1→D, H4→W, D→M

### **Gestão de Risco:**
- ✅ **Entry:** Preço de entrada calculado automaticamente
- ✅ **Stop Loss:** Baseado no pivot + margem de segurança
- ✅ **T1:** Target 1 (1:1 Risk:Reward)
- ✅ **T2:** Target 2 (1:2 Risk:Reward)
- ✅ **Trailing Stop:** Distância calculada automaticamente
- ✅ **Alavancagem Sugerida:** Baseada no risco percentual

---

## 🎯 VALIDAÇÕES

### **1. Pivots MTF (Multi-Timeframe)**
Suporte/Resistência em múltiplos timeframes:
- Lookback: 5 candles
- Confirmação em timeframe superior
- Peso: Alto

### **2. RSI (Relative Strength Index)**
Momentum e sobrecompra/sobrevenda:
- Período: 14
- Overbought: > 70
- Oversold: < 30
- Peso: Médio

### **3. Fibonacci Golden Zone**
Zona de retração ideal (0.618 - 0.786):
- Retração de 61.8% a 78.6%
- Baseado em swing high/low
- Peso: Médio

---

## 🌟 CONFLUÊNCIAS

### **Simples (1 validação)**
```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO
📊 Setup: TRS v6.1
⏱ Timeframe: 5m
━━━━━━━━━━━━━━━━━━
✅ Validação: Pivot MTF
━━━━━━━━━━━━━━━━━━
```

### **⭐ Dupla (2 validações)**
```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO ⭐
📊 Setup: TRS v6.1
⏱ Timeframe: 5m
━━━━━━━━━━━━━━━━━━
✅ Validações: Pivot MTF + RSI
━━━━━━━━━━━━━━━━━━
```

### **🌟🌟 Tripla (3 validações)**
```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO 🌟🌟
📊 Setup: TRS v6.1
⏱ Timeframe: 5m
━━━━━━━━━━━━━━━━━━
✅ Validações: Pivot MTF + RSI + Fib Golden
━━━━━━━━━━━━━━━━━━
```

---

## 🎯 CLASSIFICAÇÃO MTF

### **⭐⭐⭐ SETUP PREMIUM**
**Condição:** Setup alinhado com tendência do fractal superior

**Mensagem:**
```
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 H4 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso
```

### **⚠️ CAUTELA RECOMENDADA**
**Condição:** Fractal superior sem tendência definida

**Mensagem:**
```
⚠️ CAUTELA RECOMENDADA ⚠️
📊 H4 sem tendência definida
━━━━━━━━━━━━━━━━━━
⚠️ Fractal superior neutro - Risco elevado
```

### **🔴 CONTRA-TENDÊNCIA**
**Condição:** Setup contra a tendência do fractal superior

**Mensagem:**
```
🚫 CONTRA-TENDÊNCIA 🚫
📉 H4 em tendência de BAIXA
━━━━━━━━━━━━━━━━━━
⛔ ALTO RISCO - Operação contra o fluxo maior
⚠️ Não recomendado para iniciantes
```

---

## 🔄 FLUXO DE OPERAÇÃO

### **1. TRIGGER (Gatilho Armado)**

```
🔔 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO ⭐
📊 Setup: TRS v6.1
⏱ Timeframe: 5m

━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 60 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso

━━━━━━━━━━━━━━━━━━
💰 Preço: $95,234.50
🎯 Trigger: $95,450.00
━━━━━━━━━━━━━━━━━━
✅ Validações: Pivot MTF + RSI
━━━━━━━━━━━━━━━━━━
⚠️ Aguardando confirmação por rompimento
```

### **2. CONFIRMED (Confirmado)**

```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
✅ CONFIRMADO POR ROMPIMENTO ⭐
📊 Setup: TRS v6.1
⏱ Timeframe: 5m

━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 60 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso

━━━━━━━━━━━━━━━━━━
🎯 ENTRADA
💰 Preço: $95,450.00
🛑 Stop Loss: $94,850.20
📊 Risco: 2.45% ($384.30)

━━━━━━━━━━━━━━━━━━
🎯 ALVOS
✅ T1: $96,049.80 (1:1)
✅ T2: $96,649.60 (1:2)

━━━━━━━━━━━━━━━━━━
⚙️ GESTÃO
📈 Ao atingir T1:
   • Realizar 50%
   • Breakeven no stop
   • Ativar trailing

🔄 Trailing Stop: $150.00

━━━━━━━━━━━━━━━━━━
📊 INDICADORES
✅ Validações: Pivot MTF + RSI
⚖️ Alavancagem: 5-10x
━━━━━━━━━━━━━━━━━━
```

---

## 🛠️ CONFIGURAÇÃO

### **1. TradingView (Pine Script)**

**Arquivo:** [`pinescript/trs_v6.1_mtf.pine`](pinescript/trs_v6.1_mtf.pine)

**Parâmetros:**
- **Lookback Pivots:** 5
- **RSI Period:** 14
- **RSI Overbought:** 70
- **RSI Oversold:** 30
- **Fibonacci Levels:** 0.618, 0.786
- **Risk Percent:** 2.5%

**Alertas:**
1. Criar alerta no indicador
2. Condição: "Any alert() function call"
3. Webhook URL: `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
4. Formato: JSON

---

### **2. n8n (Processamento)**

**Arquivo:** [`n8n/processador_v6.1.js`](n8n/processador_v6.1.js)

**Workflow:**
1. **Webhook:** Recebe JSON do TradingView
2. **Processador:** Formata mensagem com bloco MTF
3. **Telegram:** Envia notificação

---

## 📊 LÓGICA MTF

### **Hierarquia de Timeframes:**

| Timeframe Atual | Fractal Superior (HTF) |
|-----------------|------------------------|
| 1 minuto        | 15 minutos             |
| 5 minutos       | 60 minutos (H1)        |
| 15 minutos      | 240 minutos (H4)       |
| 60 minutos (H1) | Daily (D)              |
| 240 minutos (H4)| Weekly (W)             |
| Daily (D)       | Monthly (M)            |

### **Detecção de Tendência:**

**Tendência de ALTA:**
```pinescript
htf_trendUp = (htf_ema55 > htf_ema233) and 
              (htf_ema55 > htf_ema55[1]) and 
              (htf_close > htf_ema55)
```

**Tendência de BAIXA:**
```pinescript
htf_trendDown = (htf_ema55 < htf_ema233) and 
                (htf_ema55 < htf_ema55[1]) and 
                (htf_close < htf_ema55)
```

---

## 📁 ARQUIVOS

### **Pine Script:**
- [`pinescript/trs_v6.1_mtf.pine`](pinescript/trs_v6.1_mtf.pine)

### **n8n:**
- [`n8n/processador_v6.1.js`](n8n/processador_v6.1.js)
- [`n8n/workflow.json`](n8n/workflow.json)

### **Documentação:**
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md)

---

## 🚀 QUICK START

### **Passo 1: Adicionar Indicador**
1. TradingView → Pine Editor
2. Copiar código de `pinescript/trs_v6.1_mtf.pine`
3. Salvar como "TRS v6.1"
4. Adicionar ao gráfico

### **Passo 2: Configurar Alerta**
1. Botão direito no indicador → "Add alert..."
2. Condição: "Any alert() function call"
3. Webhook: `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
4. Salvar

### **Passo 3: Configurar n8n**
1. Importar `n8n/workflow.json`
2. Configurar Telegram
3. Ativar workflow

---

## 📊 INDICADORES UTILIZADOS

### **EMA 9:**
- Base para detecção de reversões
- Cruzamento de preço indica reversão

### **RSI (Relative Strength Index):**
- Período: 14
- Overbought: > 70
- Oversold: < 30

### **Pivots:**
- Lookback: 5
- Suporte/Resistência automáticos

### **Fibonacci:**
- Golden Zone: 0.618 - 0.786
- Retração ideal para reversões

---

## 📈 ESTATÍSTICAS

### **Timeframes Recomendados:**
- ✅ **5 minutos** (principal)
- ✅ **15 minutos**
- ✅ **60 minutos**

### **Ativos:**
- BTC/USDT
- ETH/USDT
- SOL/USDT
- BNB/USDT

### **Gestão de Risco:**
- Risco: 2-3%
- Alavancagem: 5-10x
- Stop Loss: Obrigatório

---

## 📝 CHANGELOG

### **[10/01/2026] - v6.1 COM MTF**
- ✨ Lógica MTF completa
- ✨ Classificação PREMIUM/CAUTELA/CONTRA
- ✨ Processador atualizado
- 📚 Documentação completa

---

## ⚠️ IMPORTANTE

- ✅ Priorizar confluências duplas/triplas
- ✅ Priorizar setups PREMIUM
- ✅ Evitar setups CONTRA
- ✅ Sempre usar stop loss

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 10/01/2026  
**Versão:** 6.1
