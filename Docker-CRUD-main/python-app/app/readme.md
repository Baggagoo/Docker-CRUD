# Complemento do README.md

Este arquivo complementa o README principal do projeto, trazendo detalhes técnicos e práticos sobre a aplicação backend desenvolvida em Python/Flask.

---

## Descrição da Arquitetura do Backend

A aplicação backend foi desenvolvida utilizando o framework Flask, estruturada em módulos para cada entidade principal do sistema escolar (alunos, professores, pagamentos, presenças, atividades, usuários). Cada módulo possui suas próprias rotas (endpoints) e lógica de negócio, facilitando a manutenção e a escalabilidade.

- **Blueprints:** Cada módulo (ex: alunos, professores) é implementado como um Blueprint Flask, permitindo organização e separação de responsabilidades.
- **Banco de Dados:** Utiliza PostgreSQL, com conexão gerenciada por funções utilitárias centralizadas.
- **Logs:** Todas as operações importantes são registradas em um sistema de logs centralizado, facilitando auditoria e manutenção.
- **Testes:** Existem arquivos de testes automatizados para cada módulo, utilizando pytest e mocks para simular o banco de dados.
- **Documentação:** A API é documentada automaticamente com Swagger (via Flasgger), permitindo fácil consulta e testes dos endpoints.

---

## Instruções para Executar a Aplicação Python no Docker

1. **Pré-requisitos:**  
   Certifique-se de que o Docker está instalado em sua máquina.

2. **Navegue até a raiz do projeto no terminal:**
   ```sh
   cd Docker-CRUD-main

3. **Suba os containers (backend, banco de dados, etc):**
     docker-compose up --build
    **Isso irá construir e iniciar todos os serviços necessários.**

4. **A aplicação Flask estará disponível em:**
    http://localhost:8000


5. **Para parar os containers:**
    docker-compose down


**Exemplos de CRUD** 

**A- Listar Alunos** 
   GET /alunos

**B - Adicionar Aluno**
 POST /alunos
Content-Type: application/json

{
  "nome": "João Silva",
  "idade": 10,
  "turma": "5A"
}

**C - Atualizar aluno**
PUT /alunos/1
Content-Type: application/json

{
  "nome": "João Silva",
  "idade": 11,
  "turma": "6A"
}

**D- Remover aluno**
 DELETE /alunos/1

6. **Como acessar a documentação do Swagger**
  A documentação interativa da API está disponível automaticamente via Swagger (Flasgger):
  http://localhost:8000/apidocs
