# 🚀 GUIA RÁPIDO - Corrigir Telegram no n8n

## ✅ O QUE VOCÊ PRECISA FAZER:

Substituir o **chat_id** em 3 workflows do n8n pelo valor correto: **-1003672123657**

---

## 📝 PASSO A PASSO (Repita para cada workflow)

### **WORKFLOW 1: DNP - Alertas TradingView**

1. **Abra o workflow:**
   - Acesse: https://cryptomindia.app.n8n.cloud/workflow/22fCVF5cebKDeNvD
   - Ou clique em "DNP - Alertas TradingView" na lista de workflows

2. **Encontre o nó "Enviar Telegram":**
   - É o último nó do workflow (à direita)
   - Tem um ícone de globo 🌐
   - Mostra: "POST: https://api.telegram.org/..."

3. **Clique no nó para abrir o editor:**
   - Clique UMA VEZ no nó "Enviar Telegram"
   - Um painel lateral deve abrir à direita

4. **Localize o campo chat_id:**
   - No painel lateral, role para baixo até encontrar **"Body Parameters"** ou **"Specify Body"**
   - Procure o campo chamado **"chat_id"**
   - Você verá algo como: `@CryptoMind_Alerts_Bot` ou outro valor

5. **SUBSTITUA o valor:**
   - Apague o valor atual do chat_id
   - Digite: `-1003672123657`
   - **IMPORTANTE:** Inclua o sinal de menos (-) no início!

6. **Salve as alterações:**
   - Clique no botão **"Save"** no canto superior direito
   - Aguarde a mensagem de confirmação

7. **Ative o workflow (se necessário):**
   - Verifique se há um botão "Activate" ou "Ativar"
   - Se houver, clique nele para ativar o workflow

---

### **WORKFLOW 2: CryptoMind IA - Alertas TRS**

1. **Volte para a lista de workflows:**
   - Clique em "Workflows" no menu lateral esquerdo
   - Ou acesse: https://cryptomindia.app.n8n.cloud/home/workflows

2. **Abra o workflow:**
   - Clique em "CryptoMind IA - Alertas TRS"

3. **Repita os passos 2 a 7 do Workflow 1:**
   - Encontre o nó "Enviar Telegram"
   - Clique nele
   - Localize o campo chat_id
   - Substitua por: `-1003672123657`
   - Salve
   - Ative (se necessário)

---

### **WORKFLOW 3: CryptoMind IA - USDT.D Monitor**

1. **Volte para a lista de workflows:**
   - Clique em "Workflows" no menu lateral esquerdo

2. **Abra o workflow:**
   - Clique em "CryptoMind IA - USDT.D Monitor"

3. **Repita os passos 2 a 7 do Workflow 1:**
   - Encontre o nó "Enviar Telegram"
   - Clique nele
   - Localize o campo chat_id
   - Substitua por: `-1003672123657`
   - Salve
   - Ative (se necessário)

---

## 🧪 TESTE RÁPIDO

Após corrigir os 3 workflows:

1. **Abra qualquer workflow corrigido**
2. **Clique no botão "Execute workflow"** (botão vermelho no canto inferior)
3. **Verifique seu canal do Telegram:** https://t.me/CryptoMind_Alerts_Bot
4. **Você deve receber uma mensagem de teste!**

---

## ❓ DÚVIDAS COMUNS

### "Não encontro o campo chat_id"
- Procure por "Body Parameters" ou "Specify Body"
- Pode estar dentro de uma seção "JSON" ou "Form"
- Role o painel lateral para baixo

### "O painel lateral não abre"
- Tente dar um duplo clique no nó
- Ou clique com o botão direito e selecione "Edit"

### "Não sei se salvou"
- Procure por uma mensagem verde de confirmação
- Ou veja se o botão "Save" mudou para "Saved"

---

## 📊 CHECKLIST

- [ ] Workflow 1: DNP - Alertas TradingView ✅
- [ ] Workflow 2: CryptoMind IA - Alertas TRS ✅
- [ ] Workflow 3: CryptoMind IA - USDT.D Monitor ✅
- [ ] Teste manual executado ✅
- [ ] Mensagem recebida no canal ✅

---

## 🎯 VALOR CORRETO DO CHAT_ID

```
-1003672123657
```

**COPIE E COLE EXATAMENTE ESTE VALOR!**

---

## 🆘 PRECISA DE AJUDA?

Se tiver qualquer dúvida durante o processo, me avise que eu te ajudo!

---

**Tempo estimado:** 5 minutos para os 3 workflows  
**Dificuldade:** Fácil 🟢
