// ============================================
// PROCESSADOR N8N - USDT.D MONITOR v12.0 (8 CENÁRIOS CORRETOS)
// ============================================
// Processa alertas do USDT.D Monitor v12.0 (LuxAlgo Edition)
// Interpreta 8 tipos de cenários:
// 1. Touch Regular High (Resistência ativa)
// 2. Touch Regular Low (Suporte ativo)
// 3. Touch Missed High (Reteste de resistência ex-suporte)
// 4. Touch Missed Low (Reteste de suporte ex-resistência)
// 5. Break Regular High (Rompimento de resistência)
// 6. Break Regular Low (Rompimento de suporte)
// 7. Break Missed High (Rompimento de resistência ex-suporte)
// 8. Break Missed Low (Rompimento de suporte ex-resistência)

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
  // LÓGICA DE CENÁRIOS (8 CENÁRIOS CORRETOS)
  // ============================================
  
  if (eventType === "TOUCH") {
    // ========== TOQUE EM NÍVEL ==========
    
    if (pivotType === "REGULAR") {
      // PIVOTS REGULARES (Níveis ativos)
      
      if (direction === "HIGH") {
        // CENÁRIO 1: TOQUE EM RESISTÊNCIA ATIVA
        emoji = "🟡";
        titulo = "RESISTÊNCIA DETECTADA";
        subtitulo = "📊 POSSÍVEL FUNDO NAS CRIPTOS";
        descricao = `📈 USDT.D tocou resistência ativa\nNível: ${level.toFixed(4)}% | Timeframe: ${tfReadable}\nPivot confirmado (Length ${pivotLength})\n🔄 Pode respeitar e cair (USDT)\n💚 Criptos podem fazer fundo e subir`;
        impacto = "👀 Atenção: Aguardar confirmação de rejeição";
      } else {
        // CENÁRIO 2: TOQUE EM SUPORTE ATIVO
        emoji = "🟠";
        titulo = "SUPORTE DETECTADO";
        subtitulo = "📊 POSSÍVEL TOPO NAS CRIPTOS";
        descricao = `📉 USDT.D tocou suporte ativo\nNível: ${level.toFixed(4)}% | Timeframe: ${tfReadable}\nPivot confirmado (Length ${pivotLength})\n🔄 Pode respeitar e subir (USDT)\n🔴 Criptos podem fazer topo e cair`;
        impacto = "⚠️ Cautela: Aguardar confirmação de rejeição";
      }
      
    } else if (pivotType === "MISSED") {
      // MISSED REVERSALS (Níveis invertidos = Retestes)
      
      if (direction === "HIGH") {
        // CENÁRIO 3: RETESTE DE RESISTÊNCIA (ex-Suporte)
        emoji = "🔄⚠️";
        titulo = "RETESTE CONFIRMADO!";
        subtitulo = "🛑 RESISTÊNCIA VALIDADA PÓS-ROMPIMENTO";
        descricao = `📉 USDT.D retestou nível rompido\nNível: ${level.toFixed(4)}% | Timeframe: ${tfReadable}\n🔓 Ex-suporte agora é resistência\n✅ Confirmação de inversão de papel\n📊 Topo descendente confirmado\n📉 Continuação de queda no USDT\n🚀 CONTINUAÇÃO DE ALTA NAS CRIPTOS`;
        impacto = "💡 Oportunidade: Reteste confirma tendência de alta nas criptos";
      } else {
        // CENÁRIO 4: RETESTE DE SUPORTE (ex-Resistência)
        emoji = "🔄🔴";
        titulo = "RETESTE CONFIRMADO!";
        subtitulo = "💪 SUPORTE VALIDADO PÓS-ROMPIMENTO";
        descricao = `📈 USDT.D retestou nível rompido\nNível: ${level.toFixed(4)}% | Timeframe: ${tfReadable}\n🔓 Ex-resistência agora é suporte\n✅ Confirmação de inversão de papel\n📊 Fundo ascendente confirmado\n📈 Continuação de alta no USDT\n📉 CONTINUAÇÃO DE QUEDA NAS CRIPTOS`;
        impacto = "⚠️ Cautela: Reteste confirma tendência de queda nas criptos";
      }
    }
    
  } else if (eventType === "BREAK") {
    // ========== ROMPIMENTO DE NÍVEL ==========
    
    if (pivotType === "REGULAR") {
      // ROMPIMENTOS DE PIVOTS REGULARES
      
      if (direction === "HIGH") {
        // CENÁRIO 5: ROMPIMENTO DE RESISTÊNCIA ATIVA
        emoji = "⚠️🔴";
        titulo = "RESISTÊNCIA ROMPIDA!";
        subtitulo = "🚨 ALERTA DE PANIC SELL NAS CRIPTOS!";
        descricao = `📈 USDT.D rompeu resistência ${level.toFixed(4)}%\nTimeframe: ${tfReadable} | Pivot confirmado\n💸 Dinheiro entrando em stablecoins\n📉 Possível correção forte nas criptos`;
        impacto = "⚠️ Cautela: Risco de queda acentuada";
        
      } else {
        // CENÁRIO 6: ROMPIMENTO DE SUPORTE ATIVO
        emoji = "🔥🚀";
        titulo = "SUPORTE ROMPIDO!";
        subtitulo = "⚡ FRENESI DE ALTA NAS CRIPTOS!";
        descricao = `📉 USDT.D rompeu suporte ${level.toFixed(4)}%\nTimeframe: ${tfReadable} | Pivot confirmado\n💰 Dinheiro saindo de stablecoins\n🚀 Possível rally altista nas criptos`;
        impacto = "💡 Oportunidade: Momentum de alta confirmado";
      }
      
    } else if (pivotType === "MISSED") {
      // ROMPIMENTOS DE MISSED REVERSALS
      
      if (direction === "HIGH") {
        // CENÁRIO 7: ROMPIMENTO DE RESISTÊNCIA (ex-Suporte)
        emoji = "🔄⚠️";
        titulo = "ESTRUTURA ROMPIDA!";
        subtitulo = "⚡ QUEBRA DE TOPOS DESCENDENTES";
        descricao = `📈 USDT.D rompeu resistência ${level.toFixed(4)}%\nTimeframe: ${tfReadable} | Nível invertido\n🔓 Ex-suporte agora rompido\n⚠️ USDT pode estar revertendo para alta\n📉 Possível fim da tendência de queda no USDT`;
        impacto = "⚠️ Cautela: Possível reversão - Risco para criptos";
        
      } else {
        // CENÁRIO 8: ROMPIMENTO DE SUPORTE (ex-Resistência)
        emoji = "🔄🚀";
        titulo = "ESTRUTURA ROMPIDA!";
        subtitulo = "⚡ QUEBRA DE FUNDOS ASCENDENTES";
        descricao = `📉 USDT.D rompeu suporte ${level.toFixed(4)}%\nTimeframe: ${tfReadable} | Nível invertido\n🔓 Ex-resistência agora rompida\n💡 USDT pode estar revertendo para baixa\n🚀 Possível fim da tendência de alta no USDT`;
        impacto = "💡 Oportunidade: Possível reversão - Alta nas criptos";
      }
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
