# ADR-004: Persistência relacional atrás de contratos

- **Estado:** Aceito para desenvolvimento e testes; produção pendente
- **Data:** 2026-11-09
- **RNFs:** RNF02, RNF12, RNF13 e RNF20

## Contexto

O modelo de dados é relacional e contém referências entre sessões, filmes, salas, assentos, clientes e reservas. Integridade referencial e operações consistentes são necessárias, mas nenhuma tecnologia de armazenamento foi selecionada.

## Decisão

Manter o modelo relacional descrito em DBML. A espinha dorsal usa SQLite com restrições e transações para execução local e testes, com esquema inicial criado na inicialização. A integração de produção deve usar PostgreSQL, indicado pelo DBML, mas ainda não existe adaptador PostgreSQL nem estratégia de migração.

## Consequências

- O adaptador local suporta transações, restrições únicas e integridade referencial, mas não é a base validada para produção.
- Contratos reduzem acoplamento, mas não eliminam a necessidade de validar semântica específica do armazenamento escolhido.
- Um adaptador e migrações PostgreSQL deverão preservar dados e ser verificados antes de produção.
- Consistência temporal de horários precisa de validações além de chaves estrangeiras.
