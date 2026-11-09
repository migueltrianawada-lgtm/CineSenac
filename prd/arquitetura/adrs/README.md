# Índice de ADRs

ADRs (Architecture Decision Records) registram contexto, decisão e consequências das táticas arquiteturais. **Proposto** significa que a direção está documentada para validação; não afirma que foi implementada nem que tecnologias foram selecionadas.

| ADR | Tática | Estado |
|---|---|---|
| [ADR-001](ADR-001-modularidade-e-camadas.md) | Modularidade e separação por responsabilidades | Parcialmente implementado |
| [ADR-002](ADR-002-frontend-web.md) | Frontend responsivo, acessível e compatível | Aceito para o protótipo |
| [ADR-003](ADR-003-seguranca-e-autorizacao.md) | Autorização no servidor e proteção de dados | Parcialmente implementado |
| [ADR-004](ADR-004-persistencia-relacional.md) | Persistência relacional atrás de contratos | SQLite local/testes; produção pendente |
| [ADR-005](ADR-005-consistencia-de-reservas.md) | Reserva transacional e idempotente | Aceito para o protótipo |
| [ADR-006](ADR-006-desempenho-e-escalabilidade.md) | Escala horizontal e cache seletivo | Proposto |
| [ADR-007](ADR-007-falhas-e-observabilidade.md) | Tratamento explícito de falhas | Parcialmente implementado |
| [ADR-008](ADR-008-qualidade-e-testes.md) | Verificação contínua e contratos testáveis | Parcialmente implementado |
| [ADR-009](ADR-009-configuracao-e-implantacao.md) | Configuração externa e ambientes reproduzíveis | Parcialmente implementado |

## Relação com os RNFs

| Tática | RNFs cobertos |
|---|---|
| Modularidade | RNF01–RNF02, RNF18–RNF20 |
| Frontend web | RNF05–RNF10, RNF21 |
| Segurança e autorização | RNF14–RNF17 |
| Persistência relacional | RNF02, RNF12–RNF13, RNF20 |
| Consistência de reservas | RNF11–RNF13 |
| Desempenho e escalabilidade | RNF03–RNF05, RNF11 |
| Falhas e observabilidade | RNF11, RNF13 |
| Qualidade e testes | RNF01, RNF18–RNF20 |
| Configuração e implantação | RNF22 |
