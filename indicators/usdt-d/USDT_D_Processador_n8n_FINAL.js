// ============================================
// PROCESSADOR N8N - USDT.D MONITOR v11.0 (FINAL)
// ============================================
// Processa alertas do USDT.D Monitor v11.0 (LuxAlgo Edition)
// Interpreta 6 tipos de cenários:
// 1. Touch Regular High (Resistência)
// 2. Touch Regular Low (Suporte)
// 3. Touch Missed High (Reteste de topo intermediário)
// 4. Touch Missed Low (Reteste de fundo intermediário)
// 5. Break Regular High (Rompimento de resistência)
// 6. Break Regular Low (Rompimento de suporte)

const data = $input.all();

function processAlert(item) {
  // Tratamento robusto de JSON
  let payload;
  
  try {
    const body = item.json.body;
    
    if (typeof body === 'string') {
      payload = JSON.parse(body);
    } else if (typeof body === 'object' && body !== null) {
      payload = body;
    } else {
      payload = item.json;
    }
  } catch (error) {
    payload = item.json;
  }
  
  // Extrair dados do alerta com valores default
  const action = payload.action || 'UNKNOWN';
  const timeframe = payload.timeframe || '60';
  const eventType = payload.eventType || 'TOUCH';
  const dominance = payload.dominance || 0;
  const timestamp = payload.timestamp || new Date().toISOString();
  
  // Extrair pivotInfo com validação
  const pivotInfo = payload.pivotInfo || {};
  const pivotType = pivotInfo.type || 'REGULAR';
  const direction = pivotInfo.direction || 'HIGH';
  const level = pivotInfo.level || 0;
  const pivotLength = pivotInfo.pivotLength || 50;
  
  // Converter timeframe numérico para legível
  const tfMap = {
    "60": "H1",
    "240": "H4",
    "D": "D1",
    "W": "W1",
    "M": "M"
  };
  
  const tfReadable = tfMap[timeframe] || timeframe;
  
  // Variáveis para mensagem
  let emoji = "";
  let titulo = "";
  let subtitulo = "";
  let descricao = "";
  let impacto = "";
  
  // ============================================
  // LÓGICA DE CENÁRIOS
  // ============================================
  
  if (eventType === "TOUCH") {
    // ========== TOQUE EM NÍVEL ==========
    
    if (pivotType === "REGULAR") {
      // PIVOTS REGULARES
      
      if (direction === "HIGH") {
        // CENÁRIO 1: TOQUE EM RESISTÊNCIA REGULAR
        emoji = "🟡";
        titulo = "RESISTÊNCIA DETECTADA";
        subtitulo = "📊 POSSÍVEL FUNDO NAS CRIPTOS";
        descricao = `📈 USDT.D tocou resistência automática\nTimeframe: ${tfReadable} | Nível: ${level.toFixed(4)}%\nPivot detectado (Length ${pivotLength})\n🔄 Pode respeitar e cair (USDT)\n💚 Criptos podem fazer fundo e subir`;
        impacto = "👀 Atenção: Aguardar confirmação de rejeição";
      } else {
        // CENÁRIO 2: TOQUE EM SUPORTE REGULAR
        emoji = "🟠";
        titulo = "SUPORTE DETECTADO";
        subtitulo = "📊 POSSÍVEL TOPO NAS CRIPTOS";
        descricao = `📉 USDT.D tocou suporte automático\nTimeframe: ${tfReadable} | Nível: ${level.toFixed(4)}%\nPivot detectado (Length ${pivotLength})\n🔄 Pode respeitar e subir (USDT)\n🔴 Criptos podem fazer topo e cair`;
        impacto = "⚠️ Cautela: Aguardar confirmação de rejeição";
      }
      
    } else if (pivotType === "MISSED") {
      // REVERSÕES PERDIDAS (MISSED REVERSALS)
      
      if (direction === "HIGH") {
        // CENÁRIO 3: RETESTE DE TOPO INTERMEDIÁRIO
        emoji = "👻";
        titulo = "RETESTE DE NÍVEL INTERMEDIÁRIO";
        subtitulo = "⚡ TOPO INTERMEDIÁRIO IMPORTANTE";
        descricao = `📈 USDT.D retestando topo intermediário\nTimeframe: ${tfReadable} | Nível: ${level.toFixed(4)}%\n🔍 Reversão detectada pelo algoritmo LuxAlgo\n🎯 Pode atuar como resistência temporária\n💡 Nível ignorado por pivots tradicionais`;
        impacto = "🔍 Insight: Monitorar reação do preço neste ponto";
      } else {
        // CENÁRIO 4: RETESTE DE FUNDO INTERMEDIÁRIO
        emoji = "👻";
        titulo = "RETESTE DE NÍVEL INTERMEDIÁRIO";
        subtitulo = "⚡ FUNDO INTERMEDIÁRIO IMPORTANTE";
        descricao = `📉 USDT.D retestando fundo intermediário\nTimeframe: ${tfReadable} | Nível: ${level.toFixed(4)}%\n🔍 Reversão detectada pelo algoritmo LuxAlgo\n🎯 Pode atuar como suporte temporário\n💡 Nível ignorado por pivots tradicionais`;
        impacto = "🔍 Insight: Monitorar reação do preço neste ponto";
      }
    }
    
  } else if (eventType === "BREAK") {
    // ========== ROMPIMENTO DE NÍVEL ==========
    
    if (direction === "HIGH") {
      // CENÁRIO 5: ROMPIMENTO DE RESISTÊNCIA
      emoji = "⚠️🔴";
      titulo = "RESISTÊNCIA ROMPIDA!";
      subtitulo = "🚨 ALERTA DE PANIC SELL NAS CRIPTOS!";
      descricao = `📈 USDT.D rompeu resistência ${level.toFixed(4)}%\nTimeframe: ${tfReadable} | Pivot confirmado\n💸 Dinheiro entrando em stablecoins\n📉 Possível correção forte nas criptos`;
      impacto = "⚠️ Cautela: Risco de queda acentuada";
      
    } else {
      // CENÁRIO 6: ROMPIMENTO DE SUPORTE
      emoji = "🔥🚀";
      titulo = "SUPORTE ROMPIDO!";
      subtitulo = "⚡ FRENESI DE ALTA NAS CRIPTOS!";
      descricao = `📉 USDT.D rompeu suporte ${level.toFixed(4)}%\nTimeframe: ${tfReadable} | Pivot confirmado\n💰 Dinheiro saindo de stablecoins\n🚀 Possível rally altista nas criptos`;
      impacto = "💡 Oportunidade: Momentum de alta confirmado";
    }
  }
  
  // Construir mensagem formatada
  const message = `${emoji} ${titulo}
━━━━━━━━━━━━━━━━━━
${subtitulo}

${descricao}
━━━━━━━━━━━━━━━━━━
${impacto}
━━━━━━━━━━━━━━━━━━
⚠️ Não é recomendação de investimento`;

  return {
    json: {
      message: message,
      eventType: eventType,
      pivotType: pivotType,
      direction: direction,
      timeframe: tfReadable,
      level: level,
      pivotLength: pivotLength,
      dominance: dominance,
      emoji: emoji,
      timestamp: timestamp
    }
  };
}

// Processar todos os itens
return data.map(processAlert);
