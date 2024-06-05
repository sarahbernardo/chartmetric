#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sarah Bernardo
"""

import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
import pandas as pd

infile = 'apr_25_chtmt.csv'


def clean_data(infile):
    # read in csv
    unclean_df = pd.read_csv(infile)

    # drop any rows where more than 50% of the data is missing
    df = unclean_df.dropna(axis=1, thresh=225)
    df = df.iloc[:500]
    print(df)
    return df

def pron_df(df):
    # initialize row of 1s to count number of pronouns
    df["Counter"] = 1

    # new df of only desired cols
    pron_df = df[["Pronouns", "Solo/Group", "Counter"]].copy()

    # group by pronouns and solo/group status to account for groups registered as they/them pronouns
    pron_df = pron_df.groupby(['Pronouns', 'Solo/Group'])["Counter"].sum().reset_index()
    pron_df = pron_df.drop([0])

    return pron_df

def pron_graph(df):
    fig = px.bar(df, x="Pronouns", y="Counter",
                       color='Solo/Group', barmode='group',
                       text="Counter")
    fig.update_layout(title_text='Top 500 Artists by Pronouns')
    fig.show()

def pron_sunburst(df):
    fig = px.sunburst(df, path=['Pronouns', 'Solo/Group'],
                      values='Counter',
                      color='Pronouns')
    fig.update_layout(title_text='Distribution of Pronouns')

    fig.show()

def pie_pron(df):
    fig = px.pie(df, values='Counter', names='Pronouns', title='Population of European continent')
    fig.update_layout(title_text='Distribution of Pronouns')
    fig.show()

def measure_genres(df):
    genre_dct = {}

    # iterate through each artist's genres
    for index, row in df.iterrows():
        genr = row["Genres"]
        per_artist = genr.split(",")

        # add one count for each time a genre appears
        for each in per_artist:
            if each not in genre_dct:
                genre_dct[each] = 1
            elif each in genre_dct:
                genre_dct[each] += 1

    # sort the values
    sorted_values = sorted(genre_dct.values(), reverse=True)
    sorted_dict = {}

    for i in sorted_values:
        for k in genre_dct.keys():
            if genre_dct[k] == i:
                sorted_dict[k] = genre_dct[k]

    print(sorted_dict)
    return sorted_dict


def graph_genres(dct):
    del_lst = []

    # narrow down dictionary to any genre with more than 20 artists in it
    for each in dct:
        if int(dct.get(each)) <= 20:
            del_lst.append(each)
    for each in del_lst:
        del dct[each]

    x = list(dct.keys())
    y = list(dct.values())
    sns.barplot(x=x, y=y)
    plt.title('Top Genres')
    plt.xlabel('Genres')
    plt.ylabel('Number of Artists in Genre')
    plt.xticks(
        rotation=20,
        horizontalalignment='right')
    plt.show()

def graphCountry(df):
    df["Number of Artists"] = 1
    cy = df.copy()
    cy = cy.groupby(df["Country"])["Number of Artists"].sum().sort_values(ascending=False).reset_index()
    cy.drop(cy.loc[cy['Number of Artists'] <= 10].index, inplace=True)

    fig = px.bar(cy, x="Country", y="Number of Artists",
                 color='Country', text="Number of Artists")
    fig.update_layout(title_text='Number of Artists by Country')
    fig.show()

def stage_trend_df(df):

    df["Counter"] = 1
    print(list(df.columns))
    stgdf = df[['Career Stage', 'Career Trend', 'Counter']].copy()

    stg = stgdf.replace('Developing', "A")
    stg = stg.replace('Mid-Level', "B")
    stg = stg.replace('Mainstream', "C")
    stg = stg.replace('Superstar', "D")
    stg = stg.replace('Legendary', "E")

    stg = stg.replace('Decline', "F")
    stg = stg.replace('Steady', "G")
    stg = stg.replace('Growth', "H")
    stg = stg.replace('High Growth', "I")
    stg = stg.replace('Explosive Growth', "J")

    grouped = stg.groupby(['Career Stage', 'Career Trend'])["Counter"].sum().reset_index()

    dfg = grouped.replace("A", 'Developing')
    dfg = dfg.replace("B", 'Mid-Level')
    dfg = dfg.replace("C", 'Mainstream')
    dfg = dfg.replace("D", 'Superstar')
    dfg = dfg.replace("E", 'Legendary')

    dfg = dfg.replace("F", 'Decline')
    dfg = dfg.replace("G", 'Steady')
    dfg = dfg.replace("H", 'Growth')
    dfg = dfg.replace("I", 'High Growth')
    dfg = dfg.replace("J", 'Explosive Growth')

    return dfg

def stage_trend_graph(df):
    fig = px.scatter(df, x="Career Stage", y="Career Trend", text="Counter",
                     size='Counter', color="Counter", color_continuous_scale=px.colors.sequential.Plotly3)
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text='Career Stage vs Career Trend')
    fig.update_yaxes(categoryorder='array',
                     categoryarray=['Decline', 'Steady', 'Growth', 'High Growth', 'Explosive Growth'])

    fig.show()

def main():
    df = clean_data(infile)

    pron = pron_df(df)
    pron_graph(pron)

    gen = measure_genres(df)
    graph_genres(gen)

    pron_sunburst(pron)

    graphCountry(df)

    yas = stage_trend_df(df)
    stage_trend_graph(yas)

main()














