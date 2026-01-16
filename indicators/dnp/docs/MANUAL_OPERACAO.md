# 📚 MANUAL DE OPERAÇÃO - SISTEMA DNP v1.1

**CryptoMind IA - Trading Automation System**  
**Data:** 10 de Janeiro de 2026  
**Versão:** 1.1

---

## 📋 ÍNDICE

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Fluxo de Operação](#fluxo-de-operação)
3. [Interpretação de Sinais](#interpretação-de-sinais)
4. [Gestão de Risco](#gestão-de-risco)
5. [Execução de Trades](#execução-de-trades)
6. [Monitoramento e Ajustes](#monitoramento-e-ajustes)
7. [Boas Práticas](#boas-práticas)
8. [FAQ](#faq)

---

## 🎯 VISÃO GERAL DO SISTEMA

### **O que é o DNP?**

**DNP (Didi's Needle Prick)** é um sistema de trading automatizado que identifica pontos de entrada de alta probabilidade em criptomoedas usando múltiplos indicadores técnicos:

- **Didi Index:** Identifica cruzamentos próximos ao eixo (momentum)
- **ADX/DMI:** Confirma força e direção da tendência
- **REMI (Bollinger Bands):** Valida expansão de volatilidade
- **Pivots S/R:** Confirma rompimento de suporte/resistência
- **Candle Forte:** Filtra candles com corpo forte e pavio pequeno

### **Arquitetura do Sistema**

```
TradingView (DNP v1.1)
        ↓
    Alertas
        ↓
   Webhook n8n
        ↓
  Processamento
        ↓
    Telegram
        ↓
     Trader
```

### **Tipos de Sinais**

1. **TRIGGER (Gatilho):** Setup formado, aguardando confirmação
2. **CONFIRMED (Confirmado):** Entrada validada, executar trade

---

## 🔄 FLUXO DE OPERAÇÃO

### **ETAPA 1: RECEBER ALERTA TRIGGER**

**Exemplo de mensagem:**

```
🔔 🟢 LONG BTCUSDT

📊 Setup DNP by CryptoMind IA
⏱️ 15m • 🕐 10/01/2026 12:30

🔔 GATILHO ARMADO

🎯 Indicadores:
• ADX: 22.45
• REMI: 1.85

💰 Preço Atual: $90907.39

📍 Aguardando Rompimento

⚠️ Entrada será confirmada no rompimento do gatilho
```

**O QUE FAZER:**
1. ✅ **Ler a mensagem** e entender a direção (LONG/SHORT)
2. ✅ **Abrir o gráfico** no TradingView
3. ✅ **Verificar visualmente** se o setup faz sentido
4. ✅ **Aguardar** o próximo candle
5. ❌ **NÃO ENTRAR** ainda!

**OBSERVAÇÕES:**
- Setup pode **expirar** se não romper no próximo candle
- Você receberá um CONFIRMED se romper, ou nada se expirar

---

### **ETAPA 2: RECEBER ALERTA CONFIRMED**

**Exemplo de mensagem:**

```
✅ 🟢 LONG BTCUSDT

📊 Setup DNP by CryptoMind IA
⏱️ 15m • 🕐 10/01/2026 12:45

✅ CONFIRMADO POR ROMPIMENTO

🎯 Indicadores:
• ADX: 23.10
• REMI: 1.92

💰 Preço Atual: $91100.00

🚀 Entrada Ativa

🎯 Entrada: $91050.00
🛑 Stop Loss: $90500.00 (0.60%)

⚙️ Gestão de Risco:
• Risco: 1% da banca
• Alavancagem: 16x
• Risco Real: 9.6%

📈 Alvos:
1️⃣ $91600.00 (1R) → Realizar 40%
   ⚡ Mover SL para entrada + Trailing 0.60%
2️⃣ $92150.00 (2R) → Ativar Trailing Stop ($275.00)

❌ Invalidação: Se não romper no próximo candle

⚠️ Não é recomendação de investimento
```

**O QUE FAZER:**
1. ✅ **Executar entrada** imediatamente
2. ✅ **Configurar Stop Loss** no preço indicado
3. ✅ **Configurar Target 1** (1R)
4. ✅ **Configurar Target 2** (2R)
5. ✅ **Monitorar** a operação

---

### **ETAPA 3: GERENCIAR A OPERAÇÃO**

#### **AO ATINGIR TARGET 1 (1R):**

**Ações:**
1. ✅ **Realizar 40%** da posição
2. ✅ **Mover Stop Loss** para o preço de entrada (breakeven)
3. ✅ **Ativar Trailing Stop** de 0.5R nos 60% restantes
4. ✅ **Aguardar** Target 2

**Exemplo:**
- Entrada: $91050.00
- Target 1: $91600.00 ✅ **ATINGIDO**
- **Ação:** Vender 40% da posição
- **Novo SL:** $91050.00 (breakeven)
- **Trailing:** $275.00 (0.5R)

#### **AO ATINGIR TARGET 2 (2R):**

**Ações:**
1. ✅ **Realizar 100%** da posição restante (ou parcial)
2. ✅ **Encerrar** a operação
3. ✅ **Registrar** resultado

**Exemplo:**
- Target 2: $92150.00 ✅ **ATINGIDO**
- **Ação:** Vender 60% restante
- **Resultado:** +2R (200% do risco)

#### **SE STOP LOSS FOR ATINGIDO:**

**Ações:**
1. ✅ **Aceitar** a perda (faz parte do jogo)
2. ✅ **Registrar** resultado
3. ✅ **Aguardar** próximo sinal
4. ❌ **NÃO REVENGE TRADE** (não tentar recuperar imediatamente)

---

## 📊 INTERPRETAÇÃO DE SINAIS

### **SINAIS LONG (🟢)**

**Condições:**
- ✅ Didi: Curta cruza Longa para cima (próximo ao eixo)
- ✅ ADX: Subindo com força (>= 20) e inclinação (>= 1.5)
- ✅ REMI: Expansão das Bollinger Bands (>= 1.5)
- ✅ Pivot: Rompimento de resistência
- ✅ Candle: Forte e de alta (fecha nos 33% superiores)
- ✅ DMI: DI+ > DI-

**Interpretação:**
- 📈 Tendência de **alta** se formando
- 💪 Força crescente (ADX subindo)
- 🎯 Volatilidade expandindo (oportunidade)
- 🚀 Rompimento confirmado

**Entrada:**
- **Preço:** HIGH do candle gatilho
- **Stop Loss:** Abaixo do suporte (3 candles ou pivot)

---

### **SINAIS SHORT (🔴)**

**Condições:**
- ✅ Didi: Curta cruza Longa para baixo (próximo ao eixo)
- ✅ ADX: Subindo com força (>= 20) e inclinação (>= 1.5)
- ✅ REMI: Expansão das Bollinger Bands (>= 1.5)
- ✅ Pivot: Rompimento de suporte
- ✅ Candle: Forte e de baixa (fecha nos 33% inferiores)
- ✅ DMI: DI- > DI+

**Interpretação:**
- 📉 Tendência de **baixa** se formando
- 💪 Força crescente (ADX subindo)
- 🎯 Volatilidade expandindo (oportunidade)
- 🚀 Rompimento confirmado

**Entrada:**
- **Preço:** LOW do candle gatilho
- **Stop Loss:** Acima da resistência (3 candles ou pivot)

---

## 💰 GESTÃO DE RISCO

### **REGRA FUNDAMENTAL**

**NUNCA ARRISQUE MAIS DE 1-2% DA BANCA POR TRADE!**

### **CÁLCULO DE POSIÇÃO**

**Exemplo:**
- **Banca:** $10,000
- **Risco por trade:** 1% = $100
- **Entrada:** $91,050
- **Stop Loss:** $90,500
- **Risco (pontos):** $550

**Cálculo:**
```
Posição = Risco em $ / Risco em pontos
Posição = $100 / $550
Posição = 0.1818 BTC (sem alavancagem)
```

**Com Alavancagem 16x:**
```
Posição = 0.1818 / 16
Posição = 0.0114 BTC
Valor = 0.0114 × $91,050 = $1,037
```

**Risco Real:**
```
Risco Real = Risco % × Alavancagem
Risco Real = 0.60% × 16 = 9.6%
```

### **ALAVANCAGEM SUGERIDA**

O sistema calcula automaticamente a alavancagem ideal para manter o risco real abaixo de 15%:

```
Alavancagem = min(10, floor(15% / Risco %))
```

**Exemplos:**

| Risco % | Alavancagem Sugerida | Risco Real |
|---------|----------------------|------------|
| 0.50%   | 10x                  | 5.0%       |
| 0.60%   | 10x                  | 6.0%       |
| 1.00%   | 10x                  | 10.0%      |
| 1.50%   | 10x                  | 15.0%      |
| 2.00%   | 7x                   | 14.0%      |

### **REALIZAÇÃO PARCIAL**

**Target 1 (1R):**
- Realizar **40%** da posição
- Mover SL para **breakeven**
- Garantir operação **sem risco**

**Target 2 (2R):**
- Realizar **60%** restante (ou parcial)
- Trailing stop de **0.5R**
- Maximizar ganhos

**Resultado Esperado:**
- 40% × 1R = 0.4R
- 60% × 2R = 1.2R
- **Total:** 1.6R (160% do risco)

---

## 🎯 EXECUÇÃO DE TRADES

### **PLATAFORMAS RECOMENDADAS**

1. **Binance Futures**
2. **Bybit**
3. **OKX**

### **TIPO DE ORDEM**

**ENTRADA:**
- **Ordem Limite** no preço de entrada indicado
- **Validade:** GTC (Good Till Cancelled)

**STOP LOSS:**
- **Stop Market** ou **Stop Limit**
- **Preço:** Conforme indicado no alerta

**TAKE PROFIT:**
- **Ordem Limite** nos alvos indicados
- **Quantidade:** 40% no Target 1, 60% no Target 2

### **EXEMPLO PRÁTICO (BINANCE FUTURES)**

**Setup:**
- Par: BTCUSDT
- Direção: LONG
- Entrada: $91,050
- Stop Loss: $90,500
- Target 1: $91,600
- Target 2: $92,150
- Alavancagem: 16x
- Posição: 0.0114 BTC

**Passo a Passo:**

1. **Selecionar Par:** BTCUSDT
2. **Configurar Alavancagem:** 16x (Isolated)
3. **Abrir Ordem de Entrada:**
   - Tipo: Limite
   - Preço: $91,050
   - Quantidade: 0.0114 BTC
   - Direção: LONG (Buy)

4. **Configurar Stop Loss:**
   - Tipo: Stop Market
   - Trigger: $90,500
   - Quantidade: 0.0114 BTC
   - Direção: SHORT (Sell)

5. **Configurar Take Profit 1:**
   - Tipo: Limite
   - Preço: $91,600
   - Quantidade: 0.00456 BTC (40%)
   - Direção: SHORT (Sell)

6. **Configurar Take Profit 2:**
   - Tipo: Limite
   - Preço: $92,150
   - Quantidade: 0.00684 BTC (60%)
   - Direção: SHORT (Sell)

7. **Após TP1 Atingido:**
   - Cancelar SL original
   - Criar novo SL em $91,050 (breakeven)
   - Ativar Trailing Stop de $275

---

## 📈 MONITORAMENTO E AJUSTES

### **DASHBOARD DNP**

Verificar no TradingView:

**Indicadores:**
- ✅ **Didi Cruzamento:** ATIVO
- ✅ **ADX Rising:** ATIVO (ADX >= 20, Inclinação >= 1.5)
- ✅ **BB Expansion:** ATIVO (REMI >= 1.5)
- ✅ **Pivot Breakout:** ATIVO
- ✅ **Candle Forte:** ATIVO

**Direção:**
- 🟢 **LONG (DI+):** DI+ > DI-
- 🔴 **SHORT (DI-):** DI- > DI+

**Setup State:**
- ⚪ **INATIVO:** Aguardando condições
- 🟡 **CONSTRUINDO:** Condições se alinhando
- 🟠 **TRIGGER:** Gatilho formado
- 🟢 **CONFIRMADO:** Entrada validada

### **AJUSTES POR TIMEFRAME**

#### **5 MINUTOS (Scalping)**

**Parâmetros:**
- Didi Dist. Eixo: 0.10%
- ADX Mínimo: 15
- Inclinação ADX: 1.5
- REMI Mínimo: 1.5
- Pivot Breakout: Por Fechamento

**Características:**
- ⚡ Sinais mais frequentes
- 🎯 Alvos menores (1-2%)
- ⏱️ Operações rápidas (15-60 min)

#### **15 MINUTOS (Intraday)**

**Parâmetros:**
- Didi Dist. Eixo: 0.20%
- ADX Mínimo: 20
- Inclinação ADX: 2.5
- REMI Mínimo: 1.5
- Pivot Breakout: Por Fechamento

**Características:**
- ⚖️ Equilíbrio entre frequência e qualidade
- 🎯 Alvos médios (2-4%)
- ⏱️ Operações médias (1-4 horas)

#### **1 HORA (Swing)**

**Parâmetros:**
- Didi Dist. Eixo: 0.30%
- ADX Mínimo: 25
- Inclinação ADX: 3.0
- REMI Mínimo: 1.8
- Pivot Breakout: Por Pavio

**Características:**
- 🎯 Sinais mais raros mas de alta qualidade
- 💰 Alvos maiores (4-8%)
- ⏱️ Operações longas (4-24 horas)

---

## ✅ BOAS PRÁTICAS

### **ANTES DE OPERAR**

1. ✅ **Verificar condições de mercado** (tendência, volatilidade)
2. ✅ **Confirmar saldo disponível** na exchange
3. ✅ **Testar alertas** (enviar alerta de teste)
4. ✅ **Definir meta diária** (ex: 2R ou 3 trades)
5. ✅ **Preparar psicologicamente** (aceitar perdas)

### **DURANTE A OPERAÇÃO**

1. ✅ **Seguir o plano** (não alterar SL/TP)
2. ✅ **Monitorar gráfico** (mas não ficar obcecado)
3. ✅ **Registrar observações** (diário de trades)
4. ✅ **Respeitar gestão de risco** (1-2% por trade)
5. ✅ **Não operar com emoção** (medo/ganância)

### **APÓS A OPERAÇÃO**

1. ✅ **Registrar resultado** (planilha de controle)
2. ✅ **Analisar o que funcionou/falhou**
3. ✅ **Fazer pausa** (não operar imediatamente)
4. ✅ **Atualizar estatísticas** (win rate, profit factor)
5. ✅ **Ajustar parâmetros** se necessário

---

## ❌ ERROS COMUNS

### **1. ENTRAR ANTES DO CONFIRMED**

**Erro:**
- Receber TRIGGER e entrar imediatamente

**Problema:**
- Setup pode expirar
- Entrada prematura = maior risco

**Solução:**
- ✅ Aguardar sempre o CONFIRMED

### **2. MOVER STOP LOSS**

**Erro:**
- Mover SL para evitar perda

**Problema:**
- Aumenta risco real
- Pode transformar pequena perda em grande perda

**Solução:**
- ✅ Respeitar SL original (até atingir TP1)

### **3. NÃO REALIZAR PARCIAL**

**Erro:**
- Não vender 40% no Target 1

**Problema:**
- Perde oportunidade de garantir lucro
- Operação fica com risco

**Solução:**
- ✅ Sempre realizar parcial no TP1

### **4. OPERAR SEM GESTÃO DE RISCO**

**Erro:**
- Arriscar 5-10% por trade

**Problema:**
- Sequência de perdas destrói a banca
- Recuperação fica impossível

**Solução:**
- ✅ Máximo 1-2% por trade

### **5. REVENGE TRADING**

**Erro:**
- Após perda, dobrar posição para recuperar

**Problema:**
- Decisões emocionais
- Risco exponencial

**Solução:**
- ✅ Fazer pausa após perda
- ✅ Aguardar próximo sinal válido

---

## 📊 MÉTRICAS DE PERFORMANCE

### **INDICADORES PRINCIPAIS**

**Win Rate (Taxa de Acerto):**
```
Win Rate = (Trades Vencedores / Total de Trades) × 100%
```

**Expectativa:** 50-60% (setup DNP)

**Profit Factor (Fator de Lucro):**
```
Profit Factor = Lucro Total / Perda Total
```

**Expectativa:** 1.5-2.0 (setup DNP)

**Média de R por Trade:**
```
Média R = Soma de R / Total de Trades
```

**Expectativa:** 0.8-1.2R (com realização parcial)

**Drawdown Máximo:**
```
Drawdown = (Pico - Vale) / Pico × 100%
```

**Aceitável:** < 20%

### **EXEMPLO DE PLANILHA DE CONTROLE**

| Data | Hora | Par | Dir | TF | Entry | SL | TP1 | TP2 | Resultado | R | Obs |
|------|------|-----|-----|----|----|----|----|-----|-----------|---|-----|
| 10/01 | 12:45 | BTC | L | 15m | 91050 | 90500 | 91600 | 92150 | +1.6R | +$160 | Perfeito |
| 10/01 | 15:30 | ETH | S | 15m | 3200 | 3250 | 3150 | 3100 | -1R | -$100 | SL atingido |
| 11/01 | 09:15 | SOL | L | 15m | 145 | 143 | 147 | 149 | +1.2R | +$120 | TP2 não atingido |

**Total:** +1.8R = +$180

---

## ❓ FAQ (PERGUNTAS FREQUENTES)

### **1. Quantos sinais o DNP gera por dia?**

**Resposta:** Varia conforme timeframe e volatilidade:
- 5min: 5-15 sinais/dia
- 15min: 2-8 sinais/dia
- 1H: 1-3 sinais/dia

### **2. Qual a taxa de acerto esperada?**

**Resposta:** 50-60% com gestão de risco adequada. O sistema é lucrativo mesmo com 50% de acerto devido à relação risco/retorno de 1:2.

### **3. Posso usar em qualquer criptomoeda?**

**Resposta:** Sim, mas funciona melhor em:
- ✅ BTC, ETH (alta liquidez)
- ✅ SOL, AVAX, MATIC (boa volatilidade)
- ⚠️ Altcoins de baixa liquidez (cuidado com slippage)

### **4. Preciso ficar o tempo todo monitorando?**

**Resposta:** Não! Os alertas chegam no Telegram. Você só precisa:
- Executar entrada ao receber CONFIRMED
- Configurar ordens (SL/TP)
- Verificar periodicamente

### **5. O que fazer se perder 3 trades seguidos?**

**Resposta:**
1. ✅ Parar de operar
2. ✅ Revisar parâmetros
3. ✅ Verificar condições de mercado
4. ✅ Fazer pausa de 24h
5. ✅ Recomeçar com posição reduzida

### **6. Posso usar em conta demo?**

**Resposta:** Sim! Recomendado para:
- Testar o sistema
- Aprender a operar
- Validar parâmetros
- Ganhar confiança

### **7. Quanto capital inicial é necessário?**

**Resposta:**
- **Mínimo:** $500-1000 (para respeitar gestão de risco)
- **Recomendado:** $2000-5000
- **Ideal:** $10,000+

### **8. O sistema funciona em mercado lateral?**

**Resposta:** Não muito bem. O DNP é otimizado para:
- ✅ Início de tendências
- ✅ Rompimentos
- ⚠️ Mercado lateral gera sinais falsos

**Solução:** Aguardar volatilidade aumentar (REMI alto).

---

## 🎓 RECURSOS ADICIONAIS

### **DOCUMENTAÇÃO**

1. **DNP_V1.1_CORRECOES.md** - Correções técnicas
2. **GUIA_ALERTAS_TRADINGVIEW.md** - Configuração de alertas
3. **DNP_N8N_SETUP.md** - Setup do workflow n8n

### **SUPORTE**

- 📧 Email: suporte@cryptomind.com
- 💬 Telegram: @cryptomind_support
- 🌐 Site: https://cryptomind.com

---

## ⚠️ DISCLAIMER

**ESTE SISTEMA NÃO É RECOMENDAÇÃO DE INVESTIMENTO!**

- Trading de criptomoedas envolve **alto risco**
- Você pode **perder todo o capital investido**
- Resultados passados **não garantem** resultados futuros
- Opere apenas com capital que **pode perder**
- Consulte um **assessor financeiro** antes de operar

**USE POR SUA CONTA E RISCO!**

---

## 🚀 CHECKLIST OPERACIONAL

### **ANTES DE COMEÇAR:**

- [ ] DNP v1.1 instalado no TradingView
- [ ] Alertas configurados (4 por cripto/timeframe)
- [ ] Workflow n8n ativo
- [ ] Bot Telegram funcionando
- [ ] Conta na exchange configurada
- [ ] Gestão de risco definida (1-2% por trade)
- [ ] Planilha de controle preparada
- [ ] Parâmetros ajustados para o timeframe

### **DURANTE A OPERAÇÃO:**

- [ ] Receber alerta TRIGGER
- [ ] Verificar gráfico visualmente
- [ ] Aguardar alerta CONFIRMED
- [ ] Executar entrada no preço indicado
- [ ] Configurar Stop Loss
- [ ] Configurar Take Profit 1 e 2
- [ ] Monitorar operação
- [ ] Realizar parcial no TP1
- [ ] Mover SL para breakeven
- [ ] Registrar resultado

### **APÓS A OPERAÇÃO:**

- [ ] Atualizar planilha de controle
- [ ] Calcular resultado em R
- [ ] Analisar o que funcionou/falhou
- [ ] Fazer pausa antes do próximo trade
- [ ] Revisar métricas (win rate, profit factor)

---

**🎉 BOA SORTE E BONS TRADES!**

*CryptoMind IA - Automated Trading Systems*
