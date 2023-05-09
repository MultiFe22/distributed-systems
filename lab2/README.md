# Dicionário Remoto - Aplicação Distribuída

Este projeto tem como objetivo o desenvolvimento de uma aplicação distribuída para aplicar os conceitos estudados sobre arquitetura de software e arquitetura de sistema, servidores multiplexados e concorrentes, e praticar programação usando socket.

## Descrição do Projeto

A aplicação que será desenvolvida será um dicionário remoto que poderá ser consultado e alterado. As chaves e valores do dicionário serão strings. O dicionário deverá ser armazenado em disco para ser restaurado em uma execução futura.

- Para a consulta, o usuário informará uma chave e receberá como resposta a lista de valores associados a essa chave, em ordem alfabética (lista vazia caso a entrada não exista).
- Para a escrita, o usuário informará um par chave e valor e receberá como resposta a confirmação de que a nova entrada foi inserida, ou que o novo valor foi acrescentado em uma entrada existente.
- A remoção de uma entrada no dicionário somente poderá ser feita pelo administrador do dicionário.

## Arquitetura de Software

A arquitetura de software da solução conterá, no mínimo, três componentes distintos: (i) acesso e persistência de dados; (ii) processamento das requisições; e (iii) interface com o usuário.

### Estilo Arquitetural Escolhido

Para esta aplicação, o estilo arquitetural escolhido será o modelo cliente-servidor, onde o servidor será responsável por receber as requisições dos clientes e fornecer as respostas apropriadas.

### Componentes e suas Funcionalidades

a) Componente de acesso e persistência de dados:
Este componente será responsável por gerenciar o armazenamento e a recuperação de dados do dicionário no disco. As funcionalidades providas incluem:

- Leitura dos dados do dicionário armazenados no disco.
- Escrita dos dados do dicionário no disco.

Este componente será usado pelo componente de processamento de requisições para acessar e atualizar os dados do dicionário.

b) Componente de processamento de requisições:
Este componente será responsável por receber as requisições dos clientes e processá-las adequadamente. As funcionalidades providas incluem:

- Recebimento das requisições dos clientes.
- Processamento das requisições e obtenção das respostas adequadas.
- Atualização do dicionário com as informações fornecidas pelos clientes.

Este componente usará o componente de acesso e persistência de dados para acessar e atualizar os dados do dicionário.

c) Componente de interface com o usuário:
Este componente será responsável por fornecer uma interface amigável para que os usuários possam interagir com o sistema. As funcionalidades providas incluem:

- Recebimento das requisições dos usuários.
- Apresentação das respostas aos usuários.
- Envio das requisições dos usuários para o componente de processamento de requisições.

Este componente usará o componente de processamento de requisições para enviar as requisições dos usuários e obter as respostas apropriadas.

d) Modo de Conexão entre os Componentes:
Os componentes serão conectados usando o protocolo TCP/IP e a biblioteca de sockets do Python. O componente de interface com o usuário será executado em uma thread separada para permitir que múltiplos clientes se conectem ao servidor simultaneamente. O componente de acesso e persistência de dados será executado em outra thread para permitir o acesso concorrente ao dicionário.

## Instanciando a arquitetura de sistema cliente/servidor

Para instanciar a arquitetura de sistema cliente/servidor de dois níveis, com um servidor e um cliente, precisamos definir quais componentes ficarão do lado do cliente e do lado do servidor, além de definir o conteúdo e a ordem das mensagens que serão trocadas entre cliente e servidor.

### Componentes do lado do cliente

Do lado do cliente, teremos apenas um componente: a interface com o usuário. Este componente será responsável por receber as entradas do usuário e enviar as requisições correspondentes ao servidor.

### Componentes do lado do servidor

Do lado do servidor, teremos três componentes:

1. Servidor: responsável por receber as requisições dos clientes e enviá-las para o componente de processamento de requisições. Ele também enviará as respostas de volta para o cliente correspondente.
2. Processamento de requisições: responsável por processar as requisições e acessar ou atualizar o dicionário usando o componente de acesso e persistência de dados, se necessário.
3. Acesso e persistência de dados: responsável por armazenar e recuperar o dicionário em disco.

### Mensagens trocadas entre cliente e servidor

A comunicação entre cliente e servidor será baseada em mensagens trocadas por meio de sockets TCP. O conteúdo das mensagens será definido de acordo com as requisições e respostas necessárias para o funcionamento da aplicação.

As mensagens serão compostas por uma string, onde dependendo do valor recebido, comandos diferentes são executados.

Abaixo, segue a lista de comandos que serão implementados:

- `get=<chave>`: retorna os valores associados à chave informada, em ordem alfabética.

- `set=<chave>:<valor>`: insere um novo par chave-valor no dicionário, ou acrescenta o valor informado à lista de valores associada à chave informada.

- `remove=<chave>`: remove a entrada correspondente à chave informada do dicionário.

- `quit`: encerra o servidor (caso enviado do servidor) ou o cliente (caso enviado do cliente).

As mensagens serão enviadas pelo cliente para o servidor e vice-versa, e cada lado deverá estar preparado para receber e interpretar as mensagens corretamente. Quando o servidor receber uma mensagem de requisição, ele deverá enviá-la para o componente de processamento de requisições, que fará o processamento necessário e enviará a resposta de volta para o servidor, que por sua vez enviará a resposta de volta para o cliente correspondente.