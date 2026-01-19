# 🚀 Guia de Implementação - PES MVP (Tier 1)

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

Este documento fornece um guia passo a passo completo para implementar o **MVP do PES (Price Expansion System)** após a renovação de créditos em 25/01/2026.

---

## 📋 Checklist de Pré-requisitos

Antes de começar, certifique-se de ter:

- [ ] Conta ativa no **TradingView** (plano Pro ou superior para alertas webhook).
- [ ] Conta ativa no **Airtable** (plano gratuito é suficiente para o MVP).
- [ ] Conta ativa no **n8n** (pode ser self-hosted ou n8n.cloud).
- [ ] Bot do **Telegram** criado via BotFather.
- [ ] **Chat ID** do canal/grupo do Telegram onde receberá os alertas.

---

## Passo 1: Configurar o Airtable

### 1.1. Criar a Base

Acesse o Airtable e crie uma nova base chamada `[Crypto] PES Performance`.

### 1.2. Criar a Tabela `Trades`

Dentro da base, crie uma tabela chamada `Trades` e configure os seguintes campos exatamente como especificado:

| Nome do Campo | Tipo | Configuração |
|---|---|---|
| `signal_id` | `Single line text` | - |
| `status` | `Single select` | Opções: `OPEN`, `CLOSED` |
| `symbol` | `Single line text` | - |
| `timeframe` | `Single select` | Opções: `5`, `15`, `60`, `240`, `D` |
| `direction` | `Single select` | Opções: `LONG`, `SHORT` |
| `entry_price` | `Number` | Formato: Decimal 1.00000 |
| `exit_price` | `Number` | Formato: Decimal 1.00000 |
| `entry_time_utc` | `Date` | Incluir hora, formato 24h |
| `exit_time_utc` | `Date` | Incluir hora, formato 24h |
| `result_percent` | `Percent` | Fórmula: `IF({direction} = 'LONG', ({exit_price} - {entry_price}) / {entry_price}, IF({direction} = 'SHORT', ({entry_price} - {exit_price}) / {entry_price}, 0))` |

**Documentação detalhada:** Consulte `/airtable/AIRTABLE_MVP_SETUP.md`.

### 1.3. Obter a API Key

Acesse [https://airtable.com/account](https://airtable.com/account) e gere uma API Key. Guarde-a em local seguro.

---

## Passo 2: Configurar o n8n

### 2.1. Criar Credenciais

No n8n, vá em `Credentials` e crie:

1.  **Airtable API:**
    - Cole a API Key obtida no passo anterior.
    - Salve como `Airtable Crypto`.

2.  **Telegram Bot API:**
    - Cole o Access Token do seu bot.
    - Salve como `Telegram Bot Principal`.

### 2.2. Importar o Workflow

O arquivo `PES_MVP_Workflow.json` está disponível em `/n8n/`. Importe-o para o n8n:

1.  Vá em `Workflows` > `New` > `Import from File`.
2.  Selecione o arquivo JSON.
3.  O workflow será criado automaticamente.

### 2.3. Configurar Credenciais nos Nós

Abra o workflow importado e configure as credenciais:

- Todos os nós **Airtable**: Selecione `Airtable Crypto`.
- Todos os nós **Telegram**: Selecione `Telegram Bot Principal` e insira o `Chat ID`.

### 2.4. Configurar Base e Table ID

Nos nós do Airtable, você precisará inserir:

- **Base ID:** Encontre na URL da sua base Airtable (ex: `appXXXXXXXXXXXXXX`).
- **Table ID:** Geralmente é `Trades` (o nome da tabela).

### 2.5. Ativar o Workflow

Clique em `Active` no canto superior direito para ativar o workflow.

### 2.6. Obter a URL do Webhook

No nó `Webhook` (primeiro nó), copie a **Production URL**. Ela será usada no TradingView.

**Documentação detalhada:** Consulte `/n8n/N8N_MVP_WORKFLOW.md`.

---

## Passo 3: Configurar o TradingView

### 3.1. Adicionar o Indicador

1.  Abra o TradingView e vá para o gráfico do ativo desejado (ex: BTCUSDT).
2.  Clique em `Indicators` e selecione `Pine Editor`.
3.  Copie todo o código do arquivo `/pinescript/pes_v1.0_mvp.pine`.
4.  Cole no Pine Editor e clique em `Add to Chart`.

### 3.2. Configurar os Parâmetros

Ajuste os parâmetros conforme necessário:

- **Período Canal de Entrada:** 20 (padrão).
- **Período Canal de Saída:** 10 (padrão).
- **Mostrar Canais:** Ativado.

### 3.3. Criar os Alertas

Você precisará criar **4 alertas separados** no TradingView, um para cada tipo de sinal.

#### Alerta 1: LONG_ENTRY

1.  Clique no ícone de sino (Alerts).
2.  Clique em `Create Alert`.
3.  **Condition:** `PES v1.0 (MVP)` > `Any alert() function call`.
4.  **Alert name:** `PES LONG ENTRY`.
5.  **Message:** (Deixe em branco, o script já envia o JSON).
6.  **Webhook URL:** Cole a URL do webhook do n8n.
7.  **Options:** `Once Per Bar Close`.
8.  Clique em `Create`.

#### Alerta 2: LONG_EXIT

Repita o processo acima, mas nomeie como `PES LONG EXIT`.

#### Alerta 3: SHORT_ENTRY

Repita o processo acima, mas nomeie como `PES SHORT ENTRY`.

#### Alerta 4: SHORT_EXIT

Repita o processo acima, mas nomeie como `PES SHORT EXIT`.

**Importante:** O Pine Script v5 envia todos os alertas através de `alert()`, então você precisa criar um alerta genérico que capture todas as chamadas de `alert()` do indicador.

---

## Passo 4: Testar o Sistema

### 4.1. Teste Manual

1.  Aguarde um sinal de entrada no gráfico (seta verde ou vermelha).
2.  Verifique se a mensagem chegou no Telegram.
3.  Verifique se um novo registro foi criado no Airtable com status `OPEN`.
4.  Aguarde o sinal de saída (cruz).
5.  Verifique se a mensagem de saída chegou no Telegram com o resultado calculado.
6.  Verifique se o registro no Airtable foi atualizado com status `CLOSED` e o campo `result_percent` preenchido.

### 4.2. Validação

Confirme que:

- O `signal_id` é o mesmo na entrada e na saída.
- O resultado percentual está correto.
- As mensagens do Telegram estão formatadas corretamente.

---

## Passo 5: Monitorar e Coletar Dados

Com o sistema funcionando, deixe-o rodar por **1-2 semanas** em modo de observação (paper trading ou com capital reduzido). Durante este período:

- Monitore a performance dos sinais.
- Verifique se há erros no workflow do n8n.
- Analise os dados no Airtable manualmente.
- Ajuste os parâmetros dos canais (se necessário).

---

## 🎯 Próximos Passos (Após Validação do MVP)

Uma vez que o MVP esteja funcionando de forma estável e você esteja satisfeito com a lógica dos sinais, você pode avançar para:

- **Tier 2:** Implementar a análise MTF e a classificação de qualidade dos sinais.
- **Tier 3:** Implementar o sistema completo de relatórios automáticos.

---

## 📚 Referências de Documentação

- **Especificações Gerais:** `/docs/SPECIFICATIONS.md`
- **Detalhes do Tier 1:** `/docs/IMPLEMENTATION_TIER_1.md`
- **Código Pine Script:** `/pinescript/pes_v1.0_mvp.pine`
- **Setup Airtable:** `/airtable/AIRTABLE_MVP_SETUP.md`
- **Workflow n8n:** `/n8n/N8N_MVP_WORKFLOW.md`

---

**Boa sorte com a implementação! 🚀**
