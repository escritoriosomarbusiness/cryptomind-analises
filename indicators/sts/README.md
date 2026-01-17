# 🎯 STS by CryptoMind v1.0

**STS (Stormer Trap Setup)** é um indicador de **rejeição e continuação/reversão** para o ecossistema CryptoMind IA. Ele foi projetado para identificar oportunidades de trading baseadas na rejeição de zonas de preço importantes, confirmadas por um candle de ignição (martelo) e o rompimento subsequente.

---

## 📊 Conceito Principal

O STS é inspirado na **"Trap do Stormer"**, um setup que busca capturar a indecisão do mercado em zonas de suporte/resistência e capitalizar no movimento subsequente quando a direção é confirmada.

### **Estrutura do Setup:**

1.  **GATILHO (Trigger):**
    *   O preço interage com uma **zona de rejeição** (SR do HTF, Golden Zone do HTF ou EMAs).
    *   O mercado rejeita essa zona, formando um **candle martelo** (ou martelo invertido) com um pavio significativamente maior que o corpo.
    *   Isso sinaliza uma "armadilha" (trap) para traders que apostaram no rompimento da zona.

2.  **ACIONAMENTO (Confirmation):**
    *   O **candle seguinte** ao gatilho rompe a máxima (para LONG) ou a mínima (para SHORT) do candle gatilho.
    *   Este rompimento confirma a força do movimento contrário à rejeição e aciona a entrada.

---

## 🚀 Diferencial: Continuação vs. Reversão (MTF)

O grande diferencial do STS é seu **filtro MTF atuante**, que não apenas qualifica, mas **filtra** os sinais, focando em operações de maior probabilidade.

### **Cenário 1: Continuação de Tendência (PREMIUM ⭐⭐⭐)**

*   **Lógica:** O HTF (fractal superior) está em tendência clara (alta ou baixa).
*   **Setup:** O STS detecta uma trap que sinaliza um movimento **a favor** da tendência do HTF.
*   **Exemplo:** HTF em ALTA, preço faz uma pequena correção, rejeita um suporte e arma um STS LONG. Isso é uma **continuação da tendência macro**.
*   **Resultado:** Sinal de **ALTA PROBABILIDADE**.

### **Cenário 2: Reversão de Tendência (CONTRA 🎣⚠️)**

*   **Lógica:** O HTF está em tendência clara, mas o STS detecta uma trap **contra** essa tendência.
*   **Setup:**
    *   **Bottom Fishing:** HTF em BAIXA, mas o STS arma um TRAP LONG em um fundo.
    *   **Top Fishing:** HTF em ALTA, mas o STS arma um TRAP SHORT em um topo.
*   **Resultado:** Sinal de **ALTO RISCO**, claramente identificado para traders experientes que buscam reversões.

### **Cenário 3: Sem Tendência (CAUTELA - BLOQUEADO)**

*   **Lógica:** O HTF está sem tendência definida (lateral).
*   **Resultado:** O sinal **NÃO É ENVIADO** ao Telegram. O STS foca em setups onde há uma tendência macro estabelecida para se alinhar ou reverter.

---

## 🛠️ Zonas de Rejeição e Confluências

O STS valida a rejeição em até 3 tipos de zonas simultaneamente, criando um poderoso sistema de confluências.

### **Zonas de Rejeição:**

1.  **Pivots (SR) do HTF:** Suportes e resistências do timeframe superior.
2.  **Golden Zone (Fibonacci):** Níveis de 0.5 e 0.618 de retração de Fibonacci, calculados nos pivots do HTF.
3.  **Múltiplas EMAs:** Um conjunto configurável de EMAs (13, 21, 34, 55, 89, 144, 233).

### **Sistema de Confluências:**

*   **Simples:** Rejeição em 1 zona (ex: apenas SR).
*   **Dupla ⭐:** Rejeição em 2 zonas (ex: SR + EMA).
*   **Tripla 🌟🌟:** Rejeição em 3 zonas (SR + Fibo + EMA) - **SINAL DE ALTÍSSIMA PROBABILIDADE**.

### **Graduação de EMAs:**

O STS também destaca a força da barreira de EMAs:

*   **1 EMA Rejeitada:** Normal.
*   **2 EMAs Rejeitadas 🟡:** Barreira Dupla.
*   **3+ EMAs Rejeitadas 🔴:** Barreira Tripla/SUPER - **SINAL EXCEPCIONALMENTE FORTE**.

---

## ⚙️ Gestão de Risco

O STS possui uma gestão de risco clara e automatizada:

*   **Entrada:** No rompimento do trigger (máxima/mínima do candle gatilho).
*   **Stop Loss:** 1 tick abaixo/acima do candle gatilho.
*   **TP1 (1R):** Realização parcial de 50% e movimenta o Stop Loss para a entrada (breakeven).
*   **TP2 (2R):** Ativa o Trailing Stop para maximizar os ganhos nos 50% restantes da posição.
*   **Alavancagem Sugerida:**
    *   **PREMIUM:** 3x
    *   **CONTRA:** 2x (reduzida, devido ao alto risco).

---

## 📦 Conteúdo do Diretório

*   **`/pinescript/sts_v1.0_mtf.pine`**: Código fonte completo do indicador para TradingView.
*   **`/n8n/processador_v1.0.js`**: Código do node "Code" para processar e formatar os alertas no n8n.
*   **`/n8n/workflow_sts_v1.0.json`**: Workflow completo do n8n (Webhook -> Processador -> Telegram).
*   **`/docs/`**: Documentações adicionais, como o changelog.
*   **`README.md`**: Este arquivo.
