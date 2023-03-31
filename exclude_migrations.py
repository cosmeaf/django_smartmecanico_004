import os
import shutil
import sys
import subprocess

# Verifica se há um ambiente virtual criado
venv_path = os.path.join(os.getcwd(), 'venv')
if not os.path.exists(venv_path):
    print('Criando ambiente virtual...')
    subprocess.run(['python', '-m', 'venv', 'venv'], shell=True, check=True)

# Ativa o ambiente virtual
subprocess.run([os.path.join(venv_path, 'Scripts', 'activate.bat')], shell=True, check=True)

# Salva as dependências atuais
subprocess.run(['pip', 'freeze', '>', 'requirements.txt'], shell=True, check=True)

# Deleta o diretório do ambiente virtual
shutil.rmtree(venv_path)

# Remove o arquivo de banco de dados, caso exista
db_path = os.path.join(os.getcwd(), 'db.sqlite3')
if os.path.exists(db_path):
    os.remove(db_path)

# Executa o script para excluir os migrations
for app in ['app_address', 'app_auth', 'app_employees', 'app_profile', 'app_schedule', 'app_services', 'app_vehicles']:
    migrations_dir = os.path.join(os.getcwd(), app, 'migrations')
    print(migrations_dir)
    for file in os.listdir(migrations_dir):
        if file.endswith('.py'):
            os.remove(os.path.join(migrations_dir, file))
            print(f'Removed {file} from {migrations_dir}')
    for root, dirs, files in os.walk(os.getcwd()):
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            for file in os.listdir(pycache_dir):
                os.remove(os.path.join(pycache_dir, file))
                print(f'Removed {file} from {pycache_dir}')
            os.rmdir(pycache_dir)
            print(f'Removed {pycache_dir}')

# Cria um novo ambiente virtual
subprocess.run(['python', '-m', 'venv', 'venv'], shell=True, check=True)

# Ativa o ambiente virtual
subprocess.run([os.path.join(venv_path, 'Scripts', 'activate.bat')], shell=True, check=True)

# Instala as dependências salvas
subprocess.run(['pip', 'install', '-r', 'requirements.txt'], shell=True, check=True)

# Executa as migrações
for app in ['app_address', 'app_auth', 'app_employees', 'app_profile', 'app_schedule', 'app_services', 'app_vehicles']:
    subprocess.run(['python', 'manage.py', 'makemigrations', app], shell=True, check=True)
    subprocess.run(['python', 'manage.py', 'migrate', app], shell=True, check=True)

print('Script executado com sucesso!')
