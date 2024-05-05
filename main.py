# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 12:44:17 2022

@author: marcos
"""

from scripts.functions import (
    get_list_clubs, read_current_database, save_new_clubs
)
import pandas as pd

###############################################################################
# MAIN
###############################################################################


def main():

    # manual selection of clubs
    club_url = [
            "hangzhou"
    ]

    # club_url = get_list_clubs()

    df_imported = read_current_database()

    years = [2024, 2024]
    save_new_clubs(df_imported, club_url, years)

    # df = alterate_goalkeepers(df)


###############################################################################
# RUN
###############################################################################

main()
