import subprocess
import os

def convert():
    path = os.getcwd()
    path = f'{path}/tasks/00_extract/NIH_Ingest'
    files = os.listdir(path)


    for file in files:
        print('converting', file)
        command = ['Rscript', f'{path}/{file}']
        subprocess.run(command, stdout=subprocess.DEVNULL)