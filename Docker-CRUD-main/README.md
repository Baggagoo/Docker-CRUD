# Sistema CRUD Escolar com Docker, Flask, PostgreSQL, Prometheus e Grafana

Este projeto foi desenvolvido como parte do nosso aprendizado em desenvolvimento de sistemas modernos usando containers Docker, banco de dados relacional, monitoramento e boas práticas de programação. Aqui, construimos uma API para gerenciar uma escola fictícia, aplicando conceitos que aprendi durante esse semestre.

## O que o sistema faz?

- **Gerencia alunos, professores, pagamentos, presenças, atividades e usuários** através de uma API REST feita com Flask.
- **Armazena os dados no PostgreSQL**, um banco de dados robusto e muito usado no mercado.
- **Utiliza Docker** para facilitar a instalação e execução de todos os serviços, sem dor de cabeça com dependências.
- **Monitora o banco de dados com Prometheus** e **exibe gráficos no Grafana**, aprendendo na prática como grandes sistemas são acompanhados em produção.
- **Inclui testes automatizados** para garantir que as principais funcionalidades estão funcionando corretamente.
- **Registra logs centralizados** para facilitar a auditoria e o acompanhamento das operações do sistema.

## Como funciona?

- O backend é um app Flask, organizado em módulos (alunos, professores, pagamentos, etc.), cada um com suas rotas e operações CRUD.
- O banco de dados PostgreSQL é inicializado com tabelas e dados básicos via script SQL.
- O Prometheus coleta métricas do banco e o Grafana mostra dashboards para visualização.
- Tudo roda em containers Docker, então basta ter o Docker instalado para subir o sistema inteiro.

## Como usar?

1. **Clone o repositório:**

GitHub Copilot
git clone https://github.com/seuusuario/Docker-CRUD-main.git cd Docker-CRUD-main

2. **Suba os containers (ajuste conforme seu docker-compose):**

docker-compose up --build

3. **Acesse a API:**
- Acesse `http://localhost:8000` para ver a mensagem de boas-vindas.
- Use ferramentas como Postman ou Insomnia para testar as rotas (ex: `/alunos`, `/professores`, etc).

4. **Acesse o Grafana:**
- Normalmente em `http://localhost:3000` (login padrão: admin/admin).

## O que eu aprendi fazendo esse projeto?

- Como criar e organizar uma API RESTful com Flask.
- Como usar Docker para isolar e facilitar o deploy de aplicações.
- Como conectar o Flask ao PostgreSQL e criar scripts de inicialização do banco.
- Como monitorar serviços com Prometheus e criar dashboards no Grafana.
- Como escrever testes automatizados com pytest.
- Como registrar logs de operações para facilitar a manutenção e auditoria.

## Observações

- Este projeto é didático, mas já segue boas práticas do mercado.
- Fique à vontade para sugerir melhorias ou relatar problemas!

---
