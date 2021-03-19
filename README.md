## Começando o projeto

Ao iniciar esse projeto é necessário ler a funções que você irá precisar para instalação do docker. 

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

Para inicializar o projeto é necessário utilizar os seguintes comando responsáveis por criar uma imagem mysql. Primeiro execute,
```shell
docker build -t mysql-image -f db/Dockerfile .
```

aguarde a execução e a imagem mysql será criada dentro de um container docker, com todas as informações pedidas e com o usuário teamvendas e sua respectiva senha. Como não foi especificado, esse será um superusuário do banco de dados. Feito isso o próxim comando será responsável por deixar esse container rodando em background, sem ter que comprometer uma aba do terminal,

```shell
docker run -d --rm --name mysql-container mysql-image
```

