# Tutorial de uso

Este tutorial descreve o protótipo web executável do CineSenac. A interface usa formulários HTML renderizados por Jinja. A versão atual é uma espinha dorsal: não representa uma implantação pronta para produção.

Para executar localmente, siga as instruções de desenvolvimento no [README](../README.md). O administrador e o gestor precisam de contas criadas pela linha de comando. O cadastro de cliente fica associado à sessão atual do navegador; ainda não há autenticação persistente nem recuperação de conta de cliente.

## Administrador do sistema

1. Acesse a aplicação e entre com a conta de perfil `admin`.
2. No painel, escolha um fluxo. O administrador pode cadastrar e consultar salas, filmes e sessões, consultar a programação e consultar clientes.
3. Use a navegação para voltar aos filmes, acessar outro fluxo ou sair.

## Gestor

### Cadastrar uma sala

1. Entre com a conta de perfil `manager` e acesse a área de gestão de salas.
2. Informe a quantidade de assentos, os horários de funcionamento e as especificações técnicas.
3. Revise os dados e conclua o cadastro.

### Cadastrar um filme

1. Na área de gestão, escolha cadastrar filme.
2. Informe título, duração, gênero, sinopse, URL do cartaz, faixa etária e elenco.
3. Indique se o filme é uma produção nacional.
4. Revise os dados e conclua o cadastro.

### Cadastrar sessões e conferir a programação

1. Na área de gestão, escolha cadastrar sessão e selecione o filme e a sala cadastrados.
2. Informe o horário, a duração da sessão e o valor do ingresso.
3. Revise os dados e conclua o cadastro da sessão.
4. Consulte a programação por dia e confira se há ao menos uma sessão de filme nacional, conforme a legislação vigente.
5. Use as opções de consulta para conferir salas, filmes e sessões cadastrados.

## Cliente

### Escolher filme, sessão e assentos

1. Se ainda não tiver cadastro nesta sessão do navegador, informe nome, idade, e-mail e endereço no cadastro de cliente.
2. Consulte os filmes e as sessões disponíveis na página inicial.
3. Escolha uma sessão e consulte os assentos disponíveis.
4. Selecione um ou mais assentos e revise a sessão, o total e os dados cadastrais.

### Cadastrar-se e confirmar a reserva

1. Na etapa de revisão, confira filme, sessão, assentos e total.
2. Confirme a reserva.
3. Se a sessão conflitar com outra reserva ou algum assento deixar de estar disponível, volte ao catálogo e escolha outra opção.
4. Após a confirmação, consulte a página com o número da reserva.
