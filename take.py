import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

from util import plot_mwc, hovertemplate, opacity, height


def calc_take_point(player_away, opponent_away, cube_level, z):
    l = opponent_away - 1 - (cube_level * 2)
    if l < 0:
        M_l = 0.0
    else:
        M_l = z.iat[l, player_away - 1]
    p = opponent_away - 1 - cube_level
    if p < 0:
        M_p = 0.0
    else:
        M_p = z.iat[p, player_away - 1]
    w = player_away - 1 - (cube_level * 2)
    if w < 0:
        M_w = 1.0
    else:
        M_w = z.iat[opponent_away - 1, w]
    r = M_p - M_l
    g = M_w - M_p
    take_point = r / (r + g)
    return (M_l, M_p, M_w, r, g, take_point)


def take_point(met_size, met_df, player_away, opponent_away, cube_level):
    st.header('Take Point')

    col_take_point, col_take_detail = st.columns(2)
    with col_take_point:
        st.subheader(f'For {cube_level * 2} cube')
        tp_table = np.zeros((met_size, met_size))
        for ny, nx in np.ndindex(tp_table.shape):
            _, _, _, _, _, tp = calc_take_point(
                ny + 1, nx + 1, cube_level, met_df.transpose())
            tp_table[ny, nx] = tp
        axis = [i for i in range(cube_level + 1, met_size + 1)]
        tp_df = pd.DataFrame(
            tp_table[cube_level:, cube_level:], index=axis, columns=axis)
        heatmap = go.Heatmap(x=axis, y=axis, z=tp_df.values,
                             text=tp_df.values,
                             texttemplate="%{text:.2%}",
                             hovertemplate=hovertemplate)
        fig_tpt = go.Figure(data=heatmap)
        fig_tpt.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_tpt, theme=None, use_container_width=True)

        tp_df = tp_df.transpose()
        fig_tp = go.Figure(data=[
            go.Surface(
                x=axis, y=axis, z=tp_df.values,
                opacity=opacity,
                hovertemplate=hovertemplate,
                colorscale='Viridis',
                coloraxis='coloraxis'
            )
        ])
        fig_tp.update_layout(autosize=False, height=height)
        st.plotly_chart(fig_tp, theme=None, use_container_width=True)

    with col_take_detail:
        st.subheader(f'{player_away} away - {opponent_away} away')

        M_l, M_p, M_w, r, g, take_point = calc_take_point(
            player_away, opponent_away, cube_level, met_df.transpose())
        st.markdown(f'$M_l = {M_l:.4f}, M_p = {M_p:.4f}, M_w = {M_w:.4f}$')
        st.markdown(f'$Risk = {r:.4f}, Gain = {g:.4f}, Ratio = {g/r:.2f}$')
        st.markdown(f'$Take\ Point = \large{take_point * 100.0:.2f} \%$')

        fig_td = plot_mwc(player_away, opponent_away, met_df.transpose())
        fig_td.add_hline(y=M_l, annotation_text='M_l', line_dash="dot")
        fig_td.add_hline(y=M_p, annotation_text='M_p', line_dash="dot")
        fig_td.add_hline(y=M_w, annotation_text='M_w', line_dash="dot")
        fig_td.update_layout(autosize=False, height=height)
        st.plotly_chart(fig_td, theme=None, use_container_width=True)
