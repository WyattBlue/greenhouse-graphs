from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


sheet = pd.read_excel("data/ghgp_data_2021.xlsx", sheet_name="Direct Emitters")


def carbon_emissions(d: pd.Series):
    d = d.replace(float("nan"), 0)
    nums = sorted(filter(lambda v: v != 0, list(d)), reverse=True)

    df = pd.DataFrame(
        {"Direct Emitters (2021)": range(len(nums)), "Carbon Emissions": nums},
        dtype=float,
    )
    return px.bar(df, x="Direct Emitters (2021)", y="Carbon Emissions")


fig = carbon_emissions(sheet["Unnamed: 14"][3:])
fig.update_layout(
    {
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    }
)

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H3("Co2 Emissions (Greenhouse Gas Reporting Program)"),
        html.P(
            "The graph below shows all direct emitters reported by the Greenhouse Gas Reporting Program. "
            "Direct Emitters are sorted by their emissions. The curve produced follows the power law. ",
        ),
        dcc.Graph(id="graph", figure=fig),
    ]
)

app.run_server(debug=True)
