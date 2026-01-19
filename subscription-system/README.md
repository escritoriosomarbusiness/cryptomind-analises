# Sistema de Assinaturas - CryptoMind Alerts 🚀

**Versão:** 1.0  
**Data:** Janeiro de 2026  
**Status:** Em Planejamento

## Visão Geral

Este diretório contém toda a documentação, templates e configurações necessárias para a implementação de um **sistema de assinaturas 100% automatizado** para o canal privado do Telegram **CryptoMind Alerts**.

O sistema gerencia todo o ciclo de vida de uma assinatura, desde o pagamento inicial até a renovação ou expiração, sem necessidade de intervenção manual.

## Planos Disponíveis

| Plano | Duração | Preço | Preço/mês | Desconto |
|---|---|---|---|---|
| **Degustação** | 5 dias | Grátis | - | - |
| **Mensal** | 30 dias | R$ 149,00 | R$ 149,00 | - |
| **Trimestral** | 90 dias | R$ 399,00 | R$ 133,00 | 11% |
| **Semestral** | 180 dias | R$ 774,00 | R$ 129,00 | 13% |
| **Anual** | 365 dias | R$ 1.200,00 | R$ 100,00 | 33% |

## Stack Tecnológica

- **Pagamento:** Mercado Pago (Pix, Cartão, Boleto)
- **Automação:** n8n (workflows)
- **Banco de Dados:** Airtable
- **Comunicação:** Telegram Bot API + Email (SMTP/Gmail)
- **Landing Page:** HTML/CSS/JS

## Estrutura de Diretórios

```
subscription-system/
├── docs/                          # Documentação técnica
│   ├── 01_SYSTEM_ARCHITECTURE.md  # Arquitetura do sistema
│   ├── 02_TECHNICAL_SPECIFICATIONS.md # Especificações técnicas (Airtable, MP, Telegram)
│   └── 03_IMPLEMENTATION_SCHEDULE.md # Cronograma e checklist
├── workflows/                     # Templates de workflows n8n
│   ├── 01_PAYMENT_PROCESSING_WORKFLOW.md
│   └── 02_EXPIRATION_MONITORING_WORKFLOW.md
├── templates/                     # Templates de email e mensagens
├── database/                      # Scripts e configurações do Airtable
├── landing-page/                  # Código da landing page
├── scripts/                       # Scripts auxiliares (Python, etc.)
└── README.md                      # Este arquivo
```

## Documentação

A documentação completa está organizada na pasta `docs/`:

1.  **[Arquitetura do Sistema](docs/01_SYSTEM_ARCHITECTURE.md)**: Visão geral da arquitetura, componentes principais e fluxo de dados.
2.  **[Especificações Técnicas](docs/02_TECHNICAL_SPECIFICATIONS.md)**: Detalhamento da estrutura do Airtable, integração com Mercado Pago e configuração do Telegram Bot.
3.  **[Cronograma de Implementação](docs/03_IMPLEMENTATION_SCHEDULE.md)**: Cronograma de 10 dias e checklist completo de tarefas.

## Workflows n8n

Os templates dos workflows principais estão na pasta `workflows/`:

- **Processamento de Pagamento**: Recebe webhooks do Mercado Pago, registra assinantes e envia acesso.
- **Monitoramento de Vencimentos**: Executa diariamente para remover assinantes expirados.

## Próximos Passos

A implementação está programada para iniciar após o dia **25 de Janeiro de 2026**.

Consulte o [Cronograma de Implementação](docs/03_IMPLEMENTATION_SCHEDULE.md) para o plano detalhado.

---

**Desenvolvido por:** CryptoMind IA  
**Suporte:** [Inserir contato]
