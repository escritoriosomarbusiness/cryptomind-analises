# 🤖 Guia de Importação do Bot Telegram - Configuração DNP

## 📋 Visão Geral

Este guia explica como importar e configurar o workflow completo do bot de configuração Telegram no n8n.

---

## 📁 Arquivo do Workflow

**Arquivo:** `bot_config_workflow_FINAL.json`

**Características:**
- ✅ **18 nós** configurados e conectados
- ✅ **Headers Airtable** já configurados (não precisa de credenciais)
- ✅ **Token Airtable** embutido nos headers HTTP
- ⚠️ **Credencial Telegram** precisa ser configurada manualmente

---

## 🔧 Estrutura do Workflow

### **Comandos Implementados:**

1. **`/start`** - Cadastro de novo usuário
   - Cria registro no Airtable
   - Envia mensagem de boas-vindas
   - Configuração padrão: TODOS, USDT.D ativo

2. **`/config`** - Menu de configuração
   - Botão: 💰 Filtro de Moedas
   - Botão: 📊 Alertas USDT.D

3. **`/status`** - Ver configuração atual
   - Busca dados do usuário no Airtable
   - Formata e exibe preferências

4. **Callbacks (botões inline):**
   - `menu_moedas` → Mostra opções: BTC, ALTS, TODOS
   - `menu_usdt` → Mostra opções: Ativar, Desativar
   - `filtro_BTC`, `filtro_ALTS`, `filtro_TODOS` → Atualiza filtro de moedas
   - `usdt_on`, `usdt_off` → Atualiza preferência USDT.D

---

## 📊 Nós do Workflow

| # | Nome do Nó | Tipo | Função |
|---|------------|------|--------|
| 1 | Telegram Trigger | Trigger | Recebe mensagens e callbacks |
| 2 | Switch Comando | Switch | Roteia comandos (/start, /config, /status, callbacks) |
| 3 | Processar Start | Code | Prepara dados do novo usuário |
| 4 | Criar Usuário Airtable | HTTP Request | POST no Airtable |
| 5 | Enviar Boas-vindas | HTTP Request | Mensagem de cadastro |
| 6 | Enviar Menu Config | HTTP Request | Menu com botões inline |
| 7 | Buscar Usuário Status | HTTP Request | GET no Airtable |
| 8 | Formatar Status | Code | Formata mensagem de status |
| 9 | Enviar Status | HTTP Request | Envia status ao usuário |
| 10 | Processar Callback | Code | Extrai dados do callback |
| 11 | Switch Callback | Switch | Roteia callbacks |
| 12 | Mostrar Menu Moedas | HTTP Request | Menu de filtro de moedas |
| 13 | Mostrar Menu USDT | HTTP Request | Menu USDT.D |
| 14 | Buscar Usuário Callback | HTTP Request | GET no Airtable |
| 15 | Preparar Update | Code | Prepara dados para atualização |
| 16 | Atualizar Preferência | HTTP Request | PATCH no Airtable |
| 17 | Responder Callback | HTTP Request | Responde callback (popup) |
| 18 | Confirmar Atualização | HTTP Request | Mensagem de confirmação |

---

## 🚀 Passo a Passo: Importação

### **1. Acessar n8n**

```
https://cryptomindia.app.n8n.cloud
```

### **2. Importar Workflow**

1. Clique em **"+"** (novo workflow)
2. Clique nos **3 pontinhos** (menu) → **"Import from File"**
3. Selecione: `bot_config_workflow_FINAL.json`
4. Clique em **"Import"**

### **3. Configurar Credencial do Telegram**

⚠️ **IMPORTANTE:** O nó "Telegram Trigger" vai aparecer com um **triângulo vermelho** indicando que falta configurar a credencial.

**Como configurar:**

1. Clique no nó **"Telegram Trigger"** (primeiro nó)
2. Na seção **"Credential to connect with"**, clique em **"Select Credential"**
3. Selecione a credencial do Telegram que você já possui
4. Clique em **"Save"**

### **4. Verificar Headers Airtable**

Os seguintes nós já têm os headers configurados (não precisa fazer nada):

- ✅ Criar Usuário Airtable
- ✅ Buscar Usuário Status
- ✅ Buscar Usuário Callback
- ✅ Atualizar Preferência

**Para verificar (opcional):**

1. Clique em um dos nós acima
2. Role até **"Headers"**
3. Deve ter:
   - `Authorization: Bearer SEU_TOKEN_AIRTABLE_AQUI..`
   - `Content-Type: application/json`

### **5. Ativar Workflow**

1. Clique no botão **"Inactive"** (canto superior direito)
2. Deve mudar para **"Active"** (verde)

---

## ✅ Testar o Bot

### **Teste 1: Comando /start**

1. Abra o Telegram
2. Envie: `/start`
3. **Resultado esperado:**
   ```
   🤖 Bem-vindo ao CryptoMind IA!
   
   ✅ Você foi cadastrado com sucesso!
   
   📊 Configuração Padrão:
   • Moedas: TODAS
   • Alertas USDT.D: ✅ Ativo
   • Setups: TRS, DNP
   
   📝 Comandos:
   /config - Configurar preferências
   /status - Ver configuração atual
   ```

### **Teste 2: Comando /status**

1. Envie: `/status`
2. **Resultado esperado:**
   ```
   📊 Suas Configurações
   
   📊 Filtro de Moedas: TODOS
   📈 Alertas USDT.D: ✅ Ativo
   📡 Status: ✅ Ativo
   ```

### **Teste 3: Comando /config**

1. Envie: `/config`
2. **Resultado esperado:** Menu com 2 botões:
   - 💰 Filtro de Moedas
   - 📊 Alertas USDT.D

### **Teste 4: Configurar Moedas**

1. Clique em **"💰 Filtro de Moedas"**
2. Clique em **"₿ BTC"**
3. **Resultado esperado:**
   ```
   ✅ Preferência Atualizada!
   
   💰 Filtro de Moedas: BTC
   ```

### **Teste 5: Configurar USDT.D**

1. Envie `/config` novamente
2. Clique em **"📊 Alertas USDT.D"**
3. Clique em **"❌ Desativar"**
4. **Resultado esperado:**
   ```
   ✅ Preferência Atualizada!
   
   📊 Alertas USDT.D: ❌ Desativado
   ```

---

## 🔍 Verificar no Airtable

1. Acesse: https://airtable.com/appTIDQW6MXCYntnW/tblPreferencias
2. Deve ter um registro com:
   - `chat_id`: Seu ID do Telegram
   - `username`: Seu username
   - `filtro_moedas`: BTC (se você testou)
   - `filtro_usdt_d`: false (se você desativou)

---

## ⚠️ Troubleshooting

### **Erro: "Telegram Trigger" com triângulo vermelho**

**Causa:** Credencial do Telegram não configurada

**Solução:**
1. Clique no nó "Telegram Trigger"
2. Selecione a credencial do Telegram
3. Salve o workflow

### **Erro: "Usuário não encontrado" ao enviar /status**

**Causa:** Usuário não foi cadastrado com /start

**Solução:**
1. Envie `/start` primeiro
2. Depois envie `/status`

### **Erro: Headers Airtable não funcionam**

**Causa:** Headers podem ter sido removidos acidentalmente

**Solução:**
1. Clique no nó com erro (ex: "Criar Usuário Airtable")
2. Role até **"Headers"**
3. Ative **"Send Headers"**
4. Adicione:
   - Name: `Authorization`
   - Value: `Bearer SEU_TOKEN_AIRTABLE_AQUI`

### **Workflow não ativa**

**Causa:** Pode haver erro em algum nó

**Solução:**
1. Verifique se há nós com triângulo vermelho
2. Configure as credenciais faltantes
3. Salve o workflow
4. Tente ativar novamente

---

## 📚 Próximos Passos

Após o bot estar funcionando:

1. **Integrar com alertas DNP:**
   - Modificar workflow `n8n_workflow_dnp.json`
   - Adicionar nó para buscar preferências do usuário no Airtable
   - Filtrar alertas conforme `filtro_moedas` e `filtro_usdt_d`

2. **Criar alertas TRS:**
   - Desenvolver indicador TRS no Pine Script
   - Criar workflow similar ao DNP
   - Integrar com preferências do Airtable

3. **Adicionar mais filtros:**
   - Timeframes (1h, 4h, 1D)
   - Tipos de setup (apenas TRS, apenas DNP, ambos)
   - Alavancagem mínima/máxima

---

## 📞 Suporte

Se encontrar problemas, verifique:

1. ✅ Credencial do Telegram configurada
2. ✅ Workflow ativo (botão verde)
3. ✅ Headers Airtable nos 4 nós HTTP Request
4. ✅ Token Airtable correto
5. ✅ Base ID e Table ID corretos

---

**Criado por:** CryptoMind IA  
**Data:** 10/01/2026  
**Versão:** 1.0 FINAL
