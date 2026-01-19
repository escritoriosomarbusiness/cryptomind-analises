_# Especificações Técnicas - Sistema de Assinaturas

**Autor:** Manus AI  
**Data:** 18 de Janeiro de 2026

## 1. Airtable: Estrutura do Banco de Dados

A base de dados no Airtable será o ponto central de verdade para todas as informações de assinantes. 

- **Nome da Base:** `CryptoMind Subscribers`

### 1.1. Tabela: `Assinantes`

Esta tabela conterá o registro principal de cada cliente.

| Campo | Tipo de Campo | Configuração e Descrição |
|---|---|---|
| `ID` | `Autonumber` | Chave primária, ID numérico sequencial. |
| `Nome` | `Single line text` | Nome completo do cliente, obtido do Mercado Pago. |
| `Email` | `Email` | Email principal do cliente, usado para comunicação. |
| `Telefone` | `Phone number` | (Opcional) Telefone com DDD, para contato via WhatsApp. |
| `Telegram_Username` | `Single line text` | Username do Telegram (e.g., `@usuario`). Solicitado no pós-compra. |
| `Telegram_ID` | `Number` | ID numérico único do usuário no Telegram. Essencial para a automação. |
| `Plano` | `Single select` | Opções: `trial`, `monthly`, `quarterly`, `semiannual`, `annual`. |
| `Status` | `Single select` | Opções: `active`, `expired`, `cancelled`, `pending_payment`, `trial`. |
| `Data_Cadastro` | `Created time` | Data e hora automáticas da criação do registro. |
| `Data_Inicio` | `Date` | Data de início da assinatura (data do pagamento). |
| `Data_Vencimento` | `Formula` | Fórmula para calcular a data de vencimento com base no plano. |
| `Valor_Pago` | `Currency` | Último valor pago pelo cliente (R$). |
| `MP_Payment_ID` | `Single line text` | ID da transação no Mercado Pago, para referência. |
| `Invite_Link` | `URL` | Link de convite único gerado pelo bot do Telegram. |
| `Notas` | `Long text` | Campo para observações manuais do administrador. |

**Fórmula para `Data_Vencimento`:**
```
IF({Data_Inicio}, 
  DATEADD({Data_Inicio}, 
    SWITCH({Plano}, 
      'trial', 5, 
      'monthly', 30, 
      'quarterly', 90, 
      'semiannual', 180, 
      'annual', 365, 
      0
    ), 
    'days'
  )
)
```

### 1.2. Tabela: `Pagamentos`

Esta tabela servirá como um histórico de todas as transações financeiras.

| Campo | Tipo de Campo | Descrição |
|---|---|---|
| `ID` | `Autonumber` | Chave primária. |
| `Assinante` | `Link to another record` | Link para o registro correspondente na tabela `Assinantes`. |
| `Data_Pagamento` | `Created time` | Data e hora do registro do pagamento. |
| `Valor` | `Currency` | Valor exato da transação. |
| `Plano_Adquirido` | `Single select` | Plano referente a este pagamento. |
| `MP_Payment_ID` | `Single line text` | ID da transação no Mercado Pago. |
| `Status_Pagamento` | `Single select` | Opções: `approved`, `pending`, `cancelled`, `refunded`. |
| `Metodo` | `Single select` | Opções: `pix`, `credit_card`, `debit_card`, `boleto`. |

## 2. Mercado Pago: Integração

### 2.1. Credenciais

- **Access Token:** Será obtido no painel de desenvolvedor do Mercado Pago e configurado como uma credencial criptografada no n8n.
- **Conta:** Recomenda-se o uso de uma conta **Pessoa Jurídica (PJ)** para maior profissionalismo e acesso a melhores taxas no futuro.

### 2.2. Links de Pagamento

Serão criados 4 links de pagamento permanentes, um para cada plano. O campo `external_reference` será usado para identificar o plano no webhook.

| Plano | `external_reference` |
|---|---|
| Mensal | `cryptomind-monthly` |
| Trimestral | `cryptomind-quarterly` |
| Semestral | `cryptomind-semiannual` |
| Anual | `cryptomind-annual` |

### 2.3. Webhooks

Um único endpoint de webhook será criado no n8n e configurado no Mercado Pago para receber notificações dos seguintes eventos:

- **`payment.created`**: Um pagamento foi iniciado (e.g., boleto gerado).
- **`payment.updated`**: O status de um pagamento foi alterado (e.g., de `pending` para `approved`).

**URL do Webhook:** `https://[SEU_DOMINIO_N8N]/webhook/mercadopago-cryptomind`

O workflow do n8n irá filtrar os eventos para agir apenas quando `status` for `approved`.

## 3. Telegram Bot: Gerenciador de Membros

Um novo bot será criado exclusivamente para o gerenciamento de membros, separado do bot que envia os alertas.

- **Nome Sugerido:** `CryptoMindManagerBot`
- **Token:** O token do bot será armazenado como uma credencial no n8n.

### 3.1. Permissões no Canal

O bot deverá ser adicionado como **administrador** do canal `CryptoMind Alerts` com as seguintes permissões:

- `Invite users via link`
- `Ban users`

### 3.2. Funções na Automação (n8n)

- **`createChatInviteLink`**: Para gerar um link de convite com `member_limit` = 1.
- **`banChatMember`**: Para remover um membro do canal. O parâmetro `revoke_messages` será definido como `false`.
