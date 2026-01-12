# Comandos Úteis - Fasting Life

## Desenvolvimento

### Iniciar servidor de desenvolvimento
```bash
python manage.py runserver
```

### Criar migrations
```bash
python manage.py makemigrations
```

### Aplicar migrations
```bash
python manage.py migrate
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### Executar testes
```bash
python manage.py test
```

### Executar testes com verbosidade
```bash
python manage.py test --verbosity=2
```

### Executar testes específicos
```bash
python manage.py test core.tests.FastingRecordModelTest
```

### Shell interativo do Django
```bash
python manage.py shell
```

### Verificar problemas no projeto
```bash
python manage.py check
```

## Banco de Dados

### Resetar banco de dados (SQLite)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Fazer backup do banco (SQLite)
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Exportar dados
```bash
python manage.py dumpdata > backup.json
```

### Importar dados
```bash
python manage.py loaddata backup.json
```

## Git

### Inicializar repositório
```bash
git init
git add .
git commit -m "Initial commit - Fasting Life MVP"
```

### Adicionar remote
```bash
git remote add origin <url-do-repositorio>
git push -u origin main
```

## Produção

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Configurar variáveis de ambiente
```bash
cp .env.example .env
# Editar .env com suas configurações
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

### Executar migrations
```bash
python manage.py migrate --noinput
```

### Iniciar com Gunicorn
```bash
gunicorn fasting_life.wsgi:application --bind 0.0.0.0:8000
```

## Manutenção

### Ver logs do Gunicorn (systemd)
```bash
sudo journalctl -u fasting_life -f
```

### Reiniciar serviço
```bash
sudo systemctl restart fasting_life
```

### Ver status do serviço
```bash
sudo systemctl status fasting_life
```

### Backup do banco PostgreSQL
```bash
pg_dump -U fasting_user fasting_life > backup_$(date +%Y%m%d).sql
```

### Restaurar backup PostgreSQL
```bash
psql -U fasting_user fasting_life < backup_20260112.sql
```

## Desenvolvimento - Comandos Rápidos

### Resetar e popular banco com dados de teste
```bash
python manage.py flush --noinput
python manage.py migrate
python manage.py createsuperuser --noinput --email admin@test.com --name Admin
```

### Ver todas as URLs do projeto
```bash
python manage.py show_urls
```

### Criar app Django
```bash
python manage.py startapp nome_do_app
```

## Troubleshooting

### Limpar cache do Python
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Verificar versão do Django
```bash
python -m django --version
```

### Verificar dependências instaladas
```bash
pip list
```

### Atualizar dependências
```bash
pip install --upgrade -r requirements.txt
```

### Verificar problemas de segurança
```bash
python manage.py check --deploy
```
