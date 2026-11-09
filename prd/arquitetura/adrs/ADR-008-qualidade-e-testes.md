# ADR-008: Verificação contínua e contratos testáveis

- **Estado:** Parcialmente implementado
- **Data:** 2026-11-09
- **RNFs:** RNF01 e RNF18–RNF20

## Contexto

Os requisitos demandam aceitação rastreável, consistência entre frontend e persistência, cobertura de domínio e prevenção de regressões em mudanças entre componentes.

## Decisão

Usar pytest com testes da aplicação Flask/Jinja e dos serviços de reserva. A suíte cobre as jornadas atuais de cadastro e programação, autorização, e-mail único, seleção/revisão/confirmação, conflitos de horário, unicidade de assentos, atomicidade e repetição idempotente. Cobertura percentual, testes reais de navegador, testes de contrato formais, pipeline e carga de 10.000 usuários ainda não estão configurados.

## Consequências

- Testes exercitam responsabilidades e contratos sem depender de um fornecedor específico.
- A cobertura percentual é indicador complementar, não substitui testes de cenários e invariantes.
- Dados de teste e ambiente de automação precisam ser controlados para resultados repetíveis.
- A suíte deve crescer em conjunto com os RF ainda não implementados e obter cobertura medida para satisfazer os RNFs.
- A rastreabilidade entre RF, RNFs, testes e resultados deve ser mantida na documentação ou ferramenta escolhida.
