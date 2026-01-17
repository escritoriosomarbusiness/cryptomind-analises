# 🔄 TRS v6.1 - Trend Reversal Setup (COM MTF)

**Sistema de reversão de tendência baseado no Setup 9.1 de Larry Williams com análise macro**

---

## 📊 VISÃO GERAL

O **TRS (Trend Reversal Setup)** é um indicador especializado em capturar **reversões de tendência esgotadas**, baseado no clássico **Setup 9.1 de Larry Williams**. O TRS identifica momentos em que uma tendência **esbarra em zonas de reversão**, perde força e **inverte de direção**.

**Status:** ✅ Operacional com MTF  
**Versão:** 6.1  
**Última Atualização:** 17/01/2026  
**Origem:** Setup 9.1 de Larry Williams

---

## 🎯 CONCEITO: REVERSÃO vs IGNIÇÃO

### **TRS - "Reversão de Tendência"** 🔄

**Objetivo:** Capturar a **REVERSÃO** de uma tendência esgotada

**Momento:** Quando a tendência:
1. **Esbarra** em zona de reversão (SR, Golden Zone, RSI extremo)
2. **Perde força** (esgotamento)
3. **Inverte** de direção (cruza EMA 9 no sentido contrário)

**Analogia:** Entrar quando a bola bate na parede e volta

**Exemplo LONG:**
```
Tendência de BAIXA → Preço cai por 5+ candles abaixo da EMA 9
→ Toca suporte ou Golden Zone ou RSI sobrevenda
→ Perde força e cruza EMA 9 para cima
→ TRS LONG ativado (reversão para alta)
```

---

### **DNP - "Ignição de Tendência"** 🚀 (Comparação)

**Objetivo:** Capturar o **INÍCIO** de uma tendência

**Momento:** Quando a tendência **ENTRA** (ignição)

**Diferença Fundamental:**
- **TRS:** Pega o **esgotamento e virada** (reversão)
- **DNP:** Pega a **largada** (ignição)

---

## ✨ CARACTERÍSTICAS DO TRS

### **Base: Setup 9.1 de Larry Williams**

O Setup 9.1 é um dos setups mais conhecidos de Larry Williams, trader lendário e autor de diversos livros sobre trading. O conceito é simples mas poderoso:

**Regra Básica:**
- **LONG:** Preço fica X candles abaixo da EMA 9, depois cruza para cima
- **SHORT:** Preço fica X candles acima da EMA 9, depois cruza para baixo

**Lógica:** Após um movimento prolongado em uma direção, o preço tende a reverter quando cruza a EMA 9.

---

### **Validações do TRS v6.1:**

O TRS adiciona **validações rigorosas** ao Setup 9.1 original:

1. **X Candles do Mesmo Lado da EMA 9** (esgotamento)
2. **Validação por RSI** (sobrecompra/sobrevenda)
3. **Validação por SR de TF Superior** (Pivots MTF)
4. **Validação por Golden Zone** (Fibonacci 0.5-0.618)
5. **Confluências** (Simples, Dupla ⭐, Tripla 🌟🌟)
6. **MTF (Multi-Timeframe)** (tendência macro)

---

## 🔬 VALIDAÇÕES TÉCNICAS DETALHADAS

### **1. X Candles do Mesmo Lado da EMA 9**

**Objetivo:** Garantir que houve um movimento prolongado (esgotamento)

**Condições:**
- ✅ **LONG:** `candlesBelowEMA >= minCandlesBelowAbove` (padrão: 5)
  - Preço ficou 5+ candles **abaixo** da EMA 9
  - Indica esgotamento da tendência de baixa
  
- ✅ **SHORT:** `candlesAboveEMA >= minCandlesBelowAbove` (padrão: 5)
  - Preço ficou 5+ candles **acima** da EMA 9
  - Indica esgotamento da tendência de alta

**Lógica:** Quanto mais tempo em uma direção, maior a probabilidade de reversão.

---

### **2. Cruzamento da EMA 9 com Candle Forte**

**Condições LONG:**
- ✅ `close[1] < ema9[1]` e `close > ema9` (cruzamento para cima)
- ✅ Candle forte: `close >= upperThird` (fechamento no terço superior)
- ✅ Candle de alta: `close > open`

**Condições SHORT:**
- ✅ `close[1] > ema9[1]` e `close < ema9` (cruzamento para baixo)
- ✅ Candle forte: `close <= lowerThird` (fechamento no terço inferior)
- ✅ Candle de baixa: `close < open`

**Objetivo:** Garantir que o cruzamento é forte, não apenas um toque fraco.

---

### **3. Validação por RSI (Sobrecompra/Sobrevenda)**

**Componentes:**
- **RSI:** Relative Strength Index (período 14)
- **Lookback:** Últimos 5 candles

**Condições:**
- ✅ **LONG:** RSI < 30 (sobrevenda) nos últimos 5 candles
  - Indica que o ativo está oversold (vendido demais)
  - Momento ideal para reversão para alta
  
- ✅ **SHORT:** RSI > 70 (sobrecompra) nos últimos 5 candles
  - Indica que o ativo está overbought (comprado demais)
  - Momento ideal para reversão para baixa

**Objetivo:** Confirmar esgotamento por momentum extremo.

---

### **4. Validação por SR de TF Superior (Pivots MTF)**

**Componentes:**
- **Pivots:** Suporte/Resistência automáticos
- **Lookback:** 10 candles
- **Multi-Timeframe:** Busca pivots do timeframe superior

**Hierarquia:**
| TF Atual | TF Superior (Pivots) |
|----------|----------------------|
| 1m       | 15m                  |
| 5m       | 60m (H1)             |
| 15m      | 240m (H4)            |
| 60m (H1) | D (Daily)            |
| 240m (H4)| W (Weekly)           |
| D        | M (Monthly)          |

**Condições:**
- ✅ **LONG:** Preço tocou suporte e **rejeitou** (fechou acima)
  - `low <= suporte + tolerância`
  - `close > suporte` (rejeição)
  
- ✅ **SHORT:** Preço tocou resistência e **rejeitou** (fechou abaixo)
  - `high >= resistência - tolerância`
  - `close < resistência` (rejeição)

**Tolerância:** 0.1% (configurável)

**Objetivo:** Confirmar que a reversão ocorre em nível estrutural importante.

---

### **5. Validação por Golden Zone (Fibonacci 0.5-0.618)**

**Componentes:**
- **Fibonacci:** Retração de 50% a 61.8%
- **Lookback:** Últimos 3 pivots

**Cálculo LONG:**
```
1. Buscar último fundo (pivot low)
2. Buscar último topo (pivot high)
3. Golden Zone = 50% a 61.8% da distância entre fundo e topo
4. Validar se preço tocou a zona e rejeitou (fechou acima de 61.8%)
```

**Cálculo SHORT:**
```
1. Buscar último topo (pivot high)
2. Buscar último fundo (pivot low)
3. Golden Zone = 50% a 61.8% da distância entre topo e fundo
4. Validar se preço tocou a zona e rejeitou (fechou abaixo de 61.8%)
```

**Objetivo:** Confirmar que a reversão ocorre na zona ideal de retração (Golden Zone).

**Nota:** A Golden Zone (0.5-0.618) é considerada a área de maior probabilidade de reversão em análise de Fibonacci.

---

### **6. Confluências (Validações Múltiplas)**

**Sistema de Pontuação:**
- **Simples:** 1 validação (SR **ou** RSI **ou** Fib)
- **Dupla ⭐:** 2 validações (SR+RSI **ou** SR+Fib **ou** RSI+Fib)
- **Tripla 🌟🌟:** 3 validações (SR+RSI+Fib)

**Método Hybrid (padrão):**
- Aceita **qualquer** das 3 validações
- Quanto mais validações, maior a confluência
- Tripla confluência = máxima probabilidade

**Métodos Alternativos:**
- **Pivots (SR):** Apenas validação por suporte/resistência
- **RSI:** Apenas validação por sobrecompra/sobrevenda
- **Fibonacci:** Apenas validação por Golden Zone

**Recomendação:** Usar Hybrid e priorizar confluências duplas/triplas.

---

### **7. MTF (Multi-Timeframe) - Análise Macro**

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
- **PREMIUM** ⭐⭐⭐: Reversão alinhada com HTF (alta probabilidade)
  - LONG quando HTF está em alta (reversão de correção)
  - SHORT quando HTF está em baixa (reversão de correção)
  
- **CAUTELA** ⚠️: HTF neutro (risco elevado)
  
- **CONTRA** 🔴: Reversão contra HTF (alto risco)
  - LONG quando HTF está em baixa (reversão contra tendência macro)
  - SHORT quando HTF está em alta (reversão contra tendência macro)

**Interpretação para TRS:**
- **PREMIUM:** Reversão de uma correção dentro de tendência maior (ideal)
- **CONTRA:** Reversão tentando inverter tendência maior (arriscado)

---

### **ENTENDENDO O MTF NO TRS - DOMINÂNCIA MACRO**

**Princípio Fundamental:** A tendência do fractal superior **domina** a tendência do fractal inferior.

#### **EXEMPLO PRÁTICO - TRS LONG PREMIUM:**

**Cenário:**

1. **H4 (macro):** Tendência de ALTA estabelecida
   - EMA 55 > EMA 233
   - EMA 55 crescente
   - Preço acima da EMA 55

2. **H4 produz:** Onda de retração (correção)
   - Movimento natural: busca fundo ascendente
   - Objetivo: criar novo suporte acima do fundo anterior

3. **15min (micro):** Entra em tendência de BAIXA
   - Seguindo a retração do H4
   - Preço fica 5+ candles abaixo da EMA 9
   - Esgotamento da retração

4. **15min:** Rompe EMA 9 para cima
   - Validação: SR (tocou suporte) + RSI (sobrevenda)
   - **TRS LONG ativado no 15min**

5. **Classificação:** **PREMIUM** ⭐⭐⭐

**Por quê é PREMIUM?**

✅ O TRS LONG no 15min está capturando o **FIM DA RETRAÇÃO** do H4  
✅ O H4 está em ALTA, então a retração (baixa no 15min) é **temporária**  
✅ O TRS está pegando a **reversão de volta para a tendência macro**  
✅ **Alta probabilidade:** O 15min voltará a subir para acompanhar o H4  

**Analogia:**
- H4 é o rio (fluxo principal)
- 15min é a onda (movimento temporário)
- TRS PREMIUM pega a onda voltando para o fluxo do rio

---

#### **EXEMPLO PRÁTICO - TRS SHORT PREMIUM:**

**Cenário:**

1. **H4 (macro):** Tendência de BAIXA estabelecida
2. **H4 produz:** Onda de retração (correção para cima)
3. **15min (micro):** Entra em tendência de ALTA (retração)
4. **15min:** Rompe EMA 9 para baixo + validação
5. **TRS SHORT ativado no 15min**
6. **Classificação:** **PREMIUM** ⭐⭐⭐

**Por quê é PREMIUM?**

✅ Captura o fim da retração de volta para a baixa do H4  
✅ Alinhado com a tendência macro  
✅ Alta probabilidade de sucesso  

---

#### **EXEMPLO - TRS CONTRA (ALTO RISCO):**

**Cenário TRS LONG CONTRA:**

1. **H4 (macro):** Tendência de BAIXA estabelecida
2. **15min (micro):** Tenta reverter para cima
3. **15min:** Rompe EMA 9 para cima + validação
4. **TRS LONG ativado no 15min**
5. **Classificação:** **CONTRA** 🛑

**Por quê é CONTRA?**

⛔ O TRS LONG está tentando **reverter a tendência macro**  
⛔ O H4 está em BAIXA, então a alta no 15min é **contra o fluxo**  
⛔ **Baixa probabilidade:** O H4 pode continuar caindo e anular o LONG  
⛔ **Alto risco:** Operação contra a dominância macro  

---

#### **RESUMO DA LÓGICA MTF:**

| Setup | HTF | LTF | Classificação | Interpretação |
|-------|-----|-----|-----------------|-------------------|
| TRS LONG | ALTA | Retração baixa | **PREMIUM** ⭐⭐⭐ | Fim da correção, volta para alta |
| TRS SHORT | BAIXA | Retração alta | **PREMIUM** ⭐⭐⭐ | Fim da correção, volta para baixa |
| TRS LONG | BAIXA | Tentativa alta | **CONTRA** 🛑 | Tentando reverter macro (arriscado) |
| TRS SHORT | ALTA | Tentativa baixa | **CONTRA** 🛑 | Tentando reverter macro (arriscado) |
| TRS LONG/SHORT | NEUTRO | Qualquer | **CAUTELA** ⚠️ | Sem tendência macro definida |

**Conclusão:**
- **PREMIUM:** TRS pega o fim da retração de volta para a tendência macro (ideal)
- **CONTRA:** TRS tenta reverter a tendência macro (arriscado)
- **CAUTELA:** Sem tendência macro clara (risco médio)

---

## 🔄 FLUXO DE OPERAÇÃO

### **Fase 1: TRIGGER (Gatilho Armado)**

Todas as validações foram satisfeitas:
1. ✅ Preço ficou 5+ candles do mesmo lado da EMA 9
2. ✅ Cruzou a EMA 9 com candle forte
3. ✅ Pelo menos 1 validação (SR, RSI ou Fib)
4. ✅ Cooldown respeitado (5 candles desde último sinal)

**Mensagem:**
```
🔔 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
🔔 GATILHO ARMADO ⭐
📊 Setup: TRS v6.1
⏱ Timeframe: 5m
⭐ Confluência DUPLA (SR+RSI)

━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 60 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso

━━━━━━━━━━━━━━━━━━
💰 Preço: $95,234.50
⚠️ Aguardando confirmação por rompimento
━━━━━━━━━━━━━━━━━━
```

---

### **Fase 2: CONFIRMED (Confirmado por Rompimento)**

O preço rompeu o trigger no candle seguinte:

**Mensagem:**
```
✅ 🟢 LONG BTCUSDT
━━━━━━━━━━━━━━━━━━
✅ CONFIRMADO POR ROMPIMENTO ⭐
📊 Setup: TRS v6.1
⏱ Timeframe: 5m
⭐ Confluência DUPLA (SR+RSI)

━━━━━━━━━━━━━━━━━━
⭐⭐⭐ SETUP PREMIUM ⭐⭐⭐
📈 60 em tendência de ALTA favorável
━━━━━━━━━━━━━━━━━━
💡 Alta probabilidade de sucesso

━━━━━━━━━━━━━━━━━━
🎯 Entrada: $95,450.00
🛑 Stop Loss: $94,850.20
✅ TP1: $96,049.80
✅ TP2: $96,649.60
━━━━━━━━━━━━━━━━━━
⚖️ Alavancagem sugerida: 3x
📊 Risco: 2.45%
━━━━━━━━━━━━━━━━━━
⚠️ Não é recomendação de investimento
```

---

## 📋 PARÂMETROS CONFIGURÁVEIS

### **Gerais:**
- EMA: 9 (padrão do Setup 9.1)
- Mín. candles do mesmo lado: 5
- Cooldown entre sinais: 5 candles

### **Validação:**
- Método: Hybrid (Pivots ou RSI ou Fibonacci)
- Pivots MTF: Ativado
- Pivots Lookback: 10
- Tolerância SR: 0.1%

### **RSI:**
- Período: 14
- Lookback: 5 candles
- Sobrevenda (LONG): 30
- Sobrecompra (SHORT): 70

### **Fibonacci:**
- Lookback pivots: 3
- Golden Zone: 0.5 a 0.618

### **Confirmação:**
- Exigir rompimento: Ativado
- Máx. bars para manter sinal: 10

---

## 🛠️ CONFIGURAÇÃO

### **1. TradingView (Pine Script)**

**Arquivo:** [`pinescript/trs_v6.1_mtf.pine`](pinescript/trs_v6.1_mtf.pine)

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

## 📊 INDICADORES UTILIZADOS

| Indicador | Função | Parâmetros |
|-----------|--------|------------|
| **EMA 9** | Base do Setup 9.1 | Período 9 |
| **RSI** | Sobrecompra/Sobrevenda | Período 14 |
| **Pivots** | Suporte/Resistência | Lookback 10, MTF |
| **Fibonacci** | Golden Zone | 0.5 a 0.618 |
| **EMA 55/233** | Tendência HTF | Multi-Timeframe |

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
- Alavancagem: 3x (padrão)
- Stop Loss: Obrigatório
- Take Profit: TP1 (1:1) + TP2 (1:2)

---

## 🎯 DIFERENCIAIS DO TRS

### **Por que usar o TRS?**

1. **Base Sólida:** Setup 9.1 de Larry Williams (testado por décadas)
2. **Validações Múltiplas:** SR, RSI, Fibonacci (confluências)
3. **Pivots MTF:** Suporte/Resistência do timeframe superior
4. **Confluências:** Simples, Dupla ⭐, Tripla 🌟🌟
5. **MTF:** Alinhamento com tendência macro
6. **Sistema de Confirmação:** Gatilho + Rompimento

### **Comparação TRS vs DNP:**

| Característica | TRS v6.1 | DNP v2.0 |
|----------------|----------|----------|
| **Conceito** | Reversão | Ignição |
| **Momento** | Esgotamento | Início |
| **Base** | Setup 9.1 Larry Williams | Didi's Needle Prick |
| **Validações** | 3 (SR, RSI, Fib) | 7 (Didi, ADX, REMI, etc) |
| **Confluências** | ✅ Simples/Dupla/Tripla | ❌ |
| **MTF** | ✅ | ✅ |
| **Complexidade** | Média | Alta |
| **Frequência** | Média | Baixa |

**Quando usar cada um:**
- **TRS:** Reversões em zonas de SR, RSI extremo, Golden Zone
- **DNP:** Ignição de tendência com múltiplas validações simultâneas

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

## 📝 CHANGELOG

### **[17/01/2026] - v6.1 COM MTF**
- ✨ Adicionada lógica MTF completa
- ✨ Classificação PREMIUM/CAUTELA/CONTRA
- ✨ Campos MTF no JSON
- ✨ Processador n8n já atualizado
- 📚 Documentação técnica completa
- 📚 Explicação Setup 9.1 de Larry Williams
- 📚 Conceito de reversão vs ignição

### **[10/01/2026] - v6.0**
- ✨ Setup TRS v6.0 completo
- ✨ Validação tripla (Pivots MTF + RSI + Fib Golden)
- ✨ Confluências (Simples, Dupla, Tripla)
- ✨ Sistema de confirmação

---

## ⚠️ IMPORTANTE

### **Uso Responsável:**
- ✅ Priorizar confluências duplas/triplas
- ✅ Priorizar setups PREMIUM
- ✅ Evitar setups CONTRA
- ✅ Sempre usar stop loss

### **Limitações:**
- ⚠️ Reversões são mais arriscadas que continuações
- ⚠️ Nem toda reversão se confirma
- ⚠️ Usar gestão de risco adequada

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

**Código proprietário - Uso restrito**

---

**Desenvolvido por:** CryptoMind IA  
**Baseado em:** Setup 9.1 de Larry Williams  
**Última Atualização:** 17/01/2026  
**Versão:** 6.1
