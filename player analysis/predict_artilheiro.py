# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:36:44 2022

@author: marcos
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
################################################
## PERGUNTAS - PROBLEMA DE NEGÓCIO
################################################
# Prever o artilheiro da Premier League 2022-2023

################################################
## IMPORT DATA
################################################
pais = "inglaterra"
df = pd.read_csv(
    "database/" + pais + ".csv",
    sep="\t",
)

original1 = df

#%%
################################################
## PREPARE DATA
################################################
df["media"] = df["goals"] / df["matchs"]
df["media_a"] = df["assists"] / df["matchs"]
df["media"] = np.where(df["matchs"] == 0, 0, df["media"])
df["media_a"] = np.where(df["matchs"] == 0, 0, df["media_a"])

df["y"] = df["goals"]
df = df.drop(labels=["country", "ovr", "goals", "image"], axis=1)
df = df.rename(columns={"y": "goals"})
#%%
df["age"] = np.where(df["age"] > 55, 0, df["age"])
df = df.drop(df[df.position == "GOL"].index)
df = df.drop(df[df.position == "ZAG"].index)
df = df[df.year > 1995]
df = df[df.matchs > 10]

original2 = df

#%%
################################################
## EXPLORE DATA
################################################

plt.scatter(df["matchs"], df["goals"])
plt.xlabel("matchs")
plt.ylabel("goals")
plt.title("Distribuição")
plt.show()

goals27 = df[df["age"] == 27]
plt.scatter(goals27["matchs"], goals27["goals"])
plt.xlabel("matchs")
plt.ylabel("goals")
plt.title("Age = 27")
plt.show()

plt.scatter(df["age"], df["goals"])
plt.xlabel("age")
plt.ylabel("goals")
plt.title("Distribuição")
plt.show()

count = df["age"].value_counts().sort_index()
count.plot()


#%%average goals per age


#%%
################################################
## PREPARE DATA
################################################
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

################################################
## ONE HOT ENCODER
################################################
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


def encode(df, column_name):
    encoder = OneHotEncoder(handle_unknown="ignore")
    enc_df = encoder.fit_transform(df[column_name].values.reshape(-1, 1)).toarray()
    enc_df = pd.DataFrame(enc_df)
    return enc_df


df1 = encode(df, "club")
df2 = encode(df, "position")
df3 = encode(df, "name")

geral = pd.concat([df1, df2, df3], axis=1)

################################################
# SPLIT THE DATASET
################################################
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
#%%
################################################
## ML MODELS
################################################


#%%
################################################
## EVALUATE
################################################
# Confusion Matrix


#%%
################################################
## VISUALIZE DATA
################################################
