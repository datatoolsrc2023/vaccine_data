FROM python:3.9.7   

COPY vaccines /app

WORKDIR /app

RUN pip install -r requirements.txt


ENV GOOGLE_APPLICATION_CREDENTIALS=creds/sonic-ivy-388314-e05a0e8cbdfc.json

EXPOSE 5000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "5000"]