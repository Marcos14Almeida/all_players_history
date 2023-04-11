# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 12:44:17 2022

@author: marcos
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from club_urls import club_urls


def appendList(variable):
    lista = []
    for x in variable:
        lista.append(x.text.strip())
    return lista


def scrappeFromImages(variable, name_list_official):
    names = []
    images = []
    countries = []
    positions = []

    soma = 0
    for x in variable:
        x = str(x)
        name = ""
        country = ""
        # print(x)
        try:
            if "players" in x or "nofoto_jugador" in x:
                name = (
                    x.split("alt=")[1]
                    .split("loading")[0]
                    .replace('"', "")
                    .rstrip()
                    .lstrip()
                )

                try:
                    player_image = (
                        "https://cdn.resfu.com/img_data/players/medium/"
                        + x.split("medium/")[1].split("size")[0]
                    )
                except:
                    player_image = "https://cdn.resfu.com/media/img/nofoto_jugador.png?size=50x&amp;lossy=1"

                if (
                    name == name_list_official[soma]
                ):  # confere se o nome está na lista de nomes, porque se não o nome é de outro quadro/tabela
                    names.append(name)
                    images.append(player_image)
                    soma += 1
            if "flags" in x:
                country = x.split("round/")[1].split("size")[0]
                country = country.replace(".png?", "")
                countries.append(country)
        except:
            name = ""
            country = ""

    # print(names)
    # print(len(names))
    # print(countries)
    # print(images)
    # remove o primeiro elemento, porque ele pega a bandeira do treinador antes de começar
    countries.pop(0)
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

            # contra bugs
    if len(countries) > len(names):
        countries.pop(0)

    return names, images, countries, positions


def beSoccer(clubName, year, siteUrl):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    response = requests.get(siteUrl, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find_all("td", {"class": "name"})
    rendimento = soup.find_all("td", {"data-content-tab": "team_performance"})
    infos = soup.find_all("td", {"data-content-tab": "team_info"})
    country = soup.find_all("img", {"loading": "lazy"})

    # transform html content to a list
    name_list = appendList(name)
    rendimento_list = appendList(rendimento)
    infos_list = appendList(infos)

    if len(name_list) < 5:
        raise ValueError("Time com poucos jogadores")
    # Get data from images
    names, images, countries, positions = scrappeFromImages(country, name_list)

    images_list = []
    countries_list = []
    for i in range(0, len(names)):
        if names[i] in name_list:
            images_list.append(images[i])
            countries_list.append(countries[i])

    matchs = []
    matchs2 = []
    goals = []
    assists = []
    cards = []
    for i in range(0, len(rendimento_list)):
        value = int(rendimento_list[i])
        if i % 5 == 0:
            matchs.append(value)
        if i % 5 == 1:
            matchs2.append(value)
        if i % 5 == 2:
            if positions[round(i / 5)] == "GOL":
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
            ajuste_anos = 2022 - year
            if len(infos_list[i]) == 0:
                idade.append(0)
            elif int(infos_list[i]) - ajuste_anos < 16:
                idade.append(0)
            else:
                idade.append(
                    int(infos_list[i]) - ajuste_anos
                )  # idade do jogador na época
        if i % 4 == 1:
            altura.append(int(infos_list[i]))
        if i % 4 == 2:
            valor.append(infos_list[i])
        if i % 4 == 3:
            ovr.append(int(infos_list[i]))

    printar = False
    clubNames = []
    ano = []
    for i in range(0, len(name_list)):
        clubNames.append(clubName)
        ano.append(year)
        if printar:
            print("")
            print("POS:", positions[i])
            print("NOME:", name_list[i])
            print("PAIS:", countries_list[i])
            print("IMAGE:", images_list[i])
            print("JOG:", matchs[i])
            print("GOL:", goals[i])
            print("ASS:", assists[i])
            print("IDA:", idade[i])
            print("OVR:", ovr[i])

    # SAVE TO DATAFRAME
    df = pd.DataFrame(
        {
            "year": ano,
            "club": clubNames,
            "position": positions,
            "name": name_list,
            "country": countries_list,
            "matchs": matchs,
            "goals": goals,
            "assists": assists,
            "age": idade,
            "ovr": ovr,
            "image": images_list,
        }
    )

    return df


# %%
def alterate_goalkeepers(df):
    # Os goleiros quando importo o database do dataset, vem com as informações erradas
    print("Alterando os gols dos goleiros, que vem com erro do database criado...")
    zag_gol = df[(df["position"] == "ZAG") | (df["position"] == "GOL")]
    dfs = pd.DataFrame()
    for index, name in enumerate(zag_gol.name.unique()):
        print(
            f"alterando: {index}/{len(zag_gol.name.unique())} - {name}, {round(index/len(zag_gol.name.unique()),3)}%"
        )
        zags = zag_gol[(zag_gol["name"] == name)]
        # Se tiver sido mais que 1x goleiro entao é goleiro
        if len(zags.position.value_counts().index.tolist()) > 1:
            # print(zags.position.value_counts())
            zags["position"] = np.where(
                zags["position"] == "ZAG", "GOL", zags["position"]
            )
        zags["goals"] = np.where(
            np.logical_and(zags["position"] == "GOL", zags["goals"] > 0),
            0,
            zags["goals"],
        )
        zags["goals"] = np.where(zags["goals"] / zags["matchs"] > 0.5, 0, zags["goals"])
        dfs = pd.concat([dfs, zags], axis=0)
        # Remove duplicates
    zag_gol = dfs.drop_duplicates(keep="first")
    mei_ata = df[(df["position"] == "MEI") | (df["position"] == "ATA")]
    all_data = pd.concat([zag_gol, mei_ata], axis=0)
    return all_data


# %%
###############################################################################
# RUN
###############################################################################

# https://pt.besoccer.com/time/elenco/palmeiras/2020

# manual selection of clubs
club_url = [
    "valencia",
]

# Map of clubs to list
club_url = []
for filename in club_urls():
    club_url.append(club_urls()[filename])
club_url = sum(club_url, [])


# Checa se o arquivo ja existe
print("lendo o database existente...")
exception_clubname = "a"
has_database = False
try:
    df_imported = pd.read_csv(
        "jogadores.csv",
        sep="\t",
    )
    has_database = True
except:
    df_imported = pd.DataFrame(
        [
            {
                "year": 1900,
                "club": exception_clubname,
                "position": "GOL",
                "name": "a",
                "country": "br",
                "matchs": 0,
                "goals": 0,
                "assists": 0,
                "age": 30,
                "ovr": 0,
                "image": "https://cdn.resfu.com/media/img/nofoto_jugador.png?size=50x&amp;lossy=1",
            }
        ]
    )

print("Rodando a busca de clubes...")
# Loop sobre todos os times desejados
df2 = pd.DataFrame()
for club in club_url:
    if df_imported["club"].str.contains(club).any() == False:
        initial_year = 1930
        for year in range(initial_year, 2023):
            print("")
            print(f"Nova leitura: {club}/{year}")
            try:
                df = beSoccer(
                    club,
                    year,
                    "https://pt.besoccer.com/time/elenco/" + club + "/" + str(year),
                )
                print(df.name)
                if df2.empty:
                    df2 = df
                else:
                    df2 = pd.concat([df, df2], axis=0)
                print("Leitura bem sucedida")
            except ValueError:
                print("Erro: time com poucos jogadores nesse ano")

        if has_database is False:
            df_imported = df_imported.drop(
                df_imported[df_imported.club == exception_clubname].index
            )
            has_database = True
        # Se tiver novos times, concatena e adiciona no csv
        # Se nao tiver novos times nao faz nada
        try:
            df3 = pd.concat([df_imported, df2], axis=0)
            df3.to_csv("jogadores.csv", sep="\t", encoding="utf-8", index=False)
            print(f"\n{club} salvo no .csv")
        except:
            print("\nErro: Sem times novos para adicionar na planilha")

# %%
# df3 = alterate_goalkeepers(df)
# df3.to_csv("jogadores.csv", sep='\t', encoding='utf-8', index=False)
