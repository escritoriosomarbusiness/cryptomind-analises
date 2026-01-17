// ============================================
// PROCESSADOR STS v1.0 - n8n
// CryptoMind IA - Stormer Trap Setup
// ============================================

// Parse do JSON recebido do TradingView
const data = JSON.parse($input.item.json.body);

// Extrair campos do alerta
const status = data.status; // "TRIGGER" ou "CONFIRMED"
const symbol = data.symbol;
const direction = data.direction; // "LONG" ou "SHORT"
const timeframe = data.timeframe;
const setupQuality = data.setupQuality; // "PREMIUM", "CONTRA", "CAUTELA"
const htfTrend = data.htfTrend; // "ALTA", "BAIXA", "NEUTRO"
const htfTimeframe = data.htfTimeframe;
const fishingType = data.fishingType; // "NONE", "BOTTOM", "TOP"
const confluence = data.confluence; // "Simples", "Dupla ⭐", "Tripla 🌟🌟"
const rejectionZones = data.rejectionZones; // "SR,Fibo,EMA"
const emasRejected = data.emasRejected; // "89,144"
const emasCount = data.emasCount; // 2
const wickToBodyRatio = data.wickToBodyRatio; // 2.8

// Preços
const price = status === "TRIGGER" ? data.price : data.entry;
const trigger = data.trigger || null;
const sl = data.sl;
const tp1 = data.tp1;
const tp2 = data.tp2;

// ============================================
// FORMATAÇÃO DO BLOCO MTF
// ============================================
let macroBlock = "";

if (setupQuality === "PREMIUM") {
    macroBlock = `━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 ${htfTimeframe} em tendência de ${htfTrend} favorável
━━━━━━━━━━━━━━━━━━
💡 ${direction === "LONG" ? "Continuação de tendência" : "Continuação de tendência"}`;
} else if (setupQuality === "CONTRA") {
    const fishingEmoji = fishingType === "BOTTOM" ? "🎣" : fishingType === "TOP" ? "🎣" : "";
    const fishingText = fishingType === "BOTTOM" ? "BOTTOM FISHING" : fishingType === "TOP" ? "TOP FISHING" : "CONTRA TENDÊNCIA";
    const fishingDescription = fishingType === "BOTTOM" ? "Pescando reversão no FUNDO" : fishingType === "TOP" ? "Pescando reversão no TOPO" : "Contra tendência macro";
    
    macroBlock = `━━━━━━━━━━━━━━━━━━
⚠️${fishingEmoji} ${fishingText} ${fishingEmoji}⚠️
📉 ${htfTimeframe} em tendência de ${htfTrend}
${fishingEmoji} ${fishingDescription}
━━━━━━━━━━━━━━━━━━
🛑 ALTO RISCO - Contra tendência macro
💡 Apenas para traders experientes`;
}

// ============================================
// FORMATAÇÃO DAS VALIDAÇÕES
// ============================================
let validationsBlock = "";

// Candle Martelo
validationsBlock += `✅ Candle ${direction === "LONG" ? "Martelo" : "Martelo Invertido"}: Pavio ${wickToBodyRatio}x corpo\n`;

// Zonas de Rejeição
const zonesArray = rejectionZones.split(",");
let zonesText = "";

if (zonesArray.includes("SR")) zonesText += "Suporte HTF + ";
if (zonesArray.includes("Fibo")) zonesText += "Golden Zone + ";
if (zonesArray.includes("EMA")) {
    if (emasCount === 1) {
        zonesText += `EMA ${emasRejected}`;
    } else if (emasCount === 2) {
        zonesText += `EMA ${emasRejected} 🟡`;
    } else if (emasCount >= 3) {
        zonesText += `EMA ${emasRejected} 🔴`;
    }
}

// Remover último " + "
if (zonesText.endsWith(" + ")) {
    zonesText = zonesText.slice(0, -3);
}

validationsBlock += `✅ Rejeição: ${zonesText}\n`;

// Confluência
if (confluence === "Dupla ⭐") {
    validationsBlock += `⭐⭐ Confluência DUPLA`;
} else if (confluence === "Tripla 🌟🌟") {
    validationsBlock += `🌟🌟 Confluência TRIPLA`;
} else {
    validationsBlock += `⭐ Confluência SIMPLES`;
}

// Adicionar destaque para múltiplas EMAs
if (emasCount >= 2) {
    validationsBlock += `\n💪 BARREIRA EMA ${emasCount === 2 ? "DUPLA" : "TRIPLA"}`;
    if (emasCount >= 3) {
        validationsBlock += `\n🚀 Probabilidade MUITO ALTA`;
    }
}

// ============================================
// FORMATAÇÃO DA GESTÃO DE RISCO
// ============================================
const riskDistance = Math.abs(parseFloat(trigger || price) - parseFloat(sl));
const riskPercent = (riskDistance / parseFloat(price) * 100).toFixed(2);

// Alavancagem sugerida
const leverage = setupQuality === "PREMIUM" ? "3x" : "2x (REDUZIDA)";

const riskBlock = `⚖️ Alavancagem sugerida: ${leverage}
📊 Risco: ${riskPercent}%
━━━━━━━━━━━━━━━━━━
📋 GESTÃO:
1️⃣ TP1: Realizar 50% + Mover SL para entrada (breakeven)
2️⃣ TP2: Ativar trailing stop nos 50% restantes`;

// ============================================
// MENSAGEM FINAL
// ============================================
let message = "";

if (status === "TRIGGER") {
    // MENSAGEM DE GATILHO
    const directionEmoji = direction === "LONG" ? "🟢" : "🔴";
    
    message = `🔔 ${directionEmoji} ${direction} ${symbol}
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO
📊 Setup: STS by CryptoMind
⏱ Timeframe: ${timeframe}
${confluence.includes("⭐") ? confluence : "⭐ " + confluence}

${macroBlock}

━━━━━━━━━━━━━━━━━━
💰 Preço: $${parseFloat(price).toFixed(2)}
🎯 Trigger: $${parseFloat(trigger).toFixed(2)}
━━━━━━━━━━━━━━━━━━
📊 VALIDAÇÕES:
${validationsBlock}
━━━━━━━━━━━━━━━━━━
⚠️ Aguardando rompimento do trigger${setupQuality === "CONTRA" ? "\n⚠️ ATENÇÃO: Opera contra a tendência macro" : ""}`;

} else if (status === "CONFIRMED") {
    // MENSAGEM DE CONFIRMAÇÃO
    const directionEmoji = direction === "LONG" ? "🟢" : "🔴";
    
    message = `✅ ${directionEmoji} ${direction} ${symbol}
━━━━━━━━━━━━━━━━━━
✅ CONFIRMADO POR ROMPIMENTO
📊 Setup: STS by CryptoMind
⏱ Timeframe: ${timeframe}
${confluence.includes("⭐") ? confluence : "⭐ " + confluence}

${macroBlock}

━━━━━━━━━━━━━━━━━━
🎯 Entrada: $${parseFloat(price).toFixed(2)}
🛑 Stop Loss: $${parseFloat(sl).toFixed(2)}
✅ TP1 (1R): $${parseFloat(tp1).toFixed(2)} (Parcial 50% + SL para entrada)
✅ TP2 (2R): $${parseFloat(tp2).toFixed(2)} (Trailing Stop)
━━━━━━━━━━━━━━━━━━
${riskBlock}
━━━━━━━━━━━━━━━━━━${setupQuality === "CONTRA" ? "\n⚠️ OPERA CONTRA A TENDÊNCIA MACRO" : ""}
⚠️ Não é recomendação de investimento`;
}

// ============================================
// RETORNAR MENSAGEM FORMATADA
// ============================================
return {
    json: {
        message: message,
        symbol: symbol,
        direction: direction,
        timeframe: timeframe,
        setupQuality: setupQuality,
        fishingType: fishingType,
        status: status
    }
};
