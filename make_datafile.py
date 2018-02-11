"""
Using sports-reference.com to create .csv files with data for first round
games in a given year's tournament.
"""

def make_yearfile(year):
    """makes file for a single year"""

    f = open("ncaa" + str(year) + ".csv", "w")
    f.write("Hello, world!")
    f.close()


