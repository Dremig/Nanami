FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bundle/bin:$PATH"


RUN echo "deb https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib" > /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    file \
    libimage-exiftool-perl \
    binutils \
    pngcheck \
    ruby-full \
    ruby-dev \
    build-essential \
    git \
    steghide \
    && rm -rf /var/lib/apt/lists/*

RUN gem install zsteg

RUN zsteg -help

WORKDIR /app

COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]