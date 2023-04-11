# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 23:44:54 2022

@author: marcos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "jogadores.csv",
    sep="\t",
)

#%%
def get_player(player_name):
    return (
        df[df["name"].str.contains(player_name)]
        .sort_values("year", ascending=True)
        .reset_index()
    )


nomes = ["L. Messi", "C. Ronaldo", "Neymar", "Mbappé", "E. Haaland", "R. Lewandowski"]
# nomes = ["R. Firmino","Rodrygo","Vinicius Jr.","Gabriel Jesus","Richarlison"]
list_dfs = []
for nome in nomes:
    df_temporario = get_player(nome)
    list_dfs.append(df_temporario)
    plt.plot(df_temporario["age"], df_temporario["goals"])
plt.legend(nomes)
plt.show()

#%%
def solve_2leagues_1year(name):
    dataframe = get_player(name)
    count = pd.DataFrame(dataframe["year"].value_counts())
    count = count[count["year"] > 1]
    anos = count.index
    juntar = pd.DataFrame()
    for ano in anos:
        juntar = dataframe[dataframe["year"] == ano].reset_index()
        juntar.loc[0, ["goals"]] = sum(juntar["goals"])
        juntar.loc[0, ["matchs"]] = sum(juntar["matchs"])
        juntar.loc[0, ["assists"]] = sum(juntar["assists"])
        juntar = juntar.head(1)
        juntar = juntar.drop(juntar.columns[0], axis=1)
        dataframe = dataframe[dataframe["year"] != ano]
    dataframe = (
        pd.concat([dataframe, juntar], axis=0)
        .sort_values("year", ascending=True)
        .reset_index()
    )
    return dataframe


#%%
def create_acumulative_goals_column(df):
    total_goals = 0
    coluna = []
    for index, goals in enumerate(df["goals"]):
        total_goals += goals
        coluna.append(total_goals)
    df["acumulado"] = pd.DataFrame(coluna)
    return df


# nomes = ["L. Messi","C. Ronaldo","Neymar","Mbappé","E. Haaland","R. Lewandowski"]
nomes = ["R. Firmino", "Rodrygo", "Vinicius Jr.", "Gabriel Jesus", "Richarlison"]
list_dfs = []
for nome in nomes:
    df_temporario = create_acumulative_goals_column(solve_2leagues_1year(nome))
    list_dfs.append(df_temporario)
    initial_year = df_temporario["year"][0]
    plt.plot(df_temporario["year"] - initial_year, df_temporario["acumulado"])
plt.legend(nomes)
plt.show()


#%%
# ML MODEL - PREDICT GOALS CARRER
data = create_acumulative_goals_column(get_player("Gabriel Jesus"))
X = data.loc[:, ["age"]].values
y = data.loc[:, ["acumulado"]].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=1 / 3, random_state=0
)

# Training the Simple Linear Regression model on the Training set
from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)
idade = 25
y_pred = regressor.predict([[idade]])
print(y_pred)
