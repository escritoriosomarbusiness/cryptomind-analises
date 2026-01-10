# 🔐 Configuração de Credenciais - Bot Telegram

## ⚠️ Importante

Os arquivos JSON dos workflows **NÃO contêm credenciais reais** por segurança.  
Você precisa configurar suas próprias credenciais no n8n após importar o workflow.

---

## 🔑 Credenciais Necessárias

### 1. Telegram Bot Token

**Onde obter:**
1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot` e siga as instruções
3. Copie o token fornecido (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Onde configurar no n8n:**
- Nó: **"Telegram Trigger"**
- Campo: `Bot Token`
- Substitua: `YOUR_TELEGRAM_BOT_TOKEN_HERE`

---

### 2. Airtable API Key

**Onde obter:**
1. Acesse: https://airtable.com/create/tokens
2. Clique em **"Create new token"**
3. Configure:
   - Nome: `CryptoMind Bot`
   - Scopes: `data.records:read`, `data.records:write`
   - Access: Selecione a base `CryptoMind`
4. Clique em **"Create token"**
5. Copie o token (formato: `patXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX`)

**Onde configurar no n8n:**
- Nós que usam Airtable:
  - **"Criar Usuário Airtable"**
  - **"Buscar Usuário Status"**
  - **"Buscar Usuário Callback"**
  - **"Atualizar Preferência"**
- Campo: `API Key`
- Substitua: `YOUR_AIRTABLE_API_KEY_HERE`

---

## 📋 Passo a Passo de Configuração

### Após Importar o Workflow

1. **Abra o workflow no n8n**
   - Acesse: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. **Configure o Telegram Bot Token**
   - Duplo-clique no nó **"Telegram Trigger"**
   - Clique em **"Credentials"**
   - Clique em **"Create New"**
   - Cole seu Telegram Bot Token
   - Clique em **"Save"**

3. **Configure o Airtable API Key**
   - Duplo-clique em qualquer nó Airtable (ex: "Criar Usuário Airtable")
   - Clique em **"Credentials"**
   - Clique em **"Create New"**
   - Cole seu Airtable API Key
   - Clique em **"Save"**
   - **Importante:** Selecione a mesma credencial em todos os nós Airtable

4. **Salve o workflow**
   - Clique no botão **"Save"** no topo da página

5. **Ative o workflow**
   - Toggle no canto superior direito: **Active**

---

## ✅ Verificação

### Teste Rápido

1. Abra seu bot no Telegram
2. Envie: `/start`
3. Se receber resposta, as credenciais estão corretas! ✅

### Troubleshooting

**Bot não responde:**
- Verifique se o Telegram Bot Token está correto
- Verifique se o workflow está ativo (toggle verde)
- Verifique se o nó "Telegram Trigger" está ativo

**Erro ao salvar no Airtable:**
- Verifique se o Airtable API Key está correto
- Verifique se o token tem permissões de escrita
- Verifique se a Base ID está correta: `appTIDQW6MXCYntnW`

---

## 🔒 Segurança

### Boas Práticas

✅ **FAÇA:**
- Mantenha suas credenciais privadas
- Use tokens com permissões mínimas necessárias
- Revogue tokens não utilizados
- Rotacione tokens periodicamente

❌ **NÃO FAÇA:**
- Compartilhar tokens publicamente
- Commitar tokens no Git
- Usar tokens em ambientes não seguros
- Dar permissões desnecessárias aos tokens

---

## 📞 Suporte

Se tiver problemas com credenciais:
1. Verifique se os tokens estão corretos
2. Verifique permissões dos tokens
3. Consulte a documentação oficial:
   - Telegram: https://core.telegram.org/bots#6-botfather
   - Airtable: https://airtable.com/developers/web/api/authentication

---

**Lembre-se:** Nunca compartilhe suas credenciais! 🔐
