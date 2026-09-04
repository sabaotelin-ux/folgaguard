# Licença MIT

Copyright (c) 2026 Augusto Cezar de Almeida

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modification, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

# Aegis Gate V2.2

Gateway de IA modular em Open-Core construído com FastAPI, SQLite, controle de taxa, filtros de segurança (Guardrails) e automação de licenças via webhook.

## Estrutura de Endpoints
- `GET /` - Interface visual de suporte Open-Core (Qwen).
- `POST /support/qwen` - Endpoint público e gratuito com Rate Limiting.
- `POST /api/v1/pro/advanced-audit` - Rota comercial exclusiva validada por chave de licença (`x-license-key`).
- `GET /api/v1/admin/metrics` - Observabilidade e métricas de uso protegidas por chave mestre.
- `POST /api/v1/webhook/payment` - Automação de provisionamento pós-pagamento.
