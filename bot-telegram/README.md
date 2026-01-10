# 🤖 Bot Telegram CryptoMind IA - Configuração Completa

## 📋 Visão Geral

Bot Telegram configurável para alertas de criptomoedas com preferências personalizadas de:
- 💰 **Moedas** (BTC, ETH, SOL, etc.)
- 💵 **Valores USDT** (100, 500, 1000, etc.)
- 🕒 **Timeframes** (5min, 15min, 1h, 4h)

---

## 🚀 Status Atual

### ✅ Implementado
- [x] Comando `/start` - Inicialização e cadastro
- [x] Comando `/config` - Menu de configuração
- [x] Comando `/status` - Visualizar preferências
- [x] Callbacks funcionais (correção v2→v3)
- [x] Integração com Airtable
- [x] Seleção de moedas
- [x] Seleção de valores USDT
- [x] **Seleção de timeframes** (nova funcionalidade)

### 🔧 Correções Aplicadas
- [x] Estrutura Switch v2→v3 (compatibilidade n8n 2.1.5+)
- [x] Callbacks do Telegram funcionando
- [x] Roteamento correto de mensagens

---

## 📁 Estrutura de Arquivos

```
bot-telegram/
├── README.md                          # Este arquivo
├── GUIA_RAPIDO_TIMEFRAMES.md         # Implementação de timeframes (10 min)
├── IMPLEMENTACAO_TIMEFRAMES.md        # Documentação técnica completa
└── novos_nos_timeframes.json         # JSON dos novos nós

workflows/
├── workflow_corrigido_v3_final.json   # Workflow corrigido (v3)
├── workflow_v3_com_timeframes.json    # Workflow com timeframes
└── workflow_original_v2.json          # Backup do original (v2)

docs/bot/
├── SOLUCAO_COMPLETA_IMPLEMENTADA.md   # Análise técnica da correção
├── RESULTADO_FINAL_IMPLEMENTACAO.md   # Resultado executivo
├── CORRECAO_RAPIDA_NOMES_CORRETOS.md  # Guia de correção manual
├── PLANO_TESTES_VALIDACAO_100.md      # Plano de testes completo
└── CHECKLIST_VALIDACAO_RAPIDA.md      # Validação rápida (5 min)
```

---

## ⚡ Quick Start

### 1. Importar Workflow

**Opção A: Workflow Básico (Corrigido)**
```bash
Arquivo: workflows/workflow_corrigido_v3_final.json
Funcionalidades: Moedas + USDT
```

**Opção B: Workflow Completo (Com Timeframes)**
```bash
Arquivo: workflows/workflow_v3_com_timeframes.json
Funcionalidades: Moedas + USDT + Timeframes
```

### 2. Configurar Airtable

**Base:** `appTIDQW6MXCYntnW`  
**Tabela:** `Preferencias`

**Campos:**
- `chat_id` (Number)
- `username` (Text)
- `moeda_preferida` (Single select)
- `usdt_preferido` (Single select)
- `timeframe_preferido` (Single select) ← **Novo**

### 3. Configurar Credenciais n8n

- **Telegram Bot Token:** Configurar no nó "Telegram Trigger"
- **Airtable API Key:** Configurar nos nós Airtable

### 4. Ativar Workflow

1. Salvar workflow
2. Ativar (toggle no canto superior direito)
3. Testar com `/start` no bot

---

## 🎯 Funcionalidades

### Comandos Disponíveis

| Comando | Descrição | Status |
|---------|-----------|--------|
| `/start` | Iniciar bot e criar usuário | ✅ |
| `/config` | Menu de configuração | ✅ |
| `/status` | Ver preferências atuais | ✅ |

### Menu de Configuração

```
/config
  ├── 💰 Moedas
  │   └── [BTC] [ETH] [SOL] [XRP] ...
  ├── 💵 USDT
  │   └── [100] [500] [1000] [5000] ...
  └── 🕒 Timeframe
      └── [5min] [15min] [1h] [4h]
```

---

## 📊 Arquitetura

### Fluxo Principal

```
Telegram → n8n → Switch Comando → Processar Ação → Airtable → Resposta
```

### Switch Comando (4 regras)
1. `/start` → Processar Start
2. `/config` → Enviar Menu Config
3. `/status` → Buscar Usuário Status
4. `callback_query` → Processar Callback

### Switch Callback (6 regras)
1. `config_moedas` → Mostrar Menu Moedas
2. `config_usdt` → Mostrar Menu USDT
3. `set_moeda_*` → Atualizar Moeda
4. `set_usdt_*` → Atualizar USDT
5. `config_timeframe` → Mostrar Menu Timeframes ← **Novo**
6. `set_timeframe_*` → Atualizar Timeframe ← **Novo**

---

## 🔧 Implementação de Timeframes

### Guia Rápido (10 minutos)
Consulte: **`GUIA_RAPIDO_TIMEFRAMES.md`**

### Documentação Completa
Consulte: **`IMPLEMENTACAO_TIMEFRAMES.md`**

### JSON Pronto
Consulte: **`novos_nos_timeframes.json`**

---

## 🧪 Testes

### Validação Rápida (5 minutos)
```bash
1. /start → Mensagem de boas-vindas ✅
2. /config → Menu com 3 botões ✅
3. Clicar "Moedas" → Submenu aparece ✅
4. Clicar "BTC" → Confirmação ✅
5. /status → Exibe preferências ✅
```

### Validação Completa (10 testes)
Consulte: **`docs/bot/PLANO_TESTES_VALIDACAO_100.md`**

---

## 📈 Histórico de Mudanças

### 2026-01-10 - Correção Crítica + Timeframes

**Problema Resolvido:**
- Incompatibilidade estrutural Switch v2/v3
- Callbacks do Telegram não funcionavam

**Solução Aplicada:**
- Conversão automática v2→v3
- Estrutura `rules.values[]` implementada
- Callbacks 100% funcionais

**Nova Funcionalidade:**
- Seleção de timeframes (5min, 15min, 1h, 4h)
- Integração completa com Airtable
- Menu atualizado

---

## 🚨 Troubleshooting

### Callbacks não funcionam
**Causa:** Estrutura v2 ainda presente  
**Solução:** Importar `workflow_corrigido_v3_final.json`

### Timeframes não aparecem
**Causa:** Campo não criado no Airtable  
**Solução:** Adicionar campo `timeframe_preferido` (Single select)

### Erro ao salvar preferências
**Causa:** API Key sem permissão de escrita  
**Solução:** Verificar permissões no Airtable

---

## 📞 Informações Técnicas

**n8n Instance:** `https://cryptomindia.app.n8n.cloud`  
**Workflow ID:** `7V9SZdSeSfZELZ3l`  
**Versão n8n:** `2.1.5+`  
**Airtable Base:** `appTIDQW6MXCYntnW`  
**Tabela:** `Preferencias`

---

## 📚 Documentação Adicional

### Correção v2→v3
- [Solução Completa](../docs/bot/SOLUCAO_COMPLETA_IMPLEMENTADA.md)
- [Resultado Final](../docs/bot/RESULTADO_FINAL_IMPLEMENTACAO.md)
- [Guia de Correção Manual](../docs/bot/CORRECAO_RAPIDA_NOMES_CORRETOS.md)

### Testes e Validação
- [Plano de Testes Completo](../docs/bot/PLANO_TESTES_VALIDACAO_100.md)
- [Checklist Rápido](../docs/bot/CHECKLIST_VALIDACAO_RAPIDA.md)

### Implementação de Timeframes
- [Guia Rápido (10 min)](GUIA_RAPIDO_TIMEFRAMES.md)
- [Documentação Técnica](IMPLEMENTACAO_TIMEFRAMES.md)
- [JSON dos Nós](novos_nos_timeframes.json)

---

## ✅ Status do Projeto

**Versão Atual:** v1.2  
**Status:** ✅ Produção  
**Última Atualização:** 2026-01-10  
**Próximas Funcionalidades:** TBD

---

## 🎓 Conclusão

O bot está totalmente funcional com:
- ✅ Estrutura moderna (v3)
- ✅ Callbacks funcionando perfeitamente
- ✅ 3 tipos de configuração (moedas, USDT, timeframes)
- ✅ Integração completa com Airtable
- ✅ Documentação completa
- ✅ Testes validados

**Pronto para uso em produção!** 🚀
