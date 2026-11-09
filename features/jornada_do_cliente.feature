# language: pt
Funcionalidade: Cadastro e reserva de sessões
  Para assistir a um filme
  Como cliente
  Quero me cadastrar e reservar assentos disponíveis em uma sessão

  Cenário: E-mail do cliente deve ser único
    Quando cadastro um cliente com o e-mail "cliente@example.test"
    E encerro a sessão do cliente
    E tento cadastrar outro cliente com o e-mail "cliente@example.test"
    Então o cadastro duplicado deve ser rejeitado
    E os dados preenchidos devem continuar disponíveis no formulário

  Cenário: Cliente revisa e confirma mais de um assento
    Dado que existe uma sessão com três assentos disponíveis
    E que estou cadastrado como cliente
    Quando seleciono dois assentos da sessão
    Então a revisão deve exibir o cliente e a reserva
    Quando confirmo a reserva
    Então a reserva deve ser confirmada para dois assentos

  Cenário: Cliente não reserva assento já ocupado
    Dado que existe uma sessão com três assentos disponíveis
    E que um cliente já reservou um assento
    Quando outro cliente tenta reservar o mesmo assento
    Então a seleção deve informar que o assento não está disponível

  Cenário: Cliente não confirma sessões com horários conflitantes
    Dado que existem sessões às "2026-12-01T10:00" e "2026-12-01T10:30"
    E que estou cadastrado como cliente
    Quando confirmo uma reserva para a primeira sessão
    E tento confirmar uma reserva para a segunda sessão
    Então a segunda reserva deve ser rejeitada por conflito de horário

  Cenário: Confirmação de vários assentos é atômica e idempotente
    Dado que existe uma sessão preparada para teste de confirmação
    Quando confirmo um assento e repito a mesma solicitação com a mesma chave
    Então a repetição deve retornar a confirmação original
    Quando reutilizo a chave com uma solicitação diferente
    Então a solicitação deve ser rejeitada por conflito de chave
    Quando outro cliente tenta reservar o assento ocupado e um assento livre
    Então a confirmação deve falhar sem reservar parcialmente os assentos
