"""
Sarah Bernardo
Prof.  Rachlin | DS 3500
27 Jan 2023
Homework 1
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def group_df(df, char1, char2, **kwargs):
    """
    parameters df: dataframe of all data
               char1: (str) column name of the 1st characteristic we want to group by
               char2: (str) column name of the 2nd characteristic we want to group by
               kwargs: user can input a bound where any group with fewer members than the bound value will be dropped
    returns:   dataframe grouped by the desired characteristic
    """
    df["Counter"] = 1

    bound = kwargs.get('bound', 20)

    grouped = df.groupby([char1, char2])["Counter"].sum().reset_index()
    grouped.drop(grouped.loc[grouped['Counter'] <= bound].index, inplace=True)
    return grouped

def _code_mapping(df, src, targ):
    """
    parameters  df: dataframe with data being used to construct sankey diagram
                src: (str) name of column from which we'd like to take source (left side) data for diagram
                targ: (str) name of column from which we'd like to take target (right side) data for diagram
    returns:    dataframe and labels for making sankey diagram

    ** This helper function was created in class by Prof. Rachlin **
    """
    # Get distinct labels
    labels = list(set(list(df[src]) + list(df[targ])))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})
    return df, labels

def make_sankey(df, src, targ, vals=None, **kwargs):
    """
    parameters  df: dataframe with data being used to construct sankey diagram
                src: (str) name of column from which we'd like to take source (left side) data for diagram
                targ: (str) name of column from which we'd like to take target (right side) data for diagram
    returns:    sankey diagram linking src values to target values with thickness vals

    ** This function was created in class by Prof. Rachlin **
    """

    # sets values of links
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    # match link colors to node colors
    nodes = np.unique(df[['CareerTrend', 'CareerStage']], axis=None)
    nodes = pd.Series(index=nodes, data=range(len(nodes)))
    link_colors = [
        'rgba' +
        str(px.colors.hex_to_rgb(px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]) + (0.3,))
        for i in nodes.loc[df['CareerTrend']]
    ]
    node_colors = [
        px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
        for i in nodes
    ]

    # establishes source and targets for sankey links and establishes spacing of nodes
    df, labels = _code_mapping(df, src, targ)
    link = {'source':df[src], 'target':df[targ], 'value':values, 'color':link_colors}
    pad = kwargs.get('pad', 50)

    # displays sankey diagram
    node = {'label': labels, 'pad': pad, 'color': node_colors}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # establishes spacing of diagram to look better
    # width = kwargs.get('width', 800)
    # height = kwargs.get('height', 800)
    fig.update_layout(
        title="Artist Career Stage by Growth Trend")
    #     width=width,
    #     height=height)

    fig.show()

def main():
    # create df
    df = pd.read_csv("apr_25_chtmt.csv")
    df = df.iloc[:500]
    df = pd.DataFrame().assign(CareerStage=df["Career Stage"], CareerTrend=df["Career Trend"], Country=df["Country"])

    # convert year to decade
    # df["Country"] = (df["Decade"]//10)*10

    # remove all entries with decade = 0
    # df.drop(df.loc[df['Decade'] == 0].index, inplace=True)


    # make nationality --> decade sankey diagram
    # nat_dec = group_df(df, "Country", "CareerStage", bound=10)
    # make_sankey(nat_dec, "Country", "CareerStage", vals="Counter")

    # make nationality --> gender sankey diagram
    nat_gen = group_df(df, "CareerTrend", "CareerStage", bound=1)
    make_sankey(nat_gen, "CareerTrend", "CareerStage", vals="Counter")

    # make gender --> decade sankey diagram
    # gen_dec = group_df(df, "CareerTrend", "Country", bound=1)
    # make_sankey(gen_dec, "CareerTrend", "Country", vals="Counter")

if __name__ == "__main__":
    main()
