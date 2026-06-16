FROM python:3.10-slim 

# instalar herramientas mínimas 

RUN apt-get update && apt-get install -y wget unzip ca-certificates git && rm -rf /var/lib/apt/lists/*  

# descargar nuclei directamente 

RUN wget https://github.com/projectdiscovery/nuclei/releases/download/v3.8.0/nuclei_3.8.0_linux_amd64.zip \ 

    && unzip nuclei_3.8.0_linux_amd64.zip \ 

    && mv nuclei /usr/local/bin/nuclei \ 

    && chmod +x /usr/local/bin/nuclei 

# instalar flask 

RUN pip install flask 

WORKDIR /app 

COPY app.py .

CMD ["python", "app.py"] 