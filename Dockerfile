# 베이스 이미지
# FROM ubuntu:20.04
FROM python:3.9.9-buster

#설치시 질문 안나오게 설정
ARG DEBIAN_FRONTEND=noninteractive

# apt 업데이트
RUN apt-get update

# 패키지 설치
# RUN apt-get install -y build-essential curl git g++
RUN apt-get install -y curl git g++

# 디렉터리 생성
RUN mkdir /opt/comfort_chatbot_v2

# 소스코드 복사
COPY . /opt/comfort_chatbot_v2

#작업 폴더 설정
WORKDIR /opt/comfort_chatbot_v2

# pip update
RUN pip install --upgrade pip

#PyTorch 설치
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# 파이썬 패키지 설치
RUN pip install -r requirements.txt

ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN ["chmod", "+x", "./start_service.sh"]
ENTRYPOINT ["./start_service.sh"]

# 실행
# 실행 파일 지정
# -b 0.0.0.0:5000 : 모든 IP에 대해서 5000포트로 브로드캐스팅
# -w : worker의 개수. 디폴트는 1. master는 관리만 하고 실제 계산은 worker가 수행. 총 프로세스는 master + workers의 개수.
# -k gevent : 비동기적으로 worker 수행. 이 옵션이 없으면 순서대로 작업 진행.
# CMD ["python3","service.py"]
# CMD ["gunicorn", "service:app", "-b", "0.0.0.0:5000", "-w", "1", "--timeout=10", "-k", "gevent","--access-logfile", "-", "--error-logfile", "-"]