# Requisitos funcionais

Este documento descreve somente as funcionalidades necessárias para atender aos objetivos e às jornadas das personas.

## Acesso e navegação

- **RF01.** O sistema deve permitir que o administrador se autentique e acesse todos os fluxos da aplicação.
- **RF02.** O sistema deve disponibilizar ao gestor os fluxos de cadastro e consulta de salas, filmes e sessões.
- **RF03.** O sistema deve apresentar a cada persona os fluxos disponíveis para seu perfil.

## Salas, filmes e sessões

- **RF04.** O sistema deve permitir cadastrar salas com quantidade de assentos, horários de funcionamento e especificações técnicas.
- **RF05.** O sistema deve permitir cadastrar filmes com título, duração, gênero, sinopse, URL do cartaz, faixa etária, elenco e indicação de produção nacional.
- **RF06.** O sistema deve permitir cadastrar sessões, associando um filme a uma sala e informando horário, duração e valor do ingresso.
- **RF07.** O sistema deve permitir consultar a programação por dia e identificar se há ao menos uma sessão de filme nacional em cada dia.
- **RF08.** O sistema deve permitir consultar os dados cadastrados de salas, filmes e sessões.

## Clientes e reservas

- **RF09.** O sistema deve permitir cadastrar clientes com nome, idade, e-mail e endereço.
- **RF10.** O sistema deve exigir um e-mail único para cada cliente.
- **RF11.** O sistema deve permitir consultar filmes e sessões disponíveis e visualizar os detalhes do filme e da sessão selecionados.
- **RF12.** O sistema deve permitir selecionar um ou mais assentos disponíveis para uma sessão.
- **RF13.** O sistema deve impedir que um mesmo assento seja reservado mais de uma vez para a mesma sessão.
- **RF14.** O sistema deve impedir que o cliente confirme reservas para sessões com horários conflitantes.
- **RF15.** Antes da confirmação, o sistema deve apresentar ao cliente a sessão, os assentos escolhidos e seus dados cadastrais para revisão.
- **RF16.** Após a confirmação, o sistema deve registrar a reserva e apresentar sua confirmação ao cliente.
