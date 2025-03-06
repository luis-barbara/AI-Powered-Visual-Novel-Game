FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Instale dependências
RUN apt-get update && apt-get install -y \
    git \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clone o repositório do Automatic1111
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /app
WORKDIR /app

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Exponha a porta
EXPOSE 7860

# Comando para iniciar o WebUI
CMD ["python", "launch.py"]