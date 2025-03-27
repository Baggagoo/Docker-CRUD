FROM postgres:latest

# Adiciona o script de inicialização
COPY init.sql /docker-entrypoint-initdb.d/

# Define argumentos e variáveis de ambiente
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=escola

# Expõe a porta padrão do PostgreSQL
EXPOSE 5432

# Comando para iniciar o PostgreSQL
CMD ["postgres"]