# 📈 Indicador Price Expansion System (PES) v2.0 - MTF & Reporting

---

## 📊 VISÃO GERAL

O **PES (Price Expansion System)** é um sistema de trading completo baseado na estratégia clássica de Donchian Channels, aprimorado com análises de múltiplos timeframes (MTF), filtros de qualidade de sinal e um sistema robusto de relatórios de performance via n8n e Airtable.

O objetivo é fornecer sinais de entrada e saída claros, baseados no rompimento de canais de preço (Donchian Channels), e ao mesmo tempo qualificar esses sinais com base na tendência macro, permitindo uma tomada de decisão mais informada e uma análise de performance totalmente automatizada.

**Status:** 🚧 Em Desenvolvimento  
**Versão Planejada:** 2.0  

---

## ✨ CARACTERÍSTICAS PRINCIPAIS (v2.0)

1.  **Sinais de Donchian Channels:**
    *   **Entrada Long:** Rompimento do canal superior (máxima de X períodos).
    *   **Entrada Short:** Rompimento do canal inferior (mínima de X períodos).
    *   **Saída Long:** Rompimento do canal inferior de saída (mínima de Y períodos, com Y < X).
    *   **Saída Short:** Rompimento do canal superior de saída (máxima de Y períodos, com Y < X).

2.  **Análise Multi-Timeframe (MTF) Orientativa:**
    *   Analisa a tendência em um "fractal superior" (ex: 15min → H4) usando EMAs 55 e 233.
    *   **Não bloqueia sinais**, mas os qualifica em 3 níveis para análise de risco.

3.  **Classificação de Qualidade do Sinal:**
    *   🌟 **PREMIUM:** Sinal a favor da tendência macro.
    *   ⚠️ **CAUTELA:** Sinal em ambiente de tendência neutra.
    *   🚫 **CONTRA:** Sinal contra a tendência macro.

4.  **Filtro de Força do Candle:**
    *   Valida entradas apenas se o candle de rompimento fechar no seu **terço final**, indicando força e convicção no movimento.

5.  **Webhook Unificado para Automação:**
    *   Envia um JSON estruturado para o n8n a cada evento (Entrada/Saída), contendo todos os dados necessários para processamento e armazenamento.

6.  **Sistema de Relatórios de Performance (n8n + Airtable):**
    *   **Rastreamento por Trade:** Calcula o resultado (lucro/prejuízo) de cada operação individualmente.
    *   **Relatórios Automáticos:** Gera e envia para o Telegram relatórios de performance diários, semanais, mensais e anuais.
    *   **Fuso Horário Cripto:** Todos os relatórios diários respeitam o fechamento do mercado cripto às **21:00 (Brasília)**.

7.  **Melhorias Visuais no Gráfico:**
    *   Labels de entrada e saída posicionadas dinamicamente para evitar sobreposição.
    *   Cores das labels indicam a qualidade do sinal (Verde, Amarelo, Vermelho).
    *   Dashboard informativo com o status da tendência MTF.

---

## 📚 DOCUMENTAÇÃO DETALHADA

*   **[Especificações Técnicas do Indicador](./docs/SPECIFICATIONS.md):** Detalhes sobre a lógica do Pine Script, cálculos de MTF, filtros e estrutura do webhook.
*   **[Estrutura do Airtable e Relatórios](./airtable/AIRTABLE_STRUCTURE.md):** Schema completo das tabelas no Airtable e descrição dos workflows de automação no n8n.
*   **[Plano de Implementação Priorizado](./docs/IMPLEMENTATION_PLAN.md):** Divisão do desenvolvimento em 3 Tiers (MVP, Core Features, Advanced Reporting).

---

## 🚀 OBJETIVO FINAL

Criar um sistema de trading semi-automatizado que não apenas gera sinais, mas também fornece um framework completo para **análise de risco em tempo real** (via qualificação MTF) e **análise de performance histórica** (via relatórios Airtable), permitindo a otimização contínua da estratégia.
