# ADR-009: Configuração externa e ambientes reproduzíveis

- **Estado:** Parcialmente implementado
- **Data:** 2026-11-09
- **RNFs:** RNF22

## Contexto

O sistema precisa ser implantável em desenvolvimento, teste e produção sem modificar código para cada ambiente. Hospedagem e tecnologia de empacotamento ainda não foram definidas.

## Decisão

Manter caminho do banco, chave de sessão e configuração do cookie em variáveis de ambiente. O protótipo local usa arquivo SQLite em `instance/`. A aplicação recusa iniciar fora de testes/desenvolvimento quando não há chave secreta configurada. O processo e a plataforma de produção, gerenciamento de segredos, empacotamento e promoção de artefatos ainda não foram definidos.

## Consequências

- A configuração deve ser documentada e validada por ambiente.
- A chave secreta de produção deve ser forte, exclusiva e fornecida por mecanismo de segredo; `COOKIE_SECURE` deve ser habilitado atrás de HTTPS.
- Segredos não podem ser armazenados no repositório nem expostos no frontend.
- O processo de implantação precisa preservar rastreabilidade da versão e possibilitar reversão.
- A escolha do mecanismo de distribuição e implantação será uma decisão posterior, baseada nas restrições operacionais.
