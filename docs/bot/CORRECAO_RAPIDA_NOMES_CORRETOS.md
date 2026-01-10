# ⚡ Correção Rápida - Nomes EXATOS dos Nós

## 🎯 Nós que precisam ser corrigidos:

1. **Switch Comando** (nome exato no workflow)
2. **Switch Callback** (nome exato no workflow)

---

## ✅ PASSO A PASSO EXATO

### Passo 1: Corrigir "Switch Comando"

1. Acesse: https://cryptomindia.app.n8n.cloud/workflow/7V9SZdSeSfZELZ3l

2. **Localize o nó "Switch Comando"** (está conectado ao Telegram Trigger, logo após ele)

3. **Duplo-clique** no nó "Switch Comando"

4. No painel lateral que abrir, clique na aba **"JSON"** (no topo)

5. Você verá um JSON grande. **Procure pela seção `"parameters"`** (deve estar no início)

6. **Selecione APENAS o conteúdo dentro de `"parameters": { ... }`** e substitua por:

```json
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "start",
              "leftValue": "={{ $json.message.text }}",
              "rightValue": "/start",
              "operator": {
                "type": "string",
                "operation": "startsWith"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "config",
              "leftValue": "={{ $json.message.text }}",
              "rightValue": "/config",
              "operator": {
                "type": "string",
                "operation": "startsWith"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "status",
              "leftValue": "={{ $json.message.text }}",
              "rightValue": "/status",
              "operator": {
                "type": "string",
                "operation": "startsWith"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "callback",
              "leftValue": "={{ $json.callback_query }}",
              "rightValue": "",
              "operator": {
                "type": "object",
                "operation": "exists"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      }
    ]
  }
}
```

7. Clique em **"Save"** (botão no canto inferior direito do painel)

8. Feche o painel clicando no **X** ou pressionando **ESC**

---

### Passo 2: Corrigir "Switch Callback"

1. **Localize o nó "Switch Callback"** (está após "Processar Callback")

2. **Duplo-clique** no nó "Switch Callback"

3. Clique na aba **"JSON"**

4. **Selecione APENAS o conteúdo dentro de `"parameters": { ... }`** e substitua por:

```json
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "moedas",
              "leftValue": "={{ $json.callback_query.data }}",
              "rightValue": "config_moedas",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "usdt",
              "leftValue": "={{ $json.callback_query.data }}",
              "rightValue": "config_usdt",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "set_moeda",
              "leftValue": "={{ $json.callback_query.data }}",
              "rightValue": "set_moeda_",
              "operator": {
                "type": "string",
                "operation": "startsWith"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "set_usdt",
              "leftValue": "={{ $json.callback_query.data }}",
              "rightValue": "set_usdt_",
              "operator": {
                "type": "string",
                "operation": "startsWith"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": false
      }
    ]
  }
}
```

5. Clique em **"Save"**

6. Feche o painel

---

### Passo 3: Salvar o Workflow

1. Clique no botão **"Save"** (no topo da página, ao lado de "Publish")

2. Aguarde a mensagem de confirmação

---

## ✅ PRONTO!

Agora teste enviando `/config` no bot e clicando em qualquer botão. Os callbacks devem funcionar perfeitamente.

---

## 📍 Localização Visual dos Nós

**Switch Comando:**
- Logo após o nó "Telegram Trigger"
- Tem 4 saídas numeradas (0, 1, 2, 3)
- Conecta a: Processar Start, Enviar Menu Config, Buscar Usuário Status, Processar Callback

**Switch Callback:**
- Está após o nó "Processar Callback"
- Tem 4 saídas
- Conecta a: Mostrar Menu Moedas, Mostrar Menu USDT, Buscar Usuário Callback (2x)

---

**Tempo estimado:** 2-3 minutos  
**Dificuldade:** Baixa (apenas copiar e colar)
