# Cenários BDD

Os cenários estão escritos em Gherkin em português e executados com Behave.
Eles cobrem todos os cenários funcionais já presentes na suíte pytest, incluindo
autorização, CSRF, cadastro, disponibilidade, conflito de horários, atomicidade
e idempotência da reserva.

Na raiz do repositório, instale as dependências de desenvolvimento e execute:

```powershell
python -m pip install -r requirements-dev.txt
python -m behave
```

Se estiver usando o ambiente virtual deste repositório no Windows, ative-o antes:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux, use o caminho de ativação correspondente ao clone local:

```bash
source .venv/bin/activate
```
