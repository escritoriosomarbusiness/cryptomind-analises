# 🤖 Bot Telegram Configurável - CryptoMind IA

**Status:** 📋 Planejamento  
**Data:** 10/01/2026  
**Versão:** 1.0 (Esboço)

---

## 🎯 OBJETIVO

Criar um bot Telegram interativo que permita aos usuários **personalizar** quais alertas de trading desejam receber, filtrando por:

1. ⏱️ **Timeframes** (5min, 15min, 1H, 4H)
2. 📈 **Setups** (TRS, DNP)
3. 💰 **Moedas** (BTC, ALTS, ou seleção individual)

---

## 🏗️ ARQUITETURA

```
TradingView → n8n (Webhook) → Filtro de Preferências → Envio Personalizado → Telegram
                                        ↓
                                Banco de Dados
                                (User Preferences)
```

---

## 📱 INTERFACE DO USUÁRIO

### **COMANDOS PRINCIPAIS:**

```
/start → Mensagem de boas-vindas + instruções
/configurar → Abrir menu de configurações
/status → Ver configurações atuais
/ajuda → Instruções de uso
```

---

### **MENU INICIAL:**

```
🤖 Bem-vindo ao CryptoMind IA!

Receba alertas personalizados dos melhores setups de trading.

📊 Configurações Atuais:
• Timeframes: 5min, 15min ✅
• Setups: TRS ✅, DNP ✅
• Moedas: BTC + ALTS ✅

Escolha o que deseja configurar:
[⏱️ Timeframes] [📈 Setups] [💰 Moedas]

[📊 Ver Estatísticas] [❓ Ajuda]
```

---

### **SUBMENU: TIMEFRAMES**

```
⏱️ Escolha os timeframes que deseja receber:

☑️ 5 minutos (Scalping)
☑️ 15 minutos (Day Trade)
☐ 1 hora (Swing)
☐ 4 horas (Position)

[Selecionar Todos] [Limpar] [💾 Salvar]
[⬅️ Voltar]
```

---

### **SUBMENU: SETUPS**

```
📈 Escolha os setups que deseja receber:

☑️ TRS (Trend Reversal Setup)
   • Baseado em EMA 9 + Pivots/RSI/Fibonacci
   • Ideal para reversões de tendência

☑️ DNP (Didi's Needle Prick)
   • Baseado em Didi Index + ADX + REMI
   • Ideal para agulhadas próximas ao eixo

[💾 Salvar] [⬅️ Voltar]
```

---

### **SUBMENU: MOEDAS**

#### **Opção Simples (MVP):**

```
💰 Escolha as moedas que deseja receber:

☑️ BTC (Bitcoin)
   • BTCUSDT

☑️ ALTS (Altcoins)
   • ETHUSDT, ADAUSDT, SOLUSDT, etc.

[💾 Salvar] [⬅️ Voltar]
```

#### **Opção Avançada (Futuro):**

```
💰 Escolha as moedas individualmente:

☑️ BTCUSDT (Bitcoin)
☑️ ETHUSDT (Ethereum)
☑️ ADAUSDT (Cardano)
☐ SOLUSDT (Solana)
☐ DOGEUSDT (Dogecoin)
☐ BNBUSDT (Binance Coin)
☐ XRPUSDT (Ripple)
☐ MATICUSDT (Polygon)
☐ DOTUSDT (Polkadot)
☐ AVAXUSDT (Avalanche)

[Selecionar Todas] [Apenas BTC] [Apenas ALTS] [Limpar]
[💾 Salvar] [⬅️ Voltar]
```

---

## 💾 ARMAZENAMENTO DE PREFERÊNCIAS

### **ESTRUTURA DE DADOS:**

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `user_id` | Integer | ID do usuário no Telegram | `123456789` |
| `username` | String | Username do Telegram | `@joaotrader` |
| `timeframes` | Array | Timeframes selecionados | `["5", "15"]` |
| `setups` | Array | Setups selecionados | `["TRS", "DNP"]` |
| `moedas` | Array | Moedas selecionadas | `["BTC", "ALTS"]` |
| `moedas_especificas` | Array | Lista individual (futuro) | `["BTCUSDT", "ETHUSDT"]` |
| `created_at` | Timestamp | Data de cadastro | `2026-01-10 14:30:00` |
| `updated_at` | Timestamp | Última atualização | `2026-01-10 15:45:00` |
| `active` | Boolean | Usuário ativo | `true` |

---

### **EXEMPLO DE REGISTRO:**

```json
{
  "user_id": 123456789,
  "username": "@joaotrader",
  "timeframes": ["5", "15"],
  "setups": ["TRS", "DNP"],
  "moedas": ["BTC", "ALTS"],
  "moedas_especificas": [],
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T15:45:00Z",
  "active": true
}
```

---

## 🔧 IMPLEMENTAÇÃO TÉCNICA

### **FASE 1: MVP (Mínimo Viável)**

#### **1. Criar Bot no Telegram:**
- ✅ Criar bot via @BotFather
- ✅ Obter token de API
- ✅ Configurar comandos básicos

#### **2. Workflow n8n:**

**Nós necessários:**
1. **Telegram Trigger** → Recebe comandos do usuário
2. **Switch** → Roteia comandos (/start, /configurar, /status)
3. **Google Sheets** → Armazena preferências
4. **Code (JS)** → Processa lógica de filtros
5. **Telegram Send** → Envia mensagens e menus

#### **3. Armazenamento (Google Sheets):**

**Planilha: "User_Preferences"**

| user_id | username | timeframes | setups | moedas | active | updated_at |
|---------|----------|------------|--------|--------|--------|------------|
| 123456789 | @joao | 5,15 | TRS,DNP | BTC,ALTS | TRUE | 2026-01-10 |

#### **4. Filtro de Alertas:**

```javascript
// Receber alerta do TradingView
const alert = $input.first().json;

// Buscar todos os usuários ativos
const users = getActiveUsers();

// Para cada usuário, verificar preferências
for (const user of users) {
  const prefs = getUserPreferences(user.user_id);
  
  // Filtrar por timeframe
  if (!prefs.timeframes.includes(alert.timeframe)) continue;
  
  // Filtrar por setup
  if (!prefs.setups.includes(alert.setup)) continue;
  
  // Filtrar por moeda
  const symbol = alert.symbol;
  const isBTC = symbol.includes('BTC');
  const isALT = !isBTC;
  
  if (prefs.moedas.includes('BTC') && !isBTC) continue;
  if (prefs.moedas.includes('ALTS') && !isALT) continue;
  
  // Enviar alerta personalizado
  sendTelegramAlert(user.user_id, alert);
}
```

---

### **FASE 2: AVANÇADO**

#### **1. Seleção Individual de Moedas:**
- ✅ Adicionar campo `moedas_especificas` no banco
- ✅ Criar menu com lista completa de moedas
- ✅ Permitir seleção múltipla

#### **2. Migrar para Airtable:**
- ✅ Melhor performance
- ✅ Interface mais amigável
- ✅ API mais robusta

#### **3. Estatísticas:**
- ✅ Mostrar quantos alertas recebeu hoje
- ✅ Mostrar performance dos setups
- ✅ Gráfico de win rate

---

### **FASE 3: PREMIUM**

#### **1. Notificações Inteligentes:**
- ✅ Agrupar alertas similares
- ✅ Resumo diário/semanal
- ✅ Alertas de alta prioridade

#### **2. Histórico:**
- ✅ Ver últimos 10 alertas
- ✅ Filtrar por setup/moeda
- ✅ Exportar para CSV

#### **3. Análise de Performance:**
- ✅ Win rate por setup
- ✅ Melhor timeframe
- ✅ Moedas mais lucrativas

---

## 📊 OPÇÕES DE ARMAZENAMENTO

### **Opção 1: Google Sheets** ⭐ (MVP)

**Vantagens:**
- ✅ Fácil de implementar no n8n
- ✅ Fácil de visualizar e editar manualmente
- ✅ Gratuito
- ✅ Integração nativa no n8n

**Desvantagens:**
- ❌ Pode ser lento com muitos usuários (>1000)
- ❌ Limite de requisições por minuto

**Quando usar:** MVP, testes iniciais, até 500 usuários

---

### **Opção 2: Airtable** ⭐⭐ (Intermediário)

**Vantagens:**
- ✅ Interface bonita e profissional
- ✅ API fácil de usar
- ✅ Você já tem integração configurada
- ✅ Escala bem (até 50k usuários)
- ✅ Automações nativas

**Desvantagens:**
- ❌ Plano pago para mais de 1.200 registros
- ❌ Limite de 5 requisições/segundo

**Quando usar:** Após validar MVP, crescimento até 10k usuários

---

### **Opção 3: SQLite/PostgreSQL** ⭐⭐⭐ (Profissional)

**Vantagens:**
- ✅ Mais rápido
- ✅ Mais robusto
- ✅ Sem limites de requisições
- ✅ Gratuito (PostgreSQL via Supabase)

**Desvantagens:**
- ❌ Mais complexo de implementar
- ❌ Requer servidor/hosting

**Quando usar:** Escala (>10k usuários), produção séria

---

## 🎯 ROADMAP DE IMPLEMENTAÇÃO

### **✅ Fase 1: MVP (2-3 dias)**
- [x] Criar bot no Telegram
- [ ] Implementar comandos básicos (/start, /configurar)
- [ ] Criar menu com botões inline
- [ ] Implementar filtros: BTC vs ALTS
- [ ] Implementar filtros: TRS vs DNP
- [ ] Armazenar preferências no Google Sheets
- [ ] Testar com 5-10 usuários

### **🔄 Fase 2: Avançado (1 semana)**
- [ ] Adicionar filtro por timeframe
- [ ] Implementar seleção individual de moedas
- [ ] Migrar para Airtable
- [ ] Adicionar comando /status
- [ ] Adicionar estatísticas básicas

### **🚀 Fase 3: Premium (2 semanas)**
- [ ] Notificações push personalizadas
- [ ] Histórico de sinais
- [ ] Análise de performance
- [ ] Dashboard web (opcional)
- [ ] Exportação de dados

---

## 💡 EXEMPLOS DE MENSAGENS

### **Alerta Personalizado:**

```
🔔 ALERTA PERSONALIZADO

✅ Setup: TRS
⏱️ Timeframe: 5 minutos
💰 Moeda: BTCUSDT

🟢 LONG CONFIRMADO

🎯 Entrada: $90,454.97
🛑 Stop Loss: $90,300.00
📈 Alvos:
   1️⃣ $90,609.94 (1R)
   2️⃣ $90,764.91 (2R)

⚙️ Gestão: 10x alavancagem

⚠️ Não é recomendação de investimento

[📊 Ver Detalhes] [⚙️ Configurações]
```

---

### **Resumo Diário:**

```
📊 RESUMO DO DIA - 10/01/2026

Você recebeu 8 alertas hoje:

📈 TRS: 5 alertas
   • 3 LONG, 2 SHORT
   • BTC: 3, ALTS: 2

📈 DNP: 3 alertas
   • 2 LONG, 1 SHORT
   • BTC: 2, ALTS: 1

⏱️ Por Timeframe:
   • 5min: 5 alertas
   • 15min: 3 alertas

[Ver Histórico] [Estatísticas]
```

---

## ⚠️ CONSIDERAÇÕES IMPORTANTES

### **1. Privacidade:**
- ✅ Não armazenar dados sensíveis
- ✅ Permitir exclusão de dados (/deletar)
- ✅ LGPD compliance

### **2. Performance:**
- ✅ Limitar envios simultâneos (evitar spam)
- ✅ Usar fila de mensagens (queue)
- ✅ Implementar rate limiting

### **3. Segurança:**
- ✅ Validar inputs do usuário
- ✅ Proteger webhook do n8n
- ✅ Não expor tokens/APIs

### **4. UX:**
- ✅ Mensagens claras e objetivas
- ✅ Botões intuitivos
- ✅ Feedback imediato ao usuário

---

## 📝 NOTAS ADICIONAIS

### **Ideias Futuras:**

1. **Alertas de Preço:**
   - Usuário define preço alvo
   - Recebe notificação quando atingir

2. **Copy Trading:**
   - Usuário autoriza execução automática
   - Bot executa trades via API da exchange

3. **Análise de Sentimento:**
   - Integrar com Twitter/Reddit
   - Alertas de notícias relevantes

4. **Gamificação:**
   - Ranking de usuários
   - Badges por performance
   - Desafios semanais

---

## 🔗 REFERÊNCIAS

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [n8n Telegram Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Airtable API](https://airtable.com/developers/web/api/introduction)

---

**Desenvolvido por:** CryptoMind IA  
**Versão:** 1.0 (Esboço)  
**Status:** 📋 Aguardando implementação após configuração dos alertas DNP
