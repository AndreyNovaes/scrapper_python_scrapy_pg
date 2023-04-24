
# Projeto Web Scraper 🕸️💻

Este é um projeto de Web Scraper construído para coletar dados de páginas web e armazená-los em um banco de dados. Ele é projetado para ser fácil de configurar e executar tanto localmente quanto em uma instância AWS EC2, os sites utilizados foram: Mercado Livre e Buscapé, dois e-commerces Brasileiros.

## :bookmark_tabs: Índice

1. [Configuração Local](#local-setup)
2. [Configuração AWS EC2](#aws-ec2-setup)

## :wrench: Configuração Local <a id="local-setup"></a>

Siga os passos abaixo para configurar e executar o projeto localmente:

1. Clone o projeto e navegue até a pasta do projeto:

```bash
git clone https://github.com/AndreyNovaes/scrapper_python_scrapy_pg.git
```

- Copie o arquivo de exemplo de variáveis de ambiente e configure as variáveis:

```bash
cp .env.example .env
```

```bash
Lembre-se de usar aspas duplas ao definir o valor de `USER_AGENT`.
```

- Dê permissão de execução para o arquivo `start_spiders.sh` e execute-o:

```bash
chmod +x start_spiders.sh
```

- Inicie o script start_spiders

```bash
./start_spiders.sh
```

ou

```bash
bash start_spiders.sh
```

Pronto! Os dados seráo coletados e salvos no banco de dados definido pela sua conexão DATABASE_URL nas variáveis de ambiente.

## :cloud: Configuração AWS EC2 <a id="aws-ec2-setup"></a>

Siga os passos abaixo para configurar e executar o projeto em uma instância AWS EC2:

1. Crie um novo usuário com permissão de administrador e configure o AWS CLI com as credenciais do usuário:

- `aws configure`

    _Use o formato JSON como saída._

- Escolha uma região para criar o servidor spot (neste exemplo, usamos `us-west-1` - N. Califórnia).

- Crie um grupo de segurança com as seguintes regras de entrada:
  - SSH - TCP - 22

- Adicione o nome do grupo de sergurança no script handle_call_spot_spiders.sh na variável `SECURITY_GROUP_NAME`.

- Crie uma chave `.pem` na região escolhida e baixe-a para a pasta raiz do projeto, ou altere o caminho no arquivo `handle_call_spot_spiders.sh`.

- Dê permissão de execução para o arquivo `handle_call_spot_spiders.sh` e execute-o:

```bash
chmod +x handle_call_spot_spiders.sh
```

- Inicie o script

```bash
bash handle_call_spot_spiders
```

ou

```bash
./handle_call_spot_spiders.sh
```

- Dê permissão de execução para o arquivo`script_to_setup_environment.sh` e execute-o:

```bash
chmod +x script_to_setup_environment.sh
```

- Inicie o script

```bash
script_to_setup_environment.sh
```

Agora, o projeto está configurado e executando na instância AWS EC2! :rocket:, Irá funcionar da mesma maneira porém irá utilizar recursos da maquina ec2 escolhida.
