# Testes e rastreabilidade

Execute `python -m pytest`. Os testes usam uma base SQLite temporária por execução e não dependem de credenciais ou de serviços externos.

| Requisito | Cobertura automatizada |
|---|---|
| RF01–RF03 | `test_manager_routes_require_server_side_role_authorization`; navegação e controle de acesso a partir do servidor |
| RF04–RF07 | `test_manager_can_create_room_film_and_national_session`; cadastro e consulta da programação nacional |
| RF08 | `test_manager_can_consult_rooms_films_and_screenings` |
| RF09–RF10 | `test_customer_email_is_unique` |
| RF11 | `test_home_page_renders_catalog_with_jinja` e jornadas de reserva |
| RF12, RF15–RF16 | `test_customer_can_review_and_confirm_multiple_seats` |
| RF13 | `test_customer_cannot_reserve_same_seat_twice` |
| RF14 | `test_customer_cannot_confirm_conflicting_sessions` |
| RNF12–RNF13 | `test_multi_seat_confirmation_is_atomic_and_idempotent` |
| RNF15, RNF17 | `test_manager_routes_require_server_side_role_authorization`, `test_manager_cannot_read_customer_personal_data` e `test_posts_without_csrf_token_are_rejected` |

Esta suíte cobre a espinha dorsal atual, não toda a validação de cada RNF. Ainda faltam testes de navegador real, conformidade WCAG automatizada, cobertura medida de 80%, matriz de navegadores e teste de carga com 10.000 usuários.
