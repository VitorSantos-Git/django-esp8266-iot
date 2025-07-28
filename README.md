# Projeto IoT Controle

Este projeto Django integra o Celery com Redis para agendamento e execução de comandos em dispositivos IoT.

## Sumário

1.  [Pré-requisitos](#pré-requisitos)
2.  [Configuração do Ambiente de Desenvolvimento (Windows com WSL)](#configuração-do-ambiente-de-desenvolvimento-windows-com-wsl)
    * [Instalação do WSL (Ubuntu)](#instalação-do-wsl-ubuntu)
    * [Instalação e Configuração do Redis no WSL](#instalação-e-configuração-do-redis-no-wsl)
3.  [Configuração do Projeto Django](#configuração-do-projeto-django)
    * [Clonar o Repositório](#clonar-o-repositório)
    * [Configurar Ambiente Virtual Python](#configurar-ambiente-virtual-python)
    * [Instalar Dependências](#instalar-dependências)
    * [Configurações do Django](#configurações-do-django)
    * [Migrações do Banco de Dados](#migrações-do-banco-de-dados)
    * [Criação de Superusuário](#criação-de-superusuário)
    * [População de Dados Iniciais (Dias da Semana)](#população-de-dados-iniciais-dias-da-semana)
4.  [Executando o Projeto](#executando-o-projeto)
    * [Iniciar o Servidor Django](#iniciar-o-servidor-django)
    * [Iniciar o Celery Worker](#iniciar-o-celery-worker)
    * [Iniciar o Celery Beat](#iniciar-o-celery-beat)
5.  [Gerenciamento de Comandos Agendados](#gerenciamento-de-comandos-agendados)
6.  [Estrutura do Projeto](#estrutura-do-projeto)

---

## Pré-requisitos

* Python 3.9+
* pip (gerenciador de pacotes do Python)
* Git
* Windows Subsystem for Linux (WSL) com uma distribuição Linux (Ubuntu recomendado)
* Redis (instalado no WSL)

## Configuração do Ambiente de Desenvolvimento (Windows com WSL)

### Instalação do WSL (Ubuntu)

1.  **Habilitar WSL:** Abra o PowerShell como Administrador e execute:
    ```powershell
    wsl --install
    ```
    Isso instalará o WSL e o Ubuntu por padrão. Se já tiver WSL, pode ser necessário atualizar: `wsl --update`.
2.  **Configurar Ubuntu:** Após a instalação, o Ubuntu será iniciado automaticamente. Siga as instruções para criar um nome de usuário e senha UNIX.
3.  **Atualizar Pacotes:** No terminal Ubuntu (WSL), execute:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

### Instalação e Configuração do Redis no WSL

O Redis será usado como broker de mensagens para o Celery.

1.  **Instalar Redis:** No terminal Ubuntu (WSL), execute:
    ```bash
    sudo apt install redis-server -y
    ```
2.  **Iniciar Redis:**
    ```bash
    sudo service redis-server start
    ```
3.  **Verificar Status:**
    ```bash
    sudo service redis-server status
    redis-cli ping
    ```
    Você deve ver `active (running)` e `PONG`.
4.  **Configurar para Iniciar Automaticamente (Opcional, mas recomendado):**
    Edite o arquivo `~/.bashrc` ou `~/.zshrc` (dependendo do seu shell) para iniciar o Redis automaticamente ao abrir o terminal WSL. Adicione a seguinte linha no final do arquivo:
    ```bash
    # Iniciar Redis se não estiver rodando
    sudo service redis-server status | grep -q "is not running" && sudo service redis-server start
    ```
    Salve o arquivo e recarregue o shell (`source ~/.bashrc` ou `source ~/.zshrc`).

## Configuração do Projeto Django

### Clonar o Repositório

Navegue até o diretório onde deseja armazenar o projeto e clone o repositório:

    bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd IOT_Controle # Ou o nome da sua pasta raiz do projeto
    Configurar Ambiente Virtual Python
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

    Bash

    python -m venv venv
    No Windows (PowerShell/CMD):

    Bash

    .\venv\Scripts\activate
    No Linux/WSL/macOS (Bash/Zsh):

    Bash

    source venv/bin/activate
    Instalar Dependências
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias usando o requirements.txt. Certifique-se de que este arquivo foi gerado corretamente (ex: pip freeze > requirements.txt).

    Bash

    pip install -r requirements.txt
    Configurações do Django
    Ajuste as configurações básicas do projeto no arquivo iot_monitor_project/settings.py.

    Chave Secreta (SECRET_KEY): Para fins de desenvolvimento, a chave existente pode ser usada. Para ambientes de produção, é imperativo gerar uma nova chave forte e gerenciá-la como uma variável de ambiente, nunca hardcoded no código.

    Exemplo de geração de uma nova chave (no shell Python):

    Python

    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    Hosts Permitidos (ALLOWED_HOSTS): Esta configuração define quais nomes de host o seu Django pode servir.

    Para desenvolvimento local, você pode usar:

    Python

    ALLOWED_HOSTS = ['192.168.31.80', 'localhost', '127.0.0.1']
    Atenção: Em produção, NUNCA use ALLOWED_HOSTS = ['*'] pois isso é uma falha de segurança grave. Liste explicitamente os domínios e IPs do seu servidor.

    Configuração do Celery e Redis: O Celery usa o Redis como um "broker" de mensagens. Verifique as URLs configuradas no seu settings.py.

    Python

    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0' # URL do seu servidor Redis
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' # Onde os resultados das tarefas são armazenados
    Certifique-se de que o Redis esteja rodando e acessível na porta 6379.

    Migrações do Banco de Dados
    Aplique as migrações para criar as tabelas necessárias no banco de dados (SQLite por padrão neste projeto):

    Bash

    python manage.py migrate
    Criação de Superusuário
    Crie um usuário administrador para acessar o painel de administração do Django (/admin/):

    Bash

    python manage.py createsuperuser
    Siga as instruções no terminal para definir o nome de usuário, endereço de e-mail e senha.

    População de Dados Iniciais (Dias da Semana)
    O aplicativo devices utiliza o modelo DayOfWeek para representar os dias da semana em agendamentos. Para garantir que estes dados básicos estejam presentes, você pode populá-los via Django Shell:

    Bash

    python manage.py shell
    Dentro do shell Python, cole e execute os seguintes comandos:

    Python

    from devices.models import DayOfWeek
    from django.utils.translation import gettext_lazy as _

    # Mapeamento de nomes e valores numéricos para os dias da semana
    days_data = [
        (_('Sunday'), 0),
        (_('Monday'), 1),
        (_('Tuesday'), 2),
        (_('Wednesday'), 3),
        (_('Thursday'), 4),
        (_('Friday'), 5),
        (_('Saturday'), 6),
    ]

    for name, numeric_value in days_data:
        # str(name) é usado para converter o objeto proxy de tradução para string antes de comparar/criar
        DayOfWeek.objects.get_or_create(name=str(name), defaults={'numeric_value': numeric_value})
        print(f"Dia '{name}' (valor: {numeric_value}) verificado/criado.")

    exit() # Digite 'exit()' ou Ctrl+D para sair do shell

