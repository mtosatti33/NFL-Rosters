import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
from config import *

urlRoster = 'https://www.{}.com/team/players-roster/'
urlTransactions = 'https://www.{}.com/team/transactions/'


class Downloader:
    def __init__(self):
        pass

    @staticmethod
    def pull_rosters(team_id):
        """
            Download the roster for each team

            Param(s):
                team_id: Dict for referred team

            Returns: None
        """

        print('     -> Downloading rosters')

        # Create dir if dir not exists
        if not os.path.exists("rosters"):
            os.mkdir("rosters")

        df = pd.read_html(urlRoster.format(team_id["Site"]))

        if isOffseason:
            for i in range(0, len(df)):
                df[i]['Team'] = team_id["Abbrev"]

                if i == 0:
                    df[i].to_csv(f'{folders[0]}/{team_id["Site"]}.csv', sep=';')
                else:
                    df[i].to_csv(f'{folders[0]}/{team_id["Site"]}.csv', sep=';', mode='a', header=False)
        else:
            df[0]['Team'] = team_id["Abbrev"]
            df[0].to_csv(f'{folders[0]}/{team_id["Site"]}.csv', sep=';')

    @staticmethod
    def pull_transactions(team_id):
        """
            Download the transactions for each team

            Param(s):
                team_id: Dict for referred team

            Returns: None
        """
        print('     -> Downloading transactions')

        # Create dir if dir not exists
        if not os.path.exists("transactions"):
            os.mkdir("transactions")

        r = requests.get(urlTransactions.format(team_id["Site"]))
        bs = BeautifulSoup(r.content, "html.parser")

        transac_list = []

        row_list = bs.find_all(class_="d3-o-transactions__row")

        for item in row_list:

            date_list = item.find_all(class_='nfl-t-list__transaction-date')

            for date, item2 in zip(date_list, item.find_all('li')):
                transac_list.append(date.get_text() + ', ' + item2.find('p').get_text() + ', ' + team_id["Abbrev"])

        df = pd.DataFrame(transac_list)

        df.to_csv(f'{folders[1]}/{team_id["Site"]}.csv', sep=',')
