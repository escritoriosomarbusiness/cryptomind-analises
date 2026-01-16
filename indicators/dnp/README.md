# 🎯 DNP v2.0 - Dedo No Pavio (COM MTF)

**Indicador completo de entrada com validação macro (Multi-Timeframe)**

---

## 📊 VISÃO GERAL

O **DNP (Dedo No Pavio)** é o indicador **mais completo** do sistema CryptoMind IA, combinando múltiplos sinais de confirmação com análise de tendência do fractal superior (MTF).

**Status:** ✅ Operacional com MTF  
**Versão:** 2.0  
**Última Atualização:** 16/01/2026

---

## ✨ CARACTERÍSTICAS

### **Detecção de Sinais:**
- ✅ **Dedo no Pavio:** Rejeição de preço (wicks grandes)
- ✅ **REMI:** Relative Momentum Index (confirmação de momentum)
- ✅ **Pivots:** Suporte e Resistência automáticos
- ✅ **Sistema de Confirmação:** Gatilho + Rompimento

### **Análise MTF (Multi-Timeframe):** 🆕
- ✅ **Detecção de Tendência HTF:** EMA 55 vs EMA 233
- ✅ **Classificação Automática:** PREMIUM/CAUTELA/CONTRA
- ✅ **Hierarquia de Timeframes:** 1m→15m, 5m→H1, 15m→H4, H1→D, H4→W, D→M

### **Gestão de Risco:**
- ✅ **Entry:** Preço de entrada calculado automaticamente
- ✅ **Stop Loss:** Baseado no pivot + margem de segurança
- ✅ **TP1:** Target 1 (1:1 Risk:Reward)
- ✅ **TP2:** Target 2 (1:2 Risk:Reward)
- ✅ **Trailing Stop:** Distância calculada automaticamente
- ✅ **Alavancagem Sugerida:** Baseada no risco percentual

---

## 🎯 CLASSIFICAÇÃO MTF

### **⭐⭐⭐ SETUP PREMIUM**
**Condição:** Setup alinhado com tendência do fractal superior

**Exemplo LONG:**
- Sinal: LONG no timeframe 15m
- HTF: 240m (H4) em tendência de ALTA
- Resultado: Alta probabilidade de sucesso

**Mensagem:**
```
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 240 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso
```

---

### **⚠️ CAUTELA RECOMENDADA**
**Condição:** Fractal superior sem tendência definida (neutro)

**Exemplo LONG:**
- Sinal: LONG no timeframe 15m
- HTF: 240m (H4) sem tendência clara
- Resultado: Risco elevado

**Mensagem:**
```
⚠️ CAUTELA RECOMENDADA ⚠️
📊 240 sem tendência definida
━━━━━━━━━━━━━━━━━━
⚠️ Fractal superior neutro - Risco elevado
```

---

### **🔴 CONTRA-TENDÊNCIA**
**Condição:** Setup contra a tendência do fractal superior

**Exemplo LONG:**
- Sinal: LONG no timeframe 15m
- HTF: 240m (H4) em tendência de BAIXA
- Resultado: Alto risco

**Mensagem:**
```
🚫 CONTRA-TENDÊNCIA 🚫
📉 240 em tendência de BAIXA
━━━━━━━━━━━━━━━━━━
⛔ ALTO RISCO - Operação contra o fluxo maior
⚠️ Não recomendado para iniciantes
```

---

## 🔄 FLUXO DE OPERAÇÃO

### **1. TRIGGER (Gatilho Armado)**

Quando o sinal é detectado, mas ainda não confirmado:

```
🔔 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO
📊 Setup: DNP
⏱ Timeframe: 15

━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 240 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso

━━━━━━━━━━━━━━━━━━
💰 Preço: $95,234.50
🎯 Trigger: $95,450.00
━━━━━━━━━━━━━━━━━━
📈 ADX: 28.5 | REMI: 65.2
━━━━━━━━━━━━━━━━━━
⚠️ Aguardando confirmação por rompimento
```

---

### **2. CONFIRMED (Confirmado por Rompimento)**

Quando o preço rompe o trigger e confirma o sinal:

```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
✅ CONFIRMADO POR ROMPIMENTO
📊 Setup: DNP
⏱ Timeframe: 15

━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 240 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso

━━━━━━━━━━━━━━━━━━
🎯 ENTRADA
💰 Preço: $95,450.00
🛑 Stop Loss: $94,850.20
📊 Risco: 2.45% ($384.30)

━━━━━━━━━━━━━━━━━━
🎯 ALVOS (Risco:Retorno)
✅ TP1: $96,049.80 (1:1)
✅ TP2: $96,649.60 (1:2)

━━━━━━━━━━━━━━━━━━
⚙️ GESTÃO DO TRADE
📈 Ao atingir TP1:
   • Realizar 50% da posição
   • Subir stop para entrada (breakeven)
   • Ativar trailing stop

🔄 Trailing Stop:
   • Distância: $150.00
   • Seguir preço até TP2

━━━━━━━━━━━━━━━━━━
📊 INDICADORES
📈 ADX: 28.5 | REMI: 65.2
⚖️ Alavancagem sugerida: 5-10x
━━━━━━━━━━━━━━━━━━
⚠️ Não é recomendação de investimento
```

---

## 🛠️ CONFIGURAÇÃO

### **1. TradingView (Pine Script)**

**Arquivo:** [`pinescript/dnp_v2.0_mtf.pine`](pinescript/dnp_v2.0_mtf.pine)

**Parâmetros:**
- **Lookback Pivots:** 5 (padrão)
- **REMI Period:** 14 (padrão)
- **REMI Overbought:** 70
- **REMI Oversold:** 30
- **Min Distance to Pivot:** 0.5%
- **Risk Percent:** 2.5%

**Alertas:**
1. Criar alerta no indicador
2. Configurar condição: "Any alert() function call"
3. Webhook URL: `https://cryptomindia.app.n8n.cloud/webhook/dnp-alert`
4. Formato: JSON

---

### **2. n8n (Processamento)**

**Arquivo:** [`n8n/processador_v2.0.js`](n8n/processador_v2.0.js)

**Workflow:**
1. **Webhook:** Recebe JSON do TradingView
2. **Processador:** Formata mensagem com bloco MTF
3. **Telegram:** Envia notificação

**Campos MTF (novos):**
```javascript
const setupQuality = alertData.setupQuality || 'CAUTELA';
const htfTrend = alertData.htfTrend || 'NEUTRO';
const htfTimeframe = alertData.htfTimeframe || 'N/A';
```

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

### **Detecção de Tendência (HTF):**

**Tendência de ALTA (3 condições):**
```pinescript
htf_trendUp = (htf_ema55 > htf_ema233) and 
              (htf_ema55 > htf_ema55[1]) and 
              (htf_close > htf_ema55)
```

**Tendência de BAIXA (3 condições):**
```pinescript
htf_trendDown = (htf_ema55 < htf_ema233) and 
                (htf_ema55 < htf_ema55[1]) and 
                (htf_close < htf_ema55)
```

### **Classificação:**

```pinescript
setupQuality = 
    (direction == "LONG" and htf_trendUp) or 
    (direction == "SHORT" and htf_trendDown) ? "PREMIUM" :
    
    (direction == "LONG" and htf_trendDown) or 
    (direction == "SHORT" and htf_trendUp) ? "CONTRA" :
    
    "CAUTELA"
```

---

## 📁 ARQUIVOS

### **Pine Script:**
- [`pinescript/dnp_v2.0_mtf.pine`](pinescript/dnp_v2.0_mtf.pine) - Código completo do indicador

### **n8n:**
- [`n8n/processador_v2.0.js`](n8n/processador_v2.0.js) - Processador com MTF
- [`n8n/workflow.json`](n8n/workflow.json) - Workflow completo

### **Documentação:**
- [`docs/MANUAL_OPERACAO.md`](docs/MANUAL_OPERACAO.md) - Manual de operação
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md) - Histórico de mudanças

---

## 🚀 QUICK START

### **Passo 1: Adicionar Indicador**
1. Abra o TradingView
2. Copie o código de `pinescript/dnp_v2.0_mtf.pine`
3. Cole no Pine Editor
4. Salve como "DNP v2.0"
5. Adicione ao gráfico

### **Passo 2: Configurar Alerta**
1. Clique com botão direito no indicador
2. "Add alert..."
3. Condição: "Any alert() function call"
4. Webhook URL: `https://cryptomindia.app.n8n.cloud/webhook/dnp-alert`
5. Salvar

### **Passo 3: Configurar n8n**
1. Acesse n8n Cloud
2. Importe `n8n/workflow.json`
3. Configure credenciais Telegram
4. Ative workflow

### **Passo 4: Testar**
1. Dispare alerta manual no TradingView
2. Verifique recebimento no Telegram
3. Confirme bloco MTF na mensagem

---

## 📊 INDICADORES UTILIZADOS

### **REMI (Relative Momentum Index):**
- Similar ao RSI, mas mais suave
- Overbought: > 70
- Oversold: < 30
- Usado para confirmar momentum

### **Pivots (Suporte/Resistência):**
- Lookback: 5 candles
- Automático
- Usado para definir stop loss

### **ADX (Average Directional Index):**
- Mede força da tendência
- > 25: Tendência forte
- < 20: Tendência fraca

---

## 📈 ESTATÍSTICAS

### **Timeframes Recomendados:**
- ✅ **15 minutos** (principal)
- ✅ **5 minutos** (scalping)
- ✅ **60 minutos** (swing)

### **Ativos Recomendados:**
- BTC/USDT
- ETH/USDT
- SOL/USDT
- BNB/USDT
- XRP/USDT

### **Gestão de Risco:**
- **Risco por trade:** 2-3%
- **Alavancagem:** 5-10x (risco baixo)
- **Stop Loss:** Sempre obrigatório
- **Take Profit:** TP1 (50%) + TP2 (50%)

---

## 📝 CHANGELOG

### **[16/01/2026] - v2.0 COM MTF**
- ✨ Adicionada lógica MTF completa
- ✨ Classificação PREMIUM/CAUTELA/CONTRA
- ✨ Campos MTF no JSON (setupQuality, htfTrend, htfTimeframe)
- ✨ Processador n8n atualizado com bloco macro
- 📚 Documentação completa criada

### **[10/01/2026] - v1.1**
- 🔧 Correções no REMI
- 🔧 Ajustes nos pivots
- 📚 Manual de operação atualizado

---

## ⚠️ IMPORTANTE

### **Uso Responsável:**
- ✅ Sempre usar stop loss
- ✅ Respeitar gestão de risco
- ✅ Não operar contra tendência (setups CONTRA)
- ✅ Priorizar setups PREMIUM

### **Limitações:**
- ⚠️ Não é recomendação de investimento
- ⚠️ Trading envolve riscos
- ⚠️ Resultados passados não garantem resultados futuros

---

## 📞 SUPORTE

Para dúvidas ou problemas:
- Consulte o [`MANUAL_OPERACAO.md`](docs/MANUAL_OPERACAO.md)
- Verifique o [`CHANGELOG.md`](docs/CHANGELOG.md)
- Abra uma issue no GitHub

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

**Código proprietário - Uso restrito**

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 16/01/2026  
**Versão:** 2.0
