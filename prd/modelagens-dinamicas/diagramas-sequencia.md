# Diagramas dinâmicos — sequências por requisito funcional

Os diagramas são modelos lógicos do comportamento previsto e não indicam tecnologias de implementação. Os participantes de interface, aplicação, domínio e persistência representam responsabilidades. Cada seção liga o fluxo aos RNFs aplicáveis; consulte a [matriz resumida](README.md) e os [requisitos não funcionais](../requisitos-nao-funcionais.md) para os critérios completos.

## RF01 — Autenticar administrador e liberar acesso aos fluxos

**Persona:** Administrador do sistema. **RNFs:** RNF01, RNF06, RNF08–RNF09, RNF14–RNF17.

```mermaid
sequenceDiagram
    actor Admin as Administrador
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant Identidade as Serviço de identidade
    Admin->>UI: Informa credenciais
    UI->>Acesso: Solicita autenticação
    Acesso->>Identidade: Verifica credenciais e perfil
    alt Credenciais válidas e perfil administrador
        Identidade-->>Acesso: Identidade autenticada
        Acesso-->>UI: Autorizar fluxos administrativos
        UI-->>Admin: Exibe painel de administração
    else Credenciais inválidas ou perfil sem acesso
        Identidade-->>Acesso: Autenticação ou autorização negada
        Acesso-->>UI: Recusar acesso e informar erro seguro
        UI-->>Admin: Exibe mensagem de acesso negado
    end
```

## RF02 — Disponibilizar gestão de salas, filmes e sessões

**Persona:** Gestor. **RNFs:** RNF01, RNF05–RNF06, RNF08, RNF10 e RNF15.

```mermaid
sequenceDiagram
    actor Gestor
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant App as Serviço de aplicação
    Gestor->>UI: Acessa a área de gestão
    UI->>Acesso: Solicita acesso ao perfil gestor
    Acesso->>Acesso: Verifica identidade e permissões
    alt Perfil autorizado
        Acesso-->>UI: Permitir fluxos de gestão
        UI->>App: Solicita opções de salas, filmes e sessões
        App-->>UI: Retorna fluxos permitidos
        UI-->>Gestor: Exibe opções de gestão
    else Perfil não autorizado
        Acesso-->>UI: Negar acesso
        UI-->>Gestor: Exibe mensagem de acesso negado
    end
```

## RF03 — Apresentar fluxos permitidos ao perfil

**Personas:** Administrador do sistema, Gestor e Cliente. **RNFs:** RNF01, RNF03, RNF08–RNF09 e RNF15.

```mermaid
sequenceDiagram
    actor Pessoa as Pessoa autenticada
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant App as Serviço de aplicação
    Pessoa->>UI: Abre o painel
    UI->>Acesso: Solicita permissões do perfil
    Acesso->>App: Consulta fluxos permitidos
    App-->>Acesso: Retorna permissões
    Acesso-->>UI: Retorna opções autorizadas
    UI-->>Pessoa: Exibe navegação correspondente ao perfil
```

## RF04 — Cadastrar sala

**Persona:** Gestor. **RNFs:** RNF01–RNF02, RNF04, RNF10, RNF13 e RNF15.

```mermaid
sequenceDiagram
    actor Gestor
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant App as Serviço de aplicação
    participant Dominio as Domínio
    participant Repo as Repositório de salas
    participant Dados as Persistência
    Gestor->>UI: Informa assentos, funcionamento e especificações
    UI->>App: Envia dados da sala
    App->>Acesso: Validar autorização do gestor no servidor
    alt Operação autorizada
        Acesso-->>App: Permissão concedida
        App->>Dominio: Validar dados da sala
        alt Dados válidos
            Dominio->>Repo: Solicita criação da sala
            Repo->>Dados: Persistir sala
            Dados-->>Repo: Sala criada
            Repo-->>Dominio: Retorna sala criada
            Dominio-->>App: Resultado de sucesso
            App-->>UI: Retorna confirmação
            UI-->>Gestor: Exibe sala cadastrada
        else Dados inválidos
            Dominio-->>App: Retorna erros de validação
            App-->>UI: Retorna erros sem confirmar sucesso
            UI-->>Gestor: Exibe orientação para correção
        end
    else Operação não autorizada
        Acesso-->>App: Permissão negada
        App-->>UI: Recusa operação
        UI-->>Gestor: Exibe mensagem de acesso negado
    end
```

## RF05 — Cadastrar filme

**Persona:** Gestor. **RNFs:** RNF01–RNF02, RNF04, RNF10, RNF13 e RNF15.

```mermaid
sequenceDiagram
    actor Gestor
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant App as Serviço de aplicação
    participant Dominio as Domínio
    participant Repo as Repositório de filmes
    participant Dados as Persistência
    Gestor->>UI: Informa dados, cartaz e indicação nacional
    UI->>App: Envia dados do filme
    App->>Acesso: Validar autorização do gestor no servidor
    alt Operação autorizada
        Acesso-->>App: Permissão concedida
        App->>Dominio: Validar dados do filme
        alt Dados válidos
            Dominio->>Repo: Solicita criação do filme
            Repo->>Dados: Persistir filme
            Dados-->>Repo: Filme criado
            Repo-->>Dominio: Retorna filme criado
            Dominio-->>App: Resultado de sucesso
            App-->>UI: Retorna confirmação
            UI-->>Gestor: Exibe filme cadastrado
        else Dados inválidos
            Dominio-->>App: Retorna erros de validação
            App-->>UI: Retorna erros sem confirmar sucesso
            UI-->>Gestor: Exibe orientação para correção
        end
    else Operação não autorizada
        Acesso-->>App: Permissão negada
        App-->>UI: Recusa operação
        UI-->>Gestor: Exibe mensagem de acesso negado
    end
```

## RF06 — Cadastrar sessão

**Persona:** Gestor. **RNFs:** RNF01–RNF02, RNF04, RNF10, RNF13 e RNF15.

```mermaid
sequenceDiagram
    actor Gestor
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant App as Serviço de aplicação
    participant Dominio as Domínio
    participant Repo as Repositórios de sessão, filme e sala
    participant Dados as Persistência
    Gestor->>UI: Seleciona filme e sala e informa horário, duração e valor
    UI->>App: Envia dados da sessão
    App->>Acesso: Validar autorização do gestor no servidor
    alt Operação autorizada
        Acesso-->>App: Permissão concedida
        App->>Dominio: Validar dados da sessão
        Dominio->>Repo: Consultar filme e sala
        Repo->>Dados: Buscar referências
        Dados-->>Repo: Retornar filme e sala
        Repo-->>Dominio: Disponibilizar referências
        alt Referências existentes e dados válidos
            Dominio->>Repo: Solicita criação da sessão
            Repo->>Dados: Persistir sessão
            Dados-->>Repo: Sessão criada
            Repo-->>Dominio: Retorna sessão criada
            Dominio-->>App: Resultado de sucesso
            App-->>UI: Retorna confirmação
            UI-->>Gestor: Exibe sessão cadastrada
        else Referência ausente ou dados inválidos
            Dominio-->>App: Retorna erro sem persistir sessão
            App-->>UI: Informa dados que devem ser corrigidos
            UI-->>Gestor: Exibe mensagem de erro
        end
    else Operação não autorizada
        Acesso-->>App: Permissão negada
        App-->>UI: Recusa operação
        UI-->>Gestor: Exibe mensagem de acesso negado
    end
```

## RF07 — Consultar programação e identificar sessão nacional diária

**Persona:** Gestor. **RNFs:** RNF01–RNF03, RNF10 e RNF13.

```mermaid
sequenceDiagram
    actor Gestor
    participant UI as Frontend
    participant App as Serviço de programação
    participant Repo as Repositório de sessões
    participant Dados as Persistência
    Gestor->>UI: Seleciona o dia da programação
    UI->>App: Solicita programação diária
    App->>Repo: Consultar sessões, salas e nacionalidade dos filmes
    Repo->>Dados: Buscar dados do dia
    Dados-->>Repo: Retornar sessões e filmes
    Repo-->>App: Retornar programação
    App->>App: Verificar se há sessão de filme nacional
    App-->>UI: Retornar programação e resultado da verificação
    UI-->>Gestor: Exibir sessões e situação da regra diária
```

## RF08 — Consultar dados cadastrados

**Personas:** Administrador do sistema e Gestor. **RNFs:** RNF01–RNF03, RNF06, RNF09 e RNF15.

```mermaid
sequenceDiagram
    actor Pessoa as Administrador ou Gestor
    participant UI as Frontend
    participant Acesso as Acesso e autorização
    participant App as Serviço de consulta
    participant Repo as Repositórios de salas, filmes e sessões
    participant Dados as Persistência
    Pessoa->>UI: Seleciona o tipo de cadastro para consultar
    UI->>Acesso: Solicita autorização
    Acesso-->>UI: Retorna decisão de acesso
    alt Consulta autorizada
        UI->>App: Solicita registros do tipo selecionado
        App->>Acesso: Validar autorização no servidor
        alt Operação autorizada
            Acesso-->>App: Permissão concedida
            App->>Repo: Consultar registros
            Repo->>Dados: Buscar registros
            Dados-->>Repo: Retornar registros
            Repo-->>App: Retornar resultado
            App-->>UI: Disponibilizar registros
            UI-->>Pessoa: Exibir dados cadastrados
        else Operação não autorizada
            Acesso-->>App: Permissão negada
            App-->>UI: Recusar consulta
            UI-->>Pessoa: Exibir mensagem de acesso negado
        end
    else Consulta não autorizada
        UI-->>Pessoa: Exibir mensagem de acesso negado
    end
```

## RF09 — Cadastrar cliente com endereço

**Persona:** Cliente. **RNFs:** RNF01–RNF02, RNF04, RNF10, RNF13–RNF14 e RNF16–RNF17.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de clientes
    participant Dominio as Domínio
    participant Repo as Repositório de clientes
    participant Dados as Persistência
    Cliente->>UI: Informa nome, idade, e-mail e endereço
    UI->>App: Envia dados cadastrais
    App->>Dominio: Validar dados
    Dominio->>Repo: Verificar e-mail existente
    Repo->>Dados: Consultar e-mail
    Dados-->>Repo: Retornar resultado da consulta
    Repo-->>Dominio: Informar disponibilidade do e-mail
    alt Dados válidos e e-mail disponível
        Dominio->>Repo: Solicita criação do cliente
        Repo->>Dados: Persistir cliente e endereço
        Dados-->>Repo: Cliente criado
        Repo-->>Dominio: Retornar cliente
        Dominio-->>App: Confirmar cadastro
        App-->>UI: Retornar confirmação
        UI-->>Cliente: Exibir cadastro concluído
    else E-mail já cadastrado ou dados inválidos
        Dominio-->>App: Retornar erro
        App-->>UI: Informar campo que precisa de correção
        UI-->>Cliente: Exibir erro sem expor dados privados
    end
```

## RF10 — Exigir e-mail único

**Persona:** Cliente. **RNFs:** RNF01, RNF04, RNF10, RNF14 e RNF17.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de clientes
    participant Repo as Repositório de clientes
    participant Dados as Persistência
    Cliente->>UI: Envia e-mail no cadastro
    UI->>App: Solicita validação de unicidade
    App->>Repo: Consultar e-mail
    Repo->>Dados: Buscar cliente por e-mail
    Dados-->>Repo: Retornar correspondência ou ausência
    Repo-->>App: Informar disponibilidade
    alt E-mail ainda não cadastrado
        App-->>UI: Permitir prosseguir com cadastro
        UI-->>Cliente: Solicitar os demais dados
    else E-mail já cadastrado
        App-->>UI: Recusar duplicidade
        UI-->>Cliente: Informar que deve usar outro e-mail para prosseguir
    end
```

## RF11 — Consultar filmes e sessões disponíveis

**Persona:** Cliente. **RNFs:** RNF01–RNF03, RNF05–RNF07, RNF09 e RNF14.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de catálogo
    participant Repo as Repositórios de filmes e sessões
    participant Dados as Persistência
    Cliente->>UI: Abre catálogo e informa filtros opcionais
    UI->>App: Solicita filmes e sessões disponíveis
    App->>Repo: Consultar filmes e programação
    Repo->>Dados: Buscar filmes e sessões futuras
    Dados-->>Repo: Retornar resultados
    Repo-->>App: Disponibilizar catálogo
    App-->>UI: Retornar dados para apresentação
    UI-->>Cliente: Exibir filmes, detalhes e sessões
    Cliente->>UI: Seleciona filme ou sessão
    UI-->>Cliente: Exibir detalhes e horário selecionado
```

## RF12 — Selecionar assentos disponíveis

**Persona:** Cliente. **RNFs:** RNF01, RNF03, RNF07, RNF09 e RNF11.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de disponibilidade
    participant Repo as Repositórios de sessões, assentos e reservas
    participant Dados as Persistência
    Cliente->>UI: Escolhe uma sessão
    UI->>App: Solicita assentos disponíveis
    App->>Repo: Consultar assentos e reservas da sessão
    Repo->>Dados: Buscar assentos e reservas
    Dados-->>Repo: Retornar assentos e ocupação
    Repo-->>App: Calcular disponibilidade
    App-->>UI: Retornar mapa de assentos
    UI-->>Cliente: Exibir assentos disponíveis
    Cliente->>UI: Seleciona um ou mais assentos
    UI->>App: Validar seleção
    App-->>UI: Retornar resumo da seleção
    UI-->>Cliente: Exibir assentos escolhidos
```

## RF13 — Impedir reserva duplicada do assento na sessão

**Persona:** Cliente. **RNFs:** RNF01, RNF04, RNF11–RNF12 e RNF17.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de reservas
    participant Dominio as Domínio
    participant Repo as Repositório de reservas
    participant Dados as Persistência
    Cliente->>UI: Solicita reserva de assento para a sessão
    UI->>App: Envia sessão e assento selecionados
    App->>Dominio: Validar disponibilidade atual
    Dominio->>Repo: Criar reserva de forma atômica
    Repo->>Dados: Inserir reserva com unicidade por sessão e assento
    alt Assento ainda disponível
        Dados-->>Repo: Reserva persistida
        Repo-->>Dominio: Confirmar reserva do assento
        Dominio-->>App: Reserva criada
        App-->>UI: Retornar sucesso
        UI-->>Cliente: Exibir assento reservado
    else Assento já reservado
        Dados-->>Repo: Rejeitar duplicidade
        Repo-->>Dominio: Informar assento indisponível
        Dominio-->>App: Recusar reserva
        App-->>UI: Retornar conflito de disponibilidade
        UI-->>Cliente: Solicitar outro assento
    end
```

## RF14 — Impedir reserva de sessões com horários conflitantes

**Persona:** Cliente. **RNFs:** RNF01, RNF04, RNF10–RNF12.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de reservas
    participant Dominio as Domínio
    participant Repo as Repositórios de reservas e sessões
    participant Dados as Persistência
    Cliente->>UI: Solicita confirmação de sessão e assentos
    UI->>App: Envia cliente, sessão e assentos escolhidos
    App->>Dominio: Validar conflito de horário
    Dominio->>Repo: Consultar reservas e intervalos das sessões do cliente
    Repo->>Dados: Buscar reservas existentes e sessão selecionada
    Dados-->>Repo: Retornar intervalos
    Repo-->>Dominio: Disponibilizar intervalos para comparação
    alt Existe conflito de horário
        Dominio-->>App: Recusar confirmação
        App-->>UI: Informar conflito e manter seleção editável
        UI-->>Cliente: Solicitar outra sessão
    else Não existe conflito
        Dominio-->>App: Permitir continuidade da reserva
        App-->>UI: Prosseguir para revisão
        UI-->>Cliente: Exibir resumo para confirmação
    end
```

## RF15 — Revisar sessão, assentos e dados antes da confirmação

**Persona:** Cliente. **RNFs:** RNF01–RNF02, RNF05, RNF09–RNF10, RNF14 e RNF16.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de reservas
    participant Repo as Repositórios de sessões, assentos e clientes
    participant Dados as Persistência
    Cliente->>UI: Solicita revisão da reserva
    UI->>App: Solicita resumo da seleção e do cadastro
    App->>Repo: Consultar sessão, assentos e dados do cliente
    Repo->>Dados: Buscar dados necessários para o resumo
    Dados-->>Repo: Retornar dados
    Repo-->>App: Disponibilizar resumo
    App-->>UI: Retornar resumo sem dados sensíveis desnecessários
    UI-->>Cliente: Exibir filme, sessão, assentos e dados cadastrais
    alt Cliente aprova
        Cliente->>UI: Aprova revisão e prossegue
        UI->>App: Solicita validações finais de horário e disponibilidade
        App-->>UI: Retorna resultado das validações
        UI-->>Cliente: Prosseguir para confirmação final
    else Cliente solicita correção
        Cliente->>UI: Altera dados, sessão ou assentos
        UI-->>Cliente: Atualiza resumo para nova revisão
    end
```

## RF16 — Registrar reserva e apresentar confirmação

**Persona:** Cliente. **RNFs:** RNF01–RNF02, RNF04, RNF11–RNF14 e RNF16.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Frontend
    participant App as Serviço de reservas
    participant Dominio as Domínio
    participant Repo as Repositório de reservas
    participant Dados as Persistência
    Cliente->>UI: Confirma a reserva revisada
    UI->>App: Envia solicitação de confirmação
    App->>Dominio: Validar sessão, conflito e assentos
    Dominio->>Repo: Registrar uma reserva por assento
    Repo->>Dados: Persistir reservas de forma consistente
    alt Todas as reservas persistidas
        Dados-->>Repo: Retornar identificadores das reservas
        Repo-->>Dominio: Confirmar operação concluída
        Dominio-->>App: Retornar reservas confirmadas
        App-->>UI: Retornar confirmação consultável
        UI-->>Cliente: Exibir confirmação da reserva
    else Conflito ou falha de persistência
        Dados-->>Repo: Retornar conflito ou falha
        Repo-->>Dominio: Informar que a operação não foi concluída
        Dominio-->>App: Não confirmar a reserva
        App-->>UI: Retornar erro recuperável
        UI-->>Cliente: Informar o resultado sem exibir falso sucesso
    end
```
