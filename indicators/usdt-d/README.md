# 📈 USDT.D v2.0 - Monitor de Dominância

**Análise macro de mercado em tempo real**

---

## 📊 VISÃO GERAL

O **USDT.D Monitor** é um sistema de análise macro que monitora a dominância do USDT (Tether) no mercado de criptomoedas, fornecendo contexto para decisões de trading.

**Status:** ✅ Operacional  
**Versão:** 2.0  
**Última Atualização:** 10/01/2026

---

## ✨ CARACTERÍSTICAS

### **Monitoramento:**
- ✅ **Dominância USDT:** Percentual em tempo real
- ✅ **Suporte/Resistência:** Níveis automáticos
- ✅ **EMAs:** 9, 21, 200 com status
- ✅ **Alertas de Proximidade:** S/R e EMA 200

### **Análise:**
- ✅ **Distância para S/R:** Cálculo automático
- ✅ **Impacto no Mercado:** BULLISH/BEARISH para cripto
- ✅ **Posição das EMAs:** Ordenação e status
- ✅ **Contexto Macro:** Interpretação completa

---

## 🎯 INTERPRETAÇÃO

### **Dominância USDT em ALTA:**
```
📈 USDT.D SUBINDO
━━━━━━━━━━━━━━━━━━
⚠️ Capital saindo de cripto
⚠️ Investidores buscando segurança
━━━━━━━━━━━━━━━━━━
💡 BEARISH para criptomoedas
```

**Significado:**
- Investidores vendendo cripto
- Convertendo para USDT (stablecoin)
- Mercado em correção/lateralização
- **Cautela em operações LONG**

---

### **Dominância USDT em QUEDA:**
```
📉 USDT.D CAINDO
━━━━━━━━━━━━━━━━━━
✅ Capital entrando em cripto
✅ Investidores comprando ativos
━━━━━━━━━━━━━━━━━━
💡 BULLISH para criptomoedas
```

**Significado:**
- Investidores comprando cripto
- Convertendo USDT em ativos
- Mercado em alta/expansão
- **Favorável para operações LONG**

---

## 📊 ALERTAS

### **1. Proximidade de Resistência**

```
🔔 USDT.D - ALERTA DE RESISTÊNCIA
━━━━━━━━━━━━━━━━━━
📊 Dominância: 4.85%
🎯 Resistência: 5.00%
📏 Distância: 0.15% (3.09%)

━━━━━━━━━━━━━━━━━━
📈 EMAs:
   • EMA 9: 4.75%
   • EMA 21: 4.65%
   • EMA 200: 4.50%

━━━━━━━━━━━━━━━━━━
💡 INTERPRETAÇÃO:
⚠️ USDT.D próximo de resistência
⚠️ Possível rejeição e queda
✅ BULLISH para criptomoedas se rejeitar
```

**Ação:**
- Monitorar rejeição na resistência
- Se rejeitar: Favorável para LONG em cripto
- Se romper: Cautela em operações LONG

---

### **2. Proximidade de Suporte**

```
🔔 USDT.D - ALERTA DE SUPORTE
━━━━━━━━━━━━━━━━━━
📊 Dominância: 4.35%
🎯 Suporte: 4.20%
📏 Distância: 0.15% (3.45%)

━━━━━━━━━━━━━━━━━━
📈 EMAs:
   • EMA 9: 4.45%
   • EMA 21: 4.55%
   • EMA 200: 4.70%

━━━━━━━━━━━━━━━━━━
💡 INTERPRETAÇÃO:
⚠️ USDT.D próximo de suporte
⚠️ Possível rejeição e alta
⚠️ BEARISH para criptomoedas se rejeitar
```

**Ação:**
- Monitorar rejeição no suporte
- Se rejeitar: Cautela em operações LONG
- Se romper: Favorável para LONG em cripto

---

### **3. Proximidade de EMA 200**

```
🔔 USDT.D - ALERTA EMA 200
━━━━━━━━━━━━━━━━━━
📊 Dominância: 4.55%
📈 EMA 200: 4.50%
📏 Distância: 0.05% (1.11%)

━━━━━━━━━━━━━━━━━━
📊 Posição EMAs:
   • EMA 9: 4.60%
   • EMA 21: 4.58%
   • EMA 200: 4.50%

━━━━━━━━━━━━━━━━━━
💡 INTERPRETAÇÃO:
⚠️ USDT.D próximo da EMA 200
⚠️ Nível importante de suporte/resistência
⚠️ Possível ponto de reversão
```

**Ação:**
- EMA 200 é nível crítico
- Monitorar reação do preço
- Decisão de tendência de longo prazo

---

## 🛠️ CONFIGURAÇÃO

### **1. TradingView (Pine Script)**

**Arquivo:** [`pinescript/usdt_d_v2.0.pine`](pinescript/usdt_d_v2.0.pine)

**Parâmetros:**
- **Timeframe:** 4 horas (recomendado)
- **EMAs:** 9, 21, 200
- **Threshold Proximidade:** 3% (padrão)
- **Lookback S/R:** 50 candles

**Alertas:**
1. Criar alerta no indicador
2. Condição: "Any alert() function call"
3. Webhook URL: `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-alert`
4. Formato: JSON

---

### **2. n8n (Processamento)**

**Arquivo:** [`n8n/processador_v2.0.js`](n8n/processador_v2.0.js)

**Workflow:**
1. **Webhook:** Recebe JSON do TradingView
2. **Processador:** Formata mensagem
3. **Telegram:** Envia notificação

---

## 📊 INDICADORES UTILIZADOS

### **Dominância USDT:**
- Percentual de USDT no mercado total
- Indicador macro de sentimento
- Inversamente proporcional ao mercado cripto

### **EMAs (Exponential Moving Averages):**
- **EMA 9:** Tendência de curto prazo
- **EMA 21:** Tendência de médio prazo
- **EMA 200:** Tendência de longo prazo

### **Suporte/Resistência:**
- Lookback: 50 candles
- Automático
- Níveis críticos de reversão

---

## 📈 USO PRÁTICO

### **Cenário 1: USDT.D em Alta + Resistência**
```
USDT.D subindo → Resistência próxima
↓
Possível rejeição
↓
USDT.D cai → Capital volta para cripto
↓
✅ BULLISH para criptomoedas
```

**Ação:** Preparar para operações LONG em cripto

---

### **Cenário 2: USDT.D em Queda + Suporte**
```
USDT.D caindo → Suporte próximo
↓
Possível rejeição
↓
USDT.D sobe → Capital sai de cripto
↓
⚠️ BEARISH para criptomoedas
```

**Ação:** Cautela em operações LONG, considerar SHORT

---

### **Cenário 3: USDT.D Rompendo EMA 200**
```
USDT.D acima EMA 200
↓
Tendência de alta confirmada
↓
Capital saindo de cripto
↓
⚠️ BEARISH prolongado
```

**Ação:** Evitar operações LONG, mercado em correção

---

## 🔄 INTEGRAÇÃO COM OUTROS INDICADORES

### **USDT.D + DNP/TRS:**

**Contexto Favorável (BULLISH):**
- USDT.D caindo ou rejeitando resistência
- DNP/TRS sinalizam LONG
- **Alta probabilidade de sucesso**

**Contexto Desfavorável (BEARISH):**
- USDT.D subindo ou rejeitando suporte
- DNP/TRS sinalizam LONG
- **Cautela, risco elevado**

**Uso Recomendado:**
1. Verificar USDT.D antes de operar
2. Confirmar contexto macro favorável
3. Executar setup DNP/TRS

---

## 📁 ARQUIVOS

### **Pine Script:**
- [`pinescript/usdt_d_v2.0.pine`](pinescript/usdt_d_v2.0.pine)

### **n8n:**
- [`n8n/processador_v2.0.js`](n8n/processador_v2.0.js)
- [`n8n/workflow.json`](n8n/workflow.json)

### **Documentação:**
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md)

---

## 🚀 QUICK START

### **Passo 1: Adicionar Indicador**
1. TradingView → Abrir gráfico USDT.D
2. Timeframe: 4 horas
3. Pine Editor → Copiar código
4. Salvar como "USDT.D Monitor v2.0"
5. Adicionar ao gráfico

### **Passo 2: Configurar Alerta**
1. Botão direito no indicador
2. "Add alert..."
3. Condição: "Any alert() function call"
4. Webhook: `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-alert`
5. Salvar

### **Passo 3: Configurar n8n**
1. Importar workflow JSON
2. Configurar Telegram
3. Ativar workflow

---

## 📊 TIMEFRAMES RECOMENDADOS

| Timeframe | Uso | Descrição |
|-----------|-----|-----------|
| 4 horas | ✅ Principal | Análise macro equilibrada |
| Daily | ✅ Longo prazo | Tendências de longo prazo |
| 1 hora | ⚠️ Curto prazo | Muitos sinais, menos relevante |

**Recomendação:** Usar 4 horas para análise macro

---

## 📝 CHANGELOG

### **[10/01/2026] - v2.0**
- 🔧 Correção de campos vazios
- ✨ Informações completas (dominância, S/R, distância, EMAs)
- ✨ Template Telegram atualizado
- 📚 Documentação completa

### **[Versão Inicial] - v1.0**
- ✨ Monitor básico de USDT.D
- ✨ Alertas de proximidade
- ✨ Integração n8n

---

## ⚠️ IMPORTANTE

### **Uso Correto:**
- ✅ Usar como contexto macro
- ✅ Combinar com indicadores de entrada (DNP/TRS)
- ✅ Não operar apenas baseado em USDT.D

### **Limitações:**
- ⚠️ Não é sinal de entrada/saída
- ⚠️ É contexto macro, não timing
- ⚠️ Usar em conjunto com análise técnica

---

## 📞 SUPORTE

Para dúvidas:
- Consulte a documentação
- Verifique o CHANGELOG
- Abra issue no GitHub

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 10/01/2026  
**Versão:** 2.0
