# 🤖 GUIA MVP - Bot Telegram Configurável

**Data:** 10/01/2026  
**Objetivo:** Implementar sistema de preferências de usuário no Telegram

---

## 📋 VISÃO GERAL

### **O que vamos criar:**
1. Tabela no Airtable para armazenar preferências
2. Workflow n8n para bot de configuração (comandos /start, /config, /status)
3. Workflows n8n para alertas personalizados (DNP e TRS)

### **Resultado final:**
- Usuário envia `/start` → Cadastrado
- Usuário envia `/config` → Menu para escolher: BTC | ALTS | TODOS
- Alertas são filtrados conforme preferência

---

## 🔧 FASE 1: CRIAR TABELA NO AIRTABLE

### **PASSO 1.1: Acessar Airtable**

1. Abrir: https://airtable.com
2. Fazer login

### **PASSO 1.2: Criar Nova Base**

1. Clicar em **"+ Create"** (ou "Add a base")
2. Selecionar **"Start from scratch"**
3. Nome da base: **"CryptoMind Bot"**
4. Clicar em **"Create base"**

### **PASSO 1.3: Renomear Tabela**

1. A tabela padrão se chama "Table 1"
2. Clicar duas vezes no nome
3. Renomear para: **"Preferencias"**

### **PASSO 1.4: Criar Campos**

Deletar os campos padrão e criar os seguintes:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `chat_id` | Number | ID do chat do Telegram |
| `username` | Single line text | Username do usuário |
| `first_name` | Single line text | Primeiro nome |
| `filtro_moedas` | Single select | BTC, ALTS, TODOS |
| `filtro_timeframes` | Multiple select | 5, 15, 60, 240 |
| `filtro_setups` | Multiple select | TRS, DNP |
| `ativo` | Checkbox | Se está recebendo alertas |
| `created_at` | Created time | Data de cadastro |
| `updated_at` | Last modified time | Última atualização |

### **PASSO 1.5: Configurar Campo "filtro_moedas"**

1. Clicar no campo `filtro_moedas`
2. Tipo: **Single select**
3. Adicionar opções:
   - `BTC`
   - `ALTS`
   - `TODOS`
4. Salvar

### **PASSO 1.6: Configurar Campo "filtro_timeframes"**

1. Clicar no campo `filtro_timeframes`
2. Tipo: **Multiple select**
3. Adicionar opções:
   - `5`
   - `15`
   - `60`
   - `240`
4. Salvar

### **PASSO 1.7: Configurar Campo "filtro_setups"**

1. Clicar no campo `filtro_setups`
2. Tipo: **Multiple select**
3. Adicionar opções:
   - `TRS`
   - `DNP`
4. Salvar

### **PASSO 1.8: Anotar IDs**

1. Abrir a base criada
2. Na URL, copiar o **Base ID** (começa com `app...`)
3. Clicar na tabela "Preferencias"
4. Na URL, copiar o **Table ID** (começa com `tbl...`)

**Exemplo de URL:**
```
https://airtable.com/appXXXXXXXXXXXXX/tblYYYYYYYYYYYYY/...
                     ↑ Base ID           ↑ Table ID
```

**ANOTAR:**
- Base ID: `app_______________`
- Table ID: `tbl_______________`

---

## 🔧 FASE 2: CRIAR WORKFLOW BOT CONFIGURAÇÃO

### **PASSO 2.1: Criar Novo Workflow**

1. Abrir n8n: https://cryptomindia.app.n8n.cloud
2. Clicar em **"Create workflow"**
3. Renomear para: **"Bot Telegram - Configuração"**

### **PASSO 2.2: Importar Workflow**

1. Clicar nos **3 pontinhos** (⋮) no canto superior direito
2. Clicar em **"Import from File"**
3. Selecionar o arquivo: **`bot_config_workflow.json`**
4. Clicar em **"Import"**

### **PASSO 2.3: Configurar Credenciais Telegram**

1. Clicar no nó **"Telegram Trigger"**
2. Em **"Credentials"**, selecionar as credenciais existentes
3. Se não tiver, criar nova com o token do bot

### **PASSO 2.4: Configurar Airtable**

1. Clicar em cada nó que usa Airtable
2. Atualizar o **Base ID** e **Table ID** com os valores anotados

### **PASSO 2.5: Salvar e Ativar**

1. Clicar em **"Salvar"**
2. Ativar o workflow (toggle "Active")

---

## 🔧 FASE 3: CRIAR WORKFLOWS DE ALERTAS PERSONALIZADOS

### **PASSO 3.1: Workflow DNP Personalizado**

1. Criar novo workflow: **"DNP - Alertas Personalizados"**
2. Importar arquivo: **`dnp_alertas_personalizados.json`**
3. Configurar credenciais Telegram
4. Atualizar Base ID e Table ID do Airtable
5. Salvar e Ativar

### **PASSO 3.2: Workflow TRS Personalizado**

1. Criar novo workflow: **"TRS - Alertas Personalizados"**
2. Importar arquivo: **`trs_alertas_personalizados.json`**
3. Configurar credenciais Telegram
4. Atualizar Base ID e Table ID do Airtable
5. Salvar e Ativar

### **PASSO 3.3: Atualizar Alertas no TradingView**

Atualizar os webhooks dos alertas:

**DNP:**
```
https://cryptomindia.app.n8n.cloud/webhook/dnp-personalizado
```

**TRS:**
```
https://cryptomindia.app.n8n.cloud/webhook/trs-personalizado
```

---

## 🔧 FASE 4: TESTAR

### **PASSO 4.1: Testar Bot**

1. Abrir Telegram
2. Procurar pelo bot CryptoMind IA
3. Enviar: `/start`
4. Verificar se cadastrou no Airtable
5. Enviar: `/config`
6. Selecionar preferência (BTC, ALTS ou TODOS)
7. Enviar: `/status`
8. Verificar configuração

### **PASSO 4.2: Testar Alertas**

1. Aguardar um alerta real
2. Verificar se chegou no Telegram
3. Se não chegou, verificar logs no n8n

---

## 📁 ARQUIVOS NECESSÁRIOS

1. **`bot_config_workflow.json`** - Workflow de configuração do bot
2. **`dnp_alertas_personalizados.json`** - Workflow DNP com filtros
3. **`trs_alertas_personalizados.json`** - Workflow TRS com filtros

---

## ⚠️ IMPORTANTE

- **NÃO DESATIVAR** os workflows antigos (DNP e TRS) até validar os novos
- **TESTAR** completamente antes de migrar
- **BACKUP** dos workflows antigos está garantido

---

## 📞 SUPORTE

Se algo der errado:
1. Verificar logs no n8n (Executions)
2. Verificar se credenciais estão corretas
3. Verificar se Base ID e Table ID estão corretos
