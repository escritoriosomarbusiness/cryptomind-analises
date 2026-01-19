# 📱 Templates de Mensagens do Telegram - TuTCI v2.0

---

Este documento contém os templates formatados das mensagens que serão enviadas automaticamente para o Telegram pelo n8n.

## 1. Notificação de Entrada (LONG)

### Exemplo: Sinal PREMIUM

```
🟢 TURTLE LONG ENTRY - PREMIUM 🌟

Ativo: BTCUSDT
Timeframe: 15min
Preço Entrada: $93,161.00

📊 Canal Superior: $93,500.00
📊 Canal Inferior: $92,500.00

📈 Tendência Macro (H4): ALTA ✅
🎯 Qualidade: PREMIUM 🌟

⚠️ Este é um sinal de alta qualidade, alinhado com a tendência macro!

ID: BTCUSDT_15_1737301200
Horário: 19/01/2026 13:40 (GMT-3)
```

### Exemplo: Sinal de CAUTELA

```
🟡 TURTLE LONG ENTRY - CAUTELA ⚠️

Ativo: ETHUSDT
Timeframe: 1h
Preço Entrada: $3,245.80

📊 Canal Superior: $3,280.00
📊 Canal Inferior: $3,150.00

📈 Tendência Macro (D): NEUTRA 〰️
🎯 Qualidade: CAUTELA ⚠️

⚠️ Sinal em tendência neutra. Opere com gestão de risco reforçada.

ID: ETHUSDT_60_1737302400
Horário: 19/01/2026 14:00 (GMT-3)
```

### Exemplo: Sinal CONTRA Tendência

```
🔴 TURTLE LONG ENTRY - CONTRA 🚫

Ativo: SOLUSDT
Timeframe: 5min
Preço Entrada: $142.35

📊 Canal Superior: $143.00
📊 Canal Inferior: $140.50

📉 Tendência Macro (H1): BAIXA ❌
🎯 Qualidade: CONTRA 🚫

⚠️ ATENÇÃO: Sinal contra a tendência macro! Risco elevado.

ID: SOLUSDT_5_1737303000
Horário: 19/01/2026 14:10 (GMT-3)
```

---

## 2. Notificação de Saída (LONG)

### Exemplo: Trade com Lucro

```
🔴 TURTLE LONG EXIT

Ativo: BTCUSDT
Timeframe: 15min

📈 Entrada: $93,161.00 (19/01 13:40)
📉 Saída: $93,850.00 (19/01 14:25)

💰 Resultado: +0.74% ✅
⏱️ Duração: 45 minutos

🎯 Qualidade do Setup: PREMIUM 🌟
📊 Tendência Macro: ALTA ✅

ID: BTCUSDT_15_1737301200
```

### Exemplo: Trade com Prejuízo

```
🔴 TURTLE LONG EXIT

Ativo: SOLUSDT
Timeframe: 5min

📈 Entrada: $142.35 (19/01 14:10)
📉 Saída: $141.20 (19/01 14:35)

💸 Resultado: -0.81% ❌
⏱️ Duração: 25 minutos

🎯 Qualidade do Setup: CONTRA 🚫
📊 Tendência Macro: BAIXA ❌

⚠️ Prejuízo esperado em sinal contra tendência.

ID: SOLUSDT_5_1737303000
```

---

## 3. Relatório Diário

```
📊 RELATÓRIO DIÁRIO - 19/01/2026
(Período: 19/01 21:00 até 20/01 20:59)

🎯 Performance Geral:
• Total de Trades: 12
• ✅ Ganhos: 8 (66.7%)
• ❌ Perdas: 4 (33.3%)
• 💰 Lucro Total: +5.8%

🏆 Destaques:
• Melhor Trade: +2.3% (BTCUSDT LONG)
• Pior Trade: -1.1% (ETHUSDT SHORT)
• Duração Média: 38 minutos

📈 Por Qualidade:
• PREMIUM: +4.2% (5 trades, 80% win)
• CAUTELA: +1.8% (4 trades, 50% win)
• CONTRA: -0.2% (3 trades, 33% win)

⏰ Por Timeframe:
• 15min: +3.5% (7 trades)
• 1h: +2.3% (5 trades)

---
⏰ Próximo relatório: 20/01 às 20:59
```

---

## 4. Relatório Semanal

```
📊 RELATÓRIO SEMANAL - Semana 03/2026
(13/01 a 19/01)

🎯 Performance Geral:
• Total de Trades: 67
• ✅ Ganhos: 44 (65.7%)
• ❌ Perdas: 23 (34.3%)
• 💰 Lucro Total: +18.4%

📈 Evolução Diária:
• Segunda: +2.1% (10 trades)
• Terça: +3.8% (12 trades)
• Quarta: +4.2% (14 trades)
• Quinta: +2.9% (11 trades)
• Sexta: +3.5% (13 trades)
• Sábado: +1.2% (4 trades)
• Domingo: +0.7% (3 trades)

🏆 Melhores Setups:
• PREMIUM: +12.5% (28 trades, 71% win)
• CAUTELA: +4.8% (24 trades, 58% win)
• CONTRA: +1.1% (15 trades, 47% win)

💎 Ativos Mais Lucrativos:
1. BTCUSDT: +8.7% (25 trades)
2. ETHUSDT: +5.2% (18 trades)
3. SOLUSDT: +4.5% (14 trades)

---
⏰ Próximo relatório: 26/01 às 20:59
```

---

## 5. Relatório Mensal

```
📊 RELATÓRIO MENSAL - JANEIRO 2026

🎯 Performance Geral:
• Total de Trades: 287
• ✅ Ganhos: 189 (65.9%)
• ❌ Perdas: 98 (34.1%)
• 💰 Lucro Total: +42.8%
• 💵 Lucro em USD: $4,280 (capital $10k)

📈 Evolução Semanal:
• Semana 01: +8.5% (58 trades)
• Semana 02: +11.2% (72 trades)
• Semana 03: +18.4% (67 trades)
• Semana 04: +4.7% (90 trades)

🏆 Análise por Qualidade:
• PREMIUM: +28.5% (118 trades, 72% win) ⭐
• CAUTELA: +11.2% (96 trades, 61% win)
• CONTRA: +3.1% (73 trades, 52% win)

⏰ Melhor Timeframe:
• 15min: +22.3% (145 trades) 🥇
• 1h: +15.8% (89 trades) 🥈
• 5min: +4.7% (53 trades) 🥉

💎 Top 5 Ativos:
1. BTCUSDT: +18.7% (98 trades)
2. ETHUSDT: +12.5% (67 trades)
3. SOLUSDT: +8.9% (45 trades)
4. BNBUSDT: +2.1% (38 trades)
5. ADAUSDT: +0.6% (39 trades)

📊 Estatísticas Avançadas:
• Maior Sequência de Ganhos: 7 trades
• Maior Sequência de Perdas: 4 trades
• Lucro Médio por Trade: +0.15%
• Duração Média: 42 minutos

---
⏰ Próximo relatório: 28/02 às 20:59
```

---

## 6. Relatório Anual

```
📊 RELATÓRIO ANUAL - 2026

🎯 Performance Geral:
• Total de Trades: 3,458
• ✅ Ganhos: 2,287 (66.1%)
• ❌ Perdas: 1,171 (33.9%)
• 💰 Lucro Total: +487.5%
• 💵 Lucro em USD: $48,750 (capital inicial $10k)

📈 Evolução Mensal:
• Janeiro: +42.8%
• Fevereiro: +38.5%
• Março: +51.2%
• Abril: +35.9%
• Maio: +44.3%
• Junho: +39.7%
• Julho: +41.2%
• Agosto: +38.8%
• Setembro: +42.5%
• Outubro: +40.1%
• Novembro: +36.9%
• Dezembro: +35.6%

🏆 Melhor Mês: Março (+51.2%)
📉 Pior Mês: Dezembro (+35.6%)

🎯 Análise por Qualidade (Ano Todo):
• PREMIUM: +312.5% (1,421 trades, 71% win) ⭐⭐⭐
• CAUTELA: +138.7% (1,156 trades, 62% win) ⭐⭐
• CONTRA: +36.3% (881 trades, 54% win) ⭐

💎 Ativo Mais Lucrativo: BTCUSDT (+187.3%)
⏰ Timeframe Mais Lucrativo: 15min (+256.8%)

🏅 Conquistas:
• Maior Lucro Diário: +12.8% (15/03)
• Melhor Semana: +28.5% (Semana 12)
• Melhor Trade: +8.7% (BTCUSDT LONG)

---
🎉 Parabéns por um ano incrível de trading!
```
