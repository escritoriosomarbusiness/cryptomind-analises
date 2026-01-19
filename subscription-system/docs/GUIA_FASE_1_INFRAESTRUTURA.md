# Guia Passo a Passo: Fase 1 - Infraestrutura

**Autor:** Manus AI  
**Data:** 19 de Janeiro de 2026

Este guia detalha, passo a passo, como você pode configurar toda a infraestrutura (Fase 1) do sistema de assinaturas **sozinho**, economizando créditos. Siga cada etapa com atenção. Se tiver qualquer dúvida, me chame!

---

## 🎯 Objetivo da Fase 1

Ao final desta fase, você terá:

- ✅ Uma base de dados no **Airtable** pronta para receber os assinantes.
- ✅ Um **Bot do Telegram** para gerenciar o acesso ao canal.
- ✅ Uma conta **Mercado Pago** configurada para receber os pagamentos.
- ✅ As **credenciais** prontas para serem inseridas no n8n.

---

## 📝 Tarefa 1: Configurar o Airtable

**Tempo estimado:** 15-20 minutos

### Passo 1: Criar a Base

1.  Acesse sua conta no [Airtable](https://airtable.com).
2.  Clique em **"Create a base"**.
3.  Renomeie a base para **`CryptoMind Subscribers`**.

### Passo 2: Criar a Tabela `Assinantes`

1.  A primeira tabela já vem criada. Renomeie-a para **`Assinantes`**.
2.  Apague os campos padrão e crie os seguintes, **exatamente** como na tabela abaixo:

| Nome do Campo | Tipo de Campo | Notas |
|---|---|---|
| `ID` | `Autonumber` | - |
| `Nome` | `Single line text` | - |
| `Email` | `Email` | - |
| `Telefone` | `Phone number` | - |
| `Telegram_Username` | `Single line text` | - |
| `Telegram_ID` | `Number` | Formato: Integer |
| `Plano` | `Single select` | Opções: `trial`, `monthly`, `quarterly`, `semiannual`, `annual` |
| `Status` | `Single select` | Opções: `active`, `expired`, `cancelled`, `pending_payment`, `trial` |
| `Data_Cadastro` | `Created time` | - |
| `Data_Inicio` | `Date` | Formato: Friendly (e.g., Jan 19, 2026) |
| `Data_Vencimento` | `Formula` | **Cole a fórmula abaixo** |
| `Valor_Pago` | `Currency` | Formato: R$ 1,234.56 |
| `MP_Payment_ID` | `Single line text` | - |
| `Invite_Link` | `URL` | - |
| `Notas` | `Long text` | - |

3.  **Fórmula para o campo `Data_Vencimento`** (copie e cole):

    ```
    IF({Data_Inicio}, 
      DATEADD({Data_inio}, 
        SWITCH({Plano}, 
          'trial', 5, 
          'monthly', 30, 
          'quarterly', 90, 
          'semiannual', 180, 
          'annual', 365, 
          0
        ), 
        'days'
      )
    )
    ```

### Passo 3: Criar a Tabela `Pagamentos`

1.  Clique em **"Add or import"** e adicione uma nova tabela.
2.  Renomeie-a para **`Pagamentos`**.
3.  Crie os seguintes campos:

| Nome do Campo | Tipo de Campo | Notas |
|---|---|---|
| `ID` | `Autonumber` | - |
| `Assinante` | `Link to another record` | Link para a tabela `Assinantes` |
| `Data_Pagamento` | `Created time` | - |
| `Valor` | `Currency` | - |
| `Plano_Adquirido` | `Single select` | Opções: `trial`, `monthly`, `quarterly`, `semiannual`, `annual` |
| `MP_Payment_ID` | `Single line text` | - |
| `Status_Pagamento` | `Single select` | Opções: `approved`, `pending`, `cancelled`, `refunded` |
| `Metodo` | `Single select` | Opções: `pix`, `credit_card`, `debit_card`, `boleto` |

### Passo 4: Obter a API Key

1.  Clique na sua foto de perfil (canto superior direito) → **"Developer hub"**.
2.  Clique em **"Create new token"**.
3.  Dê um nome ao token (e.g., `n8n_CryptoMind`).
4.  Em **"Scopes"**, adicione:
    - `data.records:read`
    - `data.records:write`
    - `schema.bases:read`
5.  Em **"Access"**, selecione a base `CryptoMind Subscribers`.
6.  Clique em **"Create token"** e **copie a chave**. Guarde-a em um local seguro.

---

## 🤖 Tarefa 2: Criar o Bot Gerenciador no Telegram

**Tempo estimado:** 5 minutos

1.  No Telegram, procure por **`@BotFather`** (o oficial, com selo de verificação).
2.  Envie o comando `/newbot`.
3.  Dê um nome para o bot, por exemplo: **`CryptoMind Manager`**.
4.  Dê um username para o bot, que deve terminar em `bot`. Exemplo: **`CryptoMindManagerBot`**.
5.  O BotFather vai te enviar uma mensagem com o **token do bot**. Copie e guarde-o em local seguro.
6.  Abra seu canal `CryptoMind Alerts`.
7.  Vá em Administradores → Adicionar Administrador.
8.  Procure pelo seu novo bot (`@CryptoMindManagerBot`) e adicione-o.
9.  Conceda as seguintes permissões:
    - ✅ **Ban Users** (para remover membros)
    - ✅ **Invite Users via Link** (para criar links de convite)
10. Salve as alterações.

---

## 💳 Tarefa 3: Configurar o Mercado Pago

**Tempo estimado:** 20-30 minutos

### Passo 1: Acessar o Painel de Desenvolvedor

1.  Acesse sua conta no [Mercado Pago](https://www.mercadopago.com.br/).
2.  Vá em **"Seu negócio"** → **"Configurações"** → **"Gestão e Administração"** → **"Credenciais"**.
3.  Ative as **credenciais de Produção**.

### Passo 2: Criar uma Aplicação

1.  No painel de desenvolvedor, vá em **"Suas aplicações"**.
2.  Clique em **"Criar aplicação"**.
3.  Dê um nome (e.g., `CryptoMind Alerts`).
4.  Selecione **"Pagamentos Online"**.
5.  Aceite os termos e crie a aplicação.

### Passo 3: Obter o Access Token

1.  Dentro da sua nova aplicação, vá em **"Credenciais de Produção"**.
2.  Copie o **`Access Token`**. Guarde-o em local seguro.

### Passo 4: Criar os Links de Pagamento

1.  No menu, vá em **"Links de pagamento"**.
2.  Clique em **"Criar novo"**.
3.  Crie **4 links**, um para cada plano pago:

    **Exemplo para o Plano Mensal:**
    - **Título do produto:** `Assinatura Mensal - CryptoMind Alerts`
    - **Preço:** `149,00`
    - Em **"Mais opções"** → **"Meios de pagamento"**, deixe todos ativos.
    - Em **"Mais opções"** → **"Referência externa"**, coloque o ID do plano: **`cryptomind-monthly`**

4.  Repita o processo para os outros planos, usando as referências externas corretas:

| Plano | Preço | Referência Externa (`external_reference`) |
|---|---|---|
| Mensal | R$ 149,00 | `cryptomind-monthly` |
| Trimestral | R$ 399,00 | `cryptomind-quarterly` |
| Semestral | R$ 774,00 | `cryptomind-semiannual` |
| Anual | R$ 1.200,00 | `cryptomind-annual` |

5.  Copie e guarde os 4 links de pagamento gerados.

### Passo 5: Configurar Webhooks (FAREMOS JUNTOS)

**Não faça isso agora.** A configuração do webhook precisa da URL do n8n, que só teremos quando o workflow estiver ativo. Deixe esta parte para fazermos juntos.

---

## 🔐 Tarefa 4: Preparar as Credenciais para o n8n

**Tempo estimado:** 2 minutos

Ao final das tarefas acima, você deve ter as seguintes informações salvas em um local seguro (bloco de notas, gerenciador de senhas, etc.):

1.  **Airtable API Key:** `pat...` (a chave que você gerou)
2.  **Telegram Bot Token:** `8503...` (o token que o BotFather te deu)
3.  **Mercado Pago Access Token:** `APP_USR-...` (o token de produção)

Quando formos para a Fase 2, vamos usar essas chaves para criar as credenciais no n8n.

---

## ✅ Checklist de Verificação da Fase 1

- [ ] Base `CryptoMind Subscribers` criada no Airtable.
- [ ] Tabela `Assinantes` com todos os 15 campos configurados corretamente.
- [ ] Tabela `Pagamentos` com todos os 8 campos configurados.
- [ ] Fórmula do campo `Data_Vencimento` copiada e funcionando.
- [ ] API Key do Airtable gerada e salva.
- [ ] Bot `@CryptoMindManagerBot` criado no Telegram.
- [ ] Token do bot do Telegram salvo.
- [ ] Bot adicionado como administrador do canal com as permissões corretas.
- [ ] Aplicação criada no Mercado Pago.
- [ ] Access Token de Produção do Mercado Pago salvo.
- [ ] 4 links de pagamento criados com as referências externas corretas.

---

**Parabéns!** Se você completou tudo isso, a base do seu sistema de automação está pronta. A próxima fase será focada em construir os workflows no n8n para conectar tudo isso.

**Guarde este guia e as chaves que você gerou. Vamos usá-los após o dia 25!** 🚀
