from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


url = "https://www.fiba.basketball/basketballworldcup/2023/games"
main_bs = bs(requests.get(url).text, "html.parser")
game_items = main_bs.find_all("div", {"class": "game_item"})
data = []

for b_ in game_items:
    l_country = b_.find("table", {"class": "country left"}).find("span", {"class": "long"}).text.strip()
    r_country = b_.find("table", {"class": "country right"}).find("span", {"class": "long"}).text.strip()
    datetime = b_.find("a").get("data-gmt-time")
    arena = b_.find("div", {"class": "more_info"}).text.strip().replace("City, Arena: ", "")
    year, month, day, hour, minutes, gmt = datetime.split(",")
    subject = f"{l_country} vs. {r_country}"
    date = f"{month}/{day}/{year}"
    cet_hour = int(hour) - int(gmt[5]) + 2
    start_time = f"{cet_hour}:{minutes}" if arena != "Time TBC" else "00:00"
    end_time = f"{cet_hour + 2}:{minutes}" if arena != "Time TBC" else "00:00"
    all_day_event = True if arena == "Time TBC" else False
    location = arena if arena != "Time TBC" else ""
    data.append([subject, date, date, start_time, end_time, all_day_event, location])

df = pd.DataFrame(data, columns=["Subject", "Start Date", "End Date", "Start Time",
                                 "End Time", "All Day Event", "Location"])
df.to_csv("../data/mundobasket_calendar.csv")

