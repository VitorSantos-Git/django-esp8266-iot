# iot_monitor_project/settings.py

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ls0!rv^(jh$o0684#x84npnak28&9_dpz5$^o)9sx#nas5r(5u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Importante tirar o '*' após finalização !!!!!!!!!!!!!!!!

ALLOWED_HOSTS = ['192.168.31.80', 'localhost', '127.0.0.1', '*']


# Application definition

INSTALLED_APPS = [
    'jazzmin', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 
    'rest_framework.authtoken',
    'devices', 
    #'celery', 
    #'django_celery_beat', 
    # 'django_celery_results', # Opcional: Para armazenar resultados de tarefas no DB
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iot_monitor_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'iot_monitor_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale', 
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication', # Habilita autenticação por Token
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # Apenas usuários autenticados podem acessar
        # 'rest_framework.permissions.AllowAny', # Se quiser permitir acesso público em algumas APIs
    ]
}


# Celery Configuration
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0' # URL do seu servidor Redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' # Onde os resultados das tarefas são armazenados
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo' # Ou seu fuso horário local
CELERY_ENABLE_UTC = False # Defina como False se CELERY_TIMEZONE estiver definido

"""# Configurações para o Celery Beat (agendador)
CELERY_BEAT_SCHEDULE = {
    # Exemplo de tarefa agendada (pode ser removida depois)
    'add-every-10-seconds': {
        'task': 'devices.tasks.debug_task_example', # Caminho para a sua tarefa
        'schedule': 10.0, # Executa a cada 10 segundos
        'args': ('Hello from Celery Beat!',)
    },
}"""

# Tarefa para verificar e despachar comandos agendados a cada minuto
CELERY_BEAT_SCHEDULE = {
'check-and-dispatch-scheduled-commands': { 
        'task': 'devices.tasks.check_and_dispatch_scheduled_commands',
        'schedule': timedelta(seconds=30), # Executa a cada 30 segundos (0,5 minuto)
        'args': (),
    },

'check-device-status-every-minute': { # Nome único para o agendamento
        'task': 'devices.tasks.check_device_status', # O caminho para sua nova função
        'schedule': timedelta(minutes=1), # Executa a cada 60 segundos (1 minuto)
        'args': (), # Não precisa de argumentos para esta função
        'kwargs': {},
    },

}


# settings.py

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Adicione esta linha
]


JAZZMIN_SETTINGS = {
    # --- Configurações Gerais da Interface (Global) ---

    # Título da janela do navegador (aparece na aba do navegador)
    # Se ausente ou None, usará o site_title do admin.site do Django.
    "site_title": "IoT",

    # Título na tela de login do painel administrativo (máximo 19 caracteres)
    # Se ausente ou None, usará o site_header do admin.site do Django.
    "site_header": "Controle IoT",

    # Título da marca que aparece no canto superior esquerdo da sidebar (máximo 19 caracteres)
    # Geralmente acompanha o site_logo.
    "site_brand": "Controle",

    # Caminho relativo para o logo do seu site. Deve estar na pasta de arquivos estáticos.
    # Usado como logo principal no canto superior esquerdo (próximo ao site_brand).
    "site_logo": "img/IFSP_transparente.png",

    # Logo específico para a tela de login. Se None, usará o site_logo.
    "login_logo": "img/CMP_transparente.png",

    # Logo específico para a tela de login quando o tema escuro está ativado. Se None, usará login_logo.
    "login_logo_dark": "img/IFSP_CMP_transparente.png",

    # Classes CSS adicionais aplicadas à imagem do logo (site_logo).
    # Ex: "img-circle" para deixá-lo circular.
    #"site_logo_classes": None,

    # Caminho relativo para um favicon (o pequeno ícone na aba do navegador).
    # Se ausente, tentará usar o site_logo. Idealmente 32x32 pixels.
    #"site_icon": None,

    # Texto de boas-vindas exibido na tela de login.
    "welcome_sign": "Bem-vindo ao Painel de Controle IoT",

    # Texto de direitos autorais exibido no rodapé do painel administrativo.
    "copyright": "Painel de Controle IoT - Projeto de Ensino",

    # Se você quiser usar um único campo de busca, não precisa usar uma lista, pode usar uma string simples
    # Lista de modelos (formato 'app_label.ModelName') que serão incluídos na barra de pesquisa global.
    # Se esta configuração for omitida, a barra de pesquisa não será exibida.
    # "search_model": ["auth.User", "auth.Group"],

    # Nome do campo no seu modelo de usuário que contém a imagem/URL do avatar.
    # Pode ser o nome de um campo ou uma função que retorna a URL do avatar do usuário.
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Lista de links a serem exibidos na barra superior (top menu).
    # "topmenu_links": [
    #     # Exemplo de link que reverte uma URL do Django (permite controle de permissões)
    #     {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

    #     # Exemplo de link externo que abre em uma nova janela (permite controle de permissões)
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

    #     # Exemplo de link para um model admin específico (permite controle de permissões)
    #     {"model": "auth.User"},

    #     # Exemplo de link para um aplicativo que exibe um menu dropdown com todos os seus modelos
    #     {"app": "books"},
    # ],

    #############
    # User Menu #
    #############

    # Links adicionais para incluir no menu do usuário (aquele que aparece ao clicar no nome do usuário no canto superior direito).
    # O tipo 'app' não é permitido aqui.
    # "usermenu_links": [
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     {"model": "auth.user"} # Link para a página de detalhes do próprio usuário logado
    # ],

    #############
    # Side Menu #
    #############

    # Booleano que controla se o menu lateral é exibido.
    # "show_sidebar": True,

    # Booleano que controla se o menu lateral deve ser expandido automaticamente por padrão.
    # "navigation_expanded": False,

    # Lista de nomes de aplicativos ('app_label') a serem ocultados do menu lateral.
    # "hide_apps": [],

    # Lista de modelos (formato 'app_label.ModelName') a serem ocultados do menu lateral.
    # "hide_models": [],

    # Lista de aplicativos e/ou modelos para definir a ordem no menu lateral.
    # Os itens não listados aqui aparecerão após os itens especificados.
    #"order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Links personalizados para anexar a grupos de aplicativos no menu lateral.
    # A chave é o nome do aplicativo.
    # "custom_links": {
    #     "books": [{ # Para o aplicativo 'books'
    #         "name": "Make Messages", # Nome do link
    #         "url": "make_messages", # URL customizada (precisa ser configurada no urls.py do Django)
    #         "icon": "fas fa-comments", # Ícone Font Awesome para o link
    #         "permissions": ["books.view_book"] # Permissão necessária para ver o link
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    # Dicionário para definir ícones Font Awesome personalizados para aplicativos e modelos no menu lateral.
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "devices.ScheduledCommand": "fas fa-clock", # Exemplo: ajuste para seus modelos
        "devices.DayOfWeek": "fas fa-calendar-alt",
        "devices.Device": "fas fa-microchip",
        # Adicione ícones para outros modelos e apps conforme necessário fa-square-binary
    },

    # Ícones padrão usados quando nenhum ícone é especificado manualmente para um item do menu.
    # "default_icon_parents": "fas fa-chevron-circle-right", # Ícone para pais/grupos de aplicativos
    # "default_icon_children": "fas fa-circle", # Ícone para filhos/modelos

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    # Booleano para usar modais (janelas pop-up dentro da página) em vez de novas janelas pop-up do navegador
    # ao adicionar ou editar itens relacionados (ex: adicionar um autor ao criar um livro).
    # "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Caminhos relativos para arquivos CSS e JavaScript personalizados. Devem estar na pasta static.
    "custom_css": "css/custom_admin.css",
    "custom_js": None,

    # Booleano para incluir fontes do Google Fonts CDN. Se False, você precisa fornecer as fontes via custom_css.
    "use_google_fonts_cdn": True,

    # Booleano para exibir o construtor de UI (personalizador de tema) na barra lateral.
    # Recomendado ser False em produção.
    "show_ui_builder": False,
   
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    # Formato de renderização da página de alteração de modelo (editar/adicionar).
    # Opções: "single" (tudo em uma tela), "horizontal_tabs" (abas na horizontal),
    # "vertical_tabs" (abas na vertical), "collapsible" (seções recolhíveis), "carousel".
    "changeform_format": "single",

    # override change forms on a per modeladmin basis
    # Dicionário para sobrescrever o formato do formulário de alteração para modelos específicos.
    # A chave é 'app_label.ModelName'.
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},

    # Booleano para adicionar um seletor de idioma (dropdown) no painel administrativo.
    # "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
