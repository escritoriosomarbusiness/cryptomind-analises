# ✅ CHECKLIST RÁPIDO - SETUP DNP v1.1

**Guia de configuração em 10 passos**

---

## 🚀 CONFIGURAÇÃO INICIAL

### **1. TRADINGVIEW**

- [ ] Criar novo indicador Pine Script
- [ ] Copiar código de `/home/ubuntu/dnp_v1.1_remi_pivots_corrigido.txt`
- [ ] Salvar como "DNP v1.1"
- [ ] Aplicar no gráfico BTCUSDT 15min

**Parâmetros Recomendados (15min):**
```
Didi Dist. Eixo: 0.20%
ADX Mínimo: 20
Inclinação ADX: 2.5
REMI Mínimo: 1.5
Pivot Breakout: Por Fechamento (Close)
Stop Loss: 3 Candles Anteriores
```

---

### **2. N8N**

- [ ] Acessar instância n8n
- [ ] Importar workflow de `/home/ubuntu/n8n_workflow_dnp.json`
- [ ] Configurar credenciais Telegram:
  - Token do Bot
  - Chat ID
- [ ] Copiar URL do webhook (produção)
- [ ] Ativar workflow

**URL Webhook Exemplo:**
```
https://seu-n8n.com/webhook/dnp-alerts
```

---

### **3. TELEGRAM**

- [ ] Criar bot via @BotFather
- [ ] Copiar token do bot
- [ ] Obter Chat ID via @userinfobot
- [ ] Enviar `/start` para o bot
- [ ] Testar envio manual no n8n

---

### **4. ALERTAS TRADINGVIEW**

**Criar 4 alertas por cripto/timeframe:**

#### **Alerta 1: DNP LONG TRIGGER**
```
Nome: DNP LONG TRIGGER - {{ticker}} - {{interval}}
Condição: DNP by CryptoMindIA → alert() function call
Mensagem: {{plot_0}}
Webhook: https://seu-n8n.com/webhook/dnp-alerts
Frequência: Once Per Bar Close
Validade: Open-ended
```

#### **Alerta 2: DNP LONG CONFIRMED**
```
Nome: DNP LONG CONFIRMED - {{ticker}} - {{interval}}
(mesmas configurações)
```

#### **Alerta 3: DNP SHORT TRIGGER**
```
Nome: DNP SHORT TRIGGER - {{ticker}} - {{interval}}
(mesmas configurações)
```

#### **Alerta 4: DNP SHORT CONFIRMED**
```
Nome: DNP SHORT CONFIRMED - {{ticker}} - {{interval}}
(mesmas configurações)
```

---

## 🧪 TESTES

### **5. TESTE N8N**

- [ ] Abrir workflow no n8n
- [ ] Clicar em "Execute Workflow"
- [ ] Enviar JSON de teste:

```json
{
  "symbol": "BTCUSDT",
  "action": "TRIGGER",
  "direction": "LONG",
  "setup": "DNP",
  "timeframe": "15",
  "price": "90000.00",
  "triggerHigh": "90100.00",
  "adx": "22.00",
  "remi": "1.80"
}
```

- [ ] Verificar mensagem no Telegram

---

### **6. TESTE ALERTAS**

- [ ] Verificar alertas ativos no TradingView
- [ ] Aguardar sinal real ou usar replay
- [ ] Confirmar recebimento no Telegram
- [ ] Validar formato da mensagem

---

## 🎯 OPERAÇÃO

### **7. RECEBER TRIGGER**

**Quando receber:**
```
🔔 🟢 LONG BTCUSDT
📊 Setup DNP by CryptoMind IA
⏱️ 15m • 🕐 10/01/2026 12:30
🔔 GATILHO ARMADO
```

**Fazer:**
- [ ] Abrir gráfico
- [ ] Verificar visualmente
- [ ] Aguardar próximo candle
- [ ] **NÃO ENTRAR ainda!**

---

### **8. RECEBER CONFIRMED**

**Quando receber:**
```
✅ 🟢 LONG BTCUSDT
📊 Setup DNP by CryptoMind IA
⏱️ 15m • 🕐 10/01/2026 12:45
✅ CONFIRMADO POR ROMPIMENTO

🎯 Entrada: $91050.00
🛑 Stop Loss: $90500.00 (0.60%)
📈 Alvos:
1️⃣ $91600.00 (1R) → Realizar 40%
2️⃣ $92150.00 (2R) → Ativar Trailing Stop
```

**Fazer:**
- [ ] Executar entrada no preço indicado
- [ ] Configurar Stop Loss
- [ ] Configurar Take Profit 1 (40%)
- [ ] Configurar Take Profit 2 (60%)

---

### **9. GERENCIAR OPERAÇÃO**

**Ao atingir Target 1:**
- [ ] Realizar 40% da posição
- [ ] Mover SL para breakeven
- [ ] Ativar trailing stop 0.5R

**Ao atingir Target 2:**
- [ ] Realizar 60% restante
- [ ] Encerrar operação
- [ ] Registrar resultado

---

### **10. REGISTRAR RESULTADO**

- [ ] Atualizar planilha de controle
- [ ] Calcular resultado em R
- [ ] Analisar trade
- [ ] Fazer pausa antes do próximo

---

## 📊 PARÂMETROS POR TIMEFRAME

### **5 MINUTOS (Scalping)**
```
Didi Dist. Eixo: 0.10%
ADX Mínimo: 15
Inclinação ADX: 1.5
REMI Mínimo: 1.5
Pivot Breakout: Por Fechamento
```

### **15 MINUTOS (Intraday)** ⭐
```
Didi Dist. Eixo: 0.20%
ADX Mínimo: 20
Inclinação ADX: 2.5
REMI Mínimo: 1.5
Pivot Breakout: Por Fechamento
```

### **1 HORA (Swing)**
```
Didi Dist. Eixo: 0.30%
ADX Mínimo: 25
Inclinação ADX: 3.0
REMI Mínimo: 1.8
Pivot Breakout: Por Pavio
```

---

## 🎯 GESTÃO DE RISCO

**REGRA DE OURO:**
```
Risco por trade: 1-2% da banca
Alavancagem máxima: 10x
Risco real máximo: 15%
```

**Exemplo (Banca $10,000):**
```
Risco: 1% = $100
Entry: $91,050
Stop Loss: $90,500
Risco (pontos): $550

Posição = $100 / $550 = 0.1818 BTC
Com 16x: 0.1818 / 16 = 0.0114 BTC
Valor: 0.0114 × $91,050 = $1,037
```

---

## ⚠️ ERROS COMUNS

**NÃO FAZER:**
- ❌ Entrar antes do CONFIRMED
- ❌ Mover Stop Loss
- ❌ Não realizar parcial no TP1
- ❌ Arriscar mais de 2% por trade
- ❌ Revenge trading após perda

**FAZER:**
- ✅ Aguardar sempre CONFIRMED
- ✅ Respeitar SL original
- ✅ Realizar 40% no TP1
- ✅ Máximo 1-2% por trade
- ✅ Pausa após perda

---

## 📚 DOCUMENTAÇÃO COMPLETA

1. **GUIA_ALERTAS_TRADINGVIEW.md** - Configuração detalhada de alertas
2. **MANUAL_OPERACAO_DNP.md** - Manual completo de operação
3. **DNP_V1.1_CORRECOES.md** - Correções técnicas v1.1
4. **DNP_N8N_SETUP.md** - Setup do workflow n8n

---

## 🎉 PRONTO PARA OPERAR!

**Checklist Final:**
- [ ] DNP v1.1 instalado
- [ ] Workflow n8n ativo
- [ ] Bot Telegram funcionando
- [ ] 4 alertas configurados
- [ ] Testes realizados
- [ ] Gestão de risco definida
- [ ] Planilha de controle pronta

**BOA SORTE! 🚀**
