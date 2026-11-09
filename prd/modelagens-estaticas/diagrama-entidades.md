# Diagrama estático de classes das entidades

O diagrama delimita as entidades de negócio do modelo relacional atual. Os tipos são conceituais e não definem uma linguagem de programação.

```mermaid
classDiagram
    class Filme {
        +Integer id
        +String titulo
        +Integer duracaoMinutos
        +String genero
        +Text sinopse
        +URL cartazUrl
        +String faixaEtaria
        +Text elenco
        +Boolean nacional
    }

    class Sala {
        +Integer id
        +Integer quantidadeAssentos
        +Time horarioAbertura
        +Time horarioFechamento
        +Text especificacaoTecnica
    }

    class Sessao {
        +Integer id
        +DateTime inicio
        +Integer duracaoMinutos
        +Decimal valorIngresso
    }

    class Assento {
        +Integer id
        +String identificacao
    }

    class Cliente {
        +Integer id
        +String nome
        +Integer idade
        +String email
        +String logradouro
        +String numero
        +String complemento
        +String bairro
        +String cidade
        +String estado
        +String cep
    }

    class Reserva {
        +Integer id
        +Integer loteId
        +Decimal valorPago
        +DateTime criadaEm
    }

    class LoteReserva {
        +Integer id
        +String chaveIdempotencia
        +String hashSolicitacao
        +DateTime criadaEm
    }

    Filme "1" <-- "0..*" Sessao : apresenta
    Sala "1" <-- "0..*" Sessao : recebe
    Sala "1" <-- "0..*" Assento : contém
    Cliente "1" <-- "0..*" Reserva : realiza
    Sessao "1" <-- "0..*" Reserva : é reservada em
    Assento "1" <-- "0..*" Reserva : é selecionado em
    Cliente "1" <-- "0..*" LoteReserva : solicita
    Sessao "1" <-- "0..*" LoteReserva : agrupa
    LoteReserva "1" <-- "1..*" Reserva : contém
```

## Restrições representadas no modelo

- Cada sessão referencia um filme e uma sala.
- Cada assento pertence a uma sala; sua identificação é única dentro da sala.
- Cada reserva referencia um cliente, uma sessão e um assento. A sala vinculada à sessão deve ser a mesma sala do assento.
- Um cliente pode ter várias reservas; o e-mail do cliente é único.
- Um assento pode aparecer em várias reservas ao longo do tempo, mas não mais de uma vez para a mesma sessão.
- Cada reserva representa um assento reservado; a seleção de vários assentos resulta em uma reserva por assento.

As cardinalidades descrevem os relacionamentos persistidos, não garantem sozinhas regras temporais ou de concorrência. A representação de contas e credenciais do administrador e do gestor ainda não foi definida no modelo de dados.
