import plotly.express as px
import pandas as pd


sheet = pd.read_excel("data/ghgp_data_2021.xlsx", sheet_name="Direct Emitters")


def carbon_emissions(d: pd.Series):
    d = d.replace(float("nan"), 0)
    nums = sorted(filter(lambda v: v != 0, list(d)), reverse=True)

    df = pd.DataFrame(
        {"Ranked Emitters": range(len(nums)), "Carbon Emissions": nums}, dtype=float
    )
    return px.bar(df, x="Ranked Emitters", y="Carbon Emissions")


fig = carbon_emissions(sheet["Unnamed: 14"][3:])
fig.write_html("first_figure.html", auto_open=True)
