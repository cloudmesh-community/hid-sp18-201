FROM python:3-onbuild

RUN apt-get update
RUN apt-get install -q -y net-tools

COPY . C:\Users\grayb\python\prac\222\final\

WORKDIR C:\Users\grayb\python\prac\222\final\

EXPOSE 8080

CMD ["make", "run"]
