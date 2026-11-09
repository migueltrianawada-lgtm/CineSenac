# Requisitos não funcionais

Este documento define atributos de qualidade para a aplicação web completa, incluindo frontend e serviços integrados. Os requisitos não acrescentam funcionalidades aos [requisitos funcionais](requisitos-funcionais.md): definem como essas funcionalidades devem se comportar e ser avaliadas.

## Referencial e contexto de validação

A organização considera a área de qualidade de software do SWEBOK e usa as oito características do modelo de qualidade de produto da ISO/IEC 25010:2011: adequação funcional, eficiência de desempenho, compatibilidade, usabilidade, confiabilidade, segurança, manutenibilidade e portabilidade. A referência a oito características é do modelo ISO; o SWEBOK orienta a abordagem de qualidade, mas não define por si só essa lista como seus oito eixos.

Os critérios são metas iniciais verificáveis. A validação de carga deve ocorrer em ambiente controlado, com dados de teste, perfil de infraestrutura registrado e **10.000 usuários virtuais simultâneos** percorrendo as jornadas de cliente, gestor e administrador. O relatório deve registrar duração, distribuição das jornadas, configuração do ambiente, resultados e limitações; os critérios de desempenho abaixo são avaliados durante pelo menos 30 minutos de carga estável.

## 1. Adequação funcional

- **RNF01.** Para cada requisito funcional [RF01–RF16](requisitos-funcionais.md), deve existir ao menos um teste automatizado de aceitação que valide o resultado esperado na aplicação, incluindo a interação pelo frontend quando houver interface prevista. A rastreabilidade entre RF, teste e resultado deve ser mantida.
  - **Personas:** [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md) e [Cliente](persona/cliente.md).
- **RNF02.** A suíte de aceitação das jornadas completas deve verificar que as informações apresentadas no frontend correspondem aos dados persistidos e às respostas dos serviços, sem divergência nos cadastros, na programação e nas reservas.
  - **Rastreabilidade:** [RF04–RF16](requisitos-funcionais.md); [Gestor](persona/gestor.md) e [Cliente](persona/cliente.md); [Administrador do sistema](persona/administrador-do-sistema.md) ao consultar os fluxos.

## 2. Eficiência de desempenho

- **RNF03.** Com 10.000 usuários virtuais simultâneos e carga estável, pelo menos 95% das consultas de páginas, filmes, sessões e assentos devem responder em até 2 segundos, medidos da solicitação até a resposta completa do serviço.
  - **Rastreabilidade:** [RF03, RF07–RF08 e RF11–RF12](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF04.** Sob a mesma carga, pelo menos 95% das operações de cadastro e confirmação de reserva devem responder em até 3 segundos; a taxa de respostas de erro inesperadas deve permanecer abaixo de 0,5%.
  - **Rastreabilidade:** [RF01–RF06 e RF09–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF05.** Nas jornadas web representativas, o conteúdo principal de cada página deve ficar visível em até 3 segundos no percentil 95, medido no navegador em perfil de rede e dispositivo documentado no relatório de teste.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).

## 3. Compatibilidade

- **RNF06.** Os fluxos cobertos por RF01–RF16 devem funcionar nas duas versões estáveis mais recentes de Chrome, Edge, Firefox e Safari disponíveis no início de cada ciclo de validação.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF07.** A interface deve preservar conteúdo e ações essenciais em larguras de viewport a partir de 360 px, sem rolagem horizontal da página, sobreposição de controles ou perda de informação.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).

## 4. Usabilidade

- **RNF08.** Em testes moderados com participantes representativos das três personas, pelo menos 90% de cada grupo deve concluir sua jornada principal sem ajuda: acesso e consulta de fluxos para o administrador; cadastro e programação para o gestor; consulta e reserva para o cliente.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF09.** As páginas e interações da aplicação web devem atender ao nível AA da WCAG 2.2, incluindo operação por teclado, foco visível, nomes acessíveis para controles, mensagens de erro identificáveis e contraste suficiente.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF10.** Formulários e etapas de reserva devem apresentar rótulos, formatos esperados, erros e confirmações em português claro; uma mensagem de erro deve indicar o campo ou a ação que precisa de correção sem apagar dados não relacionados ao erro.
  - **Rastreabilidade:** [RF01–RF06 e RF09–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).

## 5. Confiabilidade

- **RNF11.** Durante o teste estável com 10.000 usuários virtuais simultâneos, o serviço deve manter pelo menos 99,5% de solicitações concluídas sem erro inesperado.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF12.** Mesmo sob solicitações simultâneas, nenhum assento pode resultar em reservas duplicadas para a mesma sessão, e toda reserva confirmada deve permanecer consultável após a confirmação.
  - **Rastreabilidade:** [RF12–RF16](requisitos-funcionais.md); [Cliente](persona/cliente.md).
- **RNF13.** Falhas de comunicação ou de persistência durante uma operação não devem apresentar confirmação de sucesso ao usuário quando a operação não tiver sido concluída.
  - **Rastreabilidade:** [RF04–RF06 e RF09–RF16](requisitos-funcionais.md); [Gestor](persona/gestor.md) e [Cliente](persona/cliente.md); [Administrador do sistema](persona/administrador-do-sistema.md) ao operar os fluxos.

## 6. Segurança

- **RNF14.** Todas as páginas e chamadas entre navegador e serviços devem usar HTTPS com TLS 1.2 ou superior; a aplicação não deve transmitir dados pessoais ou credenciais por conexões sem criptografia.
  - **Rastreabilidade:** [RF01, RF03, RF09–RF10 e RF15–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF15.** O servidor deve validar a autorização de cada operação, sem confiar apenas em controles de navegação ou verificações executadas no frontend.
  - **Rastreabilidade:** [RF01–RF10](requisitos-funcionais.md); [Administrador do sistema](persona/administrador-do-sistema.md) e [Gestor](persona/gestor.md).
- **RNF16.** Senhas, tokens de sessão e dados pessoais não devem ser gravados em logs, mensagens de erro ou armazenamento acessível indevidamente pelo frontend.
  - **Rastreabilidade:** [RF01 e RF09–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF17.** A aplicação deve proteger as entradas e sessões contra vulnerabilidades web comuns, incluindo injeção, cross-site scripting, cross-site request forgery e exposição de sessão, com verificações automatizadas e revisão antes da publicação.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).

## 7. Manutenibilidade

- **RNF18.** Toda alteração em uma jornada existente deve executar testes automatizados para os requisitos RF relacionados; a suíte deve identificar regressões sem depender de validação manual exclusiva pelo navegador.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF19.** A lógica de domínio coberta por testes automatizados deve manter cobertura mínima de 80%, medida por ferramenta de cobertura no pipeline de integração contínua; código gerado e arquivos de configuração podem ser excluídos, com exclusões documentadas.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF20.** Alterações nas interfaces entre frontend e serviços devem ser documentadas e verificadas por testes de contrato para evitar incompatibilidades entre versões dos componentes.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).

## 8. Portabilidade

- **RNF21.** O frontend deve ser utilizável em navegadores de desktop e dispositivos móveis que atendam ao RNF06, mantendo as jornadas descritas sem exigir uma plataforma ou sistema operacional específico.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade).
- **RNF22.** A aplicação deve poder ser implantada nos ambientes de desenvolvimento, teste e produção usando configuração externa, sem alterações no código-fonte específicas de cada ambiente.
  - **Rastreabilidade:** [RF01–RF16](requisitos-funcionais.md); [todas as personas](#matriz-de-rastreabilidade), como requisito operacional da aplicação.

## Matriz de rastreabilidade

| Eixo de qualidade | Requisitos | Requisitos funcionais relacionados | Personas |
|---|---|---|---|
| Adequação funcional | RNF01–RNF02 | [RF01–RF16](requisitos-funcionais.md) | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Eficiência de desempenho | RNF03–RNF05 | [RF01–RF16](requisitos-funcionais.md), com foco nos RF indicados em cada requisito | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Compatibilidade | RNF06–RNF07 | [RF01–RF16](requisitos-funcionais.md) | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Usabilidade | RNF08–RNF10 | [RF01–RF16](requisitos-funcionais.md), com foco nos RF indicados em cada requisito | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Confiabilidade | RNF11–RNF13 | [RF01–RF16](requisitos-funcionais.md), com foco nos RF indicados em cada requisito | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Segurança | RNF14–RNF17 | [RF01–RF16](requisitos-funcionais.md), com foco nos RF indicados em cada requisito | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Manutenibilidade | RNF18–RNF20 | [RF01–RF16](requisitos-funcionais.md) | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
| Portabilidade | RNF21–RNF22 | [RF01–RF16](requisitos-funcionais.md) | [Administrador do sistema](persona/administrador-do-sistema.md), [Gestor](persona/gestor.md), [Cliente](persona/cliente.md) |
