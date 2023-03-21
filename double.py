import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

from util import plot_mwc, hovertemplate, opacity, height


def calc_double_point(player_away, opponent_away, cube_level, z):
    ln = opponent_away - 1 - cube_level
    if ln < 0:
        E_ln = 0.0
    else:
        E_ln = z.iat[ln, player_away - 1]
    ld = opponent_away - 1 - (cube_level * 2)
    if ld < 0:
        E_ld = 0.0
    else:
        E_ld = z.iat[ld, player_away - 1]
    wn = player_away - 1 - cube_level
    if wn < 0:
        E_wn = 1.0
    else:
        E_wn = z.iat[opponent_away - 1, wn]
    wd = player_away - 1 - (cube_level * 2)
    if wd < 0:
        E_wd = 1.0
    else:
        E_wd = z.iat[opponent_away - 1, wd]
    r = E_ln - E_ld
    g = E_wd - E_wn
    if (r + g) == 0.0:
        double_point = 0.0
    else:
        double_point = r / (r + g)
    return (E_ln, E_ld, E_wn, E_wd, r, g, double_point)


def double_point(met_size, met_df, player_away, opponent_away, cube_level):
    st.header('Double point')

    col_double_point, col_double_detail = st.columns(2)
    with col_double_point:
        st.subheader(f'For {cube_level * 2} cube')
        dp_table = np.zeros((met_size, met_size))
        for ny, nx in np.ndindex(dp_table.shape):
            _, _, _, _, _, _, dp = calc_double_point(
                ny + 1, nx + 1, cube_level, met_df.transpose())
            dp_table[ny, nx] = dp
        axis = [i for i in range(cube_level + 1, met_size + 1)]
        dp_df = pd.DataFrame(
            dp_table[cube_level:, cube_level:], index=axis, columns=axis)
        heatmap = go.Heatmap(x=axis, y=axis, z=dp_df.values,
                             text=dp_df.values,
                             texttemplate="%{text:.2%}",
                             hovertemplate=hovertemplate)
        fig_dpt = go.Figure(data=heatmap)
        fig_dpt.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_dpt, theme=None, use_container_width=True)

        dp_df = dp_df.transpose()
        fig_dp = go.Figure(data=[
            go.Surface(
                x=axis, y=axis, z=dp_df.values,
                opacity=opacity,
                hovertemplate=hovertemplate,
                colorscale='Viridis',
                coloraxis='coloraxis'
            )
        ])
        fig_dp.update_layout(autosize=False, height=height)
        st.plotly_chart(fig_dp, theme=None, use_container_width=True)

    with col_double_detail:
        st.subheader(f'{player_away} away - {opponent_away} away')
        E_ln, E_ld, E_wn, E_wd, r, g, double_point = calc_double_point(
            player_away, opponent_away, cube_level, met_df.transpose())

        st.markdown(
            '$E_{ld}' + f' = {E_ld:.4f}, ' +
            'E_{ln}' + f' = {E_ln:.4f}, ' +
            'E_{wn}' + f' = {E_wn:.4f}, ' +
            'E_{wd}' + f' = {E_wd:.4f}$')
        st.markdown(f'$Risk = {r:.4f}, Gain = {g:.4f}, Ratio = {g/r:.2f}$')
        st.markdown(f'$Double\ Point = \large{double_point * 100.0:.2f} \%$')

        fig_dd = plot_mwc(player_away, opponent_away, met_df.transpose())
        fig_dd.add_hline(y=E_ln, annotation_text='E_ln', line_dash="dot")
        fig_dd.add_hline(y=E_ld, annotation_text='E_ld', line_dash="dot")
        fig_dd.add_hline(y=E_wn, annotation_text='E_wn', line_dash="dot")
        fig_dd.add_hline(y=E_wd, annotation_text='E_wd', line_dash="dot")
        fig_dd.update_layout(autosize=False, height=height)
        st.plotly_chart(fig_dd, theme=None, use_container_width=True)
