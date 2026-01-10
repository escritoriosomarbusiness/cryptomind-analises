# 🎯 CONTEXTO ATUAL - CryptoMind IA

**Última Atualização:** 10/01/2026 00:15  
**Status:** ✅ Todos os sistemas operacionais

---

## ⚡ LEIA ISTO PRIMEIRO

Este arquivo contém o **estado atual completo** do sistema CryptoMind IA.  
Use como **ponto de partida** em qualquer nova sessão.

---

## 👤 USUÁRIO

**Nome:** Samuel  
**Perfil:** Trader de criptomoedas  
**Nível Técnico:** Leigo em programação, MCP e integrações  
**Expectativa:** Sistema 100% automatizado, sem intervenção manual  
**Timeframe Principal:** 5 minutos  
**Ativos Monitorados:** BNB, ADA, LINK, BTC, ETH, SOL, XRP  

**Preferências Técnicas:**
- Lookback Pivots: **5** (para 5 minutos)
- Filtro de candle forte: **0.66** (terço superior/inferior)
- Filosofia: **Qualidade > Quantidade** de sinais

---

## 🏗️ ARQUITETURA DO SISTEMA

### **3 Sistemas Principais:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CRYPTOMIND IA                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Setup TRS v6.1 (Trend Reversal Setup)                  │
│     ├─ TradingView (Pine Script)                           │
│     ├─ n8n (Processamento)                                 │
│     └─ Telegram (Notificações)                             │
│                                                             │
│  2. Monitor USDT.D v2.0 (Análise Macro)                    │
│     ├─ TradingView (Pine Script)                           │
│     ├─ n8n (Processamento)                                 │
│     └─ Telegram (Notificações)                             │
│                                                             │
│  3. Análises Agendadas (Abertura e Fechamento)             │
│     ├─ GitHub Actions (Agendamento)                        │
│     ├─ Python Scripts (Geração)                            │
│     └─ Website (Visualização)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 INTEGRAÇÕES ATIVAS

### **TradingView → n8n:**
- **Setup TRS:** `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
- **USDT.D:** `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-alert`

### **n8n → Telegram:**
- **Bot:** CryptoMind IA
- **Chat ID:** (configurado no n8n)

### **GitHub:**
- **Repositório:** `escritoriosomarbusiness/cryptomind-analises`
- **Branch:** `main`
- **Acesso:** Autenticado via `gh` CLI

### **n8n:**
- **URL:** `https://cryptomindia.app.n8n.cloud/`
- **API Key:** Configurada em `$N8N_API_KEY`

---

## 📊 SISTEMA 1: Setup TRS v6.1

### **Status:** ✅ Operacional

### **Descrição:**
Sistema de detecção de reversões de tendência baseado em EMA 9 com validação tripla.

### **Características:**
- **Validação:** Pivots MTF + RSI + Fibonacci Golden Zone (Híbrido)
- **Confirmação:** Gatilho + Rompimento
- **Confluências:** Simples, Dupla (⭐), Tripla (🌟🌟)
- **Gestão de Risco:** Automática (alavancagem sugerida)
- **Filtros:** Candle forte (0.66), Min. 5 candles EMA, Cooldown 5

### **Alertas Configurados:**
| Par | Timeframe | Status |
|-----|-----------|--------|
| BNBUSDT | 5m | ✅ Ativo |
| ADAUSDT | 5m | ✅ Ativo |
| LINKUSDT | 5m | ✅ Ativo |

### **Tipos de Alerta:**
1. **TRIGGER** - Gatilho armado, aguardando rompimento
2. **CONFIRMED** - Rompimento confirmado, entrada ativa

### **Documentação:**
- `SETUP_TRS_V6.1.md` - Documentação completa
- `pinescript_setup_trs_v6.1.pine` - Pine Script (485 linhas)
- `n8n_workflow_setup_trs.json` - Workflow n8n

### **Última Atualização:** 10/01/2026

---

## 📊 SISTEMA 2: Monitor USDT.D v2.0

### **Status:** ✅ Operacional (Corrigido em 10/01/2026)

### **Descrição:**
Monitor de dominância do USDT.D para análise macro de mercado.

### **Características:**
- **Indicadores:** EMA 9, 21, 200
- **Alertas:** Proximidade de S/R, EMAs
- **Informações:** Dominância, Distância, Impacto (BULLISH/BEARISH)
- **Timeframe:** 4H (padrão)

### **Correções Implementadas (10/01/2026):**
- ✅ Campos vazios corrigidos (dominância, timeframe)
- ✅ Tipo de nível adicionado (Suporte/Resistência/EMA 200)
- ✅ Valor do nível adicionado
- ✅ Distância até o nível calculada
- ✅ Posição das EMAs com status (✅/❌)
- ✅ Impacto no mercado (BULLISH/BEARISH)

### **Documentação:**
- `MONITOR_USDT_D_V2.md` - Documentação completa
- `pinescript_usdt_d_monitor.pine` - Pine Script
- `n8n_workflow_usdt_d.json` - Workflow n8n

### **Última Atualização:** 10/01/2026

---

## 📊 SISTEMA 3: Análises Agendadas

### **Status:** ✅ Operacional (Reativado em 09/01/2026)

### **Descrição:**
Sistema de análises automáticas de abertura e fechamento do mercado.

### **Horários:**
- **Abertura:** ~09:30 (horário de Brasília)
- **Fechamento:** ~22:30 (horário de Brasília)

### **Última Execução:**
- **Abertura:** 09/01/2026 às 09:33
- **Fechamento:** 09/01/2026 às 22:26

### **Tecnologia:**
- **Agendamento:** GitHub Actions
- **Geração:** Python Scripts
- **Armazenamento:** JSON files
- **Visualização:** Website HTML

### **Documentação:**
- `ESPECIALISTA_CRYPTOMIND.md` - Prompt de especialização
- `README_SISTEMA.md` - Documentação do sistema
- `GITHUB_ACTIONS_SETUP.md` - Configuração do agendamento

---

## 🔧 CONFIGURAÇÕES TÉCNICAS

### **Pine Script - Setup TRS v6.1:**
```pinescript
// Configurações Principais
emaLength = 9
minCandlesBelowAbove = 5
cooldownCandles = 5
requireConfirmation = true
maxBarsToKeepSignal = 10

// Validação
validationMethod = "Hybrid (Pivots ou RSI ou Fibonacci)"
useMultiTimeframePivots = true
pivotLookback = 5  // Para 5 minutos
pivotTolerance = 0.1

// RSI
rsiPeriod = 14
rsiLookback = 5
rsiOversold = 30
rsiOverbought = 70

// Fibonacci
fibLookback = 3

// Filtro de Candle Forte
upperThird = low + (candleRange * 0.66)  // LONG
lowerThird = high - (candleRange * 0.66) // SHORT
```

### **n8n - Setup TRS:**
```javascript
// Gestão de Risco
const maxRealRisk = 15; // %
const suggestedLeverage = Math.min(10, Math.floor(maxRealRisk / riskPercent));
const realRisk = riskPercent * suggestedLeverage;

// Formatação de Preços
const formatPrice = (p) => {
  if (p === 0) return '0.00';
  if (p >= 1000) return p.toFixed(2);
  if (p >= 1) return p.toFixed(4);
  return p.toFixed(8);
};
```

### **n8n - Monitor USDT.D:**
```javascript
// Determinar nível mais próximo
if (nearEMA200) {
  nearestLevel = ema200;
  nearestLevelName = 'EMA 200';
} else if (nearResistance) {
  nearestLevel = resistance;
  nearestLevelName = 'Resistência';
} else if (nearSupport) {
  nearestLevel = support;
  nearestLevelName = 'Suporte';
}

// Calcular distância
const distToEMA200 = Math.abs(dominance - ema200);
const distToEMA200Pct = ((distToEMA200 / ema200) * 100).toFixed(3);
```

---

## 📝 DECISÕES TÉCNICAS IMPORTANTES

### **1. Filtro de Candle Forte (0.66):**
**Decisão:** MANTER em 0.66 (terço superior/inferior)  
**Motivo:** Reduz falsos sinais, garante força real do movimento  
**Alternativa Rejeitada:** 0.50 (metade do candle)  
**Data:** 10/01/2026

### **2. Lookback de Pivots (5):**
**Decisão:** Usar 5 para timeframe de 5 minutos  
**Motivo:** Detecta pivots mais recentes e relevantes para scalping  
**Padrão:** 10 para timeframes maiores  
**Data:** 10/01/2026

### **3. Gestão de Risco:**
**Fórmula:** `suggestedLeverage = Math.min(10, Math.floor(15 / riskPercent))`  
**Limites:**
- Risco por trade: 1% da banca
- Risco real máximo: 15%
- Alavancagem máxima: 10x
- Exposição máxima: 5% da banca

---

## 🧪 TESTES REALIZADOS

### **Setup TRS (10/01/2026):**
- ✅ Alerta TRIGGER recebido (ADAUSDT LONG)
- ✅ Validação dupla detectada (SR+RSI ⭐)
- ✅ Gestão de risco calculada (10x, 4.0% real)
- ✅ Template Telegram corrigido

### **Monitor USDT.D (10/01/2026):**
- ✅ Alerta recebido
- ✅ Campos vazios corrigidos
- ⏳ Aguardando próximo alerta para validação completa

---

## 📚 ARQUIVOS IMPORTANTES

### **Documentação Principal:**
1. `CONTEXTO_ATUAL.md` - **ESTE ARQUIVO** (leia primeiro!)
2. `CHANGELOG_2026-01-10.md` - Registro de mudanças
3. `SETUP_TRS_V6.1.md` - Setup TRS completo
4. `MONITOR_USDT_D_V2.md` - Monitor USDT.D completo
5. `ESPECIALISTA_CRYPTOMIND.md` - Prompt de especialização

### **Código:**
1. `pinescript_setup_trs_v6.1.pine` - Pine Script Setup TRS
2. `pinescript_usdt_d_monitor.pine` - Pine Script USDT.D
3. `n8n_workflow_setup_trs.json` - Workflow n8n Setup TRS
4. `n8n_workflow_usdt_d.json` - Workflow n8n USDT.D

### **Scripts Python:**
1. `scripts/generate_analysis.py` - Gera análises de abertura
2. `scripts/generate_closing_report.py` - Gera análises de fechamento
3. `scripts/generate_html.py` - Gera website
4. `scripts/archive_manager.py` - Gerencia arquivamento

---

## 🚨 PROBLEMAS CONHECIDOS

### **Nenhum problema crítico no momento**

**Últimos problemas resolvidos:**
- ✅ Monitor USDT.D com campos vazios (resolvido em 10/01/2026)
- ✅ Setup TRS com template antigo (resolvido em 10/01/2026)

---

## 📋 PRÓXIMOS PASSOS

### **Pendente:**
1. ⏳ Aguardar próximo alerta do Setup TRS para validação completa
2. ⏳ Aguardar próximo alerta do Monitor USDT.D para validar correções
3. ⏳ Exportar workflows n8n atualizados (opcional)

### **Concluído:**
- ✅ Setup TRS v6.1 implementado e testado
- ✅ Monitor USDT.D v2.0 corrigido
- ✅ Documentação completa criada
- ✅ Alertas TradingView configurados
- ✅ Workflows n8n atualizados
- ✅ GitHub atualizado com tudo

---

## 🔑 INFORMAÇÕES SENSÍVEIS

### **Webhooks:**
- Setup TRS: `https://cryptomindia.app.n8n.cloud/webhook/cryptomind-alert`
- USDT.D: `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-alert`

### **n8n:**
- URL: `https://cryptomindia.app.n8n.cloud/`
- API Key: Disponível em `$N8N_API_KEY`

### **GitHub:**
- Repositório: `escritoriosomarbusiness/cryptomind-analises`
- Autenticação: Via `gh` CLI (já configurado)

---

## 💡 DICAS PARA PRÓXIMAS SESSÕES

### **Ao Iniciar Nova Sessão:**
1. ✅ Ler este arquivo (`CONTEXTO_ATUAL.md`)
2. ✅ Ler `CHANGELOG_2026-01-10.md` para entender últimas mudanças
3. ✅ Verificar status dos sistemas (todos devem estar ✅)
4. ✅ Perguntar ao usuário se há novos alertas ou problemas

### **Ao Fazer Mudanças:**
1. ✅ Atualizar este arquivo (`CONTEXTO_ATUAL.md`)
2. ✅ Criar novo `CHANGELOG_YYYY-MM-DD.md`
3. ✅ Atualizar documentação específica do sistema modificado
4. ✅ Fazer commit e push para GitHub

### **Ao Resolver Problemas:**
1. ✅ Documentar problema em `CHANGELOG`
2. ✅ Documentar solução em `CHANGELOG`
3. ✅ Atualizar seção "Problemas Conhecidos" deste arquivo
4. ✅ Atualizar documentação específica se necessário

---

## 🎯 FILOSOFIA DO PROJETO

### **Regras Invioláveis:**
1. **Automação Total** - 100% sem intervenção manual
2. **Preservação do Sistema** - Nunca quebrar funcionalidades existentes
3. **Custo Zero** - Não gerar gastos antes da validação
4. **Confidencialidade** - Algoritmos são propriedade intelectual

### **Princípios:**
- Simplicidade > Complexidade
- Confiabilidade > Features
- Manutenibilidade > Performance prematura
- Qualidade > Quantidade

---

## ✅ CHECKLIST DE VALIDAÇÃO

Use este checklist para verificar se tudo está funcionando:

### **Setup TRS:**
- [ ] Alertas configurados no TradingView
- [ ] Webhook respondendo
- [ ] n8n processando corretamente
- [ ] Telegram recebendo mensagens
- [ ] Mensagens com todos os campos preenchidos
- [ ] Gestão de risco calculada corretamente

### **Monitor USDT.D:**
- [ ] Alerta configurado no TradingView
- [ ] Webhook respondendo
- [ ] n8n processando corretamente
- [ ] Telegram recebendo mensagens
- [ ] Mensagens com todos os campos preenchidos
- [ ] Dominância, timeframe, S/R, distância, EMAs visíveis

### **Análises Agendadas:**
- [ ] GitHub Actions executando
- [ ] Análises de abertura sendo geradas
- [ ] Análises de fechamento sendo geradas
- [ ] Website sendo atualizado
- [ ] Arquivos JSON sendo criados

---

**ESTE ARQUIVO É A FONTE DA VERDADE DO SISTEMA!**  
**SEMPRE ATUALIZE APÓS QUALQUER MUDANÇA!**

---

**Última Atualização:** 10/01/2026 00:15  
**Atualizado por:** Manus (CryptoMind IA)  
**Próxima Revisão:** Após qualquer mudança no sistema
