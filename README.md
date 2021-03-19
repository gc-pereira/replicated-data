## Algo necessário

Ao iniciar esse projeto é necessário ler a funções que você irá precisar para instalação do docker. 

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

## ATENÇÃO
Todos os comandos necessários para iniciar esse projeto estão no arquivo ```shell run.sh ```, caso queira apenas subir tudo que for necessário sem digitar todos os comandos, abra seu terminal na pasta raiz do projeto e digite no terminal,
```shell
source run.sh
```
Mas atente-se a mudar o caminho que irá criar sua virtual enviroment, alterando o caminho para o da pasta raiz. Se estiver interessado em saber como os comandos funcionam e oq eles faze, acompanhe o resto desse README.md.

## Começando o projeto e configuração do ambiente

Para inicializar o projeto é necessário utilizar os seguintes comando responsáveis por criar uma imagem mysql. Primeiro execute,
```shell
docker build -t mysql-image -f db/Dockerfile .
```

aguarde a execução e a imagem mysql será criada dentro de um container docker, com todas as informações pedidas e com o usuário teamvendas e sua respectiva senha. Como não foi especificado, esse será um superusuário do banco de dados. Feito isso o próxim comando será responsável por deixar esse container rodando em background, sem ter que comprometer uma aba do terminal,

```shell
docker run -d --rm --name mysql-container mysql-image
```
É necessário criar uma virtual enviroment onde ficarão hospedados todos os diretório de bibliotecas a serem utilizadas,

```shell
python3 -m venv /path/to/new/virtual/environment
```
e executar

```shell
source .venv/bin/activate
```
para os arquivos *.py entenderem qual será development kits a serem utilizados.