# 🧪 Plano de Testes - Validação 100% da Correção

## 📋 Objetivo

Validar que a correção da estrutura Switch v2→v3 resolveu completamente o problema de callbacks e que todos os fluxos do bot funcionam perfeitamente.

---

## ✅ TESTE 1: Validação Estrutural (Pré-requisito)

### Objetivo
Confirmar que a estrutura JSON foi corrigida corretamente antes de testar funcionalidades.

### Passos

1. Acesse: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. Duplo-clique no nó **"Switch Comando"**

3. Clique na aba **"JSON"**

4. Verifique se existe:
   ```json
   "parameters": {
     "mode": "rules",
     "rules": {
       "values": [
   ```

5. Repita para o nó **"Switch Callback"**

### Resultado Esperado
- ✅ Ambos os Switch têm `"mode": "rules"`
- ✅ Ambos os Switch têm `"rules": { "values": [ ... ] }`
- ❌ Se ainda tiver `"conditions": { "conditions": [ ... ] }` → workflow NÃO foi importado

### Critério de Sucesso
**OBRIGATÓRIO:** Estrutura v3 presente em ambos os Switch antes de prosseguir.

---

## ✅ TESTE 2: Comando /start (Fluxo Básico)

### Objetivo
Validar que o comando /start cria usuário no Airtable e envia mensagem de boas-vindas.

### Passos

1. Abra o bot Telegram: **@CryptoMindIA_bot** (ou o nome correto do seu bot)

2. Envie o comando: **`/start`**

3. Aguarde a resposta (máximo 5 segundos)

### Resultado Esperado
- ✅ Bot responde com mensagem de boas-vindas
- ✅ Mensagem contém instruções ou menu inicial
- ✅ Resposta em menos de 5 segundos

### Validação no Airtable
1. Acesse: https://airtable.com/appTIDQW6MXCYntnW/Preferencias
2. Verifique se um novo registro foi criado com seu `chat_id`
3. Campos esperados: `chat_id`, `username`, `moeda_preferida`, `usdt_preferido`

### Critério de Sucesso
- ✅ Mensagem recebida no Telegram
- ✅ Registro criado no Airtable

---

## ✅ TESTE 3: Comando /config (Menu com Botões)

### Objetivo
Validar que o comando /config exibe o menu de configuração com botões inline.

### Passos

1. Envie o comando: **`/config`**

2. Aguarde a resposta (máximo 3 segundos)

### Resultado Esperado
- ✅ Bot responde com mensagem de menu
- ✅ Mensagem contém **botões inline** (não apenas texto)
- ✅ Botões visíveis: "Moedas", "USDT" (ou similar)
- ✅ Resposta em menos de 3 segundos

### Critério de Sucesso
- ✅ Menu exibido com botões clicáveis

---

## ✅ TESTE 4: Callback Query - Botão "Moedas" (CRÍTICO)

### Objetivo
**ESTE É O TESTE MAIS IMPORTANTE.** Validar que os callbacks do Telegram funcionam corretamente após a correção.

### Passos

1. No menu do `/config`, **clique no botão "Moedas"** (ou equivalente)

2. Observe o comportamento (máximo 5 segundos)

### Resultado Esperado
- ✅ Botão responde **imediatamente** (sem "loading" infinito)
- ✅ Bot exibe **submenu de moedas** (BTC, ETH, etc.)
- ✅ Submenu contém **novos botões inline** para selecionar moeda
- ✅ Sem mensagens de erro no Telegram
- ✅ Resposta em menos de 5 segundos

### Resultado INCORRETO (indica problema)
- ❌ Botão fica em "loading" infinito
- ❌ Nenhuma resposta do bot
- ❌ Mensagem de erro no Telegram
- ❌ Bot não responde após 5 segundos

### Critério de Sucesso
- ✅ Callback processado e submenu exibido

---

## ✅ TESTE 5: Callback Query - Seleção de Moeda (CRÍTICO)

### Objetivo
Validar que a seleção de uma moeda específica atualiza o Airtable e confirma ao usuário.

### Passos

1. No submenu de moedas, **clique em uma moeda** (ex: "BTC")

2. Aguarde a resposta (máximo 5 segundos)

### Resultado Esperado
- ✅ Bot responde com **mensagem de confirmação** (ex: "Moeda atualizada para BTC")
- ✅ Resposta em menos de 5 segundos
- ✅ Sem erros no Telegram

### Validação no Airtable
1. Acesse: https://airtable.com/appTIDQW6MXCYntnW/Preferencias
2. Localize o registro com seu `chat_id`
3. Verifique se o campo `moeda_preferida` foi atualizado para "BTC" (ou a moeda selecionada)

### Critério de Sucesso
- ✅ Confirmação recebida no Telegram
- ✅ Campo atualizado no Airtable

---

## ✅ TESTE 6: Callback Query - Botão "USDT" (CRÍTICO)

### Objetivo
Validar o segundo fluxo de callback (configuração de USDT).

### Passos

1. Envie novamente: **`/config`**

2. **Clique no botão "USDT"** (ou equivalente)

3. Aguarde a resposta (máximo 5 segundos)

### Resultado Esperado
- ✅ Botão responde imediatamente
- ✅ Bot exibe **submenu de valores USDT** (100, 500, 1000, etc.)
- ✅ Submenu contém **novos botões inline** para selecionar valor
- ✅ Resposta em menos de 5 segundos

### Critério de Sucesso
- ✅ Callback processado e submenu USDT exibido

---

## ✅ TESTE 7: Callback Query - Seleção de USDT (CRÍTICO)

### Objetivo
Validar que a seleção de um valor USDT atualiza o Airtable.

### Passos

1. No submenu USDT, **clique em um valor** (ex: "500")

2. Aguarde a resposta (máximo 5 segundos)

### Resultado Esperado
- ✅ Bot responde com **mensagem de confirmação** (ex: "Valor USDT atualizado para 500")
- ✅ Resposta em menos de 5 segundos

### Validação no Airtable
1. Acesse: https://airtable.com/appTIDQW6MXCYntnW/Preferencias
2. Localize o registro com seu `chat_id`
3. Verifique se o campo `usdt_preferido` foi atualizado para "500"

### Critério de Sucesso
- ✅ Confirmação recebida no Telegram
- ✅ Campo atualizado no Airtable

---

## ✅ TESTE 8: Comando /status (Leitura do Airtable)

### Objetivo
Validar que o comando /status busca e exibe as preferências salvas no Airtable.

### Passos

1. Envie o comando: **`/status`**

2. Aguarde a resposta (máximo 5 segundos)

### Resultado Esperado
- ✅ Bot responde com **status atual** das preferências
- ✅ Mensagem contém:
  - Moeda preferida (ex: "BTC")
  - Valor USDT preferido (ex: "500")
- ✅ Valores correspondem aos salvos no Airtable
- ✅ Resposta em menos de 5 segundos

### Critério de Sucesso
- ✅ Status exibido corretamente
- ✅ Dados correspondem ao Airtable

---

## ✅ TESTE 9: Validação de Logs no n8n (Técnico)

### Objetivo
Verificar que não há erros nos logs de execução do workflow.

### Passos

1. Acesse: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. Clique na aba **"Executions"** (Execuções)

3. Localize as execuções dos testes anteriores

4. Clique em cada execução e verifique:
   - Status: **Success** (verde)
   - Todos os nós executados corretamente
   - Sem erros vermelhos

### Resultado Esperado
- ✅ Todas as execuções com status **Success**
- ✅ Nó "Switch Comando" roteou corretamente para:
  - Saída 0: `/start` → Processar Start
  - Saída 1: `/config` → Enviar Menu Config
  - Saída 2: `/status` → Buscar Usuário Status
  - Saída 3: `callback_query` → Processar Callback
- ✅ Nó "Switch Callback" roteou corretamente para:
  - Saída 0: `config_moedas` → Mostrar Menu Moedas
  - Saída 1: `config_usdt` → Mostrar Menu USDT
  - Saída 2: `set_moeda_*` → Buscar Usuário Callback
  - Saída 3: `set_usdt_*` → Buscar Usuário Callback

### Critério de Sucesso
- ✅ Sem erros nos logs
- ✅ Roteamento correto em todos os Switch

---

## ✅ TESTE 10: Teste de Estresse (Múltiplos Callbacks)

### Objetivo
Validar que o workflow suporta múltiplos callbacks consecutivos sem falhas.

### Passos

1. Envie: **`/config`**
2. Clique em **"Moedas"**
3. Clique em **"BTC"**
4. Envie novamente: **`/config`**
5. Clique em **"USDT"**
6. Clique em **"1000"**
7. Envie: **`/status`**
8. Repita os passos 1-7 mais **2 vezes**

### Resultado Esperado
- ✅ Todas as interações respondem corretamente
- ✅ Sem "loading" infinito em nenhum momento
- ✅ Airtable atualizado corretamente em cada mudança
- ✅ Sem erros ou timeouts

### Critério de Sucesso
- ✅ 100% de sucesso em todas as interações

---

## 📊 Resumo de Validação

### Checklist de Testes

| # | Teste | Status | Crítico |
|---|-------|--------|---------|
| 1 | Validação Estrutural JSON | ⬜ | ✅ Sim |
| 2 | Comando /start | ⬜ | Não |
| 3 | Comando /config (menu) | ⬜ | Não |
| 4 | Callback - Botão Moedas | ⬜ | ✅ Sim |
| 5 | Callback - Seleção Moeda | ⬜ | ✅ Sim |
| 6 | Callback - Botão USDT | ⬜ | ✅ Sim |
| 7 | Callback - Seleção USDT | ⬜ | ✅ Sim |
| 8 | Comando /status | ⬜ | Não |
| 9 | Validação de Logs n8n | ⬜ | Não |
| 10 | Teste de Estresse | ⬜ | Não |

### Critério de Aprovação 100%

**Testes Críticos (OBRIGATÓRIOS):**
- ✅ Teste 1: Estrutura JSON correta
- ✅ Teste 4: Callback Moedas funciona
- ✅ Teste 5: Seleção Moeda atualiza Airtable
- ✅ Teste 6: Callback USDT funciona
- ✅ Teste 7: Seleção USDT atualiza Airtable

**Testes Complementares:**
- ✅ Testes 2, 3, 8, 9, 10: Validam funcionalidades adicionais

### Resultado Final

**✅ 100% VALIDADO** se:
- Todos os 5 testes críticos passarem
- Pelo menos 8 dos 10 testes totais passarem

**❌ PROBLEMA IDENTIFICADO** se:
- Qualquer teste crítico falhar
- Menos de 7 testes totais passarem

---

## 🚨 Troubleshooting

### Se Teste 1 falhar (Estrutura JSON incorreta)
**Causa:** Workflow corrigido não foi importado  
**Solução:** Importar `workflow_corrigido_v3_final.json` novamente

### Se Testes 4-7 falharem (Callbacks não funcionam)
**Causa 1:** Estrutura ainda está v2  
**Solução 1:** Verificar Teste 1 primeiro

**Causa 2:** Webhook do Telegram não está ativo  
**Solução 2:** Verificar nó "Telegram Trigger" está ativo

**Causa 3:** Credenciais do Telegram inválidas  
**Solução 3:** Reconfigurar credenciais do bot

### Se Testes 5 ou 7 falharem (Airtable não atualiza)
**Causa:** API Key do Airtable sem permissão de escrita  
**Solução:** Verificar permissões da API Key no Airtable

---

## 📞 Suporte

Se algum teste falhar após seguir o troubleshooting:
1. Exporte os logs de execução do n8n (aba Executions)
2. Tire screenshots dos erros no Telegram
3. Verifique se o workflow foi salvo após a importação

---

**Este plano de testes garante validação 100% da correção implementada.**
