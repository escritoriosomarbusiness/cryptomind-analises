# 🗄️ Airtable - Configuração do MVP (Tier 1)

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

## 🎯 Objetivo

Configurar a estrutura mínima necessária no Airtable para suportar o MVP do **PES (Price Expansion System)**. O foco é armazenar os trades e calcular o resultado de cada operação individualmente.

---

## 1. Criação da Base

1.  Crie uma nova base no Airtable.
2.  Nomeie a base como: `[Crypto] PES Performance`.

---

## 2. Criação da Tabela `Trades`

Dentro da base `[Crypto] PES Performance`, crie uma única tabela e nomeie-a como `Trades`.

---

## 3. Configuração dos Campos (Fields)

Delete os campos padrão e crie os seguintes campos, exatamente com os nomes e tipos especificados. O nome exato do campo (`Field Name`) é crucial para a integração com o n8n.

| Ordem | Nome do Campo (`Field Name`) | Tipo (`Type`) | Configuração / Opções |
|---|---|---|---|
| 1 | `signal_id` | `Single line text` | Será a chave primária de fato, vinda do Pine Script. |
| 2 | `status` | `Single select` | Opções: `OPEN`, `CLOSED`. Use cores para diferenciar (ex: Amarelo para OPEN, Verde para CLOSED). |
| 3 | `symbol` | `Single line text` | Armazenará o ticker do ativo (ex: "BTCUSDT"). |
| 4 | `timeframe` | `Single select` | Crie opções para os timeframes que você usa (ex: "5", "15", "60", "240", "D"). |
| 5 | `direction` | `Single select` | Opções: `LONG`, `SHORT`. Use cores (ex: Verde para LONG, Vermelho para SHORT). |
| 6 | `entry_price` | `Number` | Formato: `Decimal`, Precisão: `1.00000`. |
| 7 | `exit_price` | `Number` | Formato: `Decimal`, Precisão: `1.00000`. |
| 8 | `entry_time_utc` | `Date` | Incluir a hora (`Include a time field`) e usar formato `24 hour`. **NÃO** marcar "Use the same time zone for all collaborators". |
| 9 | `exit_time_utc` | `Date` | Mesma configuração do `entry_time_utc`. |
| 10 | `result_percent` | `Percent` | **Fórmula:** `IF({direction} = 'LONG', ({exit_price} - {entry_price}) / {entry_price}, IF({direction} = 'SHORT', ({entry_price} - {exit_price}) / {entry_price}, 0))`. <br> Formato: `Decimal`, Precisão: `1.00%`. |

### Tabela Resumo da Configuração:

| Field Name | Type | Options / Formula |
|---|---|---|
| `signal_id` | `Single line text` | - |
| `status` | `Single select` | `OPEN`, `CLOSED` |
| `symbol` | `Single line text` | - |
| `timeframe` | `Single select` | `5`, `15`, `60`, `240`, `D` |
| `direction` | `Single select` | `LONG`, `SHORT` |
| `entry_price` | `Number` | `Decimal 1.00000` |
| `exit_price` | `Number` | `Decimal 1.00000` |
| `entry_time_utc` | `Date` | `Include time`, `24 hour` |
| `exit_time_utc` | `Date` | `Include time`, `24 hour` |
| `result_percent` | `Percent` | `IF({direction} = 'LONG', ({exit_price} - {entry_price}) / {entry_price}, IF({direction} = 'SHORT', ({entry_price} - {exit_price}) / {entry_price}, 0))` |

---

## 4. Obtenção da API Key

Para que o n8n possa se conectar a esta base, você precisará de uma API Key do Airtable.

1.  Acesse a página da sua conta Airtable: [https://airtable.com/account](https://airtable.com/account)
2.  Na seção **API**, gere uma nova chave (key), se ainda não tiver uma.
3.  Copie e guarde esta chave em um local seguro. Ela será usada para configurar as credenciais do Airtable no n8n.

---

## ✅ Pronto para o Próximo Passo

Com a base e a tabela configuradas desta forma, o Airtable está pronto para receber os dados do workflow n8n do Tier 1.
