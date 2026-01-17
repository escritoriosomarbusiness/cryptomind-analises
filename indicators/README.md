# 📊 Indicadores CryptoMind IA

**Sistema completo de indicadores para trading automatizado**

---

## 🎯 VISÃO GERAL

Este diretório contém os **3 indicadores principais** do sistema CryptoMind IA, cada um com sua função específica no ecossistema de trading:

### **1. DNP v2.0 (Didi's Needle Prick)** 🎯
**Função:** Indicador completo de entrada com validação macro (MTF)  
**Status:** ✅ Operacional com MTF  
**Última Atualização:** 16/01/2026

O DNP é o indicador **mais completo** do sistema, combinando múltiplos sinais de confirmação com análise de tendência do fractal superior (Multi-Timeframe).

**Características:**
- ✅ **7 Validações Simultâneas:** Didi Index, ADX/DMI, REMI (Bollinger), Pivots S/R, Filtro de Candle, Janela Temporal
- ✅ **REMI Customizado:** Razão de expansão da Bollinger (8,2) comparada aos últimos N candles
- ✅ **ADX Dinâmico:** Exige ADX >= mínimo E crescimento entre candles
- ✅ **Didi Index:** Cruzamento próximo ao eixo para identificar início de tendência
- ✅ **Janela Temporal:** Todas as condições devem se alinhar em N candles (configurável)
- ✅ **Rompimento de Pivot:** Exige romper resistência (LONG) ou suporte (SHORT)
- ✅ **NOVO:** Análise MTF (Multi-Timeframe) com classificação PREMIUM/CAUTELA/CONTRA
- ✅ Gestão completa de risco (Entry, SL, TP1, TP2, Trailing Stop)
- ✅ Sistema de confirmação: Gatilho + Rompimento

**Classificação MTF:**
- ⭐⭐⭐ **PREMIUM:** Setup alinhado com tendência do fractal superior (alta probabilidade)
- ⚠️ **CAUTELA:** Fractal superior neutro (risco elevado)
- 🔴 **CONTRA:** Setup contra a tendência do fractal superior (alto risco)

**Documentação:** [`dnp/README.md`](dnp/README.md)

---

### **2. TRS v6.1 (Trend Reversal Setup)** 🔄
**Função:** Detecção de reversões de tendência com validação tripla  
**Status:** ✅ Operacional com MTF  
**Última Atualização:** 10/01/2026

Sistema de detecção de reversões de tendência baseado em EMA 9 com validação tripla e análise macro.

**Características:**
- ✅ Validação Híbrida: Pivots MTF + RSI + Fibonacci Golden Zone
- ✅ Sistema de Confirmação: Gatilho + Rompimento
- ✅ Detecção de Confluências: Simples, Dupla (⭐), Tripla (🌟🌟)
- ✅ Análise MTF (Multi-Timeframe) com classificação PREMIUM/CAUTELA/CONTRA
- ✅ Gestão de Risco Automática: Alavancagem sugerida
- ✅ Cálculo Automático: Entry, SL, T1, T2, Trailing Stop

**Documentação:** [`trs/README.md`](trs/README.md)

---

### **3. USDT.D v2.0 (Monitor de Dominância)** 📈
**Função:** Análise macro de mercado em tempo real  
**Status:** ✅ Operacional  
**Última Atualização:** 10/01/2026

Monitor de dominância do USDT.D para análise macro de mercado e contexto geral.

**Características:**
- ✅ Alertas de Proximidade: Suporte, Resistência, EMA 200
- ✅ Informações Completas: Dominância, Distância, Impacto
- ✅ Posição das EMAs: EMA 9, 21, 200 com status
- ✅ Interpretação: BULLISH/BEARISH para cripto
- ✅ Contexto macro para decisões de trading

**Documentação:** [`usdt-d/README.md`](usdt-d/README.md)

---

## 🏗️ ESTRUTURA DO DIRETÓRIO

```
indicators/
├── README.md (este arquivo)
│
├── dnp/                          # DNP v2.0 (Didi's Needle Prick)
│   ├── README.md                 # Documentação completa
│   ├── pinescript/
│   │   └── dnp_v2.0_mtf.pine    # Código Pine Script v2.0
│   ├── n8n/
│   │   ├── processador_v2.0.js  # Processador n8n com MTF
│   │   └── workflow.json         # Workflow n8n completo
│   └── docs/
│       ├── MANUAL_OPERACAO.md   # Manual de operação
│       └── CHANGELOG.md          # Histórico de mudanças
│
├── trs/                          # TRS v6.1 (Trend Reversal Setup)
│   ├── README.md                 # Documentação completa
│   ├── pinescript/
│   │   └── trs_v6.1_mtf.pine    # Código Pine Script v6.1
│   ├── n8n/
│   │   ├── processador_v6.1.js  # Processador n8n com MTF
│   │   └── workflow.json         # Workflow n8n completo
│   └── docs/
│       └── CHANGELOG.md          # Histórico de mudanças
│
└── usdt-d/                       # USDT.D v2.0 (Monitor)
    ├── README.md                 # Documentação completa
    ├── pinescript/
    │   └── usdt_d_v2.0.pine     # Código Pine Script v2.0
    ├── n8n/
    │   ├── processador_v2.0.js  # Processador n8n
    │   └── workflow.json         # Workflow n8n completo
    └── docs/
        └── CHANGELOG.md          # Histórico de mudanças
```

---

## 🔄 INTEGRAÇÃO ENTRE INDICADORES

### **Fluxo de Análise:**

```
┌─────────────────────────────────────────────────────────────┐
│                    ANÁLISE COMPLETA                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ USDT.D v2.0 (Contexto Macro)                           │
│     └─ Identifica momento do mercado (BULLISH/BEARISH)     │
│                                                             │
│  2️⃣ TRS v6.1 (Reversões de Tendência)                      │
│     └─ Detecta reversões com validação tripla + MTF        │
│                                                             │
│  3️⃣ DNP v2.0 (Setup Completo)                              │
│     └─ Confirmação final com análise MTF                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Uso Recomendado:**

1. **USDT.D:** Verificar contexto macro antes de operar
2. **TRS:** Identificar reversões de tendência com confluências
3. **DNP:** Entradas precisas com validação macro (MTF)

---

## 🛠️ TECNOLOGIAS

### **Indicadores:**
- **Pine Script v5/v6** - TradingView
- **Webhooks** - Comunicação em tempo real
- **JSON** - Formato de dados

### **Processamento:**
- **n8n** - Workflow automation
- **JavaScript** - Processamento de dados
- **Telegram API** - Notificações

### **Infraestrutura:**
- **TradingView** - Plataforma de gráficos
- **n8n Cloud** - Hospedagem de workflows
- **Telegram** - Canal de notificações

---

## 📊 LÓGICA MTF (MULTI-TIMEFRAME)

### **Conceito:**

A análise MTF (Multi-Timeframe) avalia a **tendência do fractal superior** para classificar a qualidade do setup.

### **Hierarquia de Timeframes:**

| Timeframe Atual | Fractal Superior (HTF) |
|-----------------|------------------------|
| 1 minuto        | 15 minutos             |
| 5 minutos       | 60 minutos (H1)        |
| 15 minutos      | 240 minutos (H4)       |
| 60 minutos (H1) | Daily (D)              |
| 240 minutos (H4)| Weekly (W)             |
| Daily (D)       | Monthly (M)            |

### **Detecção de Tendência (HTF):**

**Tendência de ALTA (3 condições simultâneas):**
1. EMA 55 > EMA 233
2. EMA 55 crescente (EMA55 > EMA55[1])
3. Preço acima da EMA 55 (Close > EMA55)

**Tendência de BAIXA (3 condições simultâneas):**
1. EMA 55 < EMA 233
2. EMA 55 decrescente (EMA55 < EMA55[1])
3. Preço abaixo da EMA 55 (Close < EMA55)

**Neutro:**
- Qualquer outra condição

### **Classificação de Setups:**

| Setup  | HTF Trend | Classificação | Emoji | Descrição |
|--------|-----------|---------------|-------|-----------|
| LONG   | ALTA      | PREMIUM       | ⭐⭐⭐ | Alta probabilidade |
| LONG   | BAIXA     | CONTRA        | 🔴    | Alto risco |
| LONG   | NEUTRO    | CAUTELA       | ⚠️    | Risco elevado |
| SHORT  | BAIXA     | PREMIUM       | ⭐⭐⭐ | Alta probabilidade |
| SHORT  | ALTA      | CONTRA        | 🔴    | Alto risco |
| SHORT  | NEUTRO    | CAUTELA       | ⚠️    | Risco elevado |

---

## 🚀 QUICK START

### **1. Configurar Indicadores no TradingView:**

1. Acesse o Pine Editor no TradingView
2. Copie o código do indicador desejado
3. Salve e adicione ao gráfico
4. Configure os alertas com webhook

### **2. Configurar Processamento no n8n:**

1. Acesse o n8n Cloud
2. Importe o workflow JSON
3. Configure o webhook URL
4. Adicione as credenciais do Telegram
5. Ative o workflow

### **3. Testar o Sistema:**

1. Dispare um alerta manual no TradingView
2. Verifique o recebimento no n8n
3. Confirme a notificação no Telegram

---

## 📚 DOCUMENTAÇÃO COMPLETA

- **DNP v2.0:** [`dnp/README.md`](dnp/README.md)
- **TRS v6.1:** [`trs/README.md`](trs/README.md)
- **USDT.D v2.0:** [`usdt-d/README.md`](usdt-d/README.md)

---

## 🔗 WEBHOOKS

### **URLs n8n:**
- **DNP:** `https://cryptomindia.app.n8n.cloud/webhook/dnp-alert`
- **TRS:** `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
- **USDT.D:** `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-alert`

---

## ⚠️ IMPORTANTE

### **Confidencialidade:**
- ✅ Todos os códigos são **proprietários**
- ✅ Não compartilhar publicamente
- ✅ Uso exclusivo do sistema CryptoMind IA

### **Atualizações:**
- ✅ Sempre usar a versão mais recente
- ✅ Verificar changelog antes de atualizar
- ✅ Testar em ambiente controlado

---

## 📝 CHANGELOG GERAL

### **[16/01/2026] - DNP v2.0 COM MTF**
- ✨ Adicionada lógica MTF ao DNP
- ✨ Classificação PREMIUM/CAUTELA/CONTRA
- ✨ Processador n8n atualizado
- 📚 Documentação completa criada

### **[10/01/2026] - TRS v6.1 + USDT.D v2.0**
- ✨ Setup TRS v6.1 completo
- ✨ Monitor USDT.D v2.0 atualizado
- 🔧 Correções de campos vazios
- 📚 Documentação completa

---

## 📞 SUPORTE

Para questões técnicas ou dúvidas sobre os indicadores:
- Consulte a documentação específica de cada indicador
- Verifique os changelogs para atualizações
- Abra uma issue no GitHub se necessário

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

**Código proprietário - Uso restrito**

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 16/01/2026  
**Versão:** 2.0
