# 📊 Monitor USDT.D v2.0 - Análise Macro de Mercado

**Versão:** 2.0 Atualizada  
**Data de Atualização:** 10/01/2026  
**Status:** ✅ Operacional

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Correções Implementadas](#correções)
3. [Pine Script](#pine-script)
4. [Integração n8n](#integração-n8n)
5. [Interpretação dos Alertas](#interpretação)

---

## 🎯 VISÃO GERAL {#visão-geral}

O **Monitor USDT.D** é um sistema de análise macro que monitora a dominância do Tether (USDT.D) no mercado cripto e alerta quando o preço se aproxima de níveis importantes de Suporte/Resistência ou EMAs.

### **Por que USDT.D é importante?**

> **USDT.D é INVERSAMENTE proporcional ao mercado cripto:**
> - **Abaixo das EMAs** = Dinheiro entrando em cripto (BULLISH)
> - **Acima das EMAs** = Dinheiro saindo de cripto (BEARISH)

---

## 🔧 CORREÇÕES IMPLEMENTADAS {#correções}

### **Problemas Corrigidos (10/01/2026):**

❌ **ANTES:**
- Dominância aparecia vazia: "USDT Dominance: %"
- Timeframe vazio: "Timeframe:"
- Não mostrava tipo de nível (Suporte/Resistência/EMA 200)
- Não mostrava valor do nível
- Não mostrava distância até o nível
- Não mostrava posição das EMAs

✅ **DEPOIS:**
- ✅ Dominância com valor: "USDT Dominance: 5.23%"
- ✅ Timeframe correto: "Timeframe: 4H"
- ✅ Tipo de nível: "Próximo de Resistência importante"
- ✅ Valor do nível: "Nível S/R: 5.35%"
- ✅ Distância: "Distância: 0.12% (2.3% de distância)"
- ✅ Posição das EMAs: EMA 9, 21 e 200 com status
- ✅ Impacto no mercado: BULLISH/BEARISH com emoji

---

## 💻 PINE SCRIPT {#pine-script}

**Arquivo:** `pinescript_usdt_d_monitor.pine`

### **Alertas Enviados:**

O Pine Script envia JSON com todas as informações necessárias:

```json
{
  "dominance": "5.23",
  "ema_9": "5.10",
  "ema_21": "5.15",
  "ema_200": "5.30",
  "resistance": "5.35",
  "support": "5.00",
  "crypto_impact": "BEARISH",
  "timeframe": "240",
  "type": "usdt_d_alert",
  "near_resistance": true,
  "near_support": false,
  "near_ema_200": false,
  "level": "resistance"
}
```

---

## ⚙️ INTEGRAÇÃO N8N {#integração-n8n}

### **Workflow:** CryptoMind IA - Monitor USDT.D

**Arquivo:** `n8n_workflow_usdt_d.json`

### **Fluxo:**
```
Webhook USDT.D → Processador de Dados USDT.D → É Alerta S/R? → Telegram
```

### **Código JavaScript (Processador):**

```javascript
// Processar dados do USDT.D recebidos do TradingView
const data = $input.first().json;

// Extrair dados
const dominance = parseFloat(data.dominance) || 0;
const ema9 = parseFloat(data.ema_9) || 0;
const ema21 = parseFloat(data.ema_21) || 0;
const ema200 = parseFloat(data.ema_200) || 0;
const resistance = parseFloat(data.resistance) || 0;
const support = parseFloat(data.support) || 0;
const cryptoImpact = data.crypto_impact || 'NEUTRO';
const timeframe = data.timeframe || 'H4';
const alertType = data.type || 'usdt_d_update';
const level = data.level || '';

// Determinar se é um alerta de nível S/R
const isAlert = alertType.includes('alert');
const nearEMA200 = data.near_ema_200 === true || data.near_ema_200 === 'true';
const nearResistance = data.near_resistance === true || data.near_resistance === 'true';
const nearSupport = data.near_support === true || data.near_support === 'true';

// Determinar emoji e cor baseado no impacto
let impactEmoji = '🟡';
let impactText = 'Neutro';
if (cryptoImpact === 'BULLISH') {
  impactEmoji = '🟢';
  impactText = 'BULLISH para Cripto';
} else if (cryptoImpact === 'BEARISH') {
  impactEmoji = '🔴';
  impactText = 'BEARISH para Cripto';
}

// Determinar nível mais próximo
let nearestLevel = '';
let nearestLevelName = '';
if (nearEMA200) {
  nearestLevel = ema200;
  nearestLevelName = 'EMA 200';
} else if (nearResistance) {
  nearestLevel = resistance;
  nearestLevelName = 'Resistência';
} else if (nearSupport) {
  nearestLevel = support;
  nearestLevelName = 'Suporte';
}

// Calcular distâncias
const distToEMA200 = Math.abs(dominance - ema200);
const distToEMA200Pct = ((distToEMA200 / ema200) * 100).toFixed(3);

return {
  dominance,
  ema9,
  ema21,
  ema200,
  resistance,
  support,
  cryptoImpact,
  impactEmoji,
  impactText,
  timeframe,
  alertType,
  isAlert,
  nearEMA200,
  nearResistance,
  nearSupport,
  nearestLevel,
  nearestLevelName,
  distToEMA200,
  distToEMA200Pct,
  level,
  belowEMA200: dominance < ema200,
  belowEMA21: dominance < ema21,
  belowEMA9: dominance < ema9,
  timestamp: new Date().toISOString()
};
```

### **Template Telegram (ATUALIZADO):**

```
🚨 <b>ALERTA USDT.D</b> 🚨

______________________________

📊 <b>USDT Dominance:</b> {{ $json.dominance }}%
⏱ <b>Timeframe:</b> {{ $json.timeframe }}
📍 <b>Status:</b> Próximo de <b>{{ $json.nearestLevelName }}</b> importante

🎯 <b>Nível S/R:</b> {{ $json.nearestLevel }}%
📏 <b>Distância:</b> {{ $json.distToEMA200 }}% ({{ $json.distToEMA200Pct }}% de distância)

{{ $json.impactEmoji }} <b>Impacto Cripto:</b> {{ $json.impactText }}

📈 <b>Posição das EMAs:</b>
• EMA 9: {{ $json.ema9 }}% {{ $json.belowEMA9 ? '✅ (Acima)' : '❌ (Abaixo)' }}
• EMA 21: {{ $json.ema21 }}% {{ $json.belowEMA21 ? '✅ (Acima)' : '❌ (Abaixo)' }}
• EMA 200: {{ $json.ema200 }}% {{ $json.belowEMA200 ? '✅ (Acima)' : '❌ (Abaixo)' }}

💡 <i>USDT.D é INVERSAMENTE proporcional ao mercado cripto.</i>
<i>Abaixo das EMAs = dinheiro entrando em cripto (BULLISH)</i>
<i>Acima das EMAs = dinheiro saindo de cripto (BEARISH)</i>

⚠️ <i>Verifique o gráfico para confirmar a ação.</i>
```

---

## 📖 INTERPRETAÇÃO DOS ALERTAS {#interpretação}

### **Cenário 1: USDT.D Próximo de Resistência**

```
📊 USDT Dominance: 5.23%
📍 Status: Próximo de Resistência importante
🎯 Nível S/R: 5.35%
📏 Distância: 0.12% (2.3% de distância)
🔴 Impacto Cripto: BEARISH para Cripto
```

**Interpretação:**
- USDT.D subindo em direção a uma resistência
- Se romper a resistência = Mais dinheiro em stablecoins = BEARISH para cripto
- Se rejeitar a resistência = Pode voltar a cair = BULLISH para cripto

**Ação Sugerida:**
- Aguardar reação no nível de resistência
- Se rejeitar: Considerar LONGs em cripto
- Se romper: Considerar SHORTs ou ficar de fora

---

### **Cenário 2: USDT.D Próximo de Suporte**

```
📊 USDT Dominance: 5.05%
📍 Status: Próximo de Suporte importante
🎯 Nível S/R: 5.00%
📏 Distância: 0.05% (1.0% de distância)
🟢 Impacto Cripto: BULLISH para Cripto
```

**Interpretação:**
- USDT.D caindo em direção a um suporte
- Se romper o suporte = Menos dinheiro em stablecoins = BULLISH para cripto
- Se rejeitar o suporte = Pode voltar a subir = BEARISH para cripto

**Ação Sugerida:**
- Aguardar reação no nível de suporte
- Se romper: Considerar LONGs agressivos em cripto
- Se rejeitar: Considerar SHORTs ou cautela

---

### **Cenário 3: USDT.D Abaixo das EMAs**

```
📈 Posição das EMAs:
• EMA 9: 5.10% ✅ (Acima)
• EMA 21: 5.15% ✅ (Acima)
• EMA 200: 5.30% ✅ (Acima)
```

**Interpretação:**
- USDT.D está abaixo de todas as EMAs
- Dinheiro saindo de stablecoins
- **BULLISH para cripto**

**Ação Sugerida:**
- Ambiente favorável para LONGs
- Evitar SHORTs
- Buscar setups de continuação de alta

---

### **Cenário 4: USDT.D Acima das EMAs**

```
📈 Posição das EMAs:
• EMA 9: 5.10% ❌ (Abaixo)
• EMA 21: 5.15% ❌ (Abaixo)
• EMA 200: 5.30% ❌ (Abaixo)
```

**Interpretação:**
- USDT.D está acima de todas as EMAs
- Dinheiro entrando em stablecoins
- **BEARISH para cripto**

**Ação Sugerida:**
- Ambiente favorável para SHORTs
- Evitar LONGs
- Buscar setups de continuação de baixa

---

## ✅ STATUS DE IMPLEMENTAÇÃO

- ✅ Pine Script funcionando
- ✅ Integração n8n atualizada
- ✅ Código JavaScript corrigido
- ✅ Template Telegram completo
- ✅ Alertas com informações completas
- ✅ Sistema 100% automatizado

---

## 📊 EXEMPLO DE ALERTA COMPLETO

```
🚨 ALERTA USDT.D 🚨

______________________________

📊 USDT Dominance: 5.23%
⏱ Timeframe: 4H
📍 Status: Próximo de Resistência importante

🎯 Nível S/R: 5.35%
📏 Distância: 0.12% (2.3% de distância)

🔴 Impacto Cripto: BEARISH para Cripto

📈 Posição das EMAs:
• EMA 9: 5.10% ❌ (Abaixo)
• EMA 21: 5.15% ❌ (Abaixo)
• EMA 200: 5.30% ❌ (Abaixo)

💡 USDT.D é INVERSAMENTE proporcional ao mercado cripto.
Abaixo das EMAs = dinheiro entrando em cripto (BULLISH)
Acima das EMAs = dinheiro saindo de cripto (BEARISH)

⚠️ Verifique o gráfico para confirmar a ação.
```

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 10/01/2026  
**Versão:** 2.0
