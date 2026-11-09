# ADR-003: Autorização no servidor e proteção de dados

- **Estado:** Parcialmente implementado no protótipo
- **Data:** 2026-11-09
- **RNFs:** RNF14–RNF17

## Contexto

O administrador tem acesso amplo, o gestor opera cadastros e o cliente consulta e reserva. Esconder opções no frontend não impede chamadas diretas aos serviços; dados cadastrais e credenciais também requerem proteção.

## Decisão

Aplicar autorização no servidor para rotas de gestão. No protótipo, contas locais de administrador e gestor são criadas por comando administrativo, senhas são armazenadas com hash Werkzeug e a sessão Flask é assinada. Formulários POST verificam token CSRF. Cookie seguro pode ser habilitado por configuração quando servido por HTTPS. Não há autenticação persistente de clientes nem provedor de identidade externo; TLS, gestão de segredos e revisão de segurança para produção continuam pendentes.

## Consequências

- Cada rota protegida valida o perfil no servidor; administrador tem acesso às rotas de gestão e gestor não pode consultar dados pessoais de clientes.
- O frontend pode adaptar navegação, mas nunca é a única barreira de autorização.
- O comando `create-account` permite bootstrap local; fluxo de recuperação, expiração de sessão, MFA e provedor externo ainda precisam ser definidos para produção.
- Testes devem cobrir chamadas não autorizadas, exposição de dados e falhas comuns de segurança web.
