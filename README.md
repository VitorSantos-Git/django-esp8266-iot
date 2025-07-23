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

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd IOT_Controle # Ou o nome da sua pasta raiz do projeto

"""
Configurar Ambiente Virtual Python
É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

Bash

python -m venv venv
Ativar Ambiente Virtual
Windows (PowerShell):

PowerShell

.\venv\Scripts\Activate.ps1

Linux/WSL (Bash/Zsh):

Bash

source venv/bin/activate
Você verá (venv) no início da linha de comando, indicando que o ambiente virtual está ativo.

"""

"""
Ótima ideia! É fundamental ter um README.md (formato Markdown é o padrão para GitHub e permite formatação) com o passo a passo para facilitar o deploy e a colaboração.

Vou criar um rascunho completo para você. Salve este conteúdo como README.md na raiz do seu projeto (onde está o manage.py).

Markdown

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

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd IOT_Controle # Ou o nome da sua pasta raiz do projeto

"""
Configurar Ambiente Virtual Python
É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

Bash

python -m venv venv
Ativar Ambiente Virtual
Windows (PowerShell):

PowerShell

.\venv\Scripts\Activate.ps1
Linux/WSL (Bash/Zsh):

Bash

source venv/bin/activate
Você verá (venv) no início da linha de comando, indicando que o ambiente virtual está ativo.

###########################################

Instalar Dependências
Com o ambiente virtual ativado, instale as dependências do projeto:

Bash

pip install -r requirements.txt # Crie este arquivo se ainda não tiver, com as dependências
# Ou instale manualmente:
pip install Django djangorestframework celery redis django-celery-beat

Migrações do Banco de Dados
Aplique as migrações para criar as tabelas do banco de dados, incluindo as do django_celery_beat e suas apps:

Bash

python manage.py makemigrations
python manage.py migrate

###########################################

Criação de Superusuário
Crie um superusuário para acessar o painel de administração do Django:

Bash

python manage.py createsuperuser

###########################################

População de Dados Iniciais (Dias da Semana)
O modelo DayOfWeek precisa ser populado uma vez.

Bash

python manage.py shell

Dentro do shell Python, execute:

Python

from devices.models import DayOfWeek

# Limpa para garantir que não haja duplicatas (apenas se for a primeira vez)
DayOfWeek.objects.all().delete()

days_data = [
    ('Domingo', 0),
    ('Segunda-feira', 1),
    ('Terça-feira', 2),
    ('Quarta-feira', 3),
    ('Quinta-feira', 4),
    ('Sexta-feira', 5),
    ('Sábado', 6),
]

for name, numeric_value in days_data:
    DayOfWeek.objects.create(name=name, numeric_value=numeric_value)
    print(f"Dia {name} ({numeric_value}) criado.")

exit()

######################

Iniciar o Servidor Django
python manage.py runserver 0.0.0.0:8000
Ótima ideia! É fundamental ter um README.md (formato Markdown é o padrão para GitHub e permite formatação) com o passo a passo para facilitar o deploy e a colaboração.

Vou criar um rascunho completo para você. Salve este conteúdo como README.md na raiz do seu projeto (onde está o manage.py).

Markdown

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

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd IOT_Controle # Ou o nome da sua pasta raiz do projeto
Configurar Ambiente Virtual Python
É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

Bash

python -m venv venv
Ativar Ambiente Virtual
Windows (PowerShell):

PowerShell

.\venv\Scripts\Activate.ps1
Linux/WSL (Bash/Zsh):

Bash

source venv/bin/activate
Você verá (venv) no início da linha de comando, indicando que o ambiente virtual está ativo.

Instalar Dependências
Com o ambiente virtual ativado, instale as dependências do projeto:

Bash

pip install -r requirements.txt # Crie este arquivo se ainda não tiver, com as dependências
# Ou instale manualmente:
pip install Django djangorestframework celery redis django-celery-beat
Configurações do Django
Certifique-se de que as configurações do Celery e das aplicações estejam corretas em iot_monitor_project/settings.py:

Python

# iot_monitor_project/settings.py

INSTALLED_APPS = [
    # ... outras apps
    'devices',
    'rest_framework',
    'django_celery_beat', # Necessário para o agendador de banco de dados
    # 'django_celery_results', # Opcional: para armazenar resultados de tarefas no DB
]

# Celery Configuration
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo' # Ajuste para seu fuso horário
CELERY_ENABLE_UTC = False # Defina como False se CELERY_TIMEZONE estiver definido

# Configurações para o Celery Beat (agendador)
CELERY_BEAT_SCHEDULE = {
    'check-and-dispatch-scheduled-commands': {
        'task': 'devices.tasks.check_and_dispatch_scheduled_commands',
        'schedule': 60.0, # Executa a cada 60 segundos (1 minuto)
        'args': (),
    },
}
Verifique também iot_monitor_project/celery.py e iot_monitor_project/__init__.py conforme a configuração padrão do Celery.

Migrações do Banco de Dados
Aplique as migrações para criar as tabelas do banco de dados, incluindo as do django_celery_beat e suas apps:

Bash

python manage.py makemigrations
python manage.py migrate
Criação de Superusuário
Crie um superusuário para acessar o painel de administração do Django:

Bash

python manage.py createsuperuser
Siga as instruções para definir nome de usuário, e-mail e senha.

População de Dados Iniciais (Dias da Semana)
O modelo DayOfWeek precisa ser populado uma vez.

Bash

python manage.py shell
Dentro do shell Python, execute:

Python

from devices.models import DayOfWeek

# Limpa para garantir que não haja duplicatas (apenas se for a primeira vez)
DayOfWeek.objects.all().delete()

days_data = [
    ('Domingo', 0),
    ('Segunda-feira', 1),
    ('Terça-feira', 2),
    ('Quarta-feira', 3),
    ('Quinta-feira', 4),
    ('Sexta-feira', 5),
    ('Sábado', 6),
]

for name, numeric_value in days_data:
    DayOfWeek.objects.create(name=name, numeric_value=numeric_value)
    print(f"Dia {name} ({numeric_value}) criado.")

exit()
Executando o Projeto
Você precisará de três terminais separados, todos com o ambiente virtual ativado.

Iniciar o Servidor Django
No primeiro terminal:

Bash

python manage.py runserver 0.0.0.0:8000

Acesse o painel de administração em
http://127.0.0.1:8000/admin/ (ou http://xxx.xxx.xxx.xxx:8000/admin/ se estiver usando o IP da sua máquina na rede).


Iniciar o Celery Worker
No segundo terminal:

Bash

celery -A iot_monitor_project worker -l info --pool=solo
Nota: O --pool=solo é crucial para ambientes Windows para evitar PermissionError. Em ambientes Linux/produção, você pode omitir ou usar prefork.

Iniciar o Celery Beat
No terceiro terminal:

Bash

celery -A iot_monitor_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
Certifique-se de que o servidor Redis esteja rodando no WSL antes de iniciar o Celery Worker e Beat.


Estrutura do Projeto
IOT_Controle/
├── iot_monitor_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│   └── celery.py        # Configuração do Celery
├── devices/
│   ├── migrations/
│   │   └── ...
│   ├── __init__.py
│   ├── admin.py         # Registro dos modelos no Admin
│   ├── apps.py
│   ├── models.py        # Modelos Device, ScheduledCommand, DayOfWeek
│   ├── serializers.py   # Serializadores para a API REST
│   ├── tasks.py         # Tarefas Celery (send_scheduled_command_to_device, check_and_dispatch_scheduled_commands)
│   ├── urls.py          # URLs da API
│   └── views.py         # Views da API
├── venv/                # Ambiente virtual Python
├── manage.py
├── README.md            # Este arquivo
└── requirements.txt     # Dependências do projeto

"""