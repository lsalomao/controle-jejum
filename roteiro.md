Roteiro de Implementação: MVP Controle de Jejum
Fase 0 — Planejamento (Concluída)
Decisões: Auth por Email, Timezone America/Sao_Paulo, Tema Laranja (Light/Dark), Validação de sobreposição via erro, Gráfico no Dashboard.

Fase 1 — Setup e Arquitetura de Dados (1-2 dias)
Bootstrap Django:
Configurar CustomUser (identificador por Email).
Configurar settings.py: TIME_ZONE = 'America/Sao_Paulo', USE_TZ = True.
Modelagem de Dados (Core):
FastingRecord: Implementar lógica de clean() para bloquear sobreposição de horários.
FastingRecord: Implementar save() para cálculo automático de duration_hours.
WeightRecord: Implementar restrição de um registro por mês por usuário.
Admin: Configurar Django Admin para gerenciar usuários e registros durante o desenvolvimento.

Fase 2 — Autenticação e Perfil (1 dia)
Fluxo de Acesso:
Telas de Login e Cadastro (Bootstrap 5).
Configuração de fasting_goal_hours no cadastro (padrão 16h).
Área Logada: Garantir que todos os registros sejam filtrados por request.user.

Fase 3 — O "Core Loop": Controle de Jejum (2 dias)
Ação em Tempo Real:
Botão Iniciar Jejum (Cria registro com start_time=now).
Botão Encerrar Jejum (Atualiza end_time=now, dispara cálculo de duração).
Estado do Dashboard:
Lógica para detectar se existe um jejum ativo e exibir o cronômetro (tempo decorrido).
Feedback Visual: Mensagens de erro (Django Messages) para tentativas de sobreposição.

Fase 4 — Histórico e Edição (1-2 dias)
Lista Cronológica:
Exibição baseada no dia de início do jejum.
Paginação simples.
Edição Retroativa:
Formulário para ajustar start_time ou end_time de registros passados.
Re-validação: O sistema deve impedir que a edição crie uma sobreposição com outros registros existentes.

Fase 5 — Inteligência: Stats e Streak (2 dias)
Cálculos de Performance:
Média 7 dias: Média de horas dos últimos 7 dias (baseado no start_time).
Consistência: Dias que atingiram a meta.
Streak: Lógica de dias consecutivos. Quebra se o dia não atingir a meta ou se não houver registro no dia.
Dashboard Indicators: Exibição desses números em cards destacados.

Fase 6 — Visualização e Peso (1-2 dias)
Gráfico de Duração:
Integração com Chart.js no Dashboard.
Eixo X: Dias | Eixo Y: Horas de Jejum.
Módulo de Peso:
Tela simples para registrar o peso do mês atual.
Lista de evolução mensal.

Fase 7 — UI/UX "Orange Theme" (1 dia)
Refinamento Visual:
Aplicação da paleta Laranja em botões, ícones e alertas.
Implementação do seletor Light/Dark mode.
Responsividade (foco total no uso via celular).

Fase 8 — Qualidade e Deploy (2 dias)
Testes de Stress:
Testar exaustivamente a sobreposição (ex: tentar criar jejum dentro de outro, ou um que comece antes e termine depois de um existente).
Deploy VPS:
Configuração Gunicorn + Nginx.
Banco PostgreSQL.
Script de backup diário do banco.