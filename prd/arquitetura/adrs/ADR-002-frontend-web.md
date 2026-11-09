# ADR-002: Frontend responsivo, acessível e compatível

- **Estado:** Aceito para o protótipo
- **Data:** 2026-11-09
- **RNFs:** RNF05–RNF10 e RNF21

## Contexto

Administrador, gestor e cliente usam jornadas distintas em frontend web, em dispositivos móveis e computadores. A interface precisa funcionar nos navegadores definidos e atender metas de acessibilidade e desempenho visual.

## Decisão

Construir o primeiro frontend com Flask e templates Jinja renderizados no servidor, HTML semântico e CSS responsivo. Tratar WCAG 2.2 nível AA, conteúdo em português claro, navegação por teclado e compatibilidade com as versões de navegadores definidas nos RNFs como critérios de aceite. Esta escolha atende ao pedido de implementação do protótipo; testes de conformidade e a estratégia de produção permanecem pendentes.

## Consequências

- O frontend precisa de testes nos navegadores, viewports e jornadas suportados.
- As regras críticas serão validadas no servidor mesmo quando também houver validação na interface.
- O orçamento de carregamento visual precisa ser medido em perfis de rede e dispositivo documentados.
- Componentes e estilos devem manter semântica e acessibilidade; não há ainda evidência de conformidade WCAG AA ou suporte validado a todos os navegadores.
