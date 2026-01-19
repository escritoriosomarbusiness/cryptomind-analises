# Templates de Email - Sistema de Assinaturas

**Autor:** Manus AI  
**Data:** 18 de Janeiro de 2026

Este documento contém os templates de email que serão utilizados pelo sistema de assinaturas para comunicação com os clientes.

## 1. Email de Boas-Vindas (Pagamento Confirmado)

**Assunto:** 🎉 Bem-vindo ao CryptoMind Alerts!

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .info-box { background: white; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Bem-vindo ao CryptoMind Alerts!</h1>
        </div>
        <div class="content">
            <p>Olá <strong>{{Nome}}</strong>,</p>
            
            <p>Seu pagamento foi confirmado com sucesso! Estamos muito felizes em tê-lo conosco.</p>
            
            <div class="info-box">
                <p><strong>📱 Plano:</strong> {{Plano}}<br>
                <strong>💰 Valor:</strong> R$ {{Valor_Pago}}<br>
                <strong>📅 Válido até:</strong> {{Data_Vencimento}}</p>
            </div>
            
            <h3>Como acessar seus alertas:</h3>
            <ol>
                <li>Clique no botão abaixo</li>
                <li>Você será redirecionado para o Telegram</li>
                <li>Entre no canal privado</li>
                <li>Ative as notificações para não perder nenhum alerta</li>
            </ol>
            
            <center>
                <a href="{{Invite_Link}}" class="button">🚀 Acessar Canal Agora</a>
            </center>
            
            <p><em>Importante: Este link é válido por 24 horas e pode ser usado apenas uma vez.</em></p>
            
            <h3>O que você vai receber:</h3>
            <ul>
                <li>✅ Alertas TRS (Trend Reversal System)</li>
                <li>✅ Alertas DNP (Dynamic Pivot Points)</li>
                <li>✅ Alertas STS (Smart Trading System)</li>
                <li>✅ Alertas USDT.D Monitor</li>
                <li>✅ Múltiplos timeframes (H1, H4, D1, W1)</li>
            </ul>
            
            <p>Precisa de ajuda? Responda este email ou entre em contato conosco.</p>
            
            <p>Bons trades! 📈<br>
            <strong>Equipe CryptoMind</strong></p>
        </div>
    </div>
</body>
</html>
```

---

## 2. Email de Lembrete (3 dias antes do vencimento)

**Assunto:** ⏰ Sua assinatura do CryptoMind Alerts vence em 3 dias

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f59e0b; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .warning-box { background: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⏰ Lembrete de Vencimento</h1>
        </div>
        <div class="content">
            <p>Olá <strong>{{Nome}}</strong>,</p>
            
            <p>Sua assinatura do CryptoMind Alerts está próxima do vencimento.</p>
            
            <div class="warning-box">
                <p><strong>📅 Data de Vencimento:</strong> {{Data_Vencimento}}<br>
                <strong>⏳ Tempo Restante:</strong> 3 dias</p>
            </div>
            
            <p>Para continuar recebendo nossos alertas profissionais de trading, renove sua assinatura agora e garanta que não vai perder nenhuma oportunidade!</p>
            
            <center>
                <a href="[LINK_RENOVACAO]" class="button">🔄 Renovar Agora</a>
            </center>
            
            <p><strong>Por que renovar?</strong></p>
            <ul>
                <li>📊 Alertas em tempo real de múltiplos indicadores</li>
                <li>🎯 Precisão comprovada em diferentes timeframes</li>
                <li>🚀 Sistema 100% automatizado</li>
                <li>💎 Suporte dedicado</li>
            </ul>
            
            <p>Dúvidas? Responda este email e nossa equipe terá prazer em ajudar.</p>
            
            <p>Até breve! 👋<br>
            <strong>Equipe CryptoMind</strong></p>
        </div>
    </div>
</body>
</html>
```

---

## 3. Email de Expiração

**Assunto:** ❌ Sua assinatura do CryptoMind Alerts expirou

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #ef4444; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .info-box { background: #fee2e2; padding: 15px; border-left: 4px solid #ef4444; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Assinatura Expirada</h1>
        </div>
        <div class="content">
            <p>Olá <strong>{{Nome}}</strong>,</p>
            
            <p>Sua assinatura do CryptoMind Alerts expirou hoje e seu acesso ao canal foi removido.</p>
            
            <div class="info-box">
                <p><strong>📅 Data de Expiração:</strong> {{Data_Vencimento}}<br>
                <strong>📱 Plano Anterior:</strong> {{Plano}}</p>
            </div>
            
            <p>Sentiremos sua falta! 😢</p>
            
            <p>Mas não se preocupe, você pode renovar sua assinatura a qualquer momento e voltar a receber nossos alertas profissionais de trading.</p>
            
            <center>
                <a href="[LINK_RENOVACAO]" class="button">🔄 Renovar Assinatura</a>
            </center>
            
            <p><strong>O que você está perdendo:</strong></p>
            <ul>
                <li>📊 Alertas TRS, DNP, STS e USDT.D em tempo real</li>
                <li>🎯 Múltiplos timeframes (H1, H4, D1, W1)</li>
                <li>🚀 Sistema automatizado 24/7</li>
                <li>💎 Comunidade exclusiva de traders</li>
            </ul>
            
            <p>Tem alguma dúvida ou feedback? Responda este email, adoraríamos ouvir você!</p>
            
            <p>Esperamos vê-lo novamente em breve! 🚀<br>
            <strong>Equipe CryptoMind</strong></p>
        </div>
    </div>
</body>
</html>
```

---

## 4. Email de Boas-Vindas (Degustação)

**Assunto:** 🎁 Bem-vindo à sua degustação gratuita do CryptoMind Alerts!

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .info-box { background: white; padding: 15px; border-left: 4px solid #10b981; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎁 Bem-vindo à sua Degustação Gratuita!</h1>
        </div>
        <div class="content">
            <p>Olá <strong>{{Nome}}</strong>,</p>
            
            <p>Seja bem-vindo ao CryptoMind Alerts! Você tem <strong>5 dias de acesso gratuito</strong> para experimentar nosso sistema profissional de alertas de trading.</p>
            
            <div class="info-box">
                <p><strong>📅 Válido até:</strong> {{Data_Vencimento}}<br>
                <strong>🎯 Acesso:</strong> Completo a todos os alertas</p>
            </div>
            
            <h3>Como acessar:</h3>
            <ol>
                <li>Clique no botão abaixo</li>
                <li>Entre no canal privado do Telegram</li>
                <li>Ative as notificações</li>
                <li>Aproveite os alertas!</li>
            </ol>
            
            <center>
                <a href="{{Invite_Link}}" class="button">🚀 Acessar Canal Agora</a>
            </center>
            
            <p><strong>Durante sua degustação você receberá:</strong></p>
            <ul>
                <li>✅ Alertas TRS, DNP, STS e USDT.D</li>
                <li>✅ Múltiplos timeframes (H1, H4, D1, W1)</li>
                <li>✅ Alertas em tempo real 24/7</li>
            </ul>
            
            <p><strong>Após os 5 dias:</strong> Seu acesso será removido automaticamente. Se gostar do serviço, você poderá escolher um dos nossos planos pagos para continuar recebendo os alertas.</p>
            
            <p>Aproveite ao máximo! 🚀<br>
            <strong>Equipe CryptoMind</strong></p>
        </div>
    </div>
</body>
</html>
```

---

## Variáveis Disponíveis

Todos os templates suportam as seguintes variáveis (substituídas dinamicamente pelo n8n):

- `{{Nome}}` - Nome do assinante
- `{{Email}}` - Email do assinante
- `{{Plano}}` - Nome do plano (Mensal, Trimestral, etc.)
- `{{Valor_Pago}}` - Valor pago formatado
- `{{Data_Vencimento}}` - Data de vencimento formatada
- `{{Invite_Link}}` - Link de convite do Telegram
- `{{MP_Payment_ID}}` - ID da transação (para referência)
