# 🧠 CryptoMind IA - Sistema Completo de Trading

**Sistema autônomo de análise técnica e sinais de trading para criptomoedas**

[![Status](https://img.shields.io/badge/Status-Operacional-success)](https://github.com/escritoriosomarbusiness/cryptomind-analises)
[![Versão](https://img.shields.io/badge/Versão-2.0-blue)](https://github.com/escritoriosomarbusiness/cryptomind-analises)
[![Última Atualização](https://img.shields.io/badge/Atualização-10%2F01%2F2026-orange)](https://github.com/escritoriosomarbusiness/cryptomind-analises)

---

## 📋 INÍCIO RÁPIDO

**🚨 LEIA PRIMEIRO:** [`CONTEXTO_ATUAL.md`](CONTEXTO_ATUAL.md) - Estado completo do sistema

**📝 Última Atualização:** [`CHANGELOG_2026-01-10.md`](CHANGELOG_2026-01-10.md)

---

## 🎯 VISÃO GERAL

O **CryptoMind IA** é um ecossistema completo de trading automatizado que combina:

1. **Setup TRS v6.1** - Sinais de reversão de tendência com validação tripla
2. **Monitor USDT.D v2.0** - Análise macro de mercado em tempo real
3. **Análises Agendadas** - Relatórios diários de abertura e fechamento

**Filosofia:** 100% automatizado, sem intervenção manual, custo zero.

---

## 🏗️ ARQUITETURA

```
┌─────────────────────────────────────────────────────────────┐
│                    CRYPTOMIND IA                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Setup TRS v6.1 (Trend Reversal Setup)                  │
│     ├─ TradingView (Pine Script)                           │
│     ├─ n8n (Processamento)                                 │
│     └─ Telegram (Notificações)                             │
│                                                             │
│  📈 Monitor USDT.D v2.0 (Análise Macro)                    │
│     ├─ TradingView (Pine Script)                           │
│     ├─ n8n (Processamento)                                 │
│     └─ Telegram (Notificações)                             │
│                                                             │
│  📅 Análises Agendadas (Abertura e Fechamento)             │
│     ├─ GitHub Actions (Agendamento)                        │
│     ├─ Python Scripts (Geração)                            │
│     └─ Website (Visualização)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 SISTEMAS

### 1. Setup TRS v6.1 (Trend Reversal Setup)

**Status:** ✅ Operacional  
**Última Atualização:** 10/01/2026

Sistema de detecção de reversões de tendência baseado em EMA 9 com validação tripla.

**Características:**
- ✅ Validação Híbrida: Pivots MTF + RSI + Fibonacci Golden Zone
- ✅ Sistema de Confirmação: Gatilho + Rompimento
- ✅ Detecção de Confluências: Simples, Dupla (⭐), Tripla (🌟🌟)
- ✅ Gestão de Risco Automática: Alavancagem sugerida
- ✅ Cálculo Automático: Entry, SL, T1, T2, Trailing Stop

**Documentação:** [`SETUP_TRS_V6.1.md`](SETUP_TRS_V6.1.md)  
**Pine Script:** [`pinescript_setup_trs_v6.1.pine`](pinescript_setup_trs_v6.1.pine)

---

### 2. Monitor USDT.D v2.0

**Status:** ✅ Operacional (Atualizado em 10/01/2026)  
**Última Atualização:** 10/01/2026

Monitor de dominância do USDT.D para análise macro de mercado.

**Características:**
- ✅ Alertas de Proximidade: Suporte, Resistência, EMA 200
- ✅ Informações Completas: Dominância, Distância, Impacto
- ✅ Posição das EMAs: EMA 9, 21, 200 com status
- ✅ Interpretação: BULLISH/BEARISH para cripto

**Documentação:** [`MONITOR_USDT_D_V2.md`](MONITOR_USDT_D_V2.md)  
**Pine Script:** [`pinescript_usdt_d_monitor.pine`](pinescript_usdt_d_monitor.pine)

---

### 3. Análises Agendadas

**Status:** ✅ Operacional  
**Última Execução:** 09/01/2026

Sistema de análises automáticas de abertura e fechamento do mercado.

**Características:**
- ✅ Análise de Abertura: ~09:30 BRT
- ✅ Análise de Fechamento: ~22:30 BRT
- ✅ Ativos: BTC, ETH, SOL, BNB, XRP
- ✅ Indicadores: USDT.D, BTC.D, Fear & Greed

**Website:** [analises.cryptomindia.com](https://analises.cryptomindia.com)  
**Documentação:** [`README_SISTEMA.md`](README_SISTEMA.md)

---

## 📚 DOCUMENTAÇÃO

### **Essencial (Leia Primeiro):**
1. [`CONTEXTO_ATUAL.md`](CONTEXTO_ATUAL.md) - **Estado completo do sistema**
2. [`CHANGELOG_2026-01-10.md`](CHANGELOG_2026-01-10.md) - Últimas mudanças
3. [`ESPECIALISTA_CRYPTOMIND.md`](ESPECIALISTA_CRYPTOMIND.md) - Prompt de especialização

### **Sistemas:**
4. [`SETUP_TRS_V6.1.md`](SETUP_TRS_V6.1.md) - Setup TRS completo
5. [`MONITOR_USDT_D_V2.md`](MONITOR_USDT_D_V2.md) - Monitor USDT.D completo
6. [`README_SISTEMA.md`](README_SISTEMA.md) - Análises agendadas

### **Técnica:**
7. [`ARCHITECTURE.md`](ARCHITECTURE.md) - Arquitetura do sistema
8. [`GITHUB_ACTIONS_SETUP.md`](GITHUB_ACTIONS_SETUP.md) - Configuração de agendamento

---

## 🛠️ TECNOLOGIAS

### **Trading:**
- **TradingView** - Pine Script v6
- **n8n** - Workflow automation
- **Telegram** - Notificações

### **Análises:**
- **Python 3.11** - Scripts de geração
- **GitHub Actions** - Agendamento
- **GitHub Pages** - Hospedagem

### **Frontend:**
- **HTML5** - Estrutura
- **CSS3** - Design System
- **JavaScript** - Interatividade

---

## 🔗 INTEGRAÇÕES

### **Webhooks:**
- Setup TRS: `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
- USDT.D: `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-alert`

### **n8n:**
- URL: `https://cryptomindia.app.n8n.cloud/`
- Workflows: 3 ativos

### **Telegram:**
- Bot: CryptoMind IA
- Notificações em tempo real

---

## 📊 ATIVOS MONITORADOS

### **Principais:**
- **BTC** (Bitcoin)
- **ETH** (Ethereum)
- **SOL** (Solana)
- **BNB** (Binance Coin)
- **XRP** (Ripple)

### **Indicadores:**
- **USDT.D** (Dominância USDT)
- **BTC.D** (Dominância Bitcoin)
- **Fear & Greed Index**

---

## ⚙️ CONFIGURAÇÕES

### **Setup TRS v6.1:**
- **Timeframe:** 5 minutos (principal)
- **Lookback Pivots:** 5
- **Filtro Candle:** 0.66 (terço superior/inferior)
- **Min. Candles EMA:** 5
- **Cooldown:** 5 candles

### **Monitor USDT.D:**
- **Timeframe:** 4 horas
- **EMAs:** 9, 21, 200
- **Alertas:** Proximidade de S/R

### **Análises Agendadas:**
- **Abertura:** 09:30 BRT
- **Fechamento:** 22:30 BRT

---

## 🧪 STATUS DOS TESTES

### **Setup TRS (10/01/2026):**
- ✅ Alerta TRIGGER recebido
- ✅ Validação dupla detectada (SR+RSI ⭐)
- ✅ Gestão de risco calculada
- ✅ Template Telegram funcionando

### **Monitor USDT.D (10/01/2026):**
- ✅ Campos vazios corrigidos
- ✅ Informações completas
- ⏳ Aguardando próximo alerta

---

## 📝 CHANGELOG

### **[10/01/2026] - Setup TRS v6.1 + Monitor USDT.D v2.0**

**Adicionado:**
- ✨ Setup TRS v6.1 completo
- ✨ Documentação completa
- ✨ Pine Script (485 linhas)
- ✨ Integração n8n

**Corrigido:**
- 🔧 Monitor USDT.D campos vazios
- 🔧 Template Telegram atualizado
- 🔧 Informações completas (dominância, S/R, distância, EMAs)

**Documentação:**
- 📚 CONTEXTO_ATUAL.md
- 📚 SETUP_TRS_V6.1.md
- 📚 MONITOR_USDT_D_V2.md
- 📚 CHANGELOG_2026-01-10.md

[Ver changelog completo](CHANGELOG_2026-01-10.md)

---

## 🔐 SEGURANÇA

- ✅ Webhooks privados
- ✅ API Keys em variáveis de ambiente
- ✅ Repositório privado
- ✅ Algoritmos proprietários

---

## 📱 RESPONSIVO

Todos os sistemas funcionam perfeitamente em:
- ✅ Desktop
- ✅ Tablet
- ✅ Smartphone

---

## 🔗 LINKS

- **Website:** [cryptomindia.com](https://cryptomindia.com)
- **Análises:** [analises.cryptomindia.com](https://analises.cryptomindia.com)
- **GitHub:** [escritoriosomarbusiness/cryptomind-analises](https://github.com/escritoriosomarbusiness/cryptomind-analises)

---

## ⚠️ DISCLAIMER

Esta análise não constitui recomendação de investimento. Trading de criptomoedas envolve riscos significativos. Faça sua própria pesquisa e opere com responsabilidade.

---

## 📞 SUPORTE

Para questões técnicas ou sugestões, abra uma issue no GitHub.

---

## 📄 LICENÇA

© 2026 CryptoMind IA. Todos os direitos reservados.

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 10/01/2026  
**Versão:** 2.0
