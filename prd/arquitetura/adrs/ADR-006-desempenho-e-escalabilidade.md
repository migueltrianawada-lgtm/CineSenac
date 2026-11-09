# ADR-006: Escala horizontal e cache seletivo

- **Estado:** Proposto
- **Data:** 2026-11-09
- **RNFs:** RNF03–RNF05 e RNF11

## Contexto

Os RNFs estabelecem testes controlados com 10.000 usuários simultâneos, limites de latência para consultas e operações e uma meta de sucesso. A implantação e o perfil real de carga ainda não foram definidos.

## Decisão

Projetar frontend e componentes de aplicação sem estado de sessão local obrigatório, de modo que possam ser replicados horizontalmente quando o ambiente escolhido oferecer esse recurso. Priorizar a medição de consultas e do caminho crítico de reserva. Cache pode ser aplicado a conteúdo de catálogo com estratégia explícita de expiração/invalidação; não usar cache como autoridade de disponibilidade ou para confirmar reservas. Validar com teste de carga antes de selecionar topologia ou ajustar capacidade.

## Consequências

- Escala horizontal depende de identidade e estado compartilhados fora da memória local de uma instância.
- Cache de catálogo pode reduzir latência, mas introduz eventual defasagem de conteúdo; sua política precisa ser definida e medida.
- A disponibilidade de assentos e a reserva continuam consultando fontes autoritativas e aplicando controles transacionais.
- Os 10.000 usuários são uma meta de validação, não garantia de capacidade antes dos testes em infraestrutura documentada.
- Produto de cache, hospedagem e capacidade instalada permanecem pendentes.
