from bs4 import BeautifulSoup
import requests


def home():
    cmd = input("\n>>> ").lower().replace(" ", "")

    # Checks the userinput and performs a specific function
    if cmd == "help":
        help_page()
    elif cmd == "x":
        print("There are no players with surnames beginning with x.")
        home()
    elif 97 <= ord(cmd) <= 122:
        page = requests.get("https://www.basketball-reference.com/players/{}/".format(cmd))
        scrape_letter(page)


def help_page():
    print("Hi.")


def scrape_letter(page):
    soup = BeautifulSoup(page.text, "html.parser")

    # Finds out the total number of players whose surname begins with the inputed letter
    div = soup.find(id="players_sh")
    h2 = div.find("h2").get_text().lower()
    print("\nThere are {}:".format(h2))

    # Gets the table from page
    table = soup.find("table")
    tbody = table.find("tbody")

    # Gets the first and last year of each player's career    
    td = tbody.find_all("td")
    year_from = []
    year_to = []
    for i in td:
        if i.get("data-stat") == "year_min":
            year_from.insert(0, i.get_text())
        elif i.get("data-stat") == "year_max":
            year_to.insert(0, i.get_text())

    # Finds out the names of all the players
    th = tbody.find_all("th")
    a = []
    for i in th:
        a.insert(0, i.find("a"))

    # Prints name index, name, first year of career, and last year of career
    for player in a:
        print("{}) {}  {}-{}".format(a.index(player) + 1, player.get_text(), year_from[a.index(player)], year_to[a.index(player)]))

    player_index = int(input("\nEnter the number of the player you would like to find out more about:\n>>> "))
    scrape_player(a[player_index - 1]["href"])


def scrape_player(url):
    page = requests.get("https://www.basketball-reference.com{}".format(url))
    soup = BeautifulSoup(page.text, "html.parser")

    # Gets the player's info
    div = soup.find_all("div")
    for info in div:
        if info.get("itemtype") == "https://schema.org/Person":
            break

    # Outputs the player's info
    p = info.find_all("p")
    print("")
    for i in p:
        print(" ".join(i.get_text().split()))

    # List of stats
    stat_list = {"g": "g",
                 "gs": "gs",
                 "mp": "mp_per_g",
                 "fg": "fg_per_g",
                 "fga": "fga_per_g",
                 "fg3": "fg3_per_g",
                 "fg3a": "fg3a_per_g",
                 "ft": "ft_per_g",
                 "fta": "fta_per_g",
                 "orb": "orb_per_g",
                 "drb": "drb_per_g",
                 "trb": "trb_per_g",
                 "ast": "ast_per_g",
                 "stl": "stl_per_g",
                 "blk": "blk_per_g",
                 "tov": "tov_per_g",
                 "pf": "pf_per_g",
                 "pts": "pts_per_g",
                 "fg pct": "fg_pct",
                 "fg3 pct": "fg3_pct",
                 "ft pct": "ft_pct",
                 "pace": "pace",
                 "efg pct": "efg_pct",
                 "tov pct": "tov_pct",
                 "orb pct": "orb_pct",
                 "ft rate": "ft_rate",
                 "off": "off_rtg"}

    print("\nThese are all the possible stats you can look at:")
    for stat in stat_list:
        print(stat)

    # User inputs what stat they want to see
    data_stat = input("\nEnter the stat you want to create a chart of:\n>>> ")

    table = soup.find("table")
    th = table.find_all("th")
    td = table.find_all("td")

    # Gets all the seasons he was in the NBA/ABA
    seasons = []
    for i in th:
        if i.get("data-stat") == "season":
            try:
                test = int(i.get_text()[:2] + i.get_text()[-2:])
                seasons.append(i.get_text().replace("-", "/"))
            except Exception:
                continue

    # Gets the stats in all seasons
    stats = []
    for i in td:
        if i.get("data-stat") == stat_list[data_stat]:
            try:
                stats.append(float(i.get_text()))
            except Exception:
                if i.get_text() == "":
                    stats.append(0)

    stats = stats[:-(len(stats) - len(seasons))]
    draw_chart(seasons, stats, stat_list[data_stat])


def draw_chart(seasons, stats, data_stat):
    import matplotlib.pyplot as plt

    title_list = {"g": "Games",
                  "gs": "Games started",
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

    print(seasons)
    print(stats)
    plt.bar(seasons, stats)
    plt.title(title_list[data_stat])
    plt.xlabel("Season")
    plt.ylabel(title_list[data_stat])
    plt.show()


print("Welcome to the NBA players statistic graph generator!")
print("Type 'help' if you are new and need assistance.")
home()
