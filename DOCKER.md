# Docker - Publicação Local

## Pré-requisitos
- Docker Desktop instalado
- Docker Compose instalado

## Comandos para executar

### 1. Build e iniciar os containers
```bash
docker-compose up --build
```

### 2. Executar em background
```bash
docker-compose up -d
```

### 3. Ver logs
```bash
docker-compose logs -f
```

### 4. Parar os containers
```bash
docker-compose down
```

### 5. Parar e remover volumes (limpar banco de dados)
```bash
docker-compose down -v
```

### 6. Criar superusuário
```bash
docker-compose exec web python manage.py createsuperuser
```

### 7. Executar migrações manualmente
```bash
docker-compose exec web python manage.py migrate
```

## Acessar a aplicação
- Aplicação: http://localhost:8000
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api

## Banco de dados
- Host: localhost
- Porta: 5432
- Database: fasting_life
- User: postgres
- Password: postgres

## Estrutura
- **Dockerfile**: Imagem da aplicação Django
- **docker-compose.yml**: Orquestração dos serviços (web + PostgreSQL)
- **.dockerignore**: Arquivos ignorados no build
