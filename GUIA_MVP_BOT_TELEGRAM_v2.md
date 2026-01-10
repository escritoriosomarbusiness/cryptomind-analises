# 🤖 GUIA MVP - Bot Telegram Configurável v2

## 📋 ESCOPO

### Filtros Disponíveis:
- **Moedas:** BTC | ALTS | TODOS
- **USDT.D:** Ativo | Desativado

### Comandos:
- `/start` - Cadastrar usuário
- `/config` - Menu de configuração
- `/status` - Ver configuração atual

---

## 📁 ARQUIVOS NECESSÁRIOS

1. `bot_config_workflow_v2.json` - Bot de configuração
2. `dnp_alertas_personalizados.json` - Alertas DNP
3. `trs_alertas_personalizados.json` - Alertas TRS
4. `usdt_d_alertas_personalizados.json` - Alertas USDT.D

---

## FASE 1: AIRTABLE (5 min)

### Passo 1.1: Criar Base
1. Acessar https://airtable.com
2. Clicar em "Add a base"
3. Nome: **CryptoMind Bot**

### Passo 1.2: Criar Tabela
1. Renomear "Table 1" para **Preferencias**

### Passo 1.3: Criar Campos

| Campo | Tipo | Observação |
|-------|------|------------|
| chat_id | Number | ID do usuário Telegram |
| username | Single line text | @username |
| first_name | Single line text | Nome do usuário |
| filtro_moedas | Single select | Opções: BTC, ALTS, TODOS |
| filtro_usdt_d | Checkbox | Receber alertas USDT.D |
| ativo | Checkbox | Usuário ativo |

### Passo 1.4: Anotar IDs
1. Abrir a base
2. Na URL, copiar o Base ID (começa com "app...")
3. Clicar na tabela Preferencias
4. Na URL, copiar o Table ID (começa com "tbl...")

**Exemplo de URL:**
```
https://airtable.com/appXXXXXXXXXXXXXX/tblYYYYYYYYYYYYYY/...
                     ↑ BASE_ID            ↑ TABLE_ID
```

---

## FASE 2: CREDENCIAIS N8N (5 min)

### Passo 2.1: Criar Credencial Airtable
1. No n8n, ir em **Credentials**
2. Clicar em **Add Credential**
3. Buscar **Header Auth**
4. Configurar:
   - **Name:** Airtable API
   - **Name (header):** Authorization
   - **Value:** Bearer SEU_TOKEN_AIRTABLE

**Como obter token Airtable:**
1. Ir em https://airtable.com/create/tokens
2. Criar novo token com permissões:
   - data.records:read
   - data.records:write
3. Selecionar a base CryptoMind Bot
4. Copiar o token

### Passo 2.2: Criar Credencial Telegram
1. No n8n, ir em **Credentials**
2. Clicar em **Add Credential**
3. Buscar **Telegram**
4. Configurar:
   - **Access Token:** 8437212177:AAEsm0d-ARdcj8zDGbqdpjeaSoQgsY-Byqc

---

## FASE 3: WORKFLOW BOT CONFIG (10 min)

### Passo 3.1: Criar Workflow
1. No n8n, clicar em **Create workflow**
2. Nome: **Bot Telegram - Configuração**

### Passo 3.2: Importar JSON
1. Clicar nos 3 pontinhos (⋮)
2. Clicar em **Import from File**
3. Selecionar: `bot_config_workflow_v2.json`

### Passo 3.3: Configurar
1. Em TODOS os nós HTTP Request que acessam Airtable:
   - Substituir `BASE_ID` pelo ID real da sua base
   - Selecionar credencial "Airtable API"

2. No nó "Telegram Trigger":
   - Selecionar credencial "Telegram account"

### Passo 3.4: Ativar
1. Salvar workflow
2. Ativar (toggle Active)

---

## FASE 4: WORKFLOW DNP (5 min)

### Passo 4.1: Criar Workflow
1. No n8n, clicar em **Create workflow**
2. Nome: **DNP - Alertas Personalizados**

### Passo 4.2: Importar JSON
1. Importar: `dnp_alertas_personalizados.json`

### Passo 4.3: Configurar
1. Substituir `BASE_ID` pelo ID real
2. Selecionar credencial "Airtable API" nos nós HTTP

### Passo 4.4: Ativar
1. Salvar e ativar

### Passo 4.5: Anotar URL do Webhook
```
https://cryptomindia.app.n8n.cloud/webhook/dnp-personalizado
```

---

## FASE 5: WORKFLOW TRS (5 min)

### Passo 5.1: Criar Workflow
1. Nome: **TRS - Alertas Personalizados**

### Passo 5.2: Importar e Configurar
1. Importar: `trs_alertas_personalizados.json`
2. Substituir `BASE_ID`
3. Selecionar credenciais

### Passo 5.3: Ativar
1. Salvar e ativar

### Passo 5.4: Anotar URL do Webhook
```
https://cryptomindia.app.n8n.cloud/webhook/trs-personalizado
```

---

## FASE 6: WORKFLOW USDT.D (5 min)

### Passo 6.1: Criar Workflow
1. Nome: **USDT.D - Alertas Personalizados**

### Passo 6.2: Importar e Configurar
1. Importar: `usdt_d_alertas_personalizados.json`
2. Substituir `BASE_ID`
3. Selecionar credenciais

### Passo 6.3: Ativar
1. Salvar e ativar

### Passo 6.4: Anotar URL do Webhook
```
https://cryptomindia.app.n8n.cloud/webhook/usdt-d-personalizado
```

---

## FASE 7: TRADINGVIEW (10 min)

### Passo 7.1: Atualizar Alertas DNP
Para cada alerta DNP, atualizar webhook para:
```
https://cryptomindia.app.n8n.cloud/webhook/dnp-personalizado
```

### Passo 7.2: Atualizar Alertas TRS
Para cada alerta TRS, atualizar webhook para:
```
https://cryptomindia.app.n8n.cloud/webhook/trs-personalizado
```

### Passo 7.3: Atualizar Alertas USDT.D
Para cada alerta USDT.D, atualizar webhook para:
```
https://cryptomindia.app.n8n.cloud/webhook/usdt-d-personalizado
```

---

## FASE 8: TESTE (5 min)

### Passo 8.1: Testar Bot
1. Abrir Telegram
2. Enviar `/start` para o bot
3. Verificar se cadastrou no Airtable
4. Enviar `/config` e testar menu
5. Enviar `/status` para ver configuração

### Passo 8.2: Testar Alertas
1. Aguardar um alerta real
2. Verificar se chegou no Telegram
3. Mudar preferência e verificar filtro

---

## ⚠️ IMPORTANTE

- **NÃO DESATIVAR** workflows antigos até validar os novos
- Testar com seu próprio chat_id primeiro
- Verificar logs do n8n se algo não funcionar

---

## 📊 RESUMO DOS WEBHOOKS

| Setup | Webhook URL |
|-------|-------------|
| DNP | `https://cryptomindia.app.n8n.cloud/webhook/dnp-personalizado` |
| TRS | `https://cryptomindia.app.n8n.cloud/webhook/trs-personalizado` |
| USDT.D | `https://cryptomindia.app.n8n.cloud/webhook/usdt-d-personalizado` |

---

## 📊 CAMPOS AIRTABLE

| Campo | Tipo | Valores |
|-------|------|---------|
| chat_id | Number | ID Telegram |
| username | Text | @username |
| first_name | Text | Nome |
| filtro_moedas | Single select | BTC, ALTS, TODOS |
| filtro_usdt_d | Checkbox | true/false |
| ativo | Checkbox | true/false |
