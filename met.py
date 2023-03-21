import plotly.graph_objects as go
import streamlit as st


from util import get_xy, get_data, hovertemplate, opacity, height


def match_equity_table(met_size, met_df, player_away, opponent_away):
    st.header('Match Equity Table')

    met_df = met_df.iloc[:met_size, :met_size]
    x, y = get_xy(met_size)

    col_met_table, col_met_3d = st.columns(2)
    with col_met_table:
        st.subheader(f'Up to {met_size} away')
        heatmap = go.Heatmap(x=x, y=y, z=met_df.values,
                             text=met_df.values,
                             texttemplate="%{text:.2%}",
                             hovertemplate=hovertemplate)
        fig_met = go.Figure(data=heatmap)
        fig_met.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_met, theme=None, use_container_width=True)

    with col_met_3d:
        st.subheader(f'{player_away} away - {opponent_away} away')
        z = met_df.transpose()
        x_, y_, z_ = get_data(player_away, opponent_away, z)
        fig = go.Figure(data=[
            go.Surface(
                x=x, y=y, z=z.values,
                opacity=opacity,
                hovertemplate=hovertemplate,
                colorscale='Viridis',
                coloraxis='coloraxis'
            ),
            go.Scatter3d(
                x=y_, y=x_, z=z_,
                hoverinfo='none',
                marker=dict(
                    size=3,
                    color=z_,
                    colorscale='Viridis',
                    coloraxis='coloraxis',
                ),
                line=dict(
                    color='darkblue',
                    width=2
                ),
            )
        ])
        fig.update_layout(autosize=False, height=height)
        st.plotly_chart(fig, theme=None, use_container_width=True)
