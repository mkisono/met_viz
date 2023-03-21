import plotly.graph_objects as go
import numpy as np

opacity = 0.5
width = 600
height = 600
hovertemplate = ' %{y}away - %{x}away <br> %{z:.2%}<extra></extra>'


def format_cube_level(level):
    return f'For {level * 2} cube'


def get_xy(met_size):
    x = np.linspace(start=1, stop=met_size, num=met_size, dtype=np.int8)
    y = np.linspace(start=1, stop=met_size, num=met_size, dtype=np.int8)
    return x, y


def get_data(x_away, y_away, z):
    x_y_away = np.array([y_away] * x_away, dtype=np.int8)
    x_lin = np.linspace(start=1, stop=y_away, num=y_away, dtype=np.int8)
    x = np.concatenate([x_lin, x_y_away])

    y_x_away = np.array([x_away] * y_away, dtype=np.int8)
    y_lin = np.linspace(start=x_away, stop=1, num=x_away, dtype=np.int8)
    y = np.concatenate([y_x_away, y_lin])

    x_value = z[x_away][:y_away].values
    y_value = z.iloc[y_away - 1][:x_away].values[::-1]
    z = np.concatenate([x_value, y_value])
    return x, y, z


def get_mwc_diag(x_away, y_away, z):
    x = np.linspace(start=(-y_away + 1), stop=(x_away - 1),
                    num=(x_away + y_away - 1), dtype=np.int8)
    x_value = z[x_away][:y_away].values[:-1]
    y_value = z.iloc[y_away - 1][:x_away].values[::-1]
    return x, np.concatenate([x_value, y_value])


def plot_mwc(x_away, y_away, z):
    x, y = get_mwc_diag(x_away, y_away, z)
    return go.Figure(data=[
        go.Scatter(
            x=x, y=y,
            marker=dict(
                size=4,
                color=y,
                colorscale='Viridis',
            ),
            line=dict(
                color='darkblue',
                width=2
            )
        )
    ])
