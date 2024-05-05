import requests
from bs4 import BeautifulSoup
import pandas as pd
from scripts.player import Player
from scripts.club_urls import club_urls


def get_list_clubs():

    # List from besoccer
    # https://pt.besoccer.com/time/elenco/palmeiras/2020

    # Map of clubs to list
    club_url = []
    for filename in club_urls():
        club_url.append(club_urls()[filename])
    club_url = sum(club_url, [])

    return club_url


def read_current_database():

    # Checa se o arquivo ja existe
    print("Lendo o database existente...")
    try:
        df_imported = pd.read_csv("datasets/jogadores.csv")
        print(df_imported)
    except:
        print("\nDatabase vazio")
        df_imported = pd.DataFrame()

    return df_imported


def save_new_clubs(df_imported, club_url, years):

    print("." * 50)
    print("Searching clubs...")

    # Loop sobre todos os times desejados
    df2 = pd.DataFrame()
    for club in club_url:

        print("." * 50)
        print(f"{club}")

        search_club = True
        # If the club is not in the dataset
        if df_imported.empty or df_imported[df_imported['club'] == club].empty:
            min_year = years[0]
        else:
            min_year = df_imported[df_imported['club'] == club]['year'].max()

        if search_club:
            for year in range(min_year, years[1]+1):
                print(f" year: {year}")
                df, team_logo, team_country = web_scraping(
                    club,
                    year,
                    years[1]-1,
                    "https://pt.besoccer.com/time/elenco/" + club + "/" + str(year),
                )

                if df2.empty:
                    df2 = df
                else:
                    df2 = pd.concat([df, df2], axis=0)

                print(" Web Scraping completo")

            # Se tiver novos times, concatena e adiciona no csv
            # Se nao tiver novos times nao faz nada
            try:
                df3 = pd.concat([df_imported, df2], axis=0)
                # Unique Ids
                df3 = set_unique_ids(df3)
                df3 = df3.drop_duplicates(subset=["player_id", "year", "club"])
                filename = "datasets/jogadores.csv"
                df3.to_csv(filename, encoding="utf-8", index=False)
                print(f"\n{club} salvo em: {filename}")
            except:
                print("\nError: Sem times novos para adicionar na planilha")

        # Save club image
        filename = "datasets/club_images.csv"
        try:
            df_clubs = pd.read_csv(filename)
        except:
            df_clubs = pd.DataFrame()
        df_new = pd.DataFrame({
                "club_name": club,
                "club_country": team_country,
                "image": team_logo,
                "index": [1]
        })
        df_new = df_new.drop(columns=['index'])
        df_clubs = pd.concat([df_clubs, df_new], axis=0)
        df_clubs = df_clubs.drop_duplicates(subset=["club_name"])
        df_clubs.to_csv(filename, encoding="utf-8", index=False)


def set_unique_ids(df):
    unique_ids = df['player_id'].unique()

    unique_number = 1

    for index, row in df.iterrows():

        if row['player_id'] == 0:
            while unique_number in unique_ids:
                unique_number += 1
            # Assign the unique number to the row
            df.at[index, 'player_id'] = unique_number
            # Update the unique_list
            unique_ids = df['player_id'].unique()

    return df


def appendList(variable):

    lista = []
    for x in variable:
        lista.append(x.text.strip())

    return lista


def get_positions(names):
    # Ajuste de posições
    if len(names) > 2:
        positions = ["GOL", "GOL"]
        for i in range(2, len(names)):
            if i < len(names) / 3:
                positions.append("ZAG")
            elif i > 2 * len(names) / 3:
                positions.append("ATA")
            else:
                positions.append("MEI")
    return positions


def web_scraping(clubName, year, final_year, siteUrl):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    response = requests.get(siteUrl, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    team_country = soup.find_all("div", {"class": "ib posr"}, {"class": "flag"})
    team_logo = soup.find_all("div", {"class": "img-wrapper shield team-shield no-circle"})
    name = soup.find_all("td", {"class": "name"})
    performance = soup.find_all("td", {"data-content-tab": "team_performance"})
    infos = soup.find_all("td", {"data-content-tab": "team_info"})
    images_html = soup.find_all("img", {"loading": "lazy"})
    countries = soup.find_all("img", {"class": "w-25"})

    # transform html content to a list
    name_list = appendList(name)
    try:
        team_country = str(team_country).split('round/')[1].split(".png")[0]
        team_logo = str(team_logo).split('src="https://')[1].split("?size")[0]
    except:
        team_country = ""
        team_logo = ""
    performance_list = appendList(performance)
    infos_list = appendList(infos)
    countries_list = [str(country).split("large/")[1].split(".png")[0] for country in countries]

    images_list = []
    players_ids = []
    for image in images_html:
        if "players/" in str(image) or "nofoto" in str(image):
            images_list.append(str(image).split('src="https://')[1].split("?size")[0])
        if ("players/" in str(image)):
            players_ids.append(str(image).split("medium/")[1].split(".jpg")[0])
        if ("nofoto" in str(image)):
            players_ids.append(0)

    if len(name_list) >= 11:

        # Descarta o técnico
        if (len(images_list) > len(name_list)):
            dif = len(images_list) > len(name_list)
            images_list = images_list[dif:]

        positions_list = get_positions(name_list)

        players = []
        for i in range(len(name_list)):
            player = Player(year, clubName, name_list[i], images_list[i], countries_list[i], players_ids[i], positions_list[i])
            players.append(player)

        matchs = []
        matchs2 = []
        goals = []
        assists = []
        cards = []
        for i in range(0, len(performance_list)):
            value = int(performance_list[i])
            if i % 5 == 0:
                matchs.append(value)
            if i % 5 == 1:
                matchs2.append(value)
            if i % 5 == 2:
                if players[round(i / 5)].position == "GOL":
                    goals.append(0)
                else:
                    goals.append(value)
            if i % 5 == 3:
                assists.append(value)
            if i % 5 == 4:
                cards.append(value)

        idade = []
        altura = []
        valor = []
        ovr = []
        for i in range(0, len(infos_list)):
            if i % 4 == 0:
                ajuste_anos = final_year - year
                if len(infos_list[i]) == 0:
                    idade.append(0)
                elif int(infos_list[i]) - ajuste_anos < 16:
                    idade.append(0)
                else:
                    idade.append(
                        int(infos_list[i]) - ajuste_anos
                    )  # idade do jogador na época
            if i % 4 == 1:
                if (infos_list[i] != "-"):
                    altura.append(int(infos_list[i]))
                else:
                    altura.append(0)
            if i % 4 == 2:
                valor.append(infos_list[i])
            if i % 4 == 3:
                ovr.append(int(infos_list[i]))

        # Save to Player Class
        for i in range(0, len(altura)):
            players[i].add_infos(idade[i], altura[i], valor[i], ovr[i])
            players[i].add_stats(matchs[i], goals[i], assists[i])
            # print(players[i])

        # SAVE TO DATAFRAME
        df = pd.DataFrame(
            {
                "player_id": [player.id for player in players],
                "year": [player.year for player in players],
                "club": [player.club for player in players],
                "position": [player.position for player in players],
                "name": [player.name for player in players],
                "country": [player.country for player in players],
                "ovr": [player.ovr for player in players],
                "age": [player.age for player in players],
                "price": [player.price for player in players],
                "matches": [player.matches for player in players],
                "goals": [player.goals for player in players],
                "assists": [player.assists for player in players],
                "image": [player.image for player in players],
            }
        )

    else:
        df = pd.DataFrame()

    return df, team_logo, team_country
