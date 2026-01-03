# CryptoMind IA - Sistema v2.0

## Visão Geral

Sistema completo de análise técnica para day trade em criptomoedas, 100% automatizado.

## Funcionalidades

### 1. Análise Multi-Timeframe
- **Timeframes:** W1, D1, H4, H1
- **Ativos:** BTC, ETH, SOL, BNB, XRP (Top 5)
- **Indicadores:** RSI, MACD, EMAs (9, 21, 200), ADX

### 2. Análise Macro
- **Fear & Greed Index** - Sentimento do mercado
- **BTC.D** - Dominância do Bitcoin
- **USDT.D** - Dominância de stablecoins (inversamente proporcional)

### 3. Trading Systems

| TS | Nome | Cor | Risco | Alavancagem | Win Rate Esperado |
|----|------|-----|-------|-------------|-------------------|
| TS1 | Rompimento | 🟦 Azul | 2% | 10x | 45-55% |
| TS2 | Continuação | 🟩 Verde | 3% | 7x | 55-65% |
| TS3 | Reversão | 🟧 Laranja | 1% | 5x | 30-40% |

### 4. Score de Confiança
- Escala de 0-10
- Algoritmo interno (caixa preta)
- Classificação: Alta (8-10), Média (5-7), Baixa (3-4)

### 5. Gestão de Risco
- Parciais automáticas
- Trailing stop após primeira parcial
- Exposição máxima: 5% da banca

### 6. Alertas Telegram
- Bot: @cryptomind_ia_bot
- Resumo diário
- Alertas de setups (score >= 5)
- Relatórios semanais e mensais

### 7. Rastreamento de Performance
- KPIs em tempo real
- Win Rate, Profit Factor
- Análise por TS, ativo e direção

## Scripts Principais

| Script | Função |
|--------|--------|
| `run_complete_cycle.py` | Executa ciclo completo |
| `multi_timeframe_analyzer.py` | Análise multi-timeframe |
| `trading_systems.py` | Detecção de setups |
| `confidence_score.py` | Cálculo de score |
| `risk_management.py` | Gestão de risco |
| `telegram_bot.py` | Alertas Telegram |
| `performance_tracker.py` | Rastreamento de performance |

## Execução

### Manual
```bash
cd /home/ubuntu/cryptomind-analises
python3 scripts/run_complete_cycle.py
```

### Automática (Manus)
As análises são executadas automaticamente:
- **Abertura:** 08:00 BRT
- **Fechamento:** 20:00 BRT
- **Semanal:** Domingos 21:15 BRT
- **Mensal:** Último dia 21:15 BRT

## Estrutura de Dados

```
data/
├── current/              # Análises atuais
├── archive/              # Histórico
├── performance/          # KPIs e rastreamento
├── index/                # Índices de navegação
├── full_analysis.json    # Análise completa
└── telegram_config.json  # Configuração do bot
```

## Site
- **URL:** https://analises.cryptomindia.com
- **Histórico:** https://analises.cryptomindia.com/history.html

## Regras de Ouro

1. **100% automatizado** - Sem intervenção manual
2. **Não quebrar funcionalidades** - Testes antes de produção
3. **Score mínimo 5** - Para alertas e operações
4. **Exposição máxima 5%** - Gestão de risco rigorosa
5. **Algoritmo interno** - Score não é revelado ao usuário

## Próximos Passos

- [ ] Validar performance real dos setups
- [ ] Ajustar parâmetros baseado em resultados
- [ ] Expandir para Top 10/20 ativos
- [ ] Implementar sistema de pagamento (após validação)

---

**Versão:** 2.0
**Data:** 03/01/2026
**Autor:** CryptoMind IA
