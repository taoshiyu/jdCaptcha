FROM python:3.10-slim-trixie
LABEL maintainer="captcha"

#RUN sed -i "s@http://deb.debian.org@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
#RUN sed -i 's|security.debian.org/debian-security|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y curl
RUN apt install -y curl gcc default-libmysqlclient-dev

RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt-get install -y nodejs

RUN npm config set prefix /usr/local
RUN npm cache clean --force
RUN rm -rf /usr/local/lib/node_modules
RUN npm install -g npm
WORKDIR app


RUN npm install  -g crypto-js sm-crypto ua-parser-js
RUN npm install  -g @babel/parser @babel/traverse @babel/generator @babel/template @babel/types
RUN npm install -g jsdom
RUN npm install -g express

RUN ls -la /usr/local/lib/node_modules/ | grep crypto
RUN npm list -g | grep crypto-js
# 很重要 不然找不到包
ENV NODE_PATH=/usr/local/lib/node_modules
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip cache purge
RUN apt-get install -y libgl1  libglib2.0-0 libsm6 libxext6 libxrender-dev libxcb1 libx11-xcb1 libxcb-xinerama0

COPY . .