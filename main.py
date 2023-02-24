from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


s2021 = pd.read_excel("data/ghgp_data_2021.xlsx", sheet_name="Direct Emitters")
s_by_year = pd.read_excel("data/ghgp_data_by_year.xlsx", sheet_name="Direct Emitters")


def carbon_emissions(s2021):
    s_num = list(s2021["Unnamed: 13"][3:].replace(float("nan"), 0))
    s_name = list(s2021["Unnamed: 2"][3:])
    s_city = list(s2021["Unnamed: 3"][3:])

    raw_pair = [
        (num, name, city) for num, name, city in zip(s_num, s_name, s_city, strict=True)
    ]
    ord_pair = sorted(raw_pair, key=lambda i: i[0], reverse=True)

    df = pd.DataFrame(
        data={
            "emitters-rank": range(1, len(ord_pair) + 1),
            "emissions": [i[0] for i in ord_pair],
            "facility-name": [i[1] for i in ord_pair],
            "city": [i[2].title() for i in ord_pair],
        },
    )
    return px.bar(
        df, x="emitters-rank", y="emissions",
        labels={
            "emitters-rank": "Direct Emitters (2021)",
            "emissions": "Carbon Emissions"
        },
        hover_data={"facility-name": True, "city": True},
    )

def emissions_by_year(sht):
    s_years = [sht[f"Unnamed: {i}"] for i in range(13, 24)]
    data = {"Years": list(range(2021, 2010, -1))}

    results = []
    for s in s_years:
        results.append(sum(list(s[3:].replace(float("nan"), 0))))

    data["emissions"] = results
    return px.scatter(pd.DataFrame(data=data), x="Years", y="emissions", trendline="ols",
        labels={"emissions": "Total Carbon Emissions"}
    )


c_emissons = carbon_emissions(s2021)
c_emissons.update_layout(
    {
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    }
)
by_year = emissions_by_year(s_by_year)
by_year.update_traces(mode="lines")
by_year.data[-1].line.color="red"
by_year.data[-1].line.dash="dash"
by_year.data[-1].opacity=0.7

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H3("2021 Carbon Emissions (Greenhouse Gas Reporting Program)"),
        html.P(
            "The graph below shows all direct emitters reported by the Greenhouse Gas Reporting Program. "
            "Direct Emitters are sorted by their emissions. The curve produced follows the power law. ",
        ),
        dcc.Graph(id="graph", figure=c_emissons),
        html.H3("Carbon Emissions Over Time (2011-2021)"),
        html.P("Total Carbon Emissions have been steadly decreasing from the high of 3.2B (2011) to 2.4B (2020)"),
        dcc.Graph(id="graph2", figure=by_year)
    ]
)

app.run_server(debug=True)
