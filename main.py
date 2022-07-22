from data import team_dict
from downloader import Downloader
from condenser import Condenser


def main():
    for i in team_dict.keys():
        print("---------------------------------------------")
        print("scrapping {}".format(team_dict[i]["Name"]))
        Downloader.pull_rosters(team_dict[i])
        Downloader.pull_transactions(team_dict[i])

    Condenser.condense_all_data()


if __name__ == "__main__":
    main()
