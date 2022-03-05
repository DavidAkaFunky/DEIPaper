# DEIPaper
Para uniformizar a gestão de publicações científicas no IST, os serviços de informática desenvolveram o sistema *ISTPaper*. As necessidades dos vários departamentos são diferentes, e por isso cada departamento terá uma aplicação sua que interage com o sistema *ISTPaper*.

Estando o DEI na vanguarda da implementação deste novo sistema, foram incubidos os bolseiros do DEI de implementar a primeira destas aplicações: **DEIPaper** (o seu exercício). No final, servirá de molde para customização pelos outros departamentos (sem promessas de suporte nosso).

Uma publicação é constituída por um Título, Autores, *Abstract* (resumo breve do conteúdo) e URL para o documento completo. É possível fazer uma submissão inicial de uma publicação sem este último campo. Algumas publicações poderão também ser acompanhadas de um pequeno logotipo, que ajuda a identificar rapidamente o projeto (ou área científica) em questão.

Por motivos de segurança, o sistema *ISTPaper* exige que cada aplicação (incluindo o DEIPaper) se autentique com um *token*, que impede de forma grosseira que os vários departamentos interfiram nas publicações dos restantes. *Endpoints* de consulta de dados não requerem autenticação.
Para este exercício deverá usar o seu IST ID (p.ex. `ist189409`).

Adicionalmente, existe um problema conhecido com o campo `offset` ao listar publicações no sistema *ISTPaper*. Em vez de passar à frente as primeiras `offset` publicações, simplesmente começa a emitir publicações a partir do ID `offset`. Garantiram-nos que será corrigido antes da aplicação **DEIPaper** entrar em produção, pelo que podemos assumir o comportamento especificado.

## O Exercício
O objectivo deste exercício é desenvolver a aplicação **DEIPaper** usando a framework **Django**[2][3] (versão 3.1.x).

A aplicação **DEIPaper** vai interagir com a API REST do sistema *ISTPaper*[1]. Deve testar os exemplos dados para cada operação de modo a perceber as características dos pedidos à API.

Inicialmente a aplicação **DEIPaper** será usada apenas por membros da secretaria, e estará acessível apenas da rede da mesma. Não se pretende também implementar, por enquanto, mecanismos de auditoria.

A aplicação **DEIPaper** deverá permitir pelo menos:
- Visualizar todas as publicações numa tabela de consulta rápida, contendo pelo menos Título e Autores;
- Visualizar uma publicação em particular, incluindo pelo menos Título, Autores, *Abstract* e link para o documento;
- Submeter novas publicações;
- Submeter correções a publicações existentes;
- Remover publicações.

A aplicação **DEIPaper** deverá ser tão flexível quanto o sistema *ISTPaper* permitir.

Deve realizar o exercício de forma modular.
Serão valorizadas qualidade e estética do código e da interface web apresentada.

Deve submeter num arquivo comprimido por email a sua solução e um ficheiro README, que descreva o procedimento para iniciar um servidor local de testes.
Prazo máximo de entrega: sexta, 11 de março de 2022, 23:59

Recursos potencialmente úteis:
- https://tailwindcss.com/
- https://getbootstrap.com/

Boa Sorte!

Nota: Durante os testes da adição de novas publicações pedimos que seja responsável nos dados utilizados.

[1]: https://aduck.rnl.tecnico.ulisboa.pt/istpaper/swagger-ui/index.html
[2]: https://www.djangoproject.com/
[3]: https://docs.djangoproject.com/en/3.1/intro/tutorial01/
