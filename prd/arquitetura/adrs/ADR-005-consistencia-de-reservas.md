# ADR-005: Reserva transacional e idempotente

- **Estado:** Aceito para o protótipo
- **Data:** 2026-11-09
- **RNFs:** RNF11–RNF13

## Contexto

Dois clientes podem selecionar simultaneamente o mesmo assento. A disponibilidade exibida pode mudar antes da confirmação; um sucesso parcial ou falso compromete a reserva.

## Decisão

Revalidar disponibilidade e conflito de horário no servidor no momento da confirmação. Registrar a seleção múltipla numa transação SQLite: confirmar o conjunto inteiro ou nenhum item. Impor unicidade por sessão e assento no armazenamento e tratar colisões como conflito recuperável. Associar cada tentativa a uma chave idempotente e ao hash do conteúdo para que uma repetição não duplique reservas nem reutilize a chave com dados diferentes.

## Consequências

- O mapa de assentos do frontend é informativo; a verificação final é autoritativa no servidor.
- O armazenamento precisa garantir atomicidade e unicidade sob concorrência.
- A interface deve permitir nova seleção após conflito sem apresentar confirmação indevida.
- O protótipo persiste lotes de reserva e usa chave interna; formato público, retenção e limpeza dos lotes precisam ser definidos antes de expor uma API.
- Política de expiração ou bloqueio temporário de assentos não está decidida e não deve ser inferida desta ADR.
