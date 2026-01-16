// ============================================
// DNP PROCESSADOR v2.0 - COM MTF (FINAL)
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

// Indicadores
const adx = alertData.adx || 'N/A';
const remi = alertData.remi || 'N/A';

// MTF - NOVO v2.0
const setupQuality = alertData.setupQuality || 'CAUTELA';
const htfTrend = alertData.htfTrend || 'NEUTRO';
const htfTimeframe = alertData.htfTimeframe || 'N/A';

// Calcular alavancagem baseada no risco
let leverage = 'N/A';
if (riskPercent !== 'N/A') {
  const riskNum = parseFloat(riskPercent);
  if (riskNum <= 2) {
    leverage = '5-10x';
  } else if (riskNum <= 4) {
    leverage = '3-5x';
  } else {
    leverage = '2-3x';
  }
}

// Emoji baseado na direção
const emoji = direction === 'LONG' ? '🟢' : '🔴';

// Moeda tipo
const moedaTipo = symbol.includes('USDT') ? 'USDT' : 'BTC';

// ============================================
// FORMATAR CLASSIFICAÇÃO DO SETUP (MTF) - NOVO v2.0
// ============================================
let qualityMessage = '';

if (setupQuality === 'PREMIUM') {
  qualityMessage = `⭐⭐⭐ <b>SETUP PREMIUM</b> ⭐⭐⭐\n`;
  qualityMessage += `📈 ${htfTimeframe} em tendência de ${htfTrend} favorável\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `💡 Alta probabilidade de sucesso`;
} else if (setupQuality === 'CAUTELA') {
  qualityMessage = `⚠️ <b>CAUTELA RECOMENDADA</b> ⚠️\n`;
  qualityMessage += `📊 ${htfTimeframe} sem tendência definida\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⚠️ Fractal superior neutro - Risco elevado`;
} else if (setupQuality === 'CONTRA') {
  qualityMessage = `🚫 <b>CONTRA-TENDÊNCIA</b> 🚫\n`;
  qualityMessage += `📉 ${htfTimeframe} em tendência de ${htfTrend}\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⛔ ALTO RISCO - Operação contra o fluxo maior\n`;
  qualityMessage += `⚠️ Não recomendado para iniciantes`;
}

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
  message += `📊 Setup: DNP\n`;
  message += `⏱ Timeframe: ${timeframe}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  if (qualityMessage) message += `${qualityMessage}\n━━━━━━━━━━━━━━━━━━\n`;
  message += `💰 Preço: $${price}\n`;
  message += `🎯 Trigger: $${trigger}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `📈 ADX: ${adx} | REMI: ${remi}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `⚠️ <i>Aguardando confirmação por rompimento</i>\n`;
}

// ============================================
// CONFIRMED (CONFIRMADO POR ROMPIMENTO)
// ============================================
else {
  message = `✅ ${emoji} <b>${direction} ${symbol}</b>\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `✅ <b>CONFIRMADO POR ROMPIMENTO</b>\n`;
  message += `📊 Setup: DNP\n`;
  message += `⏱ Timeframe: ${timeframe}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  if (qualityMessage) message += `${qualityMessage}\n━━━━━━━━━━━━━━━━━━\n`;
  
  // SEÇÃO: ENTRADA E STOP
  message += `🎯 <b>ENTRADA</b>\n`;
  message += `💰 Preço: $${price}\n`;
  message += `🛑 Stop Loss: $${stopLoss}\n`;
  message += `📊 Risco: ${riskPercent}% ($${risk})\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  
  // SEÇÃO: ALVOS
  message += `🎯 <b>ALVOS (Risco:Retorno)</b>\n`;
  message += `✅ TP1: $${target1} (1:1)\n`;
  message += `✅ TP2: $${target2} (1:2)\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  
  // SEÇÃO: GESTÃO DO TRADE
  message += `⚙️ <b>GESTÃO DO TRADE</b>\n`;
  message += `📈 <b>Ao atingir TP1:</b>\n`;
  message += `   • Realizar 50% da posição\n`;
  message += `   • Subir stop para entrada (breakeven)\n`;
  message += `   • Ativar trailing stop\n`;
  message += `\n`;
  message += `🔄 <b>Trailing Stop:</b>\n`;
  message += `   • Distância: $${trailingDistance}\n`;
  message += `   • Seguir preço até TP2\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  
  // SEÇÃO: INDICADORES
  message += `📊 <b>INDICADORES</b>\n`;
  message += `📈 ADX: ${adx} | REMI: ${remi}\n`;
  message += `⚖️ Alavancagem sugerida: ${leverage}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
}

// Aviso final
message += `⚠️ <i>Não é recomendação de investimento</i>\n`;

// ============================================
// RETORNAR DADOS (FORMATO CORRETO N8N!)
// ⚠️ CORREÇÃO CRÍTICA: Adicionar wrapper "json"
// ============================================
return {
  json: {
    symbol: symbol,
    action: action,
    direction: direction,
    moedaTipo: moedaTipo,
    timeframe: timeframe,
    message: message,
    alertData: alertData
  }
};
