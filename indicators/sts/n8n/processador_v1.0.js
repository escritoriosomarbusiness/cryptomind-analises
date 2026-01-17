// ============================================
// STS PROCESSADOR v1.0 - PADRÃO DNP/TRS
// ============================================
// Extrair dados do webhook
const body = $input.first().json.body;
const alertData = typeof body === 'string' ? JSON.parse(body) : body;

// Dados básicos
const symbol = alertData.symbol || 'N/A';
const action = alertData.action || 'CONFIRMED';
const direction = alertData.direction || 'LONG';
const timeframe = alertData.timeframe || 'N/A';
const price = alertData.price || alertData.entry || 'N/A';

// Dados de gestão
const stopLoss = alertData.stopLoss || 'N/A';
const target1 = alertData.target1 || 'N/A';
const target2 = alertData.target2 || 'N/A';
const risk = alertData.risk || 'N/A';
const riskPercent = alertData.riskPercent || 'N/A';
const trailingDistance = alertData.trailingDistance || 'N/A';

// Dados específicos do STS
const wickToBodyRatio = alertData.wickToBodyRatio || 'N/A';
const confluence = alertData.confluence || 'Simples';
const rejectionZones = alertData.rejectionZones || '';
const emasRejected = alertData.emasRejected || '';
const emasCount = alertData.emasCount || 0;

// MTF
const setupQuality = alertData.setupQuality || 'CAUTELA';
const htfTrend = alertData.htfTrend || 'NEUTRO';
const htfTimeframe = alertData.htfTimeframe || 'N/A';
const fishingType = alertData.fishingType || 'NONE';

// Calcular alavancagem baseada no setupQuality
let leverage = setupQuality === 'PREMIUM' ? '3x' : '2x (REDUZIDA)';

// Emoji baseado na direção
const emoji = direction === 'LONG' ? '🟢' : '🔴';

// ============================================
// FORMATAR CLASSIFICAÇÃO DO SETUP (MTF)
// ============================================
let qualityMessage = '';

if (setupQuality === 'PREMIUM') {
  qualityMessage = `⭐⭐⭐ <b>SETUP PREMIUM</b> ⭐⭐⭐\n`;
  qualityMessage += `📈 ${htfTimeframe} em tendência de ${htfTrend} favorável\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `💡 ${direction === "LONG" ? "Continuação de tendência" : "Continuação de tendência"}`;
} else if (setupQuality === 'CONTRA') {
  const fishingEmoji = fishingType === 'BOTTOM' ? '🎣' : fishingType === 'TOP' ? '🎣' : '';
  const fishingText = fishingType === 'BOTTOM' ? 'BOTTOM FISHING' : fishingType === 'TOP' ? 'TOP FISHING' : 'CONTRA TENDÊNCIA';
  const fishingDescription = fishingType === 'BOTTOM' ? 'Pescando reversão no FUNDO' : fishingType === 'TOP' ? 'Pescando reversão no TOPO' : 'Contra tendência macro';
  
  qualityMessage = `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⚠️${fishingEmoji} ${fishingText} ${fishingEmoji}⚠️\n`;
  qualityMessage += `📉 ${htfTimeframe} em tendência de ${htfTrend}\n`;
  qualityMessage += `${fishingEmoji} ${fishingDescription}\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `🛑 ALTO RISCO - Contra tendência macro\n`;
  qualityMessage += `💡 Apenas para traders experientes`;
} else if (setupQuality === 'CAUTELA') {
  qualityMessage = `⚠️ <b>CAUTELA RECOMENDADA</b> ⚠️\n`;
  qualityMessage += `📊 ${htfTimeframe} sem tendência definida\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⚠️ Fractal superior neutro - Risco elevado`;
}

// ============================================
// FORMATAR VALIDAÇÕES
// ============================================
let validationsBlock = '';

// Candle Martelo
validationsBlock += `✅ Candle ${direction === 'LONG' ? 'Martelo' : 'Martelo Invertido'}: Pavio ${wickToBodyRatio}x corpo\n`;

// Zonas de Rejeição
const zonesArray = rejectionZones.split(',');
let zonesText = '';

if (zonesArray.includes('SR')) zonesText += 'Suporte HTF + ';
if (zonesArray.includes('Fibo')) zonesText += 'Golden Zone + ';
if (zonesArray.includes('EMA')) {
  if (emasCount === 1) {
    zonesText += `EMA ${emasRejected}`;
  } else if (emasCount === 2) {
    zonesText += `EMA ${emasRejected} 🟡`;
  } else if (emasCount >= 3) {
    zonesText += `EMA ${emasRejected} 🔴`;
  }
}

// Remover último " + "
if (zonesText.endsWith(' + ')) {
  zonesText = zonesText.slice(0, -3);
}

validationsBlock += `✅ Rejeição: ${zonesText}\n`;

// Confluência
if (confluence === 'Dupla ⭐') {
  validationsBlock += `⭐⭐ Confluência DUPLA`;
} else if (confluence === 'Tripla 🌟🌟') {
  validationsBlock += `🌟🌟 Confluência TRIPLA`;
} else {
  validationsBlock += `⭐ Confluência SIMPLES`;
}

// Adicionar destaque para múltiplas EMAs
if (emasCount >= 2) {
  validationsBlock += `\n💪 BARREIRA EMA ${emasCount === 2 ? 'DUPLA' : 'TRIPLA'}`;
  if (emasCount >= 3) {
    validationsBlock += `\n🚀 Probabilidade MUITO ALTA`;
  }
}

// ============================================
// FORMATAR GESTÃO DE RISCO
// ============================================
const riskBlock = `⚖️ Alavancagem sugerida: ${leverage}
📊 Risco: ${riskPercent}%
━━━━━━━━━━━━━━━━━━
📋 GESTÃO:
1️⃣ TP1: Realizar 50% + Mover SL para entrada (breakeven)
2️⃣ TP2: Ativar trailing stop nos 50% restantes`;

// ============================================
// CONSTRUIR MENSAGEM
// ============================================
let message = '';

// ============================================
// TRIGGER (GATILHO ARMADO)
// ============================================
if (action === 'TRIGGER') {
  const trigger = alertData.triggerHigh || alertData.triggerLow || price;
  
  message = `🔔 ${emoji} <b>${direction} ${symbol}</b>\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `🔔 <b>GATILHO ARMADO</b>\n`;
  message += `📊 Setup: STS by CryptoMind\n`;
  message += `⏱ Timeframe: ${timeframe}\n`;
  message += `${confluence.includes('⭐') || confluence.includes('🌟') ? confluence : '⭐ ' + confluence}\n`;
  message += `\n`;
  if (qualityMessage) message += `${qualityMessage}\n`;
  message += `\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `💰 Preço: $${parseFloat(price).toFixed(2)}\n`;
  message += `🎯 Trigger: $${parseFloat(trigger).toFixed(2)}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `📊 VALIDAÇÕES:\n`;
  message += `${validationsBlock}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `⚠️ Aguardando rompimento do trigger`;
  if (setupQuality === 'CONTRA') {
    message += `\n⚠️ ATENÇÃO: Opera contra a tendência macro`;
  }
}

// ============================================
// CONFIRMED (CONFIRMADO POR ROMPIMENTO)
// ============================================
else if (action === 'CONFIRMED') {
  message = `✅ ${emoji} <b>${direction} ${symbol}</b>\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `✅ <b>CONFIRMADO POR ROMPIMENTO</b>\n`;
  message += `📊 Setup: STS by CryptoMind\n`;
  message += `⏱ Timeframe: ${timeframe}\n`;
  message += `${confluence.includes('⭐') || confluence.includes('🌟') ? confluence : '⭐ ' + confluence}\n`;
  message += `\n`;
  if (qualityMessage) message += `${qualityMessage}\n`;
  message += `\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `🎯 Entrada: $${parseFloat(price).toFixed(2)}\n`;
  message += `🛑 Stop Loss: $${parseFloat(stopLoss).toFixed(2)}\n`;
  message += `✅ TP1 (1R): $${parseFloat(target1).toFixed(2)} (Parcial 50% + SL para entrada)\n`;
  message += `✅ TP2 (2R): $${parseFloat(target2).toFixed(2)} (Trailing Stop)\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `${riskBlock}\n`;
  message += `━━━━━━━━━━━━━━━━━━`;
  if (setupQuality === 'CONTRA') {
    message += `\n⚠️ OPERA CONTRA A TENDÊNCIA MACRO`;
  }
  message += `\n⚠️ Não é recomendação de investimento`;
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
    action: action
  }
};
