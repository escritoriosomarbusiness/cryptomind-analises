# Escopo Técnico: Automação de Alertas de Trading com n8n, Airtable e Telegram

**Data:** 19 de Janeiro de 2026

**Projeto:** Price Expansion System (PES) - Automação de Sinais

---

## 1. Visão Geral do Projeto

O objetivo deste projeto é desenvolver um workflow de automação robusto utilizando a plataforma n8n para integrar um indicador de trading (Pine Script) do TradingView com o Airtable (banco de dados) e o Telegram (notificações).

O sistema deverá receber alertas via webhook, processar os dados, armazená-los de forma estruturada, realizar cálculos de performance e notificar os usuários em tempo real.

**Nota Importante:** A lógica de geração de sinais e a estratégia de trading são pré-existentes e estão fora do escopo deste projeto. O foco é exclusivamente na **arquitetura de integração e processamento de dados** (o "encanamento").

---

## 2. Objetivo da Automação

O workflow a ser desenvolvido no n8n deve ser capaz de:

1.  **Receber** alertas em formato JSON de um webhook do TradingView.
2.  **Rotear** os sinais com base no tipo (`ENTRY` ou `EXIT`).
3.  **Armazenar** os dados de entrada de um novo trade em uma base de dados no Airtable.
4.  **Buscar e atualizar** um trade existente no Airtable quando um sinal de saída for recebido.
5.  **Calcular** o resultado da operação (lucro/prejuízo) em percentual.
6.  **Notificar** os usuários via Telegram com mensagens formatadas e dinâmicas para cada tipo de sinal.

---

## 3. Arquitetura do Sistema

A automação seguirá o seguinte fluxo de dados:

```
[TradingView Pine Script] -> [Webhook Alert] -> [n8n Workflow] -> [Airtable DB] & [Telegram Bot]
```

---

## 4. Requisitos Técnicos Detalhados

### **4.1. Fonte do Alerta (TradingView)**

- Um indicador em **Pine Script v6** (código será fornecido) gera alertas utilizando a função `alert()`.
- O alerta envia um payload **JSON** para um webhook.
- O JSON contém todos os dados necessários para o processamento.

**Exemplo de Payload JSON (Entrada):**
```json
{
  "action": "PES_SIGNAL",
  "signal_id": "BTCUSDT_15_1737301200",
  "symbol": "BTCUSDT",
  "timeframe": "15",
  "type": "LONG_ENTRY",
  "price": 93161.0,
  "quality": "PREMIUM",
  "mtf_trend": "ALTA",
  "entry_channel": 93500.0,
  "exit_channel": 92500.0
}
```

**Exemplo de Payload JSON (Saída):**
```json
{
  "action": "PES_SIGNAL",
  "signal_id": "BTCUSDT_15_1737301200",
  "symbol": "BTCUSDT",
  "timeframe": "15",
  "type": "LONG_EXIT",
  "price": 93850.0
}
```

### **4.2. Workflow n8n (O Coração do Projeto)**

O workflow deverá conter a seguinte lógica:

1.  **Nó Webhook:** Ponto de entrada para receber os dados do TradingView.
2.  **Nó Switch:** Roteia o fluxo com base no campo `type` do JSON (`LONG_ENTRY`, `SHORT_ENTRY`, `LONG_EXIT`, `SHORT_EXIT`).

#### **Fluxo de ENTRADA (`*_ENTRY`):**

3.  **Nó Airtable (Create):** Cria um novo registro na tabela "Trades" com os dados recebidos do webhook. O status do trade deve ser definido como "OPEN".
4.  **Nó Telegram (Send Message):** Envia uma notificação de entrada formatada para um chat específico, contendo informações como ativo, preço, qualidade e tendência.

#### **Fluxo de SAÍDA (`*_EXIT`):**

5.  **Nó Airtable (Find):** Busca na tabela "Trades" o registro correspondente ao `signal_id` recebido no webhook de saída.
6.  **Nó IF:** Verifica se o registro foi encontrado.
7.  **Nó Airtable (Update):** Atualiza o registro encontrado com o preço de saída (`exit_price`), a data de saída e muda o status para "CLOSED".
8.  **Nó Set/Code:** Calcula o resultado da operação em percentual. A fórmula depende da direção (`LONG` ou `SHORT`).
9.  **Nó Telegram (Send Message):** Envia uma notificação de saída formatada, incluindo o resultado calculado (ex: `+0.74%`).

### **4.3. Base de Dados (Airtable)**

- Uma tabela chamada **"Trades"** será utilizada para armazenar os dados.
- A estrutura da tabela (14 campos, tipos e configurações) já foi definida e será fornecida.
- O programador deverá apenas conectar o n8n à tabela existente.

### **4.4. Notificações (Telegram)**

- O workflow deve enviar mensagens para um chat específico do Telegram.
- As mensagens devem ser bem formatadas (Markdown) e usar emojis para clareza visual.
- O conteúdo das mensagens será dinâmico, utilizando os dados do webhook e os resultados calculados.

---

## 5. Entregáveis

1.  **Arquivo JSON do Workflow n8n:** Um arquivo `.json` contendo o workflow completo e funcional, pronto para ser importado no n8n.
2.  **Documentação de Configuração:** Um breve guia em Markdown explicando:
    - Como importar o workflow.
    - Quais credenciais precisam ser criadas (Airtable, Telegram).
    - Onde inserir as variáveis (Base ID, Chat ID) nos nós correspondentes.
    - Um exemplo de comando `curl` para testar o webhook.

---

## 6. Ativos Fornecidos

Para facilitar o desenvolvimento, os seguintes materiais serão fornecidos:

- ✅ **Código Pine Script v6** completo e funcional (`pes_v2.0_tier2.txt`).
- ✅ **Estrutura detalhada da tabela Airtable** com todos os 14 campos (`AIRTABLE_TIER2_SETUP.md`).
- ✅ **Exemplos de mensagens formatadas** para o Telegram (`TELEGRAM_TEMPLATES.md`).
- ✅ **Acesso a uma conta de teste** do Airtable e Telegram, se necessário.

---

## 7. Fora do Escopo

- Criação ou modificação do código Pine Script.
- Criação da base de dados no Airtable (a estrutura será fornecida).
- Criação do bot no Telegram.
- Implementação de relatórios agendados (Tier 3).
- Qualquer funcionalidade não descrita neste documento.

---

## 8. Próximos Passos

Solicitamos um orçamento para o desenvolvimento dos entregáveis descritos acima, com uma estimativa de prazo para a conclusão. Estamos à disposição para esclarecer quaisquer dúvidas sobre o escopo.
