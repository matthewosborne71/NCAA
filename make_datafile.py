"""
Using sports-reference.com to create .csv files with data for first round
games in a given year's tournament.
"""

import bs4
import requests

def make_yearfile(year):
    """makes file for a single year"""

    f = open("ncaa" + str(year) + ".csv", "w")

    # load the webpage
    url = "https://www.sports-reference.com/cbb/postseason/" + \
            str(year) + "-ncaa.html"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rounds = soup.find_all("div", {"class": "round"})
    for i in range(0, 20, 5):
        rd = rounds[i]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]

            spans = game.find_all("span")
            links = game.find_all("a")

            f.write(spans[0].text + ",")
            f.write(links[0].text + ",")
            f.write(links[1].text + ",")

            f.write(spans[1].text + ",")
            f.write(links[2].text + ",")
            f.write(links[3].text + ",")

            f.write("\n")


    f.close()


