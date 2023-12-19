import logging
import os
from random import randint

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger()
logger.setLevel(logging.INFO)

keys = ['revenue', 'expenses', 'products_quality', 'products_quantity', 'renown', 'competition', 'money']


def plot(filename: str):
    df = pd.read_json(filename)
    fig = make_subplots(rows=3, cols=3, specs=[
        [{'type': 'box'}, {'type': 'box'}, None],
        [{'type': 'box'}, {'type': 'box'}, None],
        [{'type': 'scatter'}, {'type': 'scatter'}, {'type': 'scatter'}]
    ])
    z = 0
    x = y = 1
    for key in keys:
        if y < 3:
            fig.add_trace(go.Box(name=key, y=df[key]), row=y, col=x)
        else:
            fig.add_trace(go.Scatter(name=key, x=df.index, y=df[key]), row=y, col=x)
        z += 1
        if z == 2 or z == 5:
            z += 1
        x = z % 3 + 1
        y = (z // 3) + 1
    fig.update_layout(
        template="plotly_dark",
        annotations=[
            dict(
                text="",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=0)
        ]
    )
    fig.show()


if __name__ == '__main__':
    r = False
    r_number = 20
    filename = ""
    for root, _, files in os.walk('data'):
        if r:
            rs = [randint(0, len(files)) for _ in range(r_number)]
            for i in rs:
                logger.info(files[i])
                plot(os.path.join(root, files[i]))
        else:
            if filename == "":
                for file in files:
                    plot(os.path.join(root, file))
            else:
                plot(os.path.join(root, filename))
