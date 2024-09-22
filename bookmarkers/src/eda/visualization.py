import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Define background colors and styles
BACKGROUND_COLOR = "#f5f5f5"
FONTFAMILY = "monospace"
TITLE_PADDING = 15


def plot_popularity_growth(df: pd.DataFrame) -> None:
    """
    Plots the growth in popularity of betting houses over recent months
    with a horizontal bar chart.

    :param df: DataFrame containing the columns ['Betting_House',
        'March', 'April', 'May', 'June', 'July', 'August'].
    """
    df = df.drop(["Março", "Top"], axis=1)

    # List of month columns
    months = ["april", "may", "june", "july", "august"]

    # Ensure month columns are numeric
    df[months] = df[months].apply(pd.to_numeric, errors="coerce")

    # Select only relevant columns
    df_months = df[["betting_house"] + months]

    # Calculate total sum of accesses for each betting house
    df_months["total_sum"] = df_months[months].sum(axis=1)

    # Calculate percentage growth from March to August
    df_months["growth_percentage"] = (
        (df_months["august"] - df_months["april"]) / df_months["april"]
    ) * 100

    # Sort betting houses by highest growth percentage
    df_growth = df_months.sort_values(by="growth_percentage", ascending=False)

    # Plot the percentage growth graph with horizontal bars
    fig, ax = plt.subplots(figsize=(10, 16), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    sns.barplot(
        x="growth_percentage",
        y="betting_house",
        data=df_growth,
        palette="viridis",
        edgecolor="black",
        ax=ax,
    )

    # Add labels on top of the bars
    for bar in ax.patches:
        width = bar.get_width()
        ax.annotate(
            f"{width:.1f}%",
            (width, bar.get_y() + bar.get_height() / 2),
            ha="left",
            va="center",
            fontfamily=FONTFAMILY,
            fontsize=10,
            color="black",
            xytext=(5, 0),
            textcoords="offset points",
        )

    ax.set_title(
        "Growth in Popularity of Betting Houses",
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel("Growth (%)", fontfamily=FONTFAMILY, fontsize=12, color="gray")
    ax.set_ylabel("Betting House", fontfamily=FONTFAMILY, fontsize=12, color="gray")

    plt.xticks(fontfamily=FONTFAMILY)
    plt.yticks(fontfamily=FONTFAMILY)
    plt.tight_layout()
    plt.show()

    # Display betting houses with total accesses and growth percentage
    print("Betting Houses that gained the most popularity:")


def plot_analysis_growth(
    df: pd.DataFrame,
    x: str = "growth_percentage",
    y: str = "betting_house",
    title: str = "Crescimento de Maio a Agosto",
    xlabel: str = "Crescimento (%)",
    ylabel: str = "Betting House",
    figsize: tuple = (10, 8),
    background_color: str = BACKGROUND_COLOR,
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    palette: str = "coolwarm",
    edgecolor: str = "black",
    annotate: bool = True,
) -> None:
    """
    Plots the growth for betting houses with flexible customization options.

    :param df: DataFrame containing data to be plotted.
    :param x: Column name for x-axis values.
    :param y: Column name for y-axis values.
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param background_color: Background color for the figure.
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param palette: Color palette for the bars.
    :param edgecolor: Edge color for the bars.
    :param annotate: Whether to annotate bars with their values.
    """
    # Configuração do gráfico
    fig, ax = plt.subplots(figsize=figsize, facecolor=background_color)
    ax.set_facecolor(background_color)

    # Ajuste para evitar o aviso do hue
    sns.barplot(
        x=x,
        y=y,
        data=df,
        hue=y,
        dodge=False,
        palette=palette,
        edgecolor=edgecolor,
        ax=ax,
        legend=False,  # Remover legenda automática gerada pelo hue
    )

    # Definição dos títulos e rótulos
    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=fontfamily,
        pad=title_padding,
    )
    ax.set_xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    ax.set_ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")

    # Adicionar rótulos nos valores das barras
    if annotate:
        for bar in ax.patches:
            width = bar.get_width()
            ax.annotate(
                f"{width:.1f}%",
                (width, bar.get_y() + bar.get_height() / 2),
                ha="left",
                va="center",
                fontfamily=fontfamily,
                fontsize=10,
                color="black",
                xytext=(5, 0),
                textcoords="offset points",
            )

    # Configuração de fontes e layout
    plt.xticks(fontfamily=fontfamily)
    plt.yticks(fontfamily=fontfamily)
    plt.tight_layout()
    plt.show()


def plot_evolution(
    df: pd.DataFrame,
    title: str = "Evolução na Quantidade de Visitas",
    x_labels: list = ["may", "june", "july", "august"],
    xlabel: str = "Month",
    ylabel: str = "Number of Visits",
    figsize: tuple = (12, 8),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    line_style: str = "-",
    marker_style: str = "o",
    grid: bool = True,
    grid_style: str = "--",
    grid_alpha: float = 0.6,
    legend_loc: str = "upper left",
    legend_bbox: tuple = (1.05, 1),
) -> None:
    """
    Plots the line chart showing the evolution of visits for the given betting houses with flexible customization options.

    :param df: DataFrame containing the betting houses data.
    :param title: Title of the plot.
    :param x_labels: List of labels for the x-axis (e.g., months).
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param line_style: Line style for the plots.
    :param marker_style: Marker style for the plots.
    :param grid: Whether to show grid lines.
    :param grid_style: Style of the grid lines.
    :param grid_alpha: Transparency of the grid lines.
    :param legend_loc: Location of the legend.
    :param legend_bbox: Bounding box location for the legend.
    """
    plt.figure(figsize=figsize)

    # Usar paleta de cores do seaborn para obter cores diferentes
    colors = sns.color_palette("husl", len(df))

    # Plotar a evolução para cada casa de aposta
    for i, (_, row) in enumerate(df.iterrows()):
        plt.plot(
            x_labels,
            row[x_labels],
            marker=marker_style,
            linestyle=line_style,
            color=colors[i],  # Cor única para cada casa de aposta
            label=row["betting_house"],
        )

    plt.title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        fontfamily=fontfamily,
        pad=title_padding,
    )
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.xticks(fontfamily=fontfamily)
    plt.yticks(fontfamily=fontfamily)
    plt.legend(title="Betting House", bbox_to_anchor=legend_bbox, loc=legend_loc)

    if grid:
        plt.grid(True, linestyle=grid_style, alpha=grid_alpha)

    plt.tight_layout()
    plt.show()


def plot_stable_rankings(
    df: pd.DataFrame,
    x_labels: list = ["may", "june", "july", "august"],
    y_columns: list = ["rank_may", "rank_june", "rank_july", "rank_august"],
    title: str = "Casas de Aposta com Ranking Mais Estável",
    xlabel: str = "Mês",
    ylabel: str = "Posição",
    figsize: tuple = (12, 8),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    line_style: str = "-",
    marker_style: str = "o",
    grid: bool = True,
    grid_style: str = "--",
    grid_alpha: float = 0.6,
    legend_loc: str = "upper left",
    legend_bbox: tuple = (1.05, 1),
    invert_yaxis: bool = True,
) -> None:
    """
    Plots the line chart showing the evolution of rankings for the given betting houses with flexible customization options.

    :param df: DataFrame containing the betting houses data.
    :param x_labels: List of labels for the x-axis (e.g., months).
    :param y_columns: List of columns representing the rankings over time.
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param line_style: Line style for the plots.
    :param marker_style: Marker style for the plots.
    :param grid: Whether to show grid lines.
    :param grid_style: Style of the grid lines.
    :param grid_alpha: Transparency of the grid lines.
    :param legend_loc: Location of the legend.
    :param legend_bbox: Bounding box location for the legend.
    :param invert_yaxis: Whether to invert the y-axis (lower is better for rankings).
    """
    plt.figure(figsize=figsize)

    # Plotar a evolução para cada casa de aposta
    for _, row in df.iterrows():
        plt.plot(
            x_labels,
            row[y_columns],
            marker=marker_style,
            linestyle=line_style,
            label=row["betting_house"],
        )

    plt.title(
        title,
        fontsize=15,
        fontweight="bold",
        fontfamily=fontfamily,
        pad=title_padding,
    )
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.xticks(fontfamily=fontfamily)
    plt.yticks(fontfamily=fontfamily)
    plt.legend(title="Betting House", bbox_to_anchor=legend_bbox, loc=legend_loc)

    if grid:
        plt.grid(True, linestyle=grid_style, alpha=grid_alpha)

    if invert_yaxis:
        plt.gca().invert_yaxis()  # Inverter o eixo y para mostrar a menor posição no topo

    plt.tight_layout()
    plt.show()


def calculate_monthly_variation(df: pd.DataFrame) -> dict:
    """
    Calculate the average ranking variation for each month and identify
    the month with the highest variation.

    :param df: DataFrame containing rank change columns for each month.
    :return: A dictionary with keys 'max_change_month',
             'max_change_value', 'percent_variation', and
             'top_changes_filtered'.
    """
    # Calcular a média da variação em cada mês
    avg_rank_changes_filtered = {
        "may_june": df["rank_change_may_june"].mean(),
        "june_july": df["rank_change_june_july"].mean(),
        "july_august": df["rank_change_july_august"].mean(),
    }

    # Identificar o mês com a maior variação média
    max_change_month = max(avg_rank_changes_filtered, key=avg_rank_changes_filtered.get)
    max_change_value = avg_rank_changes_filtered[max_change_month]

    # Identificar as casas de apostas com maior variação neste mês
    df["max_rank_change"] = df[f"rank_change_{max_change_month}"]
    top_changes_filtered = df.sort_values(by="max_rank_change", ascending=False).head(
        10
    )

    # Calcular a variação percentual
    total_houses_filtered = df.shape[0]
    percent_variation = (max_change_value / total_houses_filtered) * 100

    return {
        "max_change_month": max_change_month,
        "max_change_value": max_change_value,
        "percent_variation": percent_variation,
        "top_changes_filtered": top_changes_filtered,
    }


def plot_top_changes(
    df: pd.DataFrame,
    max_change_month: str,
    title: str = "Maiores Mudanças no Ranking",
    xlabel: str = "Mudança no Ranking",
    ylabel: str = "Casa de Aposta",
    bar_color: str = "lightcoral",
    figsize: tuple = (12, 8),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    invert_yaxis: bool = True,
) -> None:
    """
    Plots the top 10 betting houses with the highest ranking change in
    the specified month.

    :param df: DataFrame containing the top changes
        filtered for the specified month.
    :param max_change_month: String representing the month with the
        highest variation.
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param bar_color: Color of the bars.
    :param figsize: Tuple representing the size of the figure (width,
        height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param invert_yaxis: Whether to invert the y-axis (default is True).
    """
    plt.figure(figsize=figsize)
    plt.barh(
        df["betting_house"],
        df["max_rank_change"],
        color=bar_color,
    )
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.title(
        f"{title} ({max_change_month.replace('_', ' ').title()})",
        fontsize=15,
        fontweight="bold",
        pad=title_padding,
        fontfamily=fontfamily,
    )

    if invert_yaxis:
        plt.gca().invert_yaxis()  # Inverter o eixo y para mostrar a maior mudança no topo

    plt.tight_layout()
    plt.show()


def display_results(variation_data: dict) -> None:
    """
    Displays the results of the analysis in a formatted manner.

    :param variation_data: Dictionary containing the analysis results.
    """
    max_change_month_formatted = (
        variation_data["max_change_month"].replace("_", "-").title()
    )
    percent_variation = variation_data["percent_variation"]
    top_changes_filtered = variation_data["top_changes_filtered"]

    print(f"Mês com maior variação: {max_change_month_formatted}")
    print(
        f"Variação média de posições: {variation_data['max_change_value']:.1f} posições"
    )
    print(f"Porcentagem de variação média: {percent_variation:.1f}%")
    print("\nTop 10 casas de apostas com maior variação no mês:")
    for index, row in top_changes_filtered.iterrows():
        print(f"{row['betting_house']}: {row['max_rank_change']} posições")


def calculate_top_growth_brands(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the top growth brands based on their improvement in
    position over the last quarter.

    :param df: DataFrame containing rank and visit data.
    :return: DataFrame with top brands having continuous improvement and
        their visit and position variation.
    """
    # Filtrar casas de apostas com dados válidos nos últimos três meses (sem zeros ou nulos)
    df_filtered = df.dropna(subset=["june", "july", "august"])
    df_filtered = df_filtered[(df_filtered[["june", "july", "august"]] > 0).all(axis=1)]

    # Calcular a melhoria acumulada em posição ao longo do trimestre
    df_filtered["position_change_q3"] = (
        df_filtered["rank_june"] - df_filtered["rank_july"]
    ) + (df_filtered["rank_july"] - df_filtered["rank_august"])

    # Filtrar apenas as marcas que melhoraram continuamente suas posições
    df_filtered = df_filtered[df_filtered["position_change_q3"] > 0]

    # Calcular a variação de visitas em porcentagem do trimestre (junho a agosto)
    df_filtered["visit_change_q3_percent"] = (
        (df_filtered["august"] - df_filtered["june"]) / df_filtered["june"]
    ) * 100

    # Calcular a variação de posicionamento em porcentagem
    df_filtered["position_change_q3_percent"] = (
        (df_filtered["rank_june"] - df_filtered["rank_august"])
        / df_filtered["rank_june"]
    ) * 100

    # Selecionar as marcas com maior melhoria acumulada
    top_growth_brands = df_filtered.sort_values(
        by="position_change_q3", ascending=False
    ).head(10)

    return top_growth_brands


def display_growth_results(top_growth_brands: pd.DataFrame) -> None:
    """
    Displays the results of the top growth brands in a formatted manner.

    :param top_growth_brands: DataFrame containing top growth brands and
        their variation data.
    """
    print("Maior crescimento acumulado em posição no último trimestre:\n")
    for _, row in top_growth_brands.iterrows():
        print(f"{row['betting_house']}:")
        print(f"  Posição em junho: {row['rank_june']}")
        print(f"  Posição em julho: {row['rank_july']}")
        print(f"  Posição em agosto: {row['rank_august']}")
        print(f"  Melhoria acumulada em posição: {row['position_change_q3']} posições")
        print(f"  Variação de visitas: {row['visit_change_q3_percent']:.2f}%")
        print(
            f"  Variação de posicionamento: {row['position_change_q3_percent']:.2f}%\n"
        )


def plot_top_growth_brands(top_growth_brands: pd.DataFrame) -> None:
    """
    Plots a horizontal bar chart for the top growth brands showing their
    position change in the last quarter.

    :param top_growth_brands: DataFrame containing top growth brands and
        their variation data.
    """
    plt.figure(figsize=(12, 8))
    plt.barh(
        top_growth_brands["betting_house"],
        top_growth_brands["position_change_q3"],
        color="lightgreen",
    )
    plt.xlabel("Melhoria Acumulada em Posições")
    plt.ylabel("Casas de Apostas")
    plt.title(
        "Top 10 Marcas com Maior Crescimento Acumulado em Posição (Último Trimestre)"
    )
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def calculate_brands_performance(
    df: pd.DataFrame, performance_type: str = "growth"
) -> pd.DataFrame:
    """
    Calculates the top brands based on their performance (growth or
    decline) in position over the last quarter.

    :param df: DataFrame containing rank and visit data.
    :param performance_type: String indicating the type of performance
        to calculate: "growth" or "decline".
    :return: DataFrame with top brands having continuous improvement or
        decline and their visit and position variation.
    """
    # Filtrar casas de apostas com dados válidos nos últimos três meses (sem zeros ou nulos)
    df_filtered = df.dropna(subset=["june", "july", "august"])
    df_filtered = df_filtered[(df_filtered[["june", "july", "august"]] > 0).all(axis=1)]

    # Calcular a mudança acumulada em posição ao longo do trimestre
    df_filtered["position_change_q3"] = (
        df_filtered["rank_june"] - df_filtered["rank_july"]
    ) + (df_filtered["rank_july"] - df_filtered["rank_august"])

    # Filtrar marcas com base no tipo de performance desejada
    if performance_type == "growth":
        df_filtered = df_filtered[df_filtered["position_change_q3"] > 0]
    elif performance_type == "decline":
        df_filtered = df_filtered[df_filtered["position_change_q3"] < 0]

    # Calcular a variação de visitas em porcentagem do trimestre (junho a agosto)
    df_filtered["visit_change_q3_percent"] = (
        (df_filtered["august"] - df_filtered["june"]) / df_filtered["june"]
    ) * 100

    # Calcular a variação de posicionamento em porcentagem
    df_filtered["position_change_q3_percent"] = (
        (df_filtered["rank_june"] - df_filtered["rank_august"])
        / df_filtered["rank_june"]
    ) * 100

    # Selecionar as marcas com maior mudança acumulada
    if performance_type == "growth":
        top_brands = df_filtered.sort_values(
            by="position_change_q3", ascending=False
        ).head(10)
    elif performance_type == "decline":
        top_brands = df_filtered.sort_values(
            by="position_change_q3", ascending=True
        ).head(10)

    return top_brands


def display_performance_results(
    top_brands: pd.DataFrame, performance_type: str = "growth"
) -> None:
    """
    Displays the results of the top brands performance (growth or
    decline) in a formatted manner.

    :param top_brands: DataFrame containing top brands and their
        variation data.
    :param performance_type: String indicating the type of performance:
        "growth" or "decline".
    """
    if performance_type == "growth":
        print("Maior crescimento acumulado em posição no último trimestre:\n")
    elif performance_type == "decline":
        print("Maior queda acumulada em posição no último trimestre:\n")

    for _, row in top_brands.iterrows():
        print(f"{row['betting_house']}:")
        print(f"  Posição em junho: {row['rank_june']}")
        print(f"  Posição em julho: {row['rank_july']}")
        print(f"  Posição em agosto: {row['rank_august']}")
        print(f"  Mudança acumulada em posição: {row['position_change_q3']} posições")
        print(f"  Variação de visitas: {row['visit_change_q3_percent']:.2f}%")
        print(
            f"  Variação de posicionamento: {row['position_change_q3_percent']:.2f}%\n"
        )


def plot_brands_performance(
    df: pd.DataFrame,
    performance_type: str = "growth",
    title_growth: str = "Maior Crescimento Acumulado",
    title_decline: str = "Maior Queda Acumulada",
    xlabel: str = "Mudança Acumulada em Posições",
    ylabel: str = "Casas de Apostas",
    bar_color_growth: str = "lightcoral",
    bar_color_decline: str = "lightcoral",
    figsize: tuple = (12, 8),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    invert_yaxis: bool = True,
) -> None:
    """
    Plots a horizontal bar chart for the top brands showing their performance (growth or decline) in the last quarter.

    :param top_brands: DataFrame containing top brands and their variation data.
    :param performance_type: String indicating the type of performance: "growth" or "decline".
    :param title_growth: Title of the plot for growth.
    :param title_decline: Title of the plot for decline.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param bar_color_growth: Color of the bars for growth.
    :param bar_color_decline: Color of the bars for decline.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param invert_yaxis: Whether to invert the y-axis (default is True).
    """
    plt.figure(figsize=figsize)
    if performance_type == "growth":
        plt.barh(
            df["betting_house"],
            df["position_change_q3"],
            color=bar_color_growth,
        )
        plt.title(
            title_growth,
            fontsize=15,
            fontweight="bold",
            pad=title_padding,
            fontfamily=fontfamily,
        )
    elif performance_type == "decline":
        plt.barh(
            df["betting_house"],
            df["position_change_q3"],
            color=bar_color_decline,
        )
        plt.title(
            title_decline,
            fontsize=15,
            fontweight="bold",
            pad=title_padding,
            fontfamily=fontfamily,
        )

    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")

    if invert_yaxis:
        plt.gca().invert_yaxis()  # Inverter o eixo y para mostrar a maior mudança no topo

    plt.tight_layout()
    plt.show()


def identify_sustained_growth_brands(
    df: pd.DataFrame, growth_threshold: float = 50
) -> pd.DataFrame:
    """
    Identifies betting houses that had a significant growth in one month
    and sustained that growth throughout the quarter.

    :param df: DataFrame containing rank and visit data.
    :param growth_threshold: Percentage threshold to define significant
        growth in a month.
    :return: DataFrame with top brands that sustained their growth.
    """
    # Filtrar casas de apostas com dados válidos nos últimos três meses (sem zeros ou nulos)
    df_filtered = df.dropna(subset=["june", "july", "august"])
    df_filtered = df_filtered[
        (df_filtered[["june", "july", "august"]] > 0).all(axis=1)
    ].copy()

    # Calcular a variação percentual de visitas mês a mês
    df_filtered["growth_june_july"] = (
        (df_filtered["july"] - df_filtered["june"]) / df_filtered["june"] * 100
    )
    df_filtered["growth_july_august"] = (
        (df_filtered["august"] - df_filtered["july"]) / df_filtered["july"] * 100
    )

    # Filtrar casas que tiveram crescimento expressivo em junho ou julho
    df_growth_peak = df_filtered[
        (df_filtered["growth_june_july"] > growth_threshold)
        | (df_filtered["growth_july_august"] > growth_threshold)
    ].copy()

    # Calcular o crescimento total do trimestre em visitas e posição
    df_growth_peak["total_growth_visits_percent"] = (
        (df_growth_peak["august"] - df_growth_peak["june"])
        / df_growth_peak["june"]
        * 100
    )
    df_growth_peak["total_position_change"] = (
        df_growth_peak["rank_june"] - df_growth_peak["rank_august"]
    )

    # Selecionar casas que mantiveram crescimento ao longo do trimestre
    df_sustained_growth = df_growth_peak[
        (df_growth_peak["growth_june_july"] > 0)
        & (df_growth_peak["growth_july_august"] > 0)
        & (df_growth_peak["total_position_change"] > 0)
    ].copy()

    # Selecionar as marcas com maior crescimento sustentado
    top_sustained_growth = df_sustained_growth.sort_values(
        by="total_growth_visits_percent", ascending=False
    ).head(10)

    return top_sustained_growth


def display_sustained_growth_results(top_sustained_growth: pd.DataFrame) -> None:
    """
    Displays the results of the brands with sustained growth in a
    formatted manner.

    :param top_sustained_growth: DataFrame containing top sustained
        growth brands and their variation data.
    """
    print("Casas de apostas que mantiveram crescimento após pico mensal:\n")
    for _, row in top_sustained_growth.iterrows():
        print(f"{row['betting_house']}:")
        print(f"  Posição em junho: {row['rank_june']}")
        print(f"  Posição em julho: {row['rank_july']}")
        print(f"  Posição em agosto: {row['rank_august']}")
        print(f"  Crescimento junho-julho: {row['growth_june_july']:.2f}%")
        print(f"  Crescimento julho-agosto: {row['growth_july_august']:.2f}%")
        print(
            f"  Crescimento total de visitas: {row['total_growth_visits_percent']:.2f}%"
        )
        print(
            f"  Mudança acumulada em posição: {row['total_position_change']} posições\n"
        )


def plot_sustained_growth(
    df: pd.DataFrame,
    title: str = "Crescimento Sustentado em Visitas",
    xlabel: str = "Crescimento Total de Visitas (%)",
    ylabel: str = "Casas de Apostas",
    bar_color: str = "lightblue",
    figsize: tuple = (12, 8),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    invert_yaxis: bool = True,
) -> None:
    """
    Plots a horizontal bar chart for the top brands showing their
    sustained growth over the last quarter.

    :param df: DataFrame containing top sustained
        growth brands and their variation data.
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param bar_color: Color of the bars.
    :param figsize: Tuple representing the size of the figure (width,
        height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param invert_yaxis: Whether to invert the y-axis (default is True).
    """
    plt.figure(figsize=figsize)
    plt.barh(
        df["betting_house"],
        df["total_growth_visits_percent"],
        color=bar_color,
    )
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.title(
        title,
        fontsize=15,
        fontweight="bold",
        pad=title_padding,
        fontfamily=fontfamily,
    )

    if invert_yaxis:
        plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.show()
