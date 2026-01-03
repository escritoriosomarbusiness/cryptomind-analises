# Parâmetros Realistas para Day Trade e Scalp em Cripto

## Problemas Identificados nas Calls Atuais

### 1. Falta de Especificidade
- ❌ "Rompimento" sem dizer de quê
- ❌ Não informa qual SR foi rompida
- ❌ Não especifica timeframe do setup

### 2. Range de Entrada Muito Amplo
- ❌ BNB: $875.55 - $897.19 = 2.47% de variação
- ✅ Máximo aceitável: 0.3% - 0.5%

### 3. Stop Loss Incorreto
- ❌ BNB: SL em $831.16 = 7.3% da entrada máxima
- ❌ Com 10x alavancagem = 73% de perda
- ✅ Máximo aceitável: 0.5% - 1.5% (5-15% com 10x)

---

## Parâmetros Corretos por Tipo de Operação

### Scalp (5-15 min)
| Parâmetro | Valor |
|-----------|-------|
| Range de entrada | 0.1% - 0.2% |
| Stop Loss | 0.3% - 0.5% |
| Take Profit | 0.5% - 1.0% |
| R:R mínimo | 1:1.5 |
| Alavancagem máx | 20x |
| Duração | 5-30 min |

### Day Trade (H1-H4)
| Parâmetro | Valor |
|-----------|-------|
| Range de entrada | 0.2% - 0.5% |
| Stop Loss | 0.5% - 1.5% |
| Take Profit | 1.0% - 3.0% |
| R:R mínimo | 1:2 |
| Alavancagem máx | 10x |
| Duração | 1-8 horas |

### Swing (D1)
| Parâmetro | Valor |
|-----------|-------|
| Range de entrada | 0.5% - 1.0% |
| Stop Loss | 1.5% - 3.0% |
| Take Profit | 3.0% - 10.0% |
| R:R mínimo | 1:2 |
| Alavancagem máx | 5x |
| Duração | 1-7 dias |

---

## Especificidade das Calls

### Formato Correto de Call

```
🟦 LONG BTC - TS1 Rompimento

📍 FUNDAMENTO:
   Rompimento da resistência de $91.200 no H4
   Confirmação: Fechamento acima com volume
   Timeframe de entrada: H1

📊 SETUP:
   Entrada: $91.250 - $91.450 (0.22%)
   Stop Loss: $90.800 (0.49%)
   
📈 ALVOS:
   TP1: $92.100 (0.93%) - Realizar 50%
   TP2: $93.000 (1.92%) - Realizar 30%
   TP3: Trailing 0.5% - Restante 20%

⚙️ GESTÃO:
   Risco: 1% da banca
   Alavancagem: 10x
   Perda máxima: 4.9% do capital alocado
   
✅ Score: 7/10 (MÉDIA)
```

### O Que Deve Constar

1. **Fundamento Técnico:**
   - Qual SR foi rompida/rejeitada
   - Em qual timeframe
   - Qual confirmação foi usada

2. **Setup Preciso:**
   - Range de entrada estreito (máx 0.5%)
   - Stop loss calculado corretamente
   - Distância do SL em % real

3. **Alvos Realistas:**
   - Baseados em SR reais
   - R:R calculado corretamente
   - Parciais definidas

4. **Gestão de Risco:**
   - Risco real em %
   - Perda máxima com alavancagem
   - Exposição total

---

## Tipos de Setup Específicos

### TS1 - Rompimento
**Fundamentos possíveis:**
- Rompimento de resistência horizontal no H4
- Rompimento de LTB (Linha de Tendência de Baixa)
- Rompimento da EMA 200 no H1
- Rompimento de range de consolidação

**Entrada:**
- Após fechamento acima/abaixo da SR
- Pullback ao nível rompido (ideal)

**Stop:**
- Abaixo/acima da SR rompida
- Máximo 0.5-1% de distância

### TS2 - Continuação (Pullback)
**Fundamentos possíveis:**
- Pullback na EMA 21 do H4
- Pullback na EMA 9 do H1
- Reteste de suporte após rompimento
- Pullback em 38.2% ou 50% de Fibo

**Entrada:**
- Na zona de pullback
- Após candle de rejeição

**Stop:**
- Abaixo do fundo do pullback
- Máximo 0.5-1% de distância

### TS3 - Reversão
**Fundamentos possíveis:**
- Rejeição de resistência importante no H4
- Divergência de RSI no H1
- Padrão de reversão (engolfo, pin bar)
- Toque em banda de Bollinger com rejeição

**Entrada:**
- Após confirmação de rejeição
- Candle de reversão fechado

**Stop:**
- Acima/abaixo do extremo
- Máximo 0.3-0.5% de distância

---

## Cálculos de Risco

### Fórmula de Tamanho de Posição
```
Tamanho = (Banca × Risco%) / (SL% × Alavancagem)

Exemplo:
- Banca: $10.000
- Risco: 1%
- SL: 0.5%
- Alavancagem: 10x

Tamanho = (10000 × 0.01) / (0.005 × 10)
Tamanho = 100 / 0.05
Tamanho = $2.000 (20% da banca)
```

### Perda Máxima Real
```
Perda Real = SL% × Alavancagem

Exemplo:
- SL: 0.5%
- Alavancagem: 10x
- Perda Real: 5% do capital alocado
```

---

## Regras de Ouro

1. **Nunca** range de entrada > 0.5%
2. **Nunca** SL > 1.5% para day trade
3. **Nunca** SL > 0.5% para scalp
4. **Sempre** especificar o fundamento
5. **Sempre** informar timeframe do setup
6. **Sempre** calcular perda real com alavancagem
7. **Sempre** R:R mínimo de 1:1.5
