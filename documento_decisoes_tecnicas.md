# Documento de Decisões Técnicas – MVP Web de Controle de Jejum

## 1. Objetivo do Sistema

Desenvolver um MVP web simples para **registrar períodos de jejum**, **calcular automaticamente** sua duração e **apresentar indicadores claros** de consistência e impacto diário.

### 1.1 Princípios

- **Simplicidade acima de tudo**
- **Automação sempre que possível**
- **Poucos dados, mas úteis**
- **Baixo custo** de desenvolvimento e manutenção

## 2. Escopo do MVP

### 2.1 O que o sistema FAZ

- Iniciar e encerrar jejuns
- Editar jejuns passados (**sempre respeitando validações**)
- Calcular duração automaticamente
- Registrar estado físico e mental básico
- Registrar **peso corporal (mensal)**
- Exibir histórico
- Exibir indicadores simples (média, consistência, streak)
- Exibir gráfico simples de duração do jejum por dia

### 2.2 O que o sistema NÃO faz (por enquanto)

- Contagem de calorias
- Controle de peso diário
- Integrações externas
- Metas complexas
- Notificações push
- Funcionamento offline (offline-first)
- Exclusão de conta

## 3. Arquitetura Geral

### 3.1 Tipo

- **Monolito web simples**

### 3.2 Justificativa

- Menos complexidade
- Menor custo
- Mais rápido para evoluir

## 4. Stack Tecnológica (fechada)

### 4.1 Backend

- Python 3.11+
- Django 5.0+
- Django REST Framework

**Motivo:** robustez, produtividade e maturidade para regras de negócio.

### 4.2 Frontend

- Django Templates
- Bootstrap 5 (mobile-first)

**Motivo:** simplicidade, rapidez e menor custo de manutenção.

### 4.3 Banco de Dados

- SQLite (desenvolvimento)
- PostgreSQL (produção)

### 4.4 Timezone

- `TIME_ZONE`: **America/Sao_Paulo**
- `USE_TZ = True`

**Regra:** horários são persistidos em **UTC**, com conversão/exibição no timezone configurado.

## 5. Autenticação e Usuários

### 5.1 Estratégia

- Sistema com autenticação desde o MVP

### 5.2 Modelo

- **Email + senha**
- Um usuário por conta
- Email é o **identificador único** (login)

### 5.3 Segurança

- Senha com hash seguro (Django default – PBKDF2/bcrypt)
- Sessão autenticada via **JWT simples**

## 6. Modelo de Dados

### 6.1 Tabela: `users`

- `id`
- `name`
- `email`
- `password_hash`
- `fasting_goal_hours` (float)
- `created_at`

### 6.2 Tabela: `fasting_records`

- `id`
- `user_id`
- `start_time`
- `end_time` (nullable)
- `duration_hours`
- `fasting_type`
- `energy_level` (1–3)
- `focus_level` (1–3)
- `mood_level` (1–3)
- `notes` (até 255 caracteres)
- `created_at`

**Observação importante (transição de dias):**

- O jejum sempre pertence ao **dia de início** (`start_time`), independentemente de atravessar dias.

### 6.3 Tabela: `weight_records`

- `id`
- `user_id`
- `weight`
- `reference_month` (YYYY-MM)
- `created_at`

## 7. Regras de Negócio

1. Apenas **um jejum ativo** por usuário
2. Não é permitido **encerrar jejum inexistente**
3. `duration_hours` é **sempre calculado pelo sistema**
4. Escalas fixas de **1 a 3** para energia, foco e humor
5. Observações (`notes`) limitadas a **255 caracteres**
6. Não é permitido **criar ou editar** jejuns com **sobreposição de horários**
7. Edição de jejuns passados é permitida, desde que todas as validações sejam respeitadas
8. Tentativas inválidas devem retornar **erro** (sem “auto-correção” no MVP)

## 8. Cálculos Oficiais

### 8.1 Padrão de Jejum do Usuário

- O usuário define livremente seu padrão de jejum (ex: 12h, 14h, 16h, 18h)
- O padrão é configurável e pode ser alterado a qualquer momento
- O valor vigente no momento do cálculo é o utilizado nos indicadores

### 8.2 Duração do Jejum

- Fórmula:

$$
\text{duration\_hours} = \text{end\_time} - \text{start\_time}
$$

- Unidade: horas decimais (ex: 16.50)
- Arredondamento: duas casas decimais

### 8.3 Média Semanal

- Média de `duration_hours` dos **últimos 7 dias corridos**
- Baseada no **dia de início** do jejum

### 8.4 Consistência

- Contagem de dias em que:

$$
\text{duration\_hours} \ge \text{fasting\_goal\_hours}
$$

### 8.5 Streak

- Dias consecutivos em que:

$$
\text{duration\_hours} \ge \text{fasting\_goal\_hours}
$$

- O streak **quebra imediatamente** no primeiro dia abaixo do padrão
- **Dias sem jejum** também quebram o streak

## 9. Dashboard – Indicadores Exibidos

### 9.1 Hoje

- Status atual (em jejum / alimentado)
- Tempo atual de jejum (se ativo)

### 9.2 Últimos 7 dias

- Média de horas em jejum
- Número de dias acima do padrão configurado

### 9.3 Histórico

- Lista cronológica de jejuns
- Possibilidade de edição dos registros

### 9.4 Visual

- Gráfico simples: duração do jejum por dia
- Renderizado no frontend via Django Templates

## 10. API – Endpoints do MVP

### 10.1 Autenticação

- `POST /auth/login`
- `POST /auth/register`

### 10.2 Jejum

- `POST /fasting/start`
- `POST /fasting/end`
- `PUT /fasting/{id}` (editar jejum)
- `GET /fasting/active`
- `GET /fasting/history`
- `GET /fasting/stats`

## 11. UX – Estados Importantes

- Novo usuário sem registros
- Usuário com jejum ativo
- Usuário sem jejum ativo
- Usuário editando registro passado
- Mensagens claras de erro e sucesso

## 12. Deploy

### 12.1 Ambiente

- Produção em VPS própria

### 12.2 Infraestrutura

- Backend, frontend e banco no mesmo servidor

### 12.3 Banco

- PostgreSQL com backup diário automático

## 13. Critérios de MVP Concluído

O MVP é considerado pronto quando:

- Usuário consegue registrar e editar jejuns por 7 dias
- Dashboard exibe indicadores corretamente
- Validações impedem estados inválidos (sobreposição, jejum duplo, etc.)
- Sistema roda sem intervenção manual

## 14. Próximos Passos (fora do MVP)

- Alertas
- Exportação de dados
- Metas personalizadas
- Integrações externas
- Exclusão de conta

## 15. Conclusão

O MVP está claramente delimitado, com decisões técnicas sólidas e baixo risco de retrabalho.

Este documento é suficiente para:

- Iniciar o desenvolvimento imediatamente
- Servir como referência única de regras de negócio
- Evitar decisões improvisadas no meio da implementação
