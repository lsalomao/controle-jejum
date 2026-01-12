# Fasting Life

MVP web para **controle de jejum**: registrar início/fim, calcular duração automaticamente e exibir indicadores simples (média, consistência e streak), com histórico editável e registro mensal de peso.

## 🎯 Objetivo

Desenvolver um MVP web simples para **registrar períodos de jejum**, **calcular automaticamente** sua duração e apresentar indicadores claros de consistência e impacto diário.

### Princípios

- Simplicidade acima de tudo
- Automação sempre que possível
- Poucos dados, mas úteis
- Baixo custo de desenvolvimento e manutenção

## ✨ Funcionalidades

### O que o sistema FAZ

- ✅ Iniciar e encerrar jejuns
- ✅ Editar jejuns passados (sempre respeitando validações)
- ✅ Calcular duração automaticamente
- ✅ Registrar estado físico e mental básico
- ✅ Registrar peso corporal (mensal)
- ✅ Exibir histórico
- ✅ Exibir indicadores simples (média, consistência, streak)
- ✅ Exibir gráfico simples de duração do jejum por dia (no Dashboard)
- ✅ Tema laranja com modo claro/escuro
- ✅ Interface responsiva (mobile-first)

### O que o sistema NÃO faz (por enquanto)

- ❌ Contagem de calorias
- ❌ Controle de peso diário
- ❌ Integrações externas
- ❌ Metas complexas
- ❌ Notificações push
- ❌ Funcionamento offline (offline-first)
- ❌ Exclusão de conta

## 🏗️ Arquitetura

- **Tipo:** Monolito web simples

**Justificativa:**
- Menos complexidade
- Menor custo
- Mais rápido para evoluir

## 🛠️ Stack Tecnológica

### Backend
- Python 3.11+
- Django 5.0+
- Django REST Framework

**Motivo:** robustez, produtividade e maturidade para regras de negócio.

### Frontend
- Django Templates
- Bootstrap 5 (mobile-first)
- Chart.js (gráficos)

**Motivo:** simplicidade, rapidez e menor custo de manutenção.

### Banco de Dados
- SQLite (desenvolvimento)
- PostgreSQL (produção)

### Timezone
- `TIME_ZONE`: `America/Sao_Paulo`
- `USE_TZ = True`

**Regra:** horários persistidos em **UTC** e exibidos no timezone configurado.

## 🔐 Autenticação e Usuários

- Autenticação desde o MVP
- Modelo: **Email + senha**
- Um usuário por conta
- Email é o identificador único (login)

**Segurança:**
- Senha com hash seguro (Django default – PBKDF2/bcrypt)
- Sessão autenticada via Django Sessions

## 📊 Modelo de Dados

### `CustomUser`
- `id`
- `name`
- `email` (único)
- `password_hash`
- `fasting_goal_hours` (float, padrão: 16.0)
- `created_at`

### `FastingRecord`
- `id`
- `user_id`
- `start_time`
- `end_time` (nullable)
- `duration_hours` (calculado automaticamente)
- `fasting_type` (intermittent, extended, other)
- `energy_level` (1–3)
- `focus_level` (1–3)
- `mood_level` (1–3)
- `notes` (até 255 caracteres)
- `created_at`

**Observação:** O jejum sempre pertence ao **dia de início** (`start_time`), independentemente de atravessar dias.

### `WeightRecord`
- `id`
- `user_id`
- `weight`
- `reference_month` (YYYY-MM)
- `created_at`

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd controle-jejum
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrations:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

7. Acesse o sistema:
- Aplicação: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📱 Uso do Sistema

### 1. Registro e Login
- Acesse a página inicial e clique em "Cadastre-se"
- Preencha: nome, email, senha e meta de jejum (ex: 16 horas)
- Faça login com seu email e senha

### 2. Dashboard
- Visualize seu status atual (em jejum ou alimentado)
- Veja estatísticas dos últimos 7 dias:
  - Média de horas em jejum
  - Dias que atingiram a meta
  - Sequência (streak) de dias consecutivos
- Acompanhe o gráfico de duração dos jejuns

### 3. Iniciar/Encerrar Jejum
- Clique em "Iniciar Jejum" quando começar seu período de jejum
- O cronômetro mostrará o tempo decorrido em tempo real
- Clique em "Encerrar Jejum" quando terminar
- A duração será calculada automaticamente

### 4. Histórico
- Acesse "Histórico" no menu
- Visualize todos os seus jejuns anteriores
- Clique em "Editar" para ajustar horários ou adicionar informações
- Adicione níveis de energia, foco, humor e observações

### 5. Controle de Peso
- Acesse "Peso" no menu
- Registre seu peso mensalmente
- Acompanhe a evolução e variação entre os meses

### 6. Tema Claro/Escuro
- Clique no ícone de lua/sol no menu para alternar entre os temas
- A preferência é salva automaticamente

## 🔒 Regras de Negócio

1. Apenas **um jejum ativo** por usuário
2. Não é permitido **encerrar jejum inexistente**
3. `duration_hours` é **sempre calculado pelo sistema**
4. Escalas fixas de **1 a 3** para energia, foco e humor
5. Observações (`notes`) limitadas a **255 caracteres**
6. Não é permitido **criar ou editar** jejuns com **sobreposição de horários**
7. Edição de jejuns passados é permitida, desde que todas as validações sejam respeitadas
8. Tentativas inválidas retornam **erro** (sem "auto-correção")

## 📈 Cálculos

### Duração do Jejum
```
duration_hours = end_time - start_time (em horas decimais)
```

### Média Semanal
Média de `duration_hours` dos **últimos 7 dias corridos** baseada no **dia de início** do jejum.

### Consistência
Contagem de dias em que `duration_hours >= fasting_goal_hours`

### Streak
Dias consecutivos em que `duration_hours >= fasting_goal_hours`. O streak **quebra imediatamente** no primeiro dia abaixo do padrão ou sem jejum.

## 🚢 Deploy

Para instruções detalhadas de deploy em produção, consulte o arquivo [DEPLOY.md](DEPLOY.md).

## 📝 Estrutura do Projeto

```
controle-jejum/
├── core/                   # App principal
│   ├── models.py          # Models (CustomUser, FastingRecord, WeightRecord)
│   ├── views.py           # Views
│   ├── forms.py           # Forms
│   ├── admin.py           # Configuração do Admin
│   └── migrations/        # Migrations do banco
├── fasting_life/          # Configurações do projeto
│   ├── settings.py        # Configurações
│   ├── urls.py            # URLs
│   └── wsgi.py            # WSGI
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── auth/              # Templates de autenticação
│   ├── dashboard/         # Templates do dashboard
│   ├── fasting/           # Templates de jejum
│   └── weight/            # Templates de peso
├── static/                # Arquivos estáticos
│   ├── css/               # CSS customizado
│   └── js/                # JavaScript
├── requirements.txt       # Dependências Python
├── manage.py              # Script de gerenciamento Django
└── README.md              # Este arquivo
```

## 🎨 Tema e Design

- **Cor primária:** Laranja (#ff7f50)
- **Modos:** Claro e Escuro
- **Framework CSS:** Bootstrap 5
- **Ícones:** Bootstrap Icons
- **Gráficos:** Chart.js
- **Responsividade:** Mobile-first

## 🧪 Testes

Para testar o sistema:

1. Crie uma conta de usuário
2. Inicie um jejum e aguarde alguns segundos
3. Encerre o jejum e verifique a duração calculada
4. Tente iniciar outro jejum (deve dar erro - apenas um jejum ativo)
5. Edite um jejum passado
6. Tente criar sobreposição de horários (deve dar erro)
7. Registre peso mensal
8. Verifique as estatísticas e gráficos no dashboard

## 📄 Licença

Este projeto é um MVP para uso pessoal.

## 👨‍💻 Desenvolvimento

Desenvolvido seguindo os princípios de simplicidade, automação e baixo custo de manutenção.

Para dúvidas ou sugestões, consulte a documentação técnica em [documento_decisoes_tecnicas.md](documento_decisoes_tecnicas.md).
