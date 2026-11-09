# CineSenac

Sistema de gestão de sessões de cinema. O protótipo executável usa Python, Flask e templates Jinja, com SQLite para desenvolvimento e testes.

## Personas

- [Administrador do sistema](prd/persona/administrador-do-sistema.md)
- [Gestor](prd/persona/gestor.md)
- [Cliente](prd/persona/cliente.md)

## Modelagem de dados

- [Diagrama relacional (DBML)](prd/modelagem-dados.dbml)
- [Modelagens estáticas](prd/modelagens-estaticas/README.md)
- [Modelagens dinâmicas](prd/modelagens-dinamicas/README.md)
- [Arquitetura e decisões arquiteturais (ADRs)](prd/arquitetura/README.md)

## Requisitos funcionais

- [Requisitos funcionais](prd/requisitos-funcionais.md)
- [Requisitos não funcionais](prd/requisitos-nao-funcionais.md)

## Fluxos da aplicação

- [Diagramas de sequência UML por requisito funcional](prd/modelagens-dinamicas/diagramas-sequencia.md)

## Tutorial

- [Tutorial de uso por persona](prd/tutorial.md)

## Desenvolvimento

Requer Python 3.11 ou superior. No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest
python -m behave
```

Os cenários BDD estão em [`features/`](features/). Para gerar os relatórios
combinados de cobertura dos testes pytest e BDD:

```powershell
python -m coverage run -m pytest
python -m coverage run --append -m behave
python -m coverage report --show-missing
python -m coverage html
```

O relatório medido e versionado está em
[`reports/coverage-report.md`](reports/coverage-report.md); o CI publica também
os formatos HTML e XML como artefatos da execução.

O workflow de CI gera os relatórios Markdown, HTML e XML como artefatos e valida
a imagem Flask com Testcontainers. Para executar esse teste localmente, construa
a imagem `cinesenac:ci` usando o `Dockerfile` e defina
`RUN_CONTAINER_TESTS=1` antes de executar `python -m pytest tests/test_container.py`.

Configure uma chave secreta local para assinar as sessões:

```powershell
$env:CINESENAC_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Crie uma conta de administrador ou gestor e inicie a aplicação:

```powershell
python -m flask --app "cine_senac:create_app()" create-account
python -m flask --app "cine_senac:create_app()" run --debug
```

O comando de criação solicita usuário, perfil e senha. Acesse `http://127.0.0.1:5000`. O banco SQLite local é criado em `instance/cine-senac.sqlite`; `CINESENAC_DATABASE` permite definir outro caminho. Em produção, configure `CINESENAC_SECRET_KEY` como segredo forte e `CINESENAC_COOKIE_SECURE=true` somente quando o acesso HTTPS estiver configurado.

Esta é uma espinha dorsal funcional, não uma implantação pronta para produção nem uma validação da meta de 10.000 usuários simultâneos. O SQLite é apenas o adaptador local/teste; a integração com PostgreSQL, a infraestrutura de produção e os testes de carga continuam pendentes.
