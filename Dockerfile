FROM python:3.9

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN git clone 'https://github.com/datatoolsrc2023/vaccine_data.git'

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /app

RUN pip install -r /app/requirements.txt

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]