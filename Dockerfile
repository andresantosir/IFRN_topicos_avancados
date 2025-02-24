# Usa uma imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Expõe a porta em que a aplicação vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]