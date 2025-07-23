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

