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

    Bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd IOT_Controle # Ou o nome da sua pasta raiz do projeto
    Configurar Ambiente Virtual Python

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

    Bash

    python -m venv venv
    No Windows (PowerShell/CMD):

Ativar o ambiente virtual
    Bash

    .\venv\Scripts\activate
    No Linux/WSL/macOS (Bash/Zsh):

Ativar o ambiente virtual
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

    ALLOWED_HOSTS = ['192.168.10.50', 'localhost', '127.0.0.1']
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

### Iniciar o Servidor Django

Após configurar o ambiente e o banco de dados, você pode iniciar o servidor de desenvolvimento do Django:

    Bash
    python manage.py runserver

O servidor estará acessível em http://127.0.0.1:8000/ ou no IP configurado no ALLOWED_HOSTS (ex: http://192.168.10.50:8000/). O painel administrativo estará em http://127.0.0.1:8000/admin/.

Iniciar o Celery Worker
O Celery Worker é responsável por executar as tarefas assíncronas (como o envio de comandos agendados). Certifique-se de que o Redis esteja em execução (conforme configurado na seção Instalação e Configuração do Redis no WSL).

Abra um novo terminal (e ative o ambiente virtual novamente, se necessário) e execute:

    Bash

    celery -A iot_monitor_project worker -l info

Este comando iniciará o worker do Celery, que ficará aguardando tarefas na fila do Redis.

Iniciar o Celery Beat
O Celery Beat é o agendador que envia as tarefas agendadas (como a verificação periódica de comandos a serem despachados) para a fila do Celery Worker.

Abra outro novo terminal (e ative o ambiente virtual novamente, se necessário) e execute:

    Bash

    celery -A iot_monitor_project beat -l info --scheduler django_celery_beat.schedulers.DatabaseScheduler

Importante: Mantenha o Celery Worker e o Celery Beat rodando em terminais separados para que o agendamento e a execução das tarefas funcionem corretamente.

### Gerenciamento de Comandos Agendados

O painel de administração do Django oferece uma interface para gerenciar os comandos que serão enviados aos seus dispositivos IoT.

1.  **Acessar o Painel Administrativo:**
    * Certifique-se de que o servidor Django está rodando (conforme a seção [Iniciar o Servidor Django](#iniciar-o-servidor-django)).
    * Abra seu navegador e acesse `http://127.0.0.1:8000/admin/` (ou o IP/domínio configurado).
    * Faça login com as credenciais do superusuário que você criou.

2.  **Navegar para Comandos Agendados:**
    * No grupo "Dispositivos", clique em "Comandos Agendados".

3.  **Adicionar um Novo Comando Agendado:**
    * Clique no botão "Adicionar Comando Agendado" no canto superior direito.
    * **Dispositivo:** Selecione o dispositivo IoT para o qual o comando será enviado. Certifique-se de que seus dispositivos estejam cadastrados previamente.
    * **Tipo de Agendamento:**
        * **Uma Vez:** Para comandos que devem ser executados em uma data e hora específicas.
        * **Diário:** Para comandos que se repetem todos os dias em um horário específico.
        * **Semanal:** Para comandos que se repetem em dias específicos da semana e em um horário específico.
    * **Comando:** Insira o comando exato a ser enviado ao dispositivo.
    * **Ativo:** Marque esta caixa para que o comando seja considerado para execução pelo Celery Beat.
    * **Outros Campos:** Preencha os campos de data, hora e dias da semana conforme o tipo de agendamento escolhido.

4.  **Monitoramento e Execução:**
    * O Celery Beat (rodando em segundo plano) verificará periodicamente os comandos agendados.
    * Quando um comando atinge sua data/hora de execução, o Celery Beat o enviará para a fila do Redis.
    * O Celery Worker (também rodando em segundo plano) pegará o comando da fila e o processará, despachando-o para o dispositivo IoT.
    * O campo `Last triggered at` será atualizado após a execução do comando.

5.  **Edição e Exclusão:**
    * Você pode editar comandos existentes clicando no nome do comando na lista.
    * Para excluir, selecione o(s) comando(s) e use a ação "Excluir comandos agendados selecionados" no menu de ações.

 ### Estrutura do Projeto

A estrutura do projeto segue as convenções padrão do Django, com a adição de configurações para Celery e Redis. 

IOT_Controle/
├── iot_monitor_project/        # Diretório principal do projeto Django
│   ├── init.py
│   ├── asgi.py
│   ├── settings.py             # Configurações gerais do Django e Celery/Redis
│   ├── urls.py                 # URLs globais do projeto
│   └── wsgi.py
├── devices/                    # Aplicativo Django para gerenciamento de dispositivos IoT
│   ├── migrations/             # Migrações do banco de dados
│   ├── init.py             # Configurações do AppConfig (verbose_name)
│   ├── admin.py                # Configurações do painel administrativo (Django Admin/Jazzmin)
│   ├── apps.py                 # Configuração do aplicativo (verbose_name)
│   ├── models.py               # Definição dos modelos de dados (Dispositivo, ComandoAgendado, etc.)
│   ├── serializers.py          # Serializadores para a API REST
│   ├── tasks.py                # Tarefas do Celery
│   ├── urls.py                 # URLs da API REST do aplicativo devices
│   └── views.py                # Views da API REST
├── locale/                     # Diretório para arquivos de tradução (.po, .mo)
│   └── pt_BR/
│       └── LC_MESSAGES/
│           ├── django.po
│           └── django.mo
├── static/                     # Arquivos estáticos personalizados (imagens, CSS, JS)
│   └── img/
│       └── logo.png            # Exemplo de imagem de logo
├── sketch_frmware_esp/         # Firmware de exemplo para dispositivos ESP (ESP8622 - IDE DO ARDUINO)
│   └── password_ssid.h         # Arquivo de configuração de Wi-Fi (DEVE ser Criador e colocado na mesma pasta com as informações indicada no firmware)
├── venv/                       # Ambiente virtual Python
├── .gitignore                  # Arquivo para ignorar arquivos e diretórios no Git
├── manage.py                   # Utilitário de linha de comando do Django
└── requirements.txt            # Lista de dependências Python do projeto
└── README.md                   # Este arquivo de documentação  


## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir, por favor, siga os seguintes passos:

1.  Faça um fork do repositório.
2.  Crie uma nova branch para sua feature (`git checkout -b feature/minha-nova-feature`).
3.  Faça suas alterações e commit-as (`git commit -m 'feat: Adiciona nova funcionalidade X'`).
4.  Envie suas alterações para o seu fork (`git push origin feature/minha-nova-feature`).
5.  Abra um Pull Request para a branch `main` deste repositório.

## Licença

Este projeto está licenciado sob a [Licença Creative Commons Atribuição-NãoComercial 4.0 Internacional (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

Você é livre para usar, adaptar e compartilhar este trabalho para fins não comerciais, desde que atribua o crédito apropriadamente. Para mais detalhes, veja o arquivo [LICENSE](LICENSE).
