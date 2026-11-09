# ADR-001: Modularidade e separação por responsabilidades

- **Estado:** Parcialmente implementado
- **Data:** 2026-11-09
- **RNFs:** RNF01, RNF02, RNF18, RNF19 e RNF20

## Contexto

O sistema combina interface web, fluxos para três personas, regras de programação e reserva, e persistência. Mudanças nesses pontos não devem obrigar a reescrever partes sem relação nem acoplar o domínio a bibliotecas ou armazenamento.

## Decisão

Organizar a solução em módulos lógicos de frontend (`templates` e `static`), rotas/casos de uso (`web.py`), regras de domínio (`services.py`) e acesso SQLite (`db.py`). A implantação física permanece em um único processo Flask. O módulo de serviços ainda acessa diretamente a conexão SQLite; a extração de interfaces de repositório e de um adaptador PostgreSQL está pendente.

## Consequências

- Mudanças e testes podem ser delimitados por responsabilidade.
- Contratos entre módulos exigem governança e testes de integração.
- Uma separação lógica não implica microsserviços nem implantação distribuída.
- O protótipo já separa responsabilidades em módulos, mas ainda não satisfaz o limite de dependência do domínio sobre contratos de persistência.
- O desenho deve ser revisto se os limites entre módulos criarem complexidade sem benefício comprovável.
