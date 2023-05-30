import subprocess
import os
from pathlib import Path
from prefect import task

@task
def convert():
    path = Path(os.path.abspath(__file__)).parent
    files = os.listdir(path)


    for file in files:
        if file.startswith('NIS'):
            print('converting', file)
            command = ['Rscript', f'{path}/{file}']
            subprocess.run(command)
        