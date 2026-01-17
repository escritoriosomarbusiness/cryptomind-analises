# 🎯 DNP v2.0 - Didi's Needle Prick (COM MTF)

**Indicador avançado de entrada com validação multi-critério e análise macro (Multi-Timeframe)**

---

## 📊 VISÃO GERAL

O **DNP (Didi's Needle Prick)** é o indicador **mais completo e rigoroso** do sistema CryptoMind IA, combinando **7 validações técnicas simultâneas** com análise de tendência do fractal superior (MTF) para identificar pontos de entrada de alta probabilidade.

**Status:** ✅ Operacional com MTF  
**Versão:** 2.0  
**Última Atualização:** 16/01/2026

---

## ✨ ARQUITETURA DO INDICADOR

O DNP utiliza uma **abordagem multi-critério rigorosa** onde TODAS as condições devem ser satisfeitas simultaneamente dentro de uma janela de tempo configurável.

### **Sistema de Validação em 7 Camadas:**

1. **Didi Index** - Cruzamento próximo ao eixo
2. **ADX/DMI** - Força e direção da tendência
3. **REMI (Bollinger)** - Expansão controlada da volatilidade
4. **Pivots S/R** - Rompimento de níveis estruturais
5. **Filtro de Candle** - Validação de pavios
6. **Janela Temporal** - Construção dentro de N candles
7. **MTF (Multi-Timeframe)** - Alinhamento com fractal superior

---

## 🔬 VALIDAÇÕES TÉCNICAS DETALHADAS

### **1. Didi Index - Cruzamento Próximo ao Eixo**

**Componentes:**
- **Curta:** SMA(3) / SMA(8)
- **Média:** SMA(8) (eixo de referência = 1.0)
- **Longa:** SMA(20) / SMA(8)

**Condições:**
- ✅ **LONG:** Curta cruza acima da Longa (`ta.crossover(curta, longa)`)
- ✅ **SHORT:** Curta cruza abaixo da Longa (`ta.crossunder(curta, longa)`)
- ✅ **Proximidade ao Eixo:** `|longa - 1.0| * 100 <= maxDistanceFromAxis`
  - Padrão: 0.15% (configurável por timeframe)
  - 5min: 0.10% | 15min: 0.20% | 1H: 0.30% | 4H: 0.50%
- ✅ **Cruzamento Recente:** Deve ocorrer dentro da janela de construção (`setupWindow`)

**Objetivo:** Identificar início de tendência quando o preço está próximo ao equilíbrio (eixo).

---

### **2. ADX/DMI - Força e Direção da Tendência**

**Componentes:**
- **ADX:** Average Directional Index (força da tendência)
- **DI+:** Directional Indicator positivo
- **DI-:** Directional Indicator negativo

**Condições:**
- ✅ **ADX Mínimo:** `adx >= adxMinValue` (padrão: 15.0)
- ✅ **ADX Crescente:** `adxSlope >= adxMinSlope`
  - `adxSlope = adx - adx[1]`
  - Inclinação mínima (configurável por timeframe):
    - 5min: 1.5 | 15min: 2.5 | 1H: 3.0 | 4H: 4.0
- ✅ **Direção LONG:** `DI+ > DI-`
- ✅ **Direção SHORT:** `DI- > DI+`

**Objetivo:** Garantir que existe força direcional crescente no momento da entrada.

---

### **3. REMI - Razão de Expansão da Bollinger (Volatilidade Controlada)**

**Componentes:**
- **Bollinger Bands:** Período 8, Desvio 2.0
- **BBW (Bandwidth):** `BBW = Upper Band - Lower Band`

**Cálculo do REMI:**
```
1. BBW atual = BBW do candle gatilho
2. BBW histórico = Média do menor e maior BBW dos últimos N candles
3. REMI = BBW atual / BBW histórico
```

**Condições:**
- ✅ **REMI Mínimo:** `REMI >= bbExpansionRatio` (padrão: 1.5)
- ✅ **REMI Máximo:** `REMI <= bbExpansionMaxRatio` (padrão: 3.0)
- ✅ **Lookback:** 7 candles (configurável)

**Objetivo:** Validar expansão de volatilidade (momentum) sem volatilidade extrema.

**Interpretação:**
- REMI < 1.5: Volatilidade insuficiente (setup rejeitado)
- REMI 1.5-3.0: Volatilidade ideal (setup válido)
- REMI > 3.0: Volatilidade extrema (setup rejeitado)

---

### **4. Pivots S/R - Rompimento de Níveis Estruturais**

**Componentes:**
- **Pivot High:** Resistência (lookback configurável, padrão: 10)
- **Pivot Low:** Suporte (lookback configurável, padrão: 10)

**Métodos de Validação (configurável):**

**A) Por Pavio (High/Low):**
- LONG: `high > resistance`
- SHORT: `low < support`

**B) Por Fechamento (Close):**
- LONG: `close > resistance`
- SHORT: `close < support`

**Objetivo:** Confirmar rompimento de níveis estruturais importantes.

---

### **5. Filtro de Candle - Validação de Pavios**

**Cálculo:**
```
candleBody = |close - open|
upperWick = high - max(close, open)
lowerWick = min(close, open) - low
```

**Condições:**
- ✅ **LONG:** `(upperWick / candleBody) <= maxWickPercent` (padrão: 0.40)
  - Pavio superior não pode ser maior que 40% do corpo
- ✅ **SHORT:** `(lowerWick / candleBody) <= maxWickPercent` (padrão: 0.40)
  - Pavio inferior não pode ser maior que 40% do corpo

**Objetivo:** Garantir que o candle tem corpo forte (não é indecisão).

---

### **6. Janela Temporal - Construção do Setup**

**Condição:**
- ✅ **Todas as validações devem ocorrer dentro de N candles** (configurável)
- ✅ **Padrão:** `setupWindow = 3 candles`
- ✅ **Range:** 2-10 candles

**Fluxo:**
1. Cruzamento Didi inicia a janela
2. Todas as outras condições devem se alinhar dentro de N candles
3. Se passar da janela, setup é descartado

**Objetivo:** Garantir que o setup é coeso e não baseado em condições espalhadas no tempo.

---

### **7. MTF (Multi-Timeframe) - Análise do Fractal Superior**

**Hierarquia:**
| Timeframe Atual | Fractal Superior (HTF) |
|-----------------|------------------------|
| 1 minuto        | 15 minutos             |
| 5 minutos       | 60 minutos (H1)        |
| 15 minutos      | 240 minutos (H4)       |
| 60 minutos (H1) | Daily (D)              |
| 240 minutos (H4)| Weekly (W)             |
| Daily (D)       | Monthly (M)            |

**Detecção de Tendência HTF:**

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

**Classificação:**
- **PREMIUM** ⭐⭐⭐: Setup alinhado com HTF (alta probabilidade)
- **CAUTELA** ⚠️: HTF neutro (risco elevado)
- **CONTRA** 🔴: Setup contra HTF (alto risco)

---

### **ENTENDENDO O MTF NO DNP - DOMINÂNCIA MACRO**

**Princípio Fundamental:** A tendência do fractal superior **domina** a tendência do fractal inferior.

#### **EXEMPLO PRÁTICO - DNP LONG PREMIUM:**

**Cenário:**

1. **H4 (macro):** Tendência de ALTA estabelecida
   - EMA 55 > EMA 233
   - EMA 55 crescente
   - Preço acima da EMA 55

2. **15min (micro):** Ignição de tendência de ALTA
   - Didi Index cruza próximo ao eixo
   - ADX crescente
   - REMI entre 1.5-3.0
   - Pivot rompido
   - Todas as 7 validações satisfeitas
   - **DNP LONG ativado no 15min**

3. **Classificação:** **PREMIUM** ⭐⭐⭐

**Por quê é PREMIUM?**

✅ O DNP LONG no 15min está capturando a **IGNIÇÃO** alinhada com o H4  
✅ O H4 está em ALTA, então a ignição de alta no 15min está **alinhada**  
✅ O DNP está pegando o **início de uma onda** na direção da tendência macro  
✅ **Alta probabilidade:** O 15min continuará subindo acompanhando o H4  

**Analogia:**
- H4 é o rio (fluxo principal)
- 15min é a onda (movimento temporário)
- DNP PREMIUM pega a onda começando na direção do rio

---

#### **EXEMPLO PRÁTICO - DNP SHORT PREMIUM:**

**Cenário:**

1. **H4 (macro):** Tendência de BAIXA estabelecida
2. **15min (micro):** Ignição de tendência de BAIXA
3. **15min:** Todas as 7 validações satisfeitas
4. **DNP SHORT ativado no 15min**
5. **Classificação:** **PREMIUM** ⭐⭐⭐

**Por quê é PREMIUM?**

✅ Ignição de baixa alinhada com a baixa do H4  
✅ Alta probabilidade de sucesso  
✅ Movimento na direção da tendência macro  

---

#### **EXEMPLO - DNP CONTRA (ALTO RISCO):**

**Cenário DNP LONG CONTRA:**

1. **H4 (macro):** Tendência de BAIXA estabelecida
2. **15min (micro):** Ignição de tendência de ALTA
3. **15min:** Todas as 7 validações satisfeitas
4. **DNP LONG ativado no 15min**
5. **Classificação:** **CONTRA** 🛑

**Por quê é CONTRA?**

⛔ O DNP LONG está tentando **iniciar tendência contra o fluxo macro**  
⛔ O H4 está em BAIXA, então a ignição de alta no 15min é **contra o fluxo**  
⛔ **Baixa probabilidade:** O H4 pode continuar caindo e anular o LONG  
⛔ **Alto risco:** Operação contra a dominância macro  

---

#### **RESUMO DA LÓGICA MTF:**

| Setup | HTF | LTF | Classificação | Interpretação |
|-------|-----|-----|-----------------|-------------------|
| DNP LONG | ALTA | Ignição alta | **PREMIUM** ⭐⭐⭐ | Início de onda alinhada com macro |
| DNP SHORT | BAIXA | Ignição baixa | **PREMIUM** ⭐⭐⭐ | Início de onda alinhada com macro |
| DNP LONG | BAIXA | Ignição alta | **CONTRA** 🛑 | Tentando iniciar contra macro (arriscado) |
| DNP SHORT | ALTA | Ignição baixa | **CONTRA** 🛑 | Tentando iniciar contra macro (arriscado) |
| DNP LONG/SHORT | NEUTRO | Qualquer | **CAUTELA** ⚠️ | Sem tendência macro definida |

**Conclusão:**
- **PREMIUM:** DNP pega a ignição alinhada com a tendência macro (ideal)
- **CONTRA:** DNP tenta iniciar contra a tendência macro (arriscado)
- **CAUTELA:** Sem tendência macro clara (risco médio)

---

### **DIFERENÇA DNP vs TRS (MTF):**

**DNP (Ignição):**
- PREMIUM: Ignição **alinhada** com HTF
- Pega o **início** do movimento

**TRS (Reversão):**
- PREMIUM: Reversão do **fim da retração** de volta para HTF
- Pega o **fim da correção**

**Ambos são PREMIUM quando alinhados com a tendência macro!**

---

## 🔄 FLUXO DE OPERAÇÃO

### **Fase 1: TRIGGER (Gatilho Armado)**

Todas as 6 validações locais foram satisfeitas:
1. ✅ Didi cruzou próximo ao eixo
2. ✅ ADX >= mínimo e crescente
3. ✅ REMI entre 1.5-3.0
4. ✅ Pivot rompido
5. ✅ Pavio validado
6. ✅ Tudo dentro da janela temporal

**Mensagem:**
```
🔔 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO
📊 Setup: DNP v2.0
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
📊 VALIDAÇÕES:
✅ Didi Index: Cruzamento próximo ao eixo
✅ ADX: 18.5 (↑ +2.1)
✅ REMI: 2.1x (expansão ideal)
✅ Pivot: Resistência rompida
✅ Candle: Pavio validado (28%)
✅ Janela: 2/3 candles
━━━━━━━━━━━━━━━━━━
⚠️ Aguardando confirmação por rompimento
```

---

### **Fase 2: CONFIRMED (Confirmado por Rompimento)**

O preço rompeu o trigger no candle seguinte:

**Mensagem:**
```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
✅ CONFIRMADO POR ROMPIMENTO
📊 Setup: DNP v2.0
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
📊 VALIDAÇÕES FINAIS
✅ Didi Index: Mantido em tendência
✅ ADX: 19.2 (força confirmada)
✅ REMI: 2.3x (volatilidade ideal)
✅ Pivot: Rompimento confirmado
✅ MTF: H4 em ALTA (PREMIUM)
⚖️ Alavancagem sugerida: 5-10x
━━━━━━━━━━━━━━━━━━
⚠️ Não é recomendação de investimento
```

---

## 📋 PARÂMETROS CONFIGURÁVEIS

### **Didi Index:**
- Curta: 3 (SMA)
- Média: 8 (SMA)
- Longa: 20 (SMA)
- Distância Máx. do Eixo: 0.15% (ajustar por timeframe)

### **ADX/DMI:**
- ADX Length: 8
- ADX Smoothing: 8
- ADX Mínimo: 15.0
- Inclinação Mínima: 1.5 (ajustar por timeframe)

### **Bollinger Bands (REMI):**
- BB Length: 8
- BB Mult: 2.0
- Lookback: 7 candles
- REMI Mínimo: 1.5
- REMI Máximo: 3.0

### **Pivots:**
- Lookback: 10
- Método: Por Fechamento (Close) ou Por Pavio (High/Low)

### **Setup:**
- Janela de Construção: 3 candles
- Pavio Máximo: 40%
- Método Stop Loss: Pivots (S/R) ou 3 Candles Anteriores

---

## 🛠️ CONFIGURAÇÃO

### **1. TradingView (Pine Script)**

**Arquivo:** [`pinescript/dnp_v2.0_mtf.pine`](pinescript/dnp_v2.0_mtf.pine)

**Alertas:**
1. Criar alerta no indicador
2. Condição: "Any alert() function call"
3. Webhook URL: `https://cryptomindia.app.n8n.cloud/webhook/dnp-alert`
4. Formato: JSON

---

### **2. n8n (Processamento)**

**Arquivo:** [`n8n/processador_v2.0.js`](n8n/processador_v2.0.js)

**Workflow:**
1. **Webhook:** Recebe JSON do TradingView
2. **Processador:** Formata mensagem com bloco MTF
3. **Telegram:** Envia notificação

---

## 📊 INDICADORES UTILIZADOS

| Indicador | Função | Parâmetros |
|-----------|--------|------------|
| **Didi Index** | Cruzamento próximo ao eixo | SMA(3,8,20) |
| **ADX** | Força da tendência | Length 8, Smoothing 8 |
| **DI+/DI-** | Direção da tendência | Parte do ADX |
| **Bollinger Bands** | Base para REMI | Período 8, Desvio 2.0 |
| **REMI** | Razão de expansão | BBW atual / BBW médio |
| **Pivots** | Suporte/Resistência | Lookback 10 |
| **EMA 55/233** | Tendência HTF | Multi-Timeframe |

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

## 🎯 DIFERENCIAIS DO DNP

### **Por que o DNP é o mais completo?**

1. **Validação Multi-Critério:** 7 validações simultâneas
2. **Janela Temporal:** Garante coesão do setup
3. **REMI Customizado:** Mede expansão real da volatilidade
4. **ADX Dinâmico:** Exige crescimento, não apenas valor mínimo
5. **Didi Index:** Cruzamento próximo ao equilíbrio
6. **Filtro de Candle:** Evita indecisão
7. **MTF:** Alinhamento com fractal superior

### **Comparação com outros indicadores:**

| Característica | DNP v2.0 | TRS v6.1 | USDT.D v2.0 |
|----------------|----------|----------|-------------|
| Validações | 7 | 3 | 1 |
| REMI | ✅ | ❌ | ❌ |
| ADX Dinâmico | ✅ | ❌ | ❌ |
| Didi Index | ✅ | ❌ | ❌ |
| Janela Temporal | ✅ | ❌ | ❌ |
| MTF | ✅ | ✅ | ❌ |
| Pivots | ✅ | ✅ | ❌ |

---

## 📁 ARQUIVOS

### **Pine Script:**
- [`pinescript/dnp_v2.0_mtf.pine`](pinescript/dnp_v2.0_mtf.pine)

### **n8n:**
- [`n8n/processador_v2.0.js`](n8n/processador_v2.0.js)
- [`n8n/workflow.json`](n8n/workflow.json)

### **Documentação:**
- [`docs/MANUAL_OPERACAO.md`](docs/MANUAL_OPERACAO.md)
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md)

---

## 📝 CHANGELOG

### **[16/01/2026] - v2.0 COM MTF**
- ✨ Adicionada lógica MTF completa
- ✨ Classificação PREMIUM/CAUTELA/CONTRA
- ✨ Campos MTF no JSON
- ✨ Processador n8n atualizado
- 📚 Documentação técnica completa

---

## ⚠️ IMPORTANTE

### **Uso Responsável:**
- ✅ Sempre usar stop loss
- ✅ Respeitar gestão de risco
- ✅ Priorizar setups PREMIUM
- ✅ Evitar setups CONTRA

### **Complexidade:**
- ⚠️ Indicador mais rigoroso do sistema
- ⚠️ Menos sinais, maior qualidade
- ⚠️ Requer paciência e disciplina

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

**Código proprietário - Uso restrito**

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 16/01/2026  
**Versão:** 2.0
