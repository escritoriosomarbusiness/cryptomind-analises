# Cronograma e Checklist de Implementação

**Autor:** Manus AI  
**Data:** 18 de Janeiro de 2026

Este documento detalha o cronograma planejado e um checklist de tarefas para a implementação completa do sistema de assinaturas do CryptoMind Alerts. A implementação está programada para iniciar após o dia 25 de Janeiro de 2026.

## Cronograma Estimado (10 dias)

| Fase | Duração | Atividades Principais |
|---|---|---|
| **Fase 1: Infraestrutura** | 2 dias | Configuração das contas, APIs e banco de dados. |
| **Fase 2: Automação (Core)** | 3 dias | Desenvolvimento dos workflows principais no n8n. |
| **Fase 3: Interface do Usuário** | 2 dias | Criação da landing page e templates de comunicação. |
| **Fase 4: Testes e Validação** | 2 dias | Testes de ponta a ponta para garantir a robustez do sistema. |
| **Fase 5: Lançamento** | 1 dia | Deploy final, documentação e início da operação. |

## Checklist de Implementação

### Fase 1: Infraestrutura (Dia 1-2)

- [ ] **Mercado Pago**
    - [ ] Confirmar (ou criar) conta Pessoa Jurídica.
    - [ ] Gerar Access Token de Produção.
    - [ ] Criar 4 links de pagamento (um para cada plano), configurando o `external_reference`.
    - [ ] Configurar o endpoint do webhook de pagamentos no painel do MP.
- [ ] **Airtable**
    - [ ] Criar a base `CryptoMind Subscribers`.
    - [ ] Criar as tabelas `Assinantes` e `Pagamentos` conforme a especificação.
    - [ ] Configurar todos os campos, tipos e fórmulas.
    - [ ] Gerar API Key para acesso do n8n.
- [ ] **Telegram**
    - [ ] Criar um novo bot (`@CryptoMindManagerBot`).
    - [ ] Obter o Token do bot.
    - [ ] Adicionar o bot como administrador do canal `@CryptoMindAlerts` com as permissões necessárias.
- [ ] **n8n**
    - [ ] Criar credencial para a API do Airtable.
    - [ ] Criar credencial para o Token do bot do Telegram.
    - [ ] Criar credencial para o Access Token do Mercado Pago.
    - [ ] Criar credencial para o serviço de envio de email (SMTP/Gmail).

### Fase 2: Automação (Core) (Dia 3-5)

- [ ] **Workflow 1: Processamento de Pagamento**
    - [ ] Implementar o workflow a partir do template.
    - [ ] Desenvolver a lógica para diferenciar novos assinantes de renovações.
    - [ ] Testar o recebimento e processamento do webhook do Mercado Pago.
- [ ] **Workflow 2: Monitoramento de Vencimentos**
    - [ ] Implementar o workflow de remoção de expirados.
    - [ ] Configurar o Cron Job para execução diária.
    - [ ] Testar a busca e remoção de um usuário de teste.
- [ ] **Workflow 3: Lembrete de Vencimento**
    - [ ] Criar um novo workflow para enviar lembretes 3 dias antes do vencimento.
    - [ ] Configurar o Cron Job para execução diária.
- [ ] **Workflow 4: Degustação (Trial)**
    - [ ] Implementar o workflow para o plano de degustação.
    - [ ] Conectar a um formulário na landing page.
    - [ ] Garantir que a remoção automática após 5 dias funcione.

### Fase 3: Interface do Usuário (Dia 6-7)

- [ ] **Landing Page**
    - [ ] Desenvolver a página estática (HTML/CSS/JS).
    - [ ] Integrar os links de pagamento do Mercado Pago.
    - [ ] Integrar o formulário de degustação.
- [ ] **Templates de Email**
    - [ ] Criar o template HTML para o email de boas-vindas.
    - [ ] Criar o template para o email de lembrete de vencimento.
    - [ ] Criar o template para o email de assinatura expirada.

### Fase 4: Testes e Validação (Dia 8-9)

- [ ] **Teste de Ponta a Ponta (Happy Path)**
    - [ ] Realizar um pagamento de teste (R$ 1,00) via Mercado Pago.
    - [ ] Validar se o registro é criado no Airtable.
    - [ ] Validar o recebimento do email de boas-vindas com o link.
    - [ ] Validar a entrada no canal do Telegram.
- [ ] **Teste de Vencimento**
    - [ ] Alterar manualmente a data de vencimento de um usuário de teste para o dia anterior.
    - [ ] Executar manualmente o workflow de monitoramento.
    - [ ] Validar se o usuário é removido do canal e o status é atualizado no Airtable.
- [ ] **Teste de Falha de Pagamento**
    - [ ] Simular um pagamento recusado ou pendente e verificar se o sistema não concede acesso.

### Fase 5: Lançamento (Dia 10)

- [ ] **Revisão Final**
    - [ ] Revisar todas as configurações, URLs e tokens.
    - [ ] Garantir que todos os workflows estão ativos.
- [ ] **Deploy**
    - [ ] Publicar a landing page em um domínio.
- [ ] **Documentação Final**
    - [ ] Criar um manual de operação simples para o administrador.
- [ ] **Go Live!**
    - [ ] Iniciar a divulgação dos planos e da página de assinatura.
