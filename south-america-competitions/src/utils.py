from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator

BACKGROUND_COLOR = "#f5f5f5"
FONTFAMILY = "monospace"
TITLE_PADDING = 15


COLOR_LIST = [
    "#ff9999",
    "#66b3ff",
    "#99ff99",
    "#ffcc99",
    "#c2c2f0",
    "#ffb3e6",
    "#c2d6d6",
    "#ffb366",
    "#b3b3b3",
    "#8cd98c",
    "#ff6666",
    "#66ff66",
    "#6666ff",
    "#ffcc00",
    "#cc99ff",
]


COUNTRY_MAPPING = {
    "Brasil": [
        "RB Bragantino",
        "Botafogo",
        "Flamengo",
        "Gremio",
        "Palmeiras",
        "Fluminense",
        "Atletico-MG",
        "Sao Paulo",
        "Atletico Paranaense",
        "Fortaleza EC",
        "Cruzeiro",
        "Corinthians",
        "Internacional",
        "Cuiaba",
        "Goias",
        "Vasco DA Gama",
        "Bahia",
        "Sport Recife",
        "America Mineiro",
        "Atletico Goianiense",
        "Botafogo SP",
        "Sao Bernardo",
        "Sampaio Correa",
        "Ferroviario",
        "Juventude",
        "Ceara",
        "CRB",
        "Criciuma",
        "ABC",
        "Brusque",
        "Vitoria",
        "Operario-PR",
        "Anápolis",
        "Caxias",
        "Amazonas",
        "Paysandu",
        "Tocantinópolis",
        "Brasiliense",
        "Nova Iguaçu",
        "Portuguesa RJ",
        "Ituano",
        "Jacuipense",
        "Confiança",
        "Sportivo Ameliano",
        "Capital",
        "Remo",
        "Ypiranga-RS",
        "Volta Redonda",
        "São Luiz",
        "Águia de Marabá",
        "Água Santa",
        "Petrolina",
        "Murici Fc",
        "Sousa",
        "Tombense",
        "Cascavel",
        "Vitoria",
        "Santo André",
    ],
    "Argentina": [
        "Godoy Cruz",
        "Lanus",
        "River Plate",
        "San Lorenzo",
        "Racing Club",
        "Boca Juniors",
        "Argentinos JRS",
        "Defensa Y Justicia",
        "Estudiantes L.P.",
        "Talleres Cordoba",
        "Belgrano Cordoba",
        "Rosario Central",
    ],
    "Colômbia": [
        "Rionegro Aguilas",
        "Atletico Nacional",
        "Junior",
        "Millonarios",
        "Deportivo Tachira FC",
        "Independiente Medellin",
        "America de Cali",
        "Alianza Petrolera",
        "Deportes Tolima",
    ],
    "Equador": [
        "Independiente del Valle",
        "LDU de Quito",
        "Barcelona SC",
        "Aucas",
        "Deportivo Cuenca",
        "Delfin SC",
        "Tecnico Universitario",
    ],
    "Paraguai": [
        "Libertad Asuncion",
        "Cerro Porteno",
        "Nacional Asuncion",
        "Club Guarani",
    ],
    "Peru": [
        "Sporting Cristal",
        "Universitario",
        "Cesar Vallejo",
        "Alianza Lima",
        "Deportivo Garcilaso",
        "Sport Huancayo",
    ],
    "Uruguai": [
        "Defensor Sporting",
        "Penarol",
        "Danubio",
        "Liverpool Montevideo",
        "Wanderers",
        "Racing Montevideo",
        "Cerro Largo",
    ],
    "Chile": [
        "Cobresal",
        "Colo Colo",
        "Universidad Catolica",
        "Union La Calera",
        "Huachipato",
        "Everton de Vina",
        "Coquimbo Unido",
    ],
    "Venezuela": [
        "Portuguesa FC",
        "Puerto Cabello",
        "Metropolitanos FC",
        "Carabobo FC",
        "Deportivo Tachira FC",
        "Rayo Zuliano",
    ],
    "Bolívia": [
        "Always Ready",
        "Bolívar",
        "The Strongest",
        "Real Tomayapo",
        "Jorge Wilstermann",
        "Nacional Potosí",
    ],
}


def get_color_mapping(df: pd.DataFrame) -> Dict[str, str]:
    """
    Generates a color mapping for the competitions present in the
    provided DataFrame.

    :param df: DataFrame containing the 'league_name' column.
    :return: Dictionary mapping each competition to a color.
    :raises ValueError: If the number of leagues exceeds the number of
        available colors.
    """
    unique_leagues = sorted(df["league_name"].unique())
    if len(unique_leagues) > len(COLOR_LIST):
        raise ValueError(
            "The color list does not have enough colors for all the competitions."
        )
    color_mapping = dict(zip(unique_leagues, COLOR_LIST[: len(unique_leagues)]))
    return color_mapping


def preprocess_match_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the match data by filling NaN values in yellow and red
    card columns with zeros, and adds columns for total yellow cards,
    total red cards, total corner kicks, and the league name based on
    league_id.

    :param df: The DataFrame containing match data with columns such as
        yellow cards, red cards, and corner kicks.
    :return: The preprocessed DataFrame with NaN values replaced,
        additional columns for totals, and league name.
    """
    league_map = {11: "Libertadores", 13: "Sulamericana", 73: "Copa do Brasil"}

    df = df.copy()
    df[
        ["yellow_cards_home", "yellow_cards_away", "red_cards_home", "red_cards_away"]
    ] = df[
        ["yellow_cards_home", "yellow_cards_away", "red_cards_home", "red_cards_away"]
    ].fillna(
        0
    )

    df["total_yellow_cards"] = df["yellow_cards_home"] + df["yellow_cards_away"]
    df["total_red_cards"] = df["red_cards_home"] + df["red_cards_away"]
    df["total_corner_kicks"] = df["corner_kicks_home"] + df["corner_kicks_away"]

    df["league_name"] = df["league_id"].map(league_map)
    df = df[df["goals_home"].notnull()].reset_index(drop=True)

    def get_country(team_name):
        """
        Retorna o país de um time com base no mapeamento de times por país.
        """
        for country, teams in COUNTRY_MAPPING.items():
            if team_name in teams:
                return country
        return "Desconhecido"

    df["home_country"] = df["home_team"].apply(get_country)
    df["away_country"] = df["away_team"].apply(get_country)

    return df


def calculate_avg_goals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the average goals for each competition.

    :param df: DataFrame containing the columns ['league_name',
        'goals_home', 'goals_away'].
    :return: DataFrame with competitions and their respective average
        goals.
    """
    avg_goals_df = df.groupby("league_name").agg(
        {"goals_home": "mean", "goals_away": "mean"}
    )
    avg_goals_df["Média de Gols"] = (
        avg_goals_df["goals_home"] + avg_goals_df["goals_away"]
    )
    avg_goals_df = avg_goals_df.reset_index()[["league_name", "Média de Gols"]]

    return avg_goals_df


def plot_avg_goals_by_league(
    df: pd.DataFrame, title: str, color_mapping: Dict[str, str]
) -> None:
    """
    Creates a bar chart for the average goals of each competition.

    :param df: DataFrame containing the columns ['league_name',
        'goals_home', 'goals_away'].
    :param title: The title of the chart.
    :param color_mapping: Dictionary mapping competitions to colors.
    """
    df["total_goals"] = df["goals_home"] + df["goals_away"]
    avg_goals = df.groupby("league_name")["total_goals"].mean().reset_index()
    avg_goals.rename(columns={"total_goals": "Média de Gols"}, inplace=True)

    avg_goals.sort_values(by="league_name", inplace=True)

    bar_colors = avg_goals["league_name"].map(color_mapping)

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    bars = ax.bar(
        avg_goals["league_name"],
        avg_goals["Média de Gols"],
        color=bar_colors,
        edgecolor="black",
    )

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontfamily=FONTFAMILY,
            fontsize=10,
            color="black",
        )
    ax.set_ylim(0, avg_goals["Média de Gols"].max() + 0.5)
    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_ylabel("Média de Gols", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    plt.xticks(fontfamily=FONTFAMILY, rotation=0)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_stacked_percentage_cards(df: pd.DataFrame) -> None:
    """
    Creates a 100% stacked bar chart to show the percentage of yellow
    and red cards relative to the total number of cards per competition.

    :param df: DataFrame containing the columns ['league_name',
        'total_yellow_cards', 'total_red_cards'].
    :return: None
    """
    df["total_cards"] = df["total_yellow_cards"] + df["total_red_cards"]
    df["percent_yellow"] = df["total_yellow_cards"] / df["total_cards"] * 100
    df["percent_red"] = df["total_red_cards"] / df["total_cards"] * 100

    df_grouped = df.groupby("league_name")[["percent_yellow", "percent_red"]].mean()

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    df_grouped.plot(
        kind="bar", stacked=True, color=["#ffcc00", "#ff3333"], edgecolor="black", ax=ax
    )

    ax.set_title(
        "Cartões Amarelos e Vermelhos por Competição",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_ylabel("Percentual (%)", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    ax.get_legend().remove()

    for container in ax.containers:
        for i, bar in enumerate(container):
            height = bar.get_height()
            width = bar.get_width()
            x = bar.get_x()
            y = bar.get_y()

            text_x = x + width / 2
            text_y = y + height / 2

            percentage = f"{height:.1f}%"

            if container.get_label() == "percent_red":
                text_color = "white"
            else:
                text_color = "black"

            ax.text(
                text_x,
                text_y,
                percentage,
                ha="center",
                va="center",
                fontsize=10,
                fontfamily=FONTFAMILY,
                color=text_color,
            )

    plt.xticks(fontfamily=FONTFAMILY, rotation=0)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_games_count_by_league(df: pd.DataFrame, title: str, color_mapping: dict):
    """
    Cria um gráfico de barras para a quantidade de jogos por competição.

    :param df: DataFrame contendo a coluna 'league_name'.
    :param title: Título do gráfico.
    :param color_mapping: Dicionário mapeando competições para cores.
    """
    games_count = df["league_name"].value_counts().reset_index()
    games_count.columns = ["Competição", "Quantidade de Jogos"]

    games_count.sort_values(by="Competição", inplace=True)

    bar_colors = games_count["Competição"].map(color_mapping)

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    bars = ax.bar(
        games_count["Competição"],
        games_count["Quantidade de Jogos"],
        color=bar_colors,
        edgecolor="black",
    )

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )
    # Ajustar o limite do eixo Y
    ax.set_ylim(0, games_count["Quantidade de Jogos"].max() + 20)
    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_ylabel(
        "Quantidade de Jogos", fontfamily=FONTFAMILY, fontsize=12, color="gray"
    )
    ax.set_xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    plt.xticks(fontfamily=FONTFAMILY, rotation=0)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_total_cards(df: pd.DataFrame) -> None:
    """
    Plots the total number of cards (yellow + red) by competition.

    :param df: DataFrame containing the columns ['league_name',
        'total_yellow_cards', 'total_red_cards'].
    :return: None
    """
    df["total_cards"] = df["total_yellow_cards"] + df["total_red_cards"]

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    sns.barplot(
        x="league_name",
        y="total_cards",
        data=df,
        ax=ax,
        palette="coolwarm",
        edgecolor="black",
    )
    ax.set_title(
        "Total de Cartões por Competição",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_ylabel("Total de Cartões", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    # Adicionar rótulos em cima das barras
    for bar in ax.patches:
        ax.annotate(
            f"{bar.get_height():.0f}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )

    # plt.xticks(fontfamily=FONTFAMILY, rotation=90)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_avg_cards_per_game(
    df: pd.DataFrame, title: str, color_mapping: Dict[str, str]
) -> None:
    """
    Plots the average number of cards (yellow and red) per game by
    competition.

    :param df: DataFrame containing the columns ['league_name',
        'total_yellow_cards', 'total_red_cards'].
    :param title: The title of the plot.
    :param color_mapping: Dictionary mapping competitions to colors.
    :return: None
    """
    df["total_cards"] = df["total_yellow_cards"] + df["total_red_cards"]

    avg_cards = df.groupby("league_name")["total_cards"].mean().reset_index()
    avg_cards.rename(columns={"total_cards": "Média de Cartões"}, inplace=True)

    # Ordenar por 'league_name' em ordem alfabética
    avg_cards.sort_values(by="league_name", inplace=True)

    # Obter as cores correspondentes às competições
    bar_colors = avg_cards["league_name"].map(color_mapping)

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    bars = ax.bar(
        avg_cards["league_name"],
        avg_cards["Média de Cartões"],
        color=bar_colors,
        edgecolor="black",
    )

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )

    # Ajustar o limite do eixo Y
    ax.set_ylim(0, avg_cards["Média de Cartões"].max() + 1)
    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_ylabel("Média de Cartões", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    plt.xticks(fontfamily=FONTFAMILY, rotation=0)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_stacked_cards(df: pd.DataFrame) -> None:
    """
    Creates a stacked bar chart for yellow and red cards by competition.

    :param df: DataFrame containing the columns ['league_name',
        'total_yellow_cards', 'total_red_cards'].
    :return: None
    """
    df_grouped = df.groupby("league_name")[
        ["total_yellow_cards", "total_red_cards"]
    ].sum()

    ax = df_grouped.plot(
        kind="bar",
        stacked=True,
        figsize=(6, 4),
        color=["#ffcc00", "#ff3333"],
        edgecolor="black",
    )

    plt.title(
        "Cartões por Competição",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    plt.xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    plt.ylabel("Total de Cartões", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    plt.ylim(0, 850)

    totals = df_grouped.sum(axis=1)
    for i, total in enumerate(totals):
        ax.text(
            i,
            total + 10,
            str(int(total)),
            ha="center",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
            rotation=0,
        )

    plt.xticks(fontfamily=FONTFAMILY, rotation=0)
    plt.yticks(fontfamily=FONTFAMILY)

    ax.get_legend().remove()

    plt.tight_layout()
    plt.show()


def create_champions_dataframe() -> pd.DataFrame:
    """
    Creates a DataFrame containing champions of competitions such as
    Libertadores, Copa Sudamericana, and Copa do Brasil.

    :return: DataFrame with columns for Competition, Team, Year, and
        Country.
    """
    data = {
        "Competição": [
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Libertadores",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa Sul-Americana",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
            "Copa do Brasil",
        ],
        "Time": [
            "Fluminense",
            "Flamengo",
            "Palmeiras",
            "Palmeiras",
            "Flamengo",
            "River Plate",
            "Grêmio",
            "Atlético Nacional",
            "River Plate",
            "San Lorenzo",
            "Atlético Mineiro",
            "Corinthians",
            "Santos",
            "Internacional",
            "Estudiantes",
            "LDU Quito",
            "Boca Juniors",
            "Internacional",
            "São Paulo",
            "Once Caldas",
            "LDU",
            "Independiente Del Valle",
            "Athletico-PR",
            "Defensa y Justicia",
            "Independiente Del Valle",
            "Athletico-PR",
            "Independiente",
            "Chapecoense",
            "Independiente Santa Fé",
            "River Plate",
            "Lanús",
            "São Paulo",
            "Universidad de Chile",
            "Independiente",
            "LDU",
            "Internacional",
            "Arsenal de Sarandí",
            "Pachuca",
            "Boca Juniors",
            "Boca Juniors",
            "São Paulo",
            "Flamengo",
            "Atlético-MG",
            "Palmeiras",
            "Athletico-PR",
            "Cruzeiro",
            "Cruzeiro",
            "Grêmio",
            "Palmeiras",
            "Atlético-MG",
            "Flamengo",
            "Palmeiras",
            "Vasco da Gama",
            "Santos",
            "Corinthians",
            "Sport Recife",
            "Fluminense",
            "Flamengo",
            "Paulista",
            "Santo André",
        ],
        "Ano": [
            2023,
            2022,
            2021,
            2020,
            2019,
            2018,
            2017,
            2016,
            2015,
            2014,
            2013,
            2012,
            2011,
            2010,
            2009,
            2008,
            2007,
            2006,
            2005,
            2004,
            2023,
            2022,
            2021,
            2020,
            2019,
            2018,
            2017,
            2016,
            2015,
            2014,
            2013,
            2012,
            2011,
            2010,
            2009,
            2008,
            2007,
            2006,
            2005,
            2004,
            2023,
            2022,
            2021,
            2020,
            2019,
            2018,
            2017,
            2016,
            2015,
            2014,
            2013,
            2012,
            2011,
            2010,
            2009,
            2008,
            2007,
            2006,
            2005,
            2004,
        ],
        "País": [
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Argentina",
            "Brasil",
            "Colômbia",
            "Argentina",
            "Argentina",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Argentina",
            "Equador",
            "Argentina",
            "Brasil",
            "Brasil",
            "Colômbia",
            "Equador",
            "Equador",
            "Brasil",
            "Argentina",
            "Equador",
            "Brasil",
            "Argentina",
            "Brasil",
            "Colômbia",
            "Argentina",
            "Argentina",
            "Brasil",
            "Chile",
            "Argentina",
            "Equador",
            "Brasil",
            "Argentina",
            "México",
            "Argentina",
            "Argentina",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
            "Brasil",
        ],
    }

    df_champions = pd.DataFrame(data)

    return df_champions


def calculate_champions_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the number of champions by country and competition,
    excluding the Copa do Brasil.

    :param df: DataFrame containing the columns ['Competição', 'País'].
    :return: DataFrame with the count of champions by country and by
        competition.
    """
    df_filtered = df[df["Competição"] != "Copa do Brasil"]
    champions_df = (
        df_filtered.groupby(["País", "Competição"]).size().unstack(fill_value=0)
    )
    champions_df["Total"] = champions_df.sum(axis=1)
    champions_df = champions_df.sort_values(by="Total", ascending=False)

    return champions_df.drop(columns=["Total"])


def plot_champions_count_by_country(df: pd.DataFrame, title: str) -> None:
    """
    Creates a stacked bar chart for the number of titles by country.

    :param df: DataFrame containing competitions and the number of
        titles by country.
    :param title: Title of the chart.
    :return: None
    """
    ax = df.plot(
        kind="bar",
        stacked=True,
        figsize=(8, 4),
        color=["#ff9999", "#66b3ff", "#99ff99"],
        edgecolor="black",
    )

    # Customizações do gráfico
    plt.title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    plt.xlabel("País", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    plt.ylabel(
        "Quantidade de Títulos", fontfamily=FONTFAMILY, fontsize=12, color="gray"
    )
    plt.ylim(0, 20)

    # Adiciona o número total de títulos em cima de cada barra
    totals = df.sum(axis=1)
    for i, total in enumerate(totals):
        ax.text(
            i,
            total + 0.5,
            str(int(total)),
            ha="center",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )

    # Ajusta os ticks do eixo Y de 0 a 20, incrementando de 2 em 2
    plt.yticks(range(0, 21, 4), fontfamily=FONTFAMILY)

    # Reduz o tamanho da legenda
    plt.legend(title="Competição", fontsize=9, title_fontsize=10)

    # Ajusta o layout
    plt.xticks(fontfamily=FONTFAMILY, rotation=0)
    plt.tight_layout()
    plt.show()


def plot_avg_cards_by_matchup(df: pd.DataFrame) -> None:
    """
    Creates a bar chart showing the average number of cards per matchup
    between countries, considering that the matchup is the same
    regardless of the home or away team.

    :param df: DataFrame containing match data, including the columns
        ['home_country', 'away_country', 'total_yellow_cards',
        'total_red_cards'].
    :return: None
    """
    # Lista de países selecionados
    selected_countries = [
        "Brasil",
        "Colômbia",
        "Peru",
        "Bolívia",
        "Chile",
        "Argentina",
        "Venezuela",
        "Uruguai",
        "Paraguai",
        "Equador",
    ]

    # Mapeamento de nomes de países para abreviações
    country_abbreviations = {
        "Brasil": "BRA",
        "Argentina": "ARG",
        "Colômbia": "COL",
        "Uruguai": "URU",
        "Chile": "CHL",
        "Paraguai": "PAR",
        "Peru": "PER",
        "Equador": "ECU",
        "Bolívia": "BOL",
        "Venezuela": "VEN",
    }

    def abbreviate_country(country_name):
        """
        Retorna a abreviação do país a partir do nome completo.
        Se o país não estiver no mapeamento, retorna 'UNK' (desconhecido).
        """
        return country_abbreviations.get(country_name, "UNK")

    # Filtrando confrontos válidos e países selecionados
    df_filtered = df[
        (df["home_country"].isin(selected_countries))
        & (df["away_country"].isin(selected_countries))
    ].copy()

    # Removendo partidas com 'Desconhecido'
    df_filtered = df_filtered[
        (df_filtered["home_country"] != "Desconhecido")
        & (df_filtered["away_country"] != "Desconhecido")
    ]

    # Calculando o total de cartões por jogo
    df_filtered["total_cards"] = (
        df_filtered["total_yellow_cards"] + df_filtered["total_red_cards"]
    )

    # Abreviando os nomes dos países
    df_filtered["home_abbrev"] = df_filtered["home_country"].apply(abbreviate_country)
    df_filtered["away_abbrev"] = df_filtered["away_country"].apply(abbreviate_country)

    # Removendo partidas com abreviação 'UNK' (países desconhecidos)
    df_filtered = df_filtered[
        (df_filtered["home_abbrev"] != "UNK") & (df_filtered["away_abbrev"] != "UNK")
    ]

    # Ordenando os países em cada confronto para que mandante/visitante não importe
    df_filtered["team_pair"] = df_filtered.apply(
        lambda row: " x ".join(sorted([row["home_abbrev"], row["away_abbrev"]])),
        axis=1,
    )

    # Agrupando por confronto e calculando a quantidade de jogos e a média de cartões
    matchup_stats = (
        df_filtered.groupby("team_pair")
        .agg(total_games=("fixture_id", "size"), average_cards=("total_cards", "mean"))
        .reset_index()
    )

    # Filtrando para considerar apenas confrontos com pelo menos 3 jogos
    filtered_matchup_stats = matchup_stats[matchup_stats["total_games"] >= 5]

    # Ordenando pela média de cartões
    filtered_matchup_stats = filtered_matchup_stats.sort_values(
        by="average_cards", ascending=False
    )

    # Limitando o número de confrontos para melhor visualização (opcional)
    top_n = 20  # Número de confrontos a serem exibidos
    filtered_matchup_stats = filtered_matchup_stats.head(top_n)

    # Criando o gráfico de barras
    plt.figure(figsize=(12, 5))
    bars = plt.bar(
        filtered_matchup_stats["team_pair"],
        filtered_matchup_stats["average_cards"],
        color="#66b3ff",
        edgecolor="black",
    )

    # Adicionando os valores acima das barras
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontfamily=FONTFAMILY,
        )

    plt.title(
        "Média de Cartões por Confronto entre Países",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="center",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    plt.xlabel(
        "Confronto entre Países",
        fontfamily=FONTFAMILY,
        fontsize=12,
        color="gray",
    )
    plt.ylabel("Média de Cartões", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    plt.xticks(rotation=45, ha="right", fontfamily=FONTFAMILY, fontsize=10)
    plt.yticks(fontfamily=FONTFAMILY)

    plt.ylim(0, 8)

    plt.tight_layout()
    plt.show()


def plot_avg_corners_by_league(df: pd.DataFrame, color_mapping: Dict[str, str]) -> None:
    """
    Plots the average number of corner kicks by league.

    :param df: DataFrame containing the columns ['league_name',
        'total_corner_kicks'].
    :param color_mapping: Dictionary mapping each league to a color.
    :return: None
    """
    avg_corners = df.groupby("league_name")["total_corner_kicks"].mean().reset_index()
    avg_corners.sort_values(by="league_name", inplace=True)
    bar_colors = avg_corners["league_name"].map(color_mapping)
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        avg_corners["league_name"],
        avg_corners["total_corner_kicks"],
        color=bar_colors,
        edgecolor="black",
    )
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontfamily=FONTFAMILY,
        )
    y_max = avg_corners["total_corner_kicks"].max()
    ax.set_ylim(0, y_max + y_max * 0.1)
    ax.set_title(
        "Média de Escanteios por Competição",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel("Competição", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_ylabel(
        "Média de Escanteios", fontfamily=FONTFAMILY, fontsize=12, color="gray"
    )
    plt.xticks(rotation=0, ha="center", fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_avg_corners_by_country(df: pd.DataFrame) -> None:
    """
    Plots the average number of corner kicks by country, considering
    both home and away teams.

    :param df: DataFrame containing match data with columns
        ['home_country', 'away_country', 'corner_kicks_home',
        'corner_kicks_away'].
    :return: None
    """
    df = df[
        (df["home_country"] != "Desconhecido") & (df["away_country"] != "Desconhecido")
    ]
    df_home = df.groupby("home_country")["corner_kicks_home"].mean().reset_index()
    df_away = df.groupby("away_country")["corner_kicks_away"].mean().reset_index()
    df_home.rename(
        columns={"home_country": "country", "corner_kicks_home": "avg_corners"},
        inplace=True,
    )
    df_away.rename(
        columns={"away_country": "country", "corner_kicks_away": "avg_corners"},
        inplace=True,
    )
    df_countries = (
        pd.concat([df_home, df_away])
        .groupby("country")["avg_corners"]
        .mean()
        .reset_index()
    )
    df_countries.sort_values(by="avg_corners", ascending=False, inplace=True)
    fig, ax = plt.subplots(figsize=(12, 4))
    bars = ax.bar(
        df_countries["country"],
        df_countries["avg_corners"],
        color="#66b3ff",
        edgecolor="black",
    )
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.05,
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontfamily=FONTFAMILY,
        )
    y_max = df_countries["avg_corners"].max()
    ax.set_ylim(0, y_max + y_max * 0.1)
    ax.set_title(
        "Média de Escanteios por País",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel("País", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_ylabel(
        "Média de Escanteios", fontfamily=FONTFAMILY, fontsize=12, color="gray"
    )
    ax.tick_params(axis="x", labelrotation=0)
    plt.tight_layout()
    plt.show()


def plot_avg_corners_by_matchup(df: pd.DataFrame) -> None:
    """
    Plots the average number of corner kicks per matchup between
    selected countries, considering that the matchup is the same
    regardless of the home or away team.

    :param df: DataFrame containing match data, including the columns
        ['home_country', 'away_country', 'corner_kicks_home',
        'corner_kicks_away', 'fixture_id'].
    :return: None
    """
    selected_countries = [
        "Brasil",
        "Colômbia",
        "Peru",
        "Bolívia",
        "Chile",
        "Argentina",
        "Venezuela",
        "Uruguai",
        "Paraguai",
        "Equador",
    ]
    country_abbreviations = {
        "Brasil": "BRA",
        "Argentina": "ARG",
        "Colômbia": "COL",
        "Uruguai": "URU",
        "Chile": "CHL",
        "Paraguai": "PAR",
        "Peru": "PER",
        "Equador": "ECU",
        "Bolívia": "BOL",
        "Venezuela": "VEN",
    }

    def abbreviate_country(country_name):
        return country_abbreviations.get(country_name, "UNK")

    df_filtered = df[
        (df["home_country"].isin(selected_countries))
        & (df["away_country"].isin(selected_countries))
    ].copy()

    df_filtered = df_filtered[
        (df_filtered["home_country"] != "Desconhecido")
        & (df_filtered["away_country"] != "Desconhecido")
    ]

    df_filtered["total_corners"] = (
        df_filtered["corner_kicks_home"] + df_filtered["corner_kicks_away"]
    )

    df_filtered["home_abbrev"] = df_filtered["home_country"].apply(abbreviate_country)
    df_filtered["away_abbrev"] = df_filtered["away_country"].apply(abbreviate_country)

    df_filtered = df_filtered[
        (df_filtered["home_abbrev"] != "UNK") & (df_filtered["away_abbrev"] != "UNK")
    ]

    df_filtered["team_pair"] = df_filtered.apply(
        lambda row: sorted([row["home_abbrev"], row["away_abbrev"]]), axis=1
    )

    df_filtered["team_pair_str"] = df_filtered["team_pair"].apply(
        lambda x: " x ".join(x)
    )

    matchup_stats = (
        df_filtered.groupby("team_pair_str")
        .agg(
            total_games=("fixture_id", "size"),
            average_corners=("total_corners", "mean"),
        )
        .reset_index()
    )

    matchup_stats = matchup_stats[matchup_stats["total_games"] >= 3]
    matchup_stats.sort_values(by="average_corners", ascending=False, inplace=True)
    top_n = 20
    matchup_stats = matchup_stats.head(top_n)

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(
        matchup_stats["team_pair_str"],
        matchup_stats["average_corners"],
        color="#66b3ff",
        edgecolor="black",
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontfamily=FONTFAMILY,
        )

    y_max = matchup_stats["average_corners"].max()
    ax.set_ylim(0, y_max + y_max * 0.1)
    ax.set_title(
        "Média de Escanteios por Confronto entre Países",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel(
        "Confronto entre Países",
        fontfamily=FONTFAMILY,
        fontsize=12,
        color="gray",
    )
    ax.set_ylabel(
        "Média de Escanteios", fontfamily=FONTFAMILY, fontsize=12, color="gray"
    )
    plt.xticks(rotation=45, ha="right", fontfamily=FONTFAMILY, fontsize=10)
    plt.tight_layout()
    plt.show()


def plot_avg_corners_by_team(df: pd.DataFrame) -> None:
    """
    Plots the top 10 teams with the highest average number of corner
    kicks per game.

    :param df: DataFrame containing match data, including the columns
        ['home_team', 'away_team', 'corner_kicks_home',
        'corner_kicks_away', 'fixture_id'].
    :return: None
    """
    df_home = (
        df.groupby("home_team")
        .agg(
            total_corners=("corner_kicks_home", "sum"),
            num_games=("fixture_id", "count"),
        )
        .reset_index()
    )
    df_away = (
        df.groupby("away_team")
        .agg(
            total_corners=("corner_kicks_away", "sum"),
            num_games=("fixture_id", "count"),
        )
        .reset_index()
    )
    df_home.rename(columns={"home_team": "team"}, inplace=True)
    df_away.rename(columns={"away_team": "team"}, inplace=True)
    df_teams = (
        pd.concat([df_home, df_away])
        .groupby("team")
        .agg(total_corners=("total_corners", "sum"), num_games=("num_games", "sum"))
        .reset_index()
    )
    df_teams = df_teams[df_teams["num_games"] >= 3]
    df_teams["avg_corners"] = df_teams["total_corners"] / df_teams["num_games"]
    df_teams.sort_values(by="avg_corners", ascending=True, inplace=True)
    top_teams = df_teams.tail(10)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(
        top_teams["team"], top_teams["avg_corners"], color="#66b3ff", edgecolor="black"
    )
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}",
            ha="left",
            va="center",
            fontsize=10,
            fontfamily=FONTFAMILY,
        )
    x_max = top_teams["avg_corners"].max()
    ax.set_xlim(0, x_max + x_max * 0.1)
    ax.set_title(
        "10 Times com Maior Média de Escanteios",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel(
        "Média de Escanteios", fontfamily=FONTFAMILY, fontsize=12, color="gray"
    )
    ax.set_ylabel("Time", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    plt.xticks(fontfamily=FONTFAMILY)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()


def plot_games_with_most_cards(df: pd.DataFrame, top_n: int = 10) -> None:
    """
    Plots the top N games with the most cards, showing yellow and red
    cards separately
    in a horizontal stacked bar chart. The total number of cards in each game is displayed
    at the end of each bar.

    :param df: DataFrame containing match data with columns
        ['fixture_id', 'home_team', 'away_team', 'yellow_cards_home',
         'yellow_cards_away', 'red_cards_home', 'red_cards_away'].
    :param top_n: Number of games to display with the most total cards.
    :return: None
    """
    # Calculating total yellow and red cards per game
    df["total_yellow_cards"] = df["yellow_cards_home"] + df["yellow_cards_away"]
    df["total_red_cards"] = df["red_cards_home"] + df["red_cards_away"]
    df["total_cards"] = df["total_yellow_cards"] + df["total_red_cards"]

    # Creating a new column for the matchup description
    df["matchup"] = df["home_team"] + " vs " + df["away_team"]

    # Sorting by total cards in descending order and selecting top N games
    top_games = df.nlargest(top_n, "total_cards").sort_values(
        by="total_cards", ascending=True
    )

    # Creating the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    bars_yellow = ax.barh(
        top_games["matchup"],
        top_games["total_yellow_cards"],
        color="#FFD700",  # Amarelo
        edgecolor="black",
        label="Cartões Amarelos",
    )

    bars_red = ax.barh(
        top_games["matchup"],
        top_games["total_red_cards"],
        left=top_games["total_yellow_cards"],
        color="#FF4500",  # Vermelho
        edgecolor="black",
        label="Cartões Vermelhos",
    )

    # Adding total number of cards at the end of each bar
    for i, (yellow, red, total) in enumerate(
        zip(
            top_games["total_yellow_cards"],
            top_games["total_red_cards"],
            top_games["total_cards"],
        )
    ):
        ax.text(
            yellow + red + 0.2,
            i,
            str(int(total)),
            ha="left",
            va="center",
            fontsize=10,
            fontfamily=FONTFAMILY,
            color="black",
        )

    # Ensuring only integer values are shown on the X-axis
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Setting labels and title
    ax.set_title(
        "Top {} Jogos com Mais Cartões".format(top_n),
        fontsize=15,
        fontweight="bold",
        color="#323232",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel("Número de Cartões", fontsize=12, fontfamily=FONTFAMILY, color="gray")
    ax.set_ylabel("Confronto", fontsize=12, fontfamily=FONTFAMILY, color="gray")

    # Adding legend
    ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()
