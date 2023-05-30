from prefect import flow
from extract.NIH.convert import convert
from load.NIH_load import nihLoad

@flow
def main():
    convert()
    nihLoad()

if __name__ == '__main__':
    main()