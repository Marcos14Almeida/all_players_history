# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 00:24:08 2022

@author: marcos
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


################################################
## PERGUNTAS - PROBLEMA DE NEGÓCIO
################################################
# Obter lista com o nome dos times

# Obter a escalação de um time em um ano
# Ex Palmeiras 1999 x Corinthians 2012

# Quem foi o artilheiro de cada ano?
# Quem teve a maior média de gols a cada ano?
# Qual a média dos 10 maiores artilheiros por ano?
# Quantos jogadores fizeram mais que 5 gols por ano?

# Quem deu mais assistencia a cada ano?
# Quem teve a maior média de assistencias a cada ano?
# Qual a média dos 10 maiores assistentes por ano?
# Quantos jogadores fizeram mais que 5 assistencias por ano?

# Qual o pais de origem dos jogadores?
# Esse numero tem mudado ao longo dos anos?

# Quais os jogadores com mais gols ao longo da carreira no Brasil?


################################################
## IMPORT DATA
################################################
pais = "inglaterra"
df = pd.read_csv(
    "database/" + pais + ".csv",
    sep="\t",
)

df = pd.read_csv("jogadores.csv", sep="\t")

#%%
################################################
## FILTER DATA
################################################

#%%
################################################
## EXPLORE DATA
################################################

df.head()
df.shape()
df.info()
df.describe(include=object)
df["year"].value_counts()


def choose_teamYear(df, club_name, year):
    time = df[(df["club"] == club_name) & (df["year"] == year)]
    return time


time = choose_teamYear(df, "palmeiras", 1999)
print(time["name"])
time = choose_teamYear(df, "corinthians", 2012)
print(time["name"])

df.groupby("name", sort=True)["goals"].sum()

#%%
################################################
## VISUALIZE DATA
################################################

xpoints = np.array([0, 6])
ypoints = np.array([0, 250])

plt.plot(xpoints, ypoints)
plt.show()
