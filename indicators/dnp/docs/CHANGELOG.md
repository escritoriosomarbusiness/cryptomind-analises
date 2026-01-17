# 📝 DNP - Changelog

**Histórico de mudanças do indicador DNP (Didi's Needle Prick)**

---

## [2.0] - 16/01/2026

### ✨ Adicionado
- **Lógica MTF (Multi-Timeframe):** Análise de tendência do fractal superior
- **Classificação de Setups:** PREMIUM/CAUTELA/CONTRA baseada no HTF
- **Campos MTF no JSON:**
  - `setupQuality`: Classificação do setup (PREMIUM/CAUTELA/CONTRA)
  - `htfTrend`: Tendência do fractal superior (ALTA/BAIXA/NEUTRO)
  - `htfTimeframe`: Timeframe do fractal superior (ex: "240")
- **Bloco Macro nas Mensagens:** Inserido entre "Timeframe" e "ENTRADA"
- **Dashboard MTF:** Informação visual no gráfico
- **Hierarquia de Timeframes:** 1m→15m, 5m→H1, 15m→H4, H1→D, H4→W, D→M

### 🔧 Modificado
- **Processador n8n:** Atualizado para formatar bloco macro
- **Mensagens Telegram:** Incluem classificação MTF
- **Documentação:** README completo com explicação MTF

### 📊 Detecção de Tendência HTF
**Tendência de ALTA (3 condições):**
- EMA 55 > EMA 233
- EMA 55 crescente (EMA55 > EMA55[1])
- Preço acima da EMA 55 (Close > EMA55)

**Tendência de BAIXA (3 condições):**
- EMA 55 < EMA 233
- EMA 55 decrescente (EMA55 < EMA55[1])
- Preço abaixo da EMA 55 (Close < EMA55)

### 📚 Arquivos Atualizados
- `pinescript/dnp_v2.0_mtf.pine` - Código Pine Script com MTF
- `n8n/processador_v2.0.js` - Processador n8n com bloco macro
- `README.md` - Documentação completa
- `docs/CHANGELOG.md` - Este arquivo

---

## [1.1] - 10/01/2026

### 🔧 Corrigido
- **REMI:** Correção no cálculo do Relative Momentum Index
- **Pivots:** Ajustes na detecção de suporte/resistência
- **Alertas:** Correção no formato JSON

### 📚 Documentação
- **Manual de Operação:** Criado `MANUAL_OPERACAO_DNP.md`
- **Configurações:** Documentação de parâmetros

---

## [1.0] - Versão Inicial

### ✨ Características Iniciais
- **Detecção de Dedo no Pavio:** Rejeição de preço (wicks grandes)
- **REMI:** Relative Momentum Index para confirmação
- **Pivots:** Suporte e Resistência automáticos
- **Sistema de Confirmação:** Gatilho + Rompimento
- **Gestão de Risco:** Entry, SL, TP1, TP2, Trailing Stop
- **Integração n8n:** Processamento de alertas
- **Notificações Telegram:** Alertas em tempo real

### 📊 Indicadores
- REMI (Relative Momentum Index)
- Pivots (Suporte/Resistência)
- ADX (Average Directional Index)

### 🎯 Timeframes Suportados
- 1 minuto
- 5 minutos
- 15 minutos
- 60 minutos (H1)
- 240 minutos (H4)
- Daily (D)

---

## 🔄 Roadmap Futuro

### 🚀 Planejado
- [ ] Backtesting automático
- [ ] Estatísticas de performance
- [ ] Alertas por email
- [ ] Dashboard web
- [ ] API REST

### 💡 Em Análise
- [ ] Machine Learning para otimização
- [ ] Integração com exchanges
- [ ] Execução automática de ordens
- [ ] Multi-asset portfolio

---

## 📊 Comparação de Versões

| Característica | v1.0 | v1.1 | v2.0 |
|----------------|------|------|------|
| Dedo no Pavio | ✅ | ✅ | ✅ |
| REMI | ✅ | ✅ | ✅ |
| Pivots | ✅ | ✅ | ✅ |
| Gestão de Risco | ✅ | ✅ | ✅ |
| MTF Analysis | ❌ | ❌ | ✅ |
| Classificação | ❌ | ❌ | ✅ |
| Bloco Macro | ❌ | ❌ | ✅ |

---

## 📝 Notas de Versão

### **v2.0 - MTF Edition**
Esta é a versão mais completa do DNP, incluindo análise de múltiplos timeframes para melhorar a qualidade dos setups. A classificação PREMIUM/CAUTELA/CONTRA ajuda a filtrar operações de baixa probabilidade.

**Recomendação:** Priorizar setups PREMIUM e evitar setups CONTRA, especialmente para traders iniciantes.

### **v1.1 - Stability Update**
Versão focada em correções e estabilidade, com ajustes no REMI e pivots.

### **v1.0 - Initial Release**
Primeira versão funcional do DNP com todas as características básicas.

---

**Desenvolvido por:** CryptoMind IA  
**Última Atualização:** 16/01/2026
