import os
import glob
import shutil
import pandas as pd
from config import folders


def remove_dirs():
    for folder in folders:
        print(f"Trying to remove {folder} dir...")
        try:
            shutil.rmtree(folder)
        except Exception as e:
            print(f"dir {folder} can not be removed due error(s). Message:{str(e)}")


def replace_comma():
    """
            Replace Comma to blank in CSV files

            Param(s): None

            Returns: None
            """

    files = os.path.join(f"{folders[0]}/", "*.csv")

    files = glob.glob(files)

    for file in files:
        text = open(file, 'r')

        text = ''.join([i for i in text]).replace(",", "")

        x = open(file, 'w')

        x.writelines(text)
        x.close()


class Condenser:
    def __init__(self):
        pass

    @staticmethod
    def condense_all_data():
        """
        Condensed all CSV Data

        Param(s): None

        Returns: None
        """

        replace_comma()

        for folder in folders:
            print(f"Condensing {folder} files")

            files = os.path.join(f"{folder}/", "*.csv")

            files = glob.glob(files)

            df = pd.concat(map(pd.read_csv, files), ignore_index=True)
            with open(f'{folder}.csv', 'wb') as f:
                df.to_csv(f)

        remove_dirs()
