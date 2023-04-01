import configparser
from io import StringIO

import streamlit as st
import pandas as pd

from met import match_equity_table
from take import take_point
from double import double_point
from util import format_cube_level


met_df = None
size = 25
cube_levels = (1, 2, 4, 8)

st.set_page_config(page_title='MET Visualizer', layout='wide')

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a met file", type='met')
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode('cp1250'))
        lines = [line.lstrip() for line in stringio.readlines()]
        config = configparser.ConfigParser()
        config.read_string(''.join(lines))
        met_info = config['PreCrawford']
        size = int(met_info.get('size'))
        met_array = []
        axis = [i for i in range(1, size + 1)]
        for i in axis:
            met_line = met_info.get(str(i))
            met_list = [float(mwc) for mwc in met_line.split(' ')]
            met_array.append(met_list)
        met_df = pd.DataFrame(met_array, index=axis, columns=axis)

    if met_df is not None:
        met_size = st.slider('table size', 3, size, 11)
        player_away = st.slider('player away', 1, met_size, met_size)
        opponent_away = st.slider('opponent away', 1, met_size, met_size)
        cube_level = st.selectbox('cube level',
                                  tuple(
                                      filter(lambda x: x * 2 <= met_size, cube_levels)),
                                  format_func=format_cube_level)

if met_df is not None:
    match_equity_table(met_size, met_df, player_away, opponent_away)
    tab_take, tab_double = st.tabs(['Take Point', 'Double Point'])
    with tab_take:
        take_point(met_size, met_df, player_away, opponent_away, cube_level)
    with tab_double:
        double_point(met_size, met_df, player_away, opponent_away, cube_level)

else:
    st.write('Please select a match equity table file (.met).')
    st.write('You\'ll find it in C:\Program Files (x86)\eXtreme Gammon 2\MET folder.')
    st.write('Copy the met file you\'d like to visualize to somewhere this app can access, such as a desktop, and drop it onto "Drag and drop file here" area in the left panel.')
