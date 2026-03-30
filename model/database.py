import pymysql
import configparser
import os
import sys

config = configparser.ConfigParser()

# Resolve o caminho do config.ini dependendo se está rodando como script normal, ou através do .exe instalado
if getattr(sys, 'frozen', False):
    # Se foi empacotado e instalado, salva o config.ini no AppData do usuário (para evitar Erro de Permissão do Windows)
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'Caobalhota')
    os.makedirs(appdata_dir, exist_ok=True)
    config_path = os.path.join(appdata_dir, 'config.ini')
else:
    # Em modo de desenvolvimento, salva na raiz do projeto
    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(application_path, 'config.ini')

# Se o config.ini não existir no diretório alvo, ele cria um novo padrão
if not os.path.exists(config_path):
    config['database'] = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'caobalhota',
        'charset': 'utf8mb4',
        'autocommit': 'False'
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)
else:
    config.read(config_path)

db_config = config['database']

DB_CONFIG = {
    "host": db_config.get('host', 'localhost'),
    "user": db_config.get('user', 'root'),
    "password": db_config.get('password', ''),
    "database": db_config.get('database', 'caobalhota'),
    "charset": db_config.get('charset', 'utf8mb4'),
    "cursorclass": pymysql.cursors.Cursor,  
    "autocommit": db_config.getboolean('autocommit', fallback=False),        
}

def get_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

get_connection()