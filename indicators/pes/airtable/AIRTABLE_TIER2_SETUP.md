# 🗄️ Airtable - Configuração do Tier 2

**Data:** 19 de Janeiro de 2026  
**Autor:** Manus AI

---

## 🎯 Objetivo

Atualizar a estrutura do Airtable para suportar os novos campos do **Tier 2** do PES, incluindo qualidade do sinal e tendência MTF.

---

## 📝 Campos Adicionais para a Tabela `Trades`

Adicione os seguintes campos à tabela `Trades` existente:

| Ordem | Nome do Campo | Tipo | Configuração / Opções |
|---|---|---|---|
| 11 | `quality` | `Single select` | Opções: `PREMIUM`, `CAUTELA`, `CONTRA`. Use cores (Verde, Amarelo, Laranja). |
| 12 | `mtf_trend` | `Single select` | Opções: `ALTA`, `BAIXA`, `NEUTRO`. Use cores (Verde, Vermelho, Cinza). |
| 13 | `entry_channel` | `Number` | Formato: `Decimal 1.00000`. Preço do canal de entrada. |
| 14 | `exit_channel` | `Number` | Formato: `Decimal 1.00000`. Preço do canal de saída. |

---

## 📊 Estrutura Completa da Tabela `Trades` (Tier 2)

| # | Nome do Campo | Tipo | Configuração |
|---|---|---|---|
| 1 | `signal_id` | `Single line text` | Chave primária |
| 2 | `status` | `Single select` | `OPEN`, `CLOSED` |
| 3 | `symbol` | `Single line text` | - |
| 4 | `timeframe` | `Single select` | `5`, `15`, `60`, `240`, `D` |
| 5 | `direction` | `Single select` | `LONG`, `SHORT` |
| 6 | `entry_price` | `Number` | Decimal 1.00000 |
| 7 | `exit_price` | `Number` | Decimal 1.00000 |
| 8 | `entry_time_utc` | `Date` | Include time, 24h |
| 9 | `exit_time_utc` | `Date` | Include time, 24h |
| 10 | `result_percent` | `Percent` | Fórmula (mesmo do Tier 1) |
| **11** | **`quality`** | **`Single select`** | **`PREMIUM`, `CAUTELA`, `CONTRA`** |
| **12** | **`mtf_trend`** | **`Single select`** | **`ALTA`, `BAIXA`, `NEUTRO`** |
| **13** | **`entry_channel`** | **`Number`** | **Decimal 1.00000** |
| **14** | **`exit_channel`** | **`Number`** | **Decimal 1.00000** |

---

## 🎨 Configuração de Cores Sugeridas

### Campo `quality`:
- **PREMIUM:** Verde (#00C851)
- **CAUTELA:** Amarelo (#FFD700)
- **CONTRA:** Laranja (#FF8800)

### Campo `mtf_trend`:
- **ALTA:** Verde (#00C851)
- **BAIXA:** Vermelho (#FF4444)
- **NEUTRO:** Cinza (#9E9E9E)

---

## ✅ Pronto para o Tier 2

Com estes campos adicionados, o Airtable está pronto para receber os dados enriquecidos do Tier 2, incluindo a qualificação de cada sinal baseada na análise MTF.
