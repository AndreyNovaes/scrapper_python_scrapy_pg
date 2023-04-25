
# Projeto Web Scraper 🕸️💻

Este é um projeto de Web Scraper construído para coletar dados de páginas web e armazená-los em um banco de dados. Ele é projetado para ser fácil de configurar e executar tanto localmente quanto em uma instância AWS EC2, os sites utilizados foram: Mercado Livre e Buscapé, dois e-commerces Brasileiros.

## :bookmark_tabs: Índice

1. [Configuração Local](#local-setup)
2. [Configuração AWS EC2](#aws-ec2-setup)

## :wrench: Configuração Local <a id="local-setup"></a>

Siga os passos abaixo para configurar e executar o projeto localmente:

1.1. Clone o projeto e navegue até a pasta do projeto:

```bash
git clone https://github.com/AndreyNovaes/scrapper_python_scrapy_pg.git
cd scrapper_python_scrapy_pg
```

1.2. Copie o arquivo de exemplo de variáveis de ambiente e configure as variáveis:
_Lembre-se de usar aspas duplas ao definir o valor de `USER_AGENT`, assim como no arquivo .env.example._

```bash
cp .env.example .env
```

1.3. Dê permissão de execução para o arquivo `start_spiders.sh` e execute-o:

```bash
chmod +x start_spiders.sh
./start_spiders.sh
```

Pronto! Os dados seráo coletados e salvos no banco de dados definido pela sua conexão DATABASE_URL nas variáveis de ambiente.

## :cloud: Configuração AWS EC2 <a id="aws-ec2-setup"></a>

Siga os passos abaixo para configurar e executar o projeto em uma instância AWS EC2:

2.1. Crie um novo usuário com permissão de administrador e configure o AWS CLI com as credenciais do usuário:

- `aws configure`

    _Use o formato JSON como saída._

2.2. Clone o projeto e navegue até a pasta do projeto:

```bash
git clone https://github.com/AndreyNovaes/scrapper_python_scrapy_pg.git
cd scrapper_python_scrapy_pg
```

2.3. Copie o arquivo de exemplo de variáveis de ambiente e configure as variáveis:

_Lembre-se de usar aspas duplas ao definir o valor de `USER_AGENT`._

```bash
cp .env.example .env
```

2.4. Escolha uma região para criar o servidor spot (neste exemplo, usamos `us-west-1` - N. Califórnia).

2.5. Crie um grupo de segurança com o nome `us-west-1`, que foi utilizado no exemplo, e adicione as seguintes regras:

- SSH - TCP - 22

2.6. Adicione o nome do grupo de segurança no script handle_call_spot_spiders.sh na variável `SECURITY_GROUP_NAME` ou, caso o nome seja `us-west-1` não precisa fazer mudança já que o nome do grupo de segurança usado no exemplo foi `us-west-1`

2.7. Crie uma chave `.pem` na região escolhida com o nome `us-west-1` e baixe-a para a pasta raiz do projeto ou altere o caminho no arquivo para que o script consiga encontrar no comando `bash handle_call_spot_spiders.sh`.

2.8. Dê permissão de execução para o arquivo `handle_call_spot_spiders.sh` e execute-o:

```bash
chmod +x handle_call_spot_spiders.sh
bash handle_call_spot_spiders
```

2.9 Agora, dentro do terminal da instância EC2, dê permissão de execução para o arquivo`script_to_setup_environment.sh` e execute-o:

```bash
chmod +x script_to_setup_environment.sh
bash script_to_setup_environment.sh
```

Se tudo ocorrer bem o projeto foi configurado e vai estar executando na instância AWS EC2! :rocket:, Irá funcionar da mesma maneira que localmente porém irá utilizar recursos da maquina ec2 escolhida, após o término do processo de coleta de dados não se esqueça de encerrar a instância para não ser cobrado por ela.
