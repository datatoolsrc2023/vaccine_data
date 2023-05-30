import polars as pl
import os
from pathlib import Path
# from ..utils import PostgresCreds figure out why this isn't importing correclty
from prefect import task, flow

@task(
    name='Filter for CSV'
)
def fileFilter(file):
    csv = file.endswith('csv')
    contents = file.find('contents')
    return csv and contents == -1

@task(
    name='convert to DFs'
)
def convertDataframe(path, csv_file):
    csv_file = f'{path}/{csv_file}'
    return pl.read_csv(csv_file, ignore_errors=True)

@task(
    name='Combine DFs'
)
def combineDataFrames(dfs):
    main_df = pl.DataFrame()

    for df in dfs.values():
        df = df.drop('')
        columns = df.columns
        for column in columns:
            df = df.with_columns(pl.col(f"{column}").cast(dtype='str'))
        main_df = pl.concat([main_df, df], how='diagonal')
    return main_df

@task(
    name='Load into PG'
)
def loadPostgres(df:pl.DataFrame):   
    # update to PostgresCreds().engine once error is figure out
    engine = 'postgresql://admin:asdf1234@0.0.0.0:5434/vaccine'
    df.write_database('vaccines', engine, if_exists='replace')

@flow
def allFilePaths(path, files):
    dfs = {}
    for file in files:
        df = convertDataframe(path, file)
        year = '20' + file[6:8]
        df = df.with_columns(year = pl.lit(year))
        dfs[file]=df
    return dfs


@flow
def nihLoad():
    path = Path(os.getcwd()) / 'data' / 'NIH_child' / 'NIH_conv'
    files = os.listdir(path)
    files = filter(fileFilter, files)
    files = list(files)
    dfs = allFilePaths(path, files)
    main_df = combineDataFrames(dfs)
    # print(main_df)
    loadPostgres(main_df)

if __name__ == '__main__':
    nihLoad()