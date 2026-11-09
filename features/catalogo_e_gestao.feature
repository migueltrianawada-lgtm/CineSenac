# language: pt
Funcionalidade: Catálogo e gestão de sessões
  Para organizar a programação do cinema
  Como gestor ou administrador
  Quero cadastrar e consultar salas, filmes e sessões

  Cenário: Exibir a página inicial do catálogo
    Quando acesso a página inicial
    Então a resposta deve ser bem-sucedida
    E devo ver "CineSenac"
    E devo ver "Filmes"

  Cenário: Gestor cadastra sala, filme nacional e sessão
    Dado que entrei como gestor
    Quando cadastro uma sala, um filme nacional e uma sessão para "2026-12-01T10:00"
    Então os três cadastros devem ser confirmados
    E a programação de "2026-12-01" deve conter "Filme nacional"

  Cenário: Administrador acessa os fluxos de gestão
    Quando tento abrir o cadastro de salas sem autenticação
    Então sou redirecionado para entrar
    Quando entro como administrador
    Então posso abrir o cadastro de salas
    E posso consultar os cadastros de clientes

  Cenário: Gestor consulta salas, filmes e sessões cadastrados
    Dado que entrei como gestor
    E que cadastrei sala, filme nacional e sessão para "2026-12-01T10:00"
    Quando consulto os cadastros de salas, filmes e sessões
    Então cada cadastro deve exibir seus dados

  Cenário: Gestor não consulta dados pessoais de clientes
    Dado que entrei como gestor
    Quando tento consultar os cadastros de clientes
    Então o acesso é negado

  Cenário: Rejeitar formulário sem token CSRF
    Quando envio o formulário de entrada sem token CSRF
    Então a requisição é rejeitada com código 400
