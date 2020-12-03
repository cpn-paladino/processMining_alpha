# Use a imagem oficial como imagem principal.
FROM python:3.8
#FROM node:current
#FROM ubuntu:18.04

RUN mkdir -p /usr/src/app

# apt-get install --no-install-recommends --no-install-suggests -y \
# Define o diretório de trabalho.
WORKDIR /usr/src/app

# Copia o arquivo do gitlab para o local atual.
#COPY package*.json ./

# Update system
RUN apt-get update -y -q

# install linux apps
RUN apt-get install graphviz 
RUN apt-get install -y unzip xvfb
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
RUN apt install -y build-essential apt-transport-https libgbm-dev
RUN apt-get update -y

# install python packages
RUN pip install tk
RUN pip install graphviz
RUN pip install --upgrade google-cloud-storage
RUN pip install urllib3
RUN pip install flask
RUN pip install bs4
RUN pip install python-dateutil
RUN pip install python-dotenv
RUN pip install wsgiserver
RUN pip install gevent

# Copia o restante do código-fonte do aplicativo do host para o sistema de arquivos de imagem.
COPY . .

EXPOSE 8080 

# Execute o comando especificado dentro do contêiner.
CMD [ "python", "index.py" ]