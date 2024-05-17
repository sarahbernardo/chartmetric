"""
Sarah Bernardo
Prof.  Rachlin | DS 3500
27 Jan 2023
Homework 1
"""

import pandas as pd
import plotly.graph_objects as go

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

def create_joined(df, char_lst, **kwargs):
    """
    parameters  df: dataframe with data being used to construct sankey diagram
                char_lst: list of characteristics that will be nodes in the sankey diagram
    returns:    dataframe with all desired characteristics, properly organized to make a sankey diagram
    """

    # establishes threshold for dropping row as user specified value, or sets it at 20 if no value was specified
    thresh = kwargs.get('threshold', 20)

    for i in range(1, len(char_lst)):
        # if there are only two column names in list, groups the two characteristics and returns that df, exits function
        if i==1 and i+1 == len(char_lst):
            joined = group_df(df, char_lst[i-1], char_lst[i], bound=thresh)
            return joined
        # creates joint data frame of first three characteristics
        elif i == 1 and i+1 != len(char_lst):
            grouped1 = group_df(df, char_lst[i-1], char_lst[i], bound=thresh)
            grouped1.columns = ["src", "targ", "count"]

            grouped2 = group_df(df, char_lst[i], char_lst[i+1], bound=thresh)
            grouped2.columns = ["src", "targ", "count"]

            joined = pd.concat([grouped1, grouped2], axis=0)
            i += 2

        # adds remaining characteristics to existing joint dataframe
        elif i>1 and i+1 < len(char_lst):
            new_group = group_df(df, char_lst[i-1], char_lst[i], bound=thresh)
            new_group.columns = ["src", "targ", "count"]

            joined = pd.concat([joined, grouped2], axis=0)
            i += 2

        # returns complete joint dataframe once all characteristics have been accounted for
        else:
            return joined

def make_sankey(df, cols, threshold=20, vals=None, **kwargs):
    """
    parameters  df: dataframe with data being used to construct sankey diagram
                cols: list of columns that will be nodes in the sankey diagram
                threshold: (float or integer) value that a group's number of members must exceed to be in the diagram
    function:   prints a stacked sankey diagram with nodes from all user-specified characteristics

    Extended functionality of make_sankey function
    """

    # sets value of links
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    # creates joint dataframe of all characteristics
    stacked = create_joined(df, cols, threshold=threshold)

    # establishes columns in joint dataframe as "src" and "targ" to be compatible with code from class
    col_lst = list(stacked.columns)
    src = col_lst[0]
    targ = col_lst[1]

    # establishes source and targets for sankey links and establishes spacing of nodes
    df, labels = _code_mapping(stacked, src, targ)
    link = {'source': df[src], 'target': df[targ], 'value': values}
    pad = kwargs.get('pad', 50)

    # creates sankey diagram
    node = {'label': labels, 'pad': pad}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # establishes spacing of diagram to look better
    width = kwargs.get('width', 1200)
    height = kwargs.get('height', 800)
    fig.update_layout(
        autosize=False,
        width=width,
        height=height)

    fig.show()

def main():
    # create df
    df = pd.read_csv("apr_25_chtmt.csv")
    df = pd.DataFrame().assign(CS=df["Career Stage"], Gender=df["Gender"], Decade=df["BeginDate"])

    # convert year to decade
    df["Decade"] = (df["Decade"]//10)*10

    # remove all entries with decade = 0
    df.drop(df.loc[df['Decade'] == 0].index, inplace=True)

    # make stacked sankey diagram with all three attributes
    make_sankey(df, ["Gender", "Decade", "Nationality"], threshold=20)

if __name__ == "__main__":
    main()
