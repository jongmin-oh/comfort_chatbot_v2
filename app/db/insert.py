from app.db.create import create_answer_table, is_exist_table
from app.config import paths

import pandas as pd

def insert_answer(engine):
    if not is_exist_table(engine, 'answer'):
        create_answer_table(engine)
        df = pd.read_excel(paths.DATA_DIR.joinpath("base_datasets.xlsx"))
        df.to_sql(name="answer", con=engine, if_exists='append',
                    chunksize=1000, method='multi', index=False)
        print(" answer table inserted ")
    else:
        print(" answer table already exists ")