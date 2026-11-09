# ADR-007: Tratamento explícito de falhas e observabilidade

- **Estado:** Parcialmente implementado
- **Data:** 2026-11-09
- **RNFs:** RNF11 e RNF13

## Contexto

Falhas de rede ou persistência podem interromper cadastros e reservas. A aplicação não deve confundir falha com sucesso; ao mesmo tempo, o sistema precisa de informação suficiente para diagnosticar erros sem expor dados pessoais.

## Decisão

Representar resultados de validação e conflito explicitamente entre domínio, rotas e frontend. Só emitir confirmação após a transação concluir; retornar mensagens ao usuário sem detalhes internos. Falhas inesperadas são registradas pelo logger Flask sem incluir conteúdo de formulário deliberadamente. Identificadores de correlação, métricas e monitoramento operacional ainda não estão implementados.

## Consequências

- Cada operação crítica precisa definir falhas recuperáveis e resposta correspondente ao usuário.
- Logs e métricas devem ser revisados para evitar conteúdo sensível.
- Identificadores de correlação ajudam a relacionar falhas entre componentes.
- A camada web captura erros inesperados e evita confirmação falsa; ainda é necessário revisar logs e definir observabilidade de produção.
- Retentativas automáticas só podem ocorrer quando forem seguras, com idempotência para comandos de escrita.
