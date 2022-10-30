def scrapesite(data_stat, webpage):
    from bs4 import BeautifulSoup
    import requests

    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.find("table")
    table_data = table.find_all("td") # + table.find_all("th")
    seasons = []
    data = []

    for td in table_data:
        if td.get("data-stat") == "season":
            try:
                seasons.append(float(td.get_text().replace("-", ".")))
            except:
                continue
        elif td.get("data-stat") == data_stat:
            try:
                data.append(float(td.get_text(data_stat).replace("-", ".")))
            except:
                data.append(0)

    return seasons[::-1], data[::-1]


def draw_chart(data_stat, webpage):
    import matplotlib.pyplot as plt

    seasons, data = scrapesite(data_stat, webpage)
    title = {"age": "Age",
             "height": "Height",
             "g": "Games",
             "mp_per_g": "Minutes played per game",
             "fg_per_g": "Field goals per game",
             "fga_per_g": "Field goal attempts per game",
             "fg3_per_g": "3-pt field goals per game",
             "fg3a_per_g": "3-pt field goal attempts per game",
             "ft_per_g": "Free throws per game",
             "fta_per_g": "Free throw attempts per game",
             "orb_per_g": "Offensive rebounds per game",
             "drb_per_g": "Devensive rebounds per game",
             "trb_per_g": "Total rebounds per game",
             "ast_per_g": "Assists per game",
             "stl_per_g": "Steals per game",
             "blk_per_g": "Blocks per game",
             "tov_per_g": "Turnovers per game",
             "pf_per_g": "Personal fouls per game",
             "pts_per_g": "Points per game",
             "fg_pct": "Field goal percentage",
             "fg3_pct": "3-pt field goal percentage",
             "ft_pct": "Free throw percentage",
             "pace": "Pace",
             "efg_pct": "Effective field goal percentage",
             "tov_pct": "Turnover percentage",
             "orb_pct": "Offensive rebound percentage",
             "ft_rate": "Free throws per field goal attempt",
             "off_rtg": "Offensive rating"}

    plt.bar(seasons, data)
    plt.title(title[data_stat])
    plt.xlabel('Season')
    plt.ylabel(title[data_stat])
    plt.show()


def menu():
    print("These are the possible data stats you can input:\n")
    print("---- Per game ----")
    print("  age")
    print("  height")
    print("  g (games)")
    print("  mp_per_g")
    print("  fg_per_g")
    print("  fga_per_g")
    print("  fg3_per_g")
    print("  fg3a_per_g")
    print("  ft_per_g")
    print("  fta_per_g")
    print("  orb_per_g")
    print("  drb_per_g")
    print("  trb_per_g")
    print("  ast_per_g")
    print("  stl_per_g")
    print("  blk_per_g")
    print("  tov_per_g")
    print("  pf_per_g")
    print("  pts_per_g")
    print("---- Shooting ----")
    print("  fg_pct")
    print("  fg3_pct")
    print("  ft_pct")
    print("---- Advanced ----")
    print("  pace")
    print("  efg_pct (Effective field goal percentage)")
    print("  tov_pct")
    print("  orb_pct")
    print("  ft_rate (Free throws per field goal attempt)")
    print("  off_rtg (Offensive rating)\n")


if __name__ == "__main__":
    menu()
    data_stat = input("What would you like to look at? ")
    draw_chart(data_stat, "https://www.basketball-reference.com/leagues/NBA_stats_per_game.html")
