// ============================================
// TRS PROCESSADOR v7.2 - WEBHOOK n8n (FINAL)
// ============================================
// Receber dados do webhook
const body = $input.first().json.body;

// Tentar parsear JSON se vier como string
let alertData;
try {
  alertData = typeof body === 'string' ? JSON.parse(body) : body;
} catch (e) {
  alertData = body;
}

// ============================================
// EXTRAIR INFORMAÇÕES DO TRS v7.0
// ============================================
const symbol = alertData.symbol || 'N/A';
const action = alertData.action || 'CONFIRMED';
const direction = alertData.direction || 'N/A';
const timeframe = alertData.timeframe || 'N/A';
const validation = alertData.validation || '';
const setupQuality = alertData.setupQuality || 'CAUTELA';
const htfTrend = alertData.htfTrend || 'NEUTRA';
const htfTimeframe = alertData.htfTimeframe || 'N/A';

// Para TRIGGER: usar "price"
// Para CONFIRMED: usar "entry"
const price = action === 'TRIGGER' ? alertData.price : alertData.entry;

// Campos específicos de CONFIRMED
const stopLoss = alertData.stopLoss || 'N/A';
const target1 = alertData.target1 || 'N/A';
const target2 = alertData.target2 || 'N/A';
const riskPercent = alertData.riskPercent || 'N/A';
const leverage = '3'; // Alavancagem sugerida fixa

// ============================================
// DETERMINAR TIPO DE MOEDA (BTC ou ALT)
// ============================================
const isBTC = symbol.toUpperCase().includes('BTC');
const moedaTipo = isBTC ? 'BTC' : 'ALTS';

// ============================================
// FORMATAR VALIDAÇÃO (CONFLUÊNCIA)
// ============================================
let validationText = '';
if (validation) {
  // Contar quantos validadores (SR, RSI, FIB)
  const validationCount = (validation.match(/\+/g) || []).length + 1;
  
  if (validationCount >= 3) {
    validationText = '🌟🌟 Confluência TRIPLA (' + validation + ')';
  } else if (validationCount === 2) {
    validationText = '⭐ Confluência DUPLA (' + validation + ')';
  } else {
    validationText = '• Validação: ' + validation;
  }
}

// ============================================
// FORMATAR CLASSIFICAÇÃO DO SETUP (MTF)
// ============================================
let qualityEmoji = '';
let qualityMessage = '';

if (setupQuality === 'PREMIUM') {
  qualityEmoji = '⭐⭐⭐';
  qualityMessage = `${qualityEmoji} <b>SETUP PREMIUM</b> ${qualityEmoji}\n`;
  qualityMessage += `📈 ${htfTimeframe} em tendência de ${htfTrend} favorável\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `💡 Alta probabilidade de sucesso`;
} else if (setupQuality === 'CAUTELA') {
  qualityEmoji = '⚠️';
  qualityMessage = `${qualityEmoji} <b>CAUTELA RECOMENDADA</b> ${qualityEmoji}\n`;
  qualityMessage += `📊 ${htfTimeframe} sem tendência definida\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⚠️ Fractal superior neutro - Risco elevado`;
} else if (setupQuality === 'CONTRA') {
  qualityEmoji = '🚫';
  qualityMessage = `${qualityEmoji} <b>CONTRA-TENDÊNCIA</b> ${qualityEmoji}\n`;
  qualityMessage += `📉 ${htfTimeframe} em tendência de ${htfTrend}\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⛔ ALTO RISCO - Operação contra o fluxo maior\n`;
  qualityMessage += `⚠️ Não recomendado para iniciantes`;
} else if (setupQuality === 'SEM_VALIDACAO_MTF') {
  qualityEmoji = '📊';
  qualityMessage = `${qualityEmoji} <b>SEM VALIDAÇÃO MTF</b> ${qualityEmoji}\n`;
  qualityMessage += `📉 ${htfTimeframe}: Dados insuficientes\n`;
  qualityMessage += `━━━━━━━━━━━━━━━━━━\n`;
  qualityMessage += `⚠️ Ativo sem histórico suficiente no fractal superior\n`;
  qualityMessage += `💡 Operação permitida, mas sem confirmação de tendência MTF`;
}

// ============================================
// FORMATAR MENSAGEM PARA TELEGRAM
// ============================================
let emoji = direction === 'LONG' || direction.includes('LONG') ? '🟢' : '🔴';
let statusEmoji = action === 'TRIGGER' ? '🔔' : '✅';
let statusText = action === 'TRIGGER' ? 'GATILHO ARMADO' : 'CONFIRMADO POR ROMPIMENTO';

let message = '';

// ============================================
// MENSAGEM PARA GATILHO (TRIGGER)
// ============================================
if (action === 'TRIGGER') {
  message = `${statusEmoji} ${emoji} <b>${direction} ${symbol}</b>\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `🔔 <b>${statusText}</b>\n`;
  message += `📊 Setup: TRS\n`;
  message += `⏱ Timeframe: ${timeframe}\n`;
  if (validationText) message += `${validationText}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  if (qualityMessage) message += `${qualityMessage}\n━━━━━━━━━━━━━━━━━━\n`;
  message += `💰 Preço: $${price}\n`;
  message += `⚠️ Aguardando confirmação por rompimento\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `⚠️ <i>Não é recomendação de investimento</i>`;
}
// ============================================
// MENSAGEM PARA CONFIRMAÇÃO (CONFIRMED)
// ============================================
else {
  message = `${statusEmoji} ${emoji} <b>${direction} ${symbol}</b>\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `✅ <b>${statusText}</b>\n`;
  message += `📊 Setup: TRS\n`;
  message += `⏱ Timeframe: ${timeframe}\n`;
  if (validationText) message += `${validationText}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  if (qualityMessage) message += `${qualityMessage}\n━━━━━━━━━━━━━━━━━━\n`;
  message += `🎯 Entrada: $${price}\n`;
  message += `🛑 Stop Loss: $${stopLoss}\n`;
  message += `✅ TP1: $${target1}\n`;
  message += `✅ TP2: $${target2}\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `⚖️ Alavancagem sugerida: ${leverage}x\n`;
  message += `📊 Risco: ${riskPercent}%\n`;
  message += `━━━━━━━━━━━━━━━━━━\n`;
  message += `⚠️ <i>Não é recomendação de investimento</i>`;
}

// ============================================
// RETORNAR DADOS PROCESSADOS
// ============================================
return {
  symbol: symbol,
  action: action,
  direction: direction,
  moedaTipo: moedaTipo,
  timeframe: timeframe,
  message: message,
  alertData: alertData
};