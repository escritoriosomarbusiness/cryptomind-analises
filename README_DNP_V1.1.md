# 📚 DOCUMENTAÇÃO COMPLETA - DNP v1.1

**CryptoMind IA - Automated Trading System**  
**Versão:** 1.1  
**Data:** 10 de Janeiro de 2026

---

## 🎯 VISÃO GERAL

O **DNP (Didi's Needle Prick)** é um sistema automatizado de trading para criptomoedas que identifica pontos de entrada de alta probabilidade usando análise técnica multi-indicador.

### **Componentes do Sistema:**

1. **Indicador Pine Script v6** (TradingView)
2. **Workflow n8n** (Automação)
3. **Bot Telegram** (Notificações)
4. **Gestão de Risco** (Automática)

---

## 📖 ÍNDICE DA DOCUMENTAÇÃO

### **1. CÓDIGO E CORREÇÕES**

#### **📄 dnp_v1.1_remi_pivots_corrigido.txt**
- Código Pine Script completo e funcional
- Correção do cálculo REMI
- Validação de pivots configurável
- Stop Loss configurável
- Dashboard completo
- Alertas JSON para n8n

**Usar este arquivo para:** Copiar e colar no TradingView

---

#### **📄 DNP_V1.1_CORRECOES.md**
- Detalhamento técnico das correções
- Problema 1: REMI sempre retornando 1.0
- Problema 2: Validação de pivots restritiva
- Comparação código v1.0 vs v1.1
- Changelog completo

**Usar este arquivo para:** Entender as mudanças técnicas

---

### **2. CONFIGURAÇÃO**

#### **📄 GUIA_ALERTAS_TRADINGVIEW.md**
- Pré-requisitos (TradingView, n8n, Telegram)
- Configuração do webhook n8n
- Criação dos 4 alertas por cripto/timeframe
- Formato JSON dos alertas
- Testes e validação
- Troubleshooting completo

**Usar este arquivo para:** Configurar alertas do zero

---

#### **📄 CHECKLIST_SETUP_RAPIDO.md**
- Guia rápido em 10 passos
- Configuração TradingView
- Configuração n8n
- Configuração Telegram
- Criação de alertas
- Testes básicos
- Parâmetros por timeframe

**Usar este arquivo para:** Setup rápido (30 minutos)

---

#### **📄 n8n_workflow_dnp.json**
- Workflow n8n completo
- Nó Webhook (recebe alertas)
- Nó Code (processa JSON)
- Nó Telegram (envia mensagens)
- Formatação de mensagens
- Cálculo de alavancagem

**Usar este arquivo para:** Importar no n8n

---

#### **📄 DNP_N8N_SETUP.md**
- Instalação do n8n (Docker/Cloud)
- Importação do workflow
- Configuração de credenciais
- Criação do bot Telegram
- Obtenção do Chat ID
- Testes de integração

**Usar este arquivo para:** Configurar n8n do zero

---

### **3. OPERAÇÃO**

#### **📄 MANUAL_OPERACAO_DNP.md**
- Visão geral do sistema
- Fluxo de operação completo
- Interpretação de sinais (LONG/SHORT)
- Gestão de risco detalhada
- Execução de trades (passo a passo)
- Monitoramento e ajustes
- Boas práticas
- Erros comuns
- Métricas de performance
- FAQ (perguntas frequentes)

**Usar este arquivo para:** Aprender a operar o sistema

---

### **4. REFERÊNCIA TÉCNICA**

#### **📄 TELEGRAM_BOT_CONFIGURAVEL.md** (Futuro)
- Arquitetura do bot configurável
- Preferências por usuário
- Filtros (timeframes, setups, moedas)
- Comandos do bot
- Banco de dados de usuários

**Usar este arquivo para:** Planejar evolução futura

---

## 🚀 INÍCIO RÁPIDO

### **Para Começar em 30 Minutos:**

1. **Ler:** `CHECKLIST_SETUP_RAPIDO.md`
2. **Copiar:** Código de `dnp_v1.1_remi_pivots_corrigido.txt`
3. **Configurar:** Alertas conforme checklist
4. **Testar:** Enviar alerta de teste
5. **Operar:** Seguir `MANUAL_OPERACAO_DNP.md`

---

### **Para Entender Tudo em Profundidade:**

1. **Ler:** `DNP_V1.1_CORRECOES.md` (entender correções)
2. **Ler:** `GUIA_ALERTAS_TRADINGVIEW.md` (configuração detalhada)
3. **Ler:** `DNP_N8N_SETUP.md` (setup n8n completo)
4. **Ler:** `MANUAL_OPERACAO_DNP.md` (operação profissional)

---

## 📊 ESTRUTURA DO SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                      TRADINGVIEW                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Indicador DNP v1.1 (Pine Script)         │    │
│  │                                                     │    │
│  │  • Didi Index (cruzamentos próximos ao eixo)      │    │
│  │  • ADX/DMI (força e direção da tendência)         │    │
│  │  • REMI/Bollinger (expansão de volatilidade)      │    │
│  │  • Pivots S/R (rompimentos)                       │    │
│  │  • Candle Forte (filtro de qualidade)             │    │
│  │                                                     │    │
│  │  Dashboard → Mostra status de todos indicadores   │    │
│  │  Alertas → Envia JSON via webhook                 │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Webhook HTTP POST)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                         N8N                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Workflow DNP Automation               │    │
│  │                                                     │    │
│  │  1. Webhook → Recebe JSON do TradingView          │    │
│  │  2. Code → Processa e formata dados               │    │
│  │  3. Telegram → Envia mensagem formatada           │    │
│  │                                                     │    │
│  │  Processamento:                                    │    │
│  │  • Extrai dados do alerta                         │    │
│  │  • Formata preços                                  │    │
│  │  • Calcula alavancagem sugerida                   │    │
│  │  • Cria mensagem HTML para Telegram               │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Telegram Bot API)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       TELEGRAM                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │                  Bot CryptoMind                    │    │
│  │                                                     │    │
│  │  Mensagens:                                        │    │
│  │  • 🔔 TRIGGER → Gatilho armado                    │    │
│  │  • ✅ CONFIRMED → Entrada confirmada              │    │
│  │                                                     │    │
│  │  Informações:                                      │    │
│  │  • Símbolo, direção, timeframe                    │    │
│  │  • Preços (entry, SL, targets)                    │    │
│  │  • Gestão de risco (alavancagem, risco real)      │    │
│  │  • Indicadores (ADX, REMI)                        │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                         (Trader)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    EXCHANGE (Binance/Bybit)                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Execução Manual do Trade              │    │
│  │                                                     │    │
│  │  1. Receber alerta CONFIRMED                       │    │
│  │  2. Abrir ordem de entrada (Limit)                │    │
│  │  3. Configurar Stop Loss (Stop Market)            │    │
│  │  4. Configurar Take Profit 1 e 2 (Limit)          │    │
│  │  5. Monitorar operação                             │    │
│  │  6. Realizar parcial no TP1                        │    │
│  │  7. Mover SL para breakeven                        │    │
│  │  8. Ativar trailing stop                           │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 INDICADORES TÉCNICOS

### **1. DIDI INDEX**
- **Função:** Identificar cruzamentos de médias móveis
- **Validação:** Cruzamento próximo ao eixo (< 0.15%)
- **LONG:** Curta cruza Longa para cima
- **SHORT:** Curta cruza Longa para baixo

### **2. ADX/DMI**
- **Função:** Medir força e direção da tendência
- **Validação:** ADX >= 20 e subindo >= 1.5 pontos
- **LONG:** DI+ > DI-
- **SHORT:** DI- > DI+

### **3. REMI (Bollinger Bands)**
- **Função:** Detectar expansão de volatilidade
- **Cálculo:** BBW atual / BBW médio dos últimos 7 candles
- **Validação:** REMI >= 1.5
- **Interpretação:** Quanto maior, mais oportunidade

### **4. PIVOTS S/R**
- **Função:** Identificar rompimentos de suporte/resistência
- **Validação:** Configurável (Pavio ou Fechamento)
- **LONG:** Rompimento de resistência
- **SHORT:** Rompimento de suporte

### **5. CANDLE FORTE**
- **Função:** Filtrar candles de qualidade
- **Validação:** Fecha nos 33% superiores/inferiores
- **Filtro Pavio:** Pavio <= 20% do corpo
- **LONG:** Candle de alta forte
- **SHORT:** Candle de baixa forte

---

## ⚙️ CONFIGURAÇÕES RECOMENDADAS

### **TIMEFRAME 5 MINUTOS (Scalping)**

| Parâmetro | Valor |
|-----------|-------|
| Didi Dist. Eixo | 0.10% |
| ADX Mínimo | 15 |
| Inclinação ADX | 1.5 |
| REMI Mínimo | 1.5 |
| Pivot Breakout | Por Fechamento |
| Stop Loss | 3 Candles |

**Características:**
- ⚡ 5-15 sinais/dia
- 🎯 Alvos: 1-2%
- ⏱️ Duração: 15-60 min

---

### **TIMEFRAME 15 MINUTOS (Intraday)** ⭐ RECOMENDADO

| Parâmetro | Valor |
|-----------|-------|
| Didi Dist. Eixo | 0.20% |
| ADX Mínimo | 20 |
| Inclinação ADX | 2.5 |
| REMI Mínimo | 1.5 |
| Pivot Breakout | Por Fechamento |
| Stop Loss | 3 Candles |

**Características:**
- ⚖️ 2-8 sinais/dia
- 🎯 Alvos: 2-4%
- ⏱️ Duração: 1-4 horas

---

### **TIMEFRAME 1 HORA (Swing)**

| Parâmetro | Valor |
|-----------|-------|
| Didi Dist. Eixo | 0.30% |
| ADX Mínimo | 25 |
| Inclinação ADX | 3.0 |
| REMI Mínimo | 1.8 |
| Pivot Breakout | Por Pavio |
| Stop Loss | Pivots S/R |

**Características:**
- 🎯 1-3 sinais/dia
- 💰 Alvos: 4-8%
- ⏱️ Duração: 4-24 horas

---

## 💰 GESTÃO DE RISCO

### **REGRAS FUNDAMENTAIS**

1. **Risco por Trade:** 1-2% da banca
2. **Alavancagem Máxima:** 10x
3. **Risco Real Máximo:** 15%
4. **Realização Parcial:** 40% no TP1
5. **Breakeven:** Após TP1

### **CÁLCULO DE POSIÇÃO**

```
Risco $ = Banca × Risco %
Posição = Risco $ / (Entry - Stop Loss)
Posição Alavancada = Posição / Alavancagem
```

**Exemplo:**
```
Banca: $10,000
Risco: 1% = $100
Entry: $91,050
Stop Loss: $90,500
Risco (pontos): $550

Posição = $100 / $550 = 0.1818 BTC
Com 16x: 0.1818 / 16 = 0.0114 BTC
Valor: $1,037
```

---

## 📈 PERFORMANCE ESPERADA

### **MÉTRICAS**

| Métrica | Valor Esperado |
|---------|----------------|
| Win Rate | 50-60% |
| Profit Factor | 1.5-2.0 |
| Média R/Trade | 0.8-1.2R |
| Drawdown Máx | < 20% |

### **EXEMPLO DE RESULTADOS (100 TRADES)**

```
Trades Vencedores: 55 (55%)
Trades Perdedores: 45 (45%)

Lucro Médio: +1.6R
Perda Média: -1.0R

Lucro Total: 55 × 1.6R = 88R
Perda Total: 45 × 1.0R = 45R

Resultado Líquido: 43R (+43%)

Com banca de $10,000 e risco 1%:
Resultado: $4,300 (43% de retorno)
```

---

## 🔧 TROUBLESHOOTING

### **Problema: Alerta não dispara**
- ✅ Verificar se alerta está ativo
- ✅ Verificar validade (Open-ended)
- ✅ Verificar condições no dashboard

### **Problema: Webhook não recebe**
- ✅ Verificar URL do webhook
- ✅ Verificar se workflow está ativo
- ✅ Testar com Postman/curl

### **Problema: Mensagem não chega no Telegram**
- ✅ Verificar token do bot
- ✅ Verificar Chat ID
- ✅ Enviar /start para o bot

### **Problema: REMI sempre 1.0**
- ✅ Usar código v1.1 (corrigido)
- ✅ Verificar se código foi copiado completo

### **Problema: Nenhum sinal aparece**
- ✅ Verificar parâmetros (muito restritivos?)
- ✅ Verificar mercado (lateral?)
- ✅ Testar em timeframe diferente

---

## 📞 SUPORTE

### **Documentação**
- 📄 Todos os arquivos neste repositório
- 🔍 Use o índice acima para navegar

### **Contato**
- 📧 Email: suporte@cryptomind.com
- 💬 Telegram: @cryptomind_support
- 🌐 Site: https://cryptomind.com

---

## ⚠️ DISCLAIMER

**AVISO IMPORTANTE:**

Este sistema é fornecido apenas para fins educacionais e informativos. Trading de criptomoedas envolve alto risco e você pode perder todo o capital investido.

- ❌ **NÃO É** recomendação de investimento
- ❌ **NÃO GARANTE** lucros
- ❌ Resultados passados **NÃO GARANTEM** resultados futuros
- ✅ Opere apenas com capital que **PODE PERDER**
- ✅ Consulte um **assessor financeiro** profissional

**USE POR SUA CONTA E RISCO!**

---

## 📝 CHANGELOG

### **v1.1 (10/01/2026)**
- ✅ **CORRIGIDO:** Cálculo REMI (agora funciona corretamente)
- ✅ **ADICIONADO:** Validação de pivots configurável (Pavio/Fechamento)
- ✅ **ADICIONADO:** Dashboard mostra método de pivot ativo
- ✅ **MELHORADO:** Documentação completa

### **v1.0 (09/01/2026)**
- ✅ Versão inicial do DNP
- ✅ Integração com n8n
- ✅ Stop Loss configurável
- ❌ REMI com bug (corrigido na v1.1)

---

## 🎯 PRÓXIMOS PASSOS

### **Curto Prazo**
1. ✅ Testar DNP v1.1 em múltiplas criptos
2. ✅ Validar taxa de acerto
3. ✅ Ajustar parâmetros conforme necessário

### **Médio Prazo**
1. ⏳ Desenvolver TRS (Trend Reversal Setup)
2. ⏳ Integrar TRS com mesma estrutura
3. ⏳ Criar alertas combinados (DNP + TRS)

### **Longo Prazo**
1. ⏳ Bot Telegram configurável
2. ⏳ Preferências por usuário
3. ⏳ Filtros personalizados
4. ⏳ Execução automática (API exchanges)

---

## 🚀 COMEÇAR AGORA

**Passo 1:** Ler `CHECKLIST_SETUP_RAPIDO.md`  
**Passo 2:** Configurar sistema (30 minutos)  
**Passo 3:** Testar com alertas  
**Passo 4:** Operar seguindo `MANUAL_OPERACAO_DNP.md`

---

**🎉 BOA SORTE E BONS TRADES!**

*CryptoMind IA - Automated Trading Systems*  
*Versão 1.1 - Janeiro 2026*
