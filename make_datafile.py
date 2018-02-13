"""
Using sports-reference.com to create .csv files with data for first round
games in a given year"s tournament.
"""

import bs4
import requests
import logging

logging.basicConfig(level = logging.INFO)

def get_team_stats(team_url):
    """calculates stats for the team with that url"""

    logging.info("get_team_stats: entered")
    logging.info("get_team_stats: get response from" + team_url)
    response = requests.get(team_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    stats = {
            "games": 0,
            "fg": 0,
            "fga": 0,
            "fg%": 0.0,
            "3p": 0,
            "3pa": 0,
            "3p%": 0.0,
            "2p": 0,
            "2pa": 0,
            "2p%": 0.0,
            "ft": 0,
            "fta": 0,
            "ft%": 0.0,
            "drb": 0,
            "orb": 0,
            "ast": 0,
            "stl": 0,
            "blk": 0,
            "tov": 0,
            "pts": 0,
            "opp_pts": 0,
            "poss": 0,
            "ts%": 0.0,
            "efg%": 0.0,
            "to%": 0.0,
            "ftr": 0.0,
            "ortg": 0.0,
            "drtg": 0.0,
            "sos": 0.0
            }

    # read off values from sports-ref table
    logging.info("get_team_stats: getting stats from the soup")
    tr_stats = soup.find("table", id = "team_stats").find_all("tr")[1]
    stats["games"] = int(tr_stats.find("td", {"data-stat": "g"}).text)
    stats["fg"] = int(tr_stats.find("td", {"data-stat": "fg"}).text)
    stats["fga"] = int(tr_stats.find("td", {"data-stat": "fga"}).text)
    stats["fg%"] = float(tr_stats.find("td", {"data-stat": "fg_pct"}).text)
    stats["3p"] = int(tr_stats.find("td", {"data-stat": "fg3"}).text)
    stats["3pa"] = int(tr_stats.find("td", {"data-stat": "fg3a"}).text)
    stats["3p%"] = float(tr_stats.find("td", {"data-stat": "fg3_pct"}).text)
    stats["2p"] = int(tr_stats.find("td", {"data-stat": "fg2"}).text)
    stats["2pa"] = int(tr_stats.find("td", {"data-stat": "fg2a"}).text)
    stats["2p%"] = float(tr_stats.find("td", {"data-stat": "fg_pct"}).text)
    stats["ft"] = int(tr_stats.find("td", {"data-stat": "ft"}).text)
    stats["fta"] = int(tr_stats.find("td", {"data-stat": "fta"}).text)
    stats["ft%"] = float(tr_stats.find("td", {"data-stat": "ft_pct"}).text)
    stats["drb"] = int(tr_stats.find("td", {"data-stat": "drb"}).text)
    stats["orb"] = int(tr_stats.find("td", {"data-stat": "orb"}).text)
    stats["ast"] = int(tr_stats.find("td", {"data-stat": "ast"}).text)
    stats["stl"] = int(tr_stats.find("td", {"data-stat": "stl"}).text)
    stats["blk"] = int(tr_stats.find("td", {"data-stat": "blk"}).text)
    stats["tov"] = int(tr_stats.find("td", {"data-stat": "tov"}).text)
    stats["pts"] = int(tr_stats.find("td", {"data-stat": "pts"}).text)
    
    tr_opp_stats = soup.find("table", id = "team_stats").find_all("tr")[3]
    stats["opp_pts"] = \
            int(tr_opp_stats.find("td", {"data-stat": "opp_pts"}).text)

    # estimate number of posessions
    stats["poss"] = 0.5 * ((stats["fga"] + 0.4 * stats["fta"] - 1.07 * \
            (stats["orb"] / (stats["drb"] + stats["orb"])) * \
            (stats["fga"] - stats["fg"]) + stats["tov"]) + \
            (stats["fga"] + 0.4 * stats["fta"] - 1.07 * \
            (stats["orb"] / (stats["drb"] + stats["orb"])) * \
            (stats["fga"] - stats["fg"]) + stats["tov"]))

    # calculate "advanced" stats - edited by Matt on 2/13/18
    logging.info("get_team_stats: calculating advanced stats")
    stats["ts%"] = stats["pts"] / (2 * (stats["fga"] + 0.44 * stats["fta"]))
    stats["efg%"] = (0.5 * stats["3p"] + stats["fg"]) / stats["fga"]
    stats["to%"] = stats["tov"] / stats["poss"] #changed to% to tov
    # can"t get orb% because don"t have opponent defensive rebounds
    stats["ftr"] = stats["fta"] / stats["fga"] # Note for some reason this is producing 0, not sure why
    stats["ortg"] = stats["pts"] / stats["poss"]
    stats["drtg"] = stats["opp_pts"] / stats["poss"]

    # get strength of schedule
    logging.info("get_team_stats: getting strength of schedule")
    div_meta = soup.find("div", id = "meta")
    sos_text = ""
    for p in div_meta.find_all("p"):
        if p.strong is not None:
            if p.strong.text == "SOS:":
                stats["sos"] = float(p.text.split()[1])
                break

    logging.info("get_team_stats: exiting")
    return stats

def write_team_stats(f, stats):
    """writes the team stats in order in the file"""

    logging.info("write_team_stats: entered")
    f.write(str(stats["fg%"]) + ",")
    f.write(str(stats["3p%"]) + ",")
    f.write(str(stats["2p%"]) + ",")
    f.write(str(stats["ts%"]) + ",")
    f.write(str(stats["efg%"]) + ",")
    f.write(str(stats["to%"]) + ",")
    f.write(str(stats["ftr"]) + ",")
    f.write(str(stats["ortg"]) + ",")
    f.write(str(stats["drtg"]) + ",")
    f.write(str(stats["sos"]))
    logging.info("write_team_stats: exiting")

def make_yearfile(year):
    """makes file for a single year"""

    logging.info("make_yearfile: entered")
    file_name = "ncaa" + str(year) + ".csv"
    f = open(file_name, "w")
    logging.info("make_yearfile: writing to: " + file_name)
    f.write("seed,team,score,fg%,3p%,2p%,ts%,efg%,to%,ftr,ortg,drtg,sos\n")

    # load the webpage
    sports_ref_url = "https://www.sports-reference.com"
    year_url = sports_ref_url + "/cbb/postseason/" + str(year) + "-ncaa.html"
    logging.info("make_yearfile: getting response from " + year_url)
    response = requests.get(year_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # the page is organized by round
    rounds = soup.find_all("div", {"class": "round"})
    for i in range(0, 20, 5):
        rd = rounds[i]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]

            spans = game.find_all("span")
            links = game.find_all("a")

            logging.info("make_yearfile: %s", links[0].text)
            f.write(spans[0].text + ",") # higher seed
            f.write(links[0].text + ",") # name
            f.write(links[1].text + ",") # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            logging.info("make_yearfile: %s", links[2].text)
            f.write(spans[1].text + ",") # lower seed
            f.write(links[2].text + ",") # name
            f.write(links[3].text + ",") # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

    f.close()
    logging.info("make_yearfile: exiting")


for year in range(2000, 2007):
    make_yearfile(year)
