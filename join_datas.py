# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 17:05:00 2022

@author: marcos
"""
import pandas as pd
import os

from club_urls import club_urls


# %%
# JOIN DATASETS
# Se voce tem varios datasets de paises e quer dividir em um dataset global
def join_datasets():
    df_all = pd.DataFrame()
    for filename in club_urls():
        print(filename)
        df_imported = pd.read_csv(
            "database/" + filename + ".csv",
            sep="\t",
        )
        df_all = pd.concat([df_imported, df_all], axis=0)
    df_all.to_csv(
        "database/all.csv",
        sep="\t",
        encoding="utf-8",
        index=False,
    )


# %%
# SPLIT DATASETS
# Se voce formou o dataset_all e quer dividir em subarquivos para cada pais
def split_dataset():
    df_imported = pd.read_csv(
        "jogadores.csv",
        sep="\t",
    )
    for filename in club_urls():
        df_country = pd.DataFrame()
        for club in club_urls()[filename]:
            df = df_imported[df_imported.club == club]
            df_country = pd.concat([df_country, df], axis=0)
        if not os.path.isdir("database"):
            os.makedirs("database")
        print(f"Saving filename {filename}")
        df_country.to_csv(
            "database/" + filename + ".csv",
            sep="\t",
            encoding="utf-8",
            index=False,
        )


split_dataset()
