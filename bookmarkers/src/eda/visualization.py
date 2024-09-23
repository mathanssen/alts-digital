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


def calculate_position_variation(
    df: pd.DataFrame, ranking_columns: list
) -> pd.DataFrame:
    """
    Calculates the position variation for betting houses across the given ranking columns.

    :param df: DataFrame containing betting houses and their rankings over time.
    :param ranking_columns: List of columns representing rankings over time.
    :return: DataFrame with betting houses, initial and final ranking, and position variation.
    """
    df["initial_rank"] = df[ranking_columns[0]]
    df["final_rank"] = df[ranking_columns[-1]]
    df["position_variation"] = df["initial_rank"] - df["final_rank"]

    # Classificar as casas de apostas
    df["performance"] = df["position_variation"].apply(
        lambda x: "Gained" if x > 0 else "Lost" if x < 0 else "Maintained"
    )

    return df[
        [
            "betting_house",
            "initial_rank",
            "final_rank",
            "position_variation",
            "performance",
        ]
    ]


def plot_position_gain_loss_simple(
    df: pd.DataFrame, title: str = "Position Gain/Loss for Betting Houses"
) -> None:
    """
    Plots a horizontal bar chart showing position gain/loss for betting houses.

    :param df: DataFrame containing betting houses and their position variations.
    :param title: Title of the plot.
    """
    df_sorted = df.sort_values(by="position_variation", ascending=False)

    plt.figure(figsize=(12, 8))
    plt.barh(
        df_sorted["betting_house"],
        df_sorted["position_variation"],
        color=df_sorted["performance"].map(
            {"Gained": "lightgreen", "Lost": "lightcoral", "Maintained": "lightgray"}
        ),
    )
    plt.xlabel("Position Variation")
    plt.ylabel("Betting House")
    plt.title(title)
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_position_gain_loss(
    df: pd.DataFrame,
    show_top_n: int = 5,
    show_only: str = None,
    title: str = "Position Gain/Loss for Betting Houses",
    xlabel: str = "Position Variation",
    ylabel: str = "Betting House",
    bar_color_gained: str = "lightgreen",
    bar_color_lost: str = "lightcoral",
    bar_color_maintained: str = "lightgray",
    figsize: tuple = (12, 8),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    invert_yaxis: bool = True,
) -> None:
    """
    Plots a horizontal bar chart showing position gain/loss for betting houses.

    :param df: DataFrame containing betting houses and their position variations.
    :param show_top_n: Number of top gainers and losers to show.
    :param show_only: "Gained", "Lost", or "Maintained" to show only those groups.
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param bar_color_gained: Color of bars for gained positions.
    :param bar_color_lost: Color of bars for lost positions.
    :param bar_color_maintained: Color of bars for maintained positions.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param invert_yaxis: Whether to invert the y-axis (default is True).
    """
    # Filtrar com base no parâmetro show_only
    if show_only in ["Gained", "Lost", "Maintained"]:
        df_filtered = df[df["performance"] == show_only]
    else:
        # Mostrar top N ganhadores e perdedores
        top_gainers = df[df["performance"] == "Gained"].nlargest(
            show_top_n, "position_variation"
        )
        top_losers = df[df["performance"] == "Lost"].nsmallest(
            show_top_n, "position_variation"
        )
        df_filtered = pd.concat([top_gainers, top_losers])

    df_sorted = df_filtered.sort_values(by="position_variation", ascending=False)

    plt.figure(figsize=figsize)
    plt.barh(
        df_sorted["betting_house"],
        df_sorted["position_variation"],
        color=df_sorted["performance"].map(
            {
                "Gained": bar_color_gained,
                "Lost": bar_color_lost,
                "Maintained": bar_color_maintained,
            }
        ),
    )
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.title(
        title,
        fontsize=15,
        fontweight="bold",
        fontfamily=fontfamily,
        pad=title_padding,
        loc="left",
    )

    if invert_yaxis:
        plt.gca().invert_yaxis()

    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def get_top_movers(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Returns a DataFrame with the top 'n' gainers, top 'n' losers, and those that maintained their position.

    :param df: DataFrame containing betting houses and their position variations.
    :param top_n: Number of top gainers and top losers to include.
    :return: DataFrame containing the top gainers, top losers, and maintained positions.
    """
    # Selecionar os que mantiveram a posição
    maintained_df = df[df["performance"] == "Maintained"]

    # Selecionar os maiores ganhadores
    top_gainers_df = df[df["performance"] == "Gained"].nlargest(
        top_n, "position_variation"
    )

    # Selecionar os maiores perdedores
    top_losers_df = df[df["performance"] == "Lost"].nsmallest(
        top_n, "position_variation"
    )

    # Concatenar os DataFrames
    result_df = pd.concat([maintained_df, top_gainers_df, top_losers_df]).reset_index(
        drop=True
    )

    return result_df


def calculate_drop_and_recovery(
    df: pd.DataFrame, ranking_columns: list
) -> pd.DataFrame:
    """
    Identifies betting houses that had a significant drop in one month and recovered in subsequent months.
    Returns the betting houses with the largest recoveries and their rankings over all months.

    :param df: DataFrame containing betting houses and their rankings over time.
    :param ranking_columns: List of columns representing rankings over time.
    :return: DataFrame with betting houses, rank in each month, and ordered by the largest recoveries.
    """
    recovery_data = []

    # Iterar sobre os meses para verificar quedas e recuperações subsequentes
    for i in range(len(ranking_columns) - 1):
        for j in range(i + 1, len(ranking_columns)):
            drop_col = ranking_columns[i]
            recovery_col = ranking_columns[j]

            # Identificar casas que tiveram queda e recuperação subsequente
            df_temp = df.copy()
            df_temp["drop_amount"] = df_temp[drop_col] - df_temp[recovery_col]
            df_temp["dropped"] = df_temp["drop_amount"] > 0
            df_temp["recovered"] = df_temp[recovery_col] < df_temp[drop_col]

            # Filtrar apenas casas que tiveram queda e recuperação
            df_dropped_recovered = df_temp[
                df_temp["dropped"] & df_temp["recovered"]
            ].copy()
            df_dropped_recovered["drop_month"] = drop_col
            df_dropped_recovered["recovery_month"] = recovery_col

            # Calcular a magnitude da recuperação
            df_dropped_recovered["recovery_amount"] = df_dropped_recovered[
                "drop_amount"
            ]

            # Armazenar resultados na lista
            recovery_data.append(df_dropped_recovered)

    # Concatenar todos os resultados
    if recovery_data:
        df_recovered = pd.concat(recovery_data, ignore_index=True)
    else:
        df_recovered = pd.DataFrame(
            columns=["betting_house"] + ranking_columns + ["recovery_amount"]
        )

    # Agrupar por casa de apostas e calcular a maior recuperação para cada uma
    df_recovered_max = df_recovered.groupby("betting_house", as_index=False).agg(
        {
            "recovery_amount": "max",
            ranking_columns[0]: "first",
            ranking_columns[1]: "first",
            ranking_columns[2]: "first",
            ranking_columns[3]: "first",
        }
    )

    # Ordenar pelo maior valor de recuperação
    df_recovered_max = df_recovered_max.sort_values(
        by="recovery_amount", ascending=False
    ).reset_index(drop=True)

    return df_recovered_max[["betting_house"] + ranking_columns + ["recovery_amount"]]


def plot_position_recovery_trend(
    df: pd.DataFrame,
    ranking_columns: list = ["rank_may", "rank_june", "rank_july", "rank_august"],
    title: str = "Recovery Trend of Betting Houses",
    figsize: tuple = (12, 6),
    fontfamily: str = "monospace",
    title_padding: int = 15,
    marker: str = "o",
    legend_title: str = "Betting House",
    grid_style: str = "--",
    grid_alpha: float = 0.6,
) -> None:
    """
    Plots the position trend for betting houses that dropped and recovered over time.

    :param df: DataFrame containing the betting houses and their rankings.
    :param ranking_columns: List of columns representing rankings over time.
    :param title: Title of the plot.
    :param figsize: Size of the figure (width, height).
    :param fontfamily: Font family for the text in the plot.
    :param title_padding: Padding for the title.
    :param line_color: Color of the lines in the plot.
    :param marker: Marker style for the points.
    :param legend_title: Title for the legend.
    :param grid_style: Line style for the grid.
    :param grid_alpha: Transparency level for the grid lines.
    """
    months = ranking_columns

    plt.figure(figsize=figsize, facecolor=BACKGROUND_COLOR)
    plt.gca().set_facecolor(BACKGROUND_COLOR)

    for _, row in df.iterrows():
        plt.plot(
            months,
            row[months],
            marker=marker,
            label=row["betting_house"],
        )

    plt.title(
        title, fontsize=15, fontweight="bold", pad=title_padding, fontfamily=fontfamily
    )
    plt.xlabel("Month", fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(
        "Ranking Position (Lower is Better)",
        fontfamily=fontfamily,
        fontsize=12,
        color="gray",
    )
    plt.legend(
        title=legend_title, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10
    )
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle=grid_style, alpha=grid_alpha)
    plt.xticks(fontfamily=fontfamily)
    plt.yticks(fontfamily=fontfamily)
    plt.tight_layout()
    plt.show()


def identify_significant_drops(
    df: pd.DataFrame, columns: list, drop_threshold: int = 3
) -> pd.DataFrame:
    """
    Identifies betting houses with significant drops in rankings between
    consecutive months.

    :param df: DataFrame containing betting houses and their rankings
        over time.
    :param columns: List of columns representing rankings over
        consecutive months.
    :param drop_threshold: Minimum drop in ranking positions considered
        significant.
    :return: DataFrame with betting houses and their significant drops.
    """
    df_drops = pd.DataFrame()
    for i in range(len(columns) - 1):
        df_temp = df.copy()
        df_temp["drop"] = df[columns[i]] - df[columns[i + 1]]
        df_temp = df_temp[df_temp["drop"] >= drop_threshold]
        df_temp["from_month"] = columns[i]
        df_temp["to_month"] = columns[i + 1]
        df_temp["significant_drop"] = df_temp["drop"]
        df_drops = pd.concat(
            [
                df_drops,
                df_temp[
                    ["betting_house", "from_month", "to_month", "significant_drop"]
                ],
            ]
        )

    return df_drops.reset_index(drop=True)


def identify_recoveries(
    df: pd.DataFrame, drop_df: pd.DataFrame, columns: list
) -> pd.DataFrame:
    """
    Identifies betting houses that recovered their rankings after a significant drop.

    :param df: DataFrame containing betting houses and their rankings over time.
    :param drop_df: DataFrame containing betting houses with significant drops.
    :param columns: List of columns representing rankings over consecutive months.
    :return: DataFrame with betting houses that recovered after a significant drop.
    """
    recoveries = []
    for _, row in drop_df.iterrows():
        house = row["betting_house"]
        from_month = row["from_month"]
        to_month = row["to_month"]
        drop_index = columns.index(to_month)
        if drop_index + 1 < len(columns):
            # Verificar se recuperou no mês seguinte
            recovery = df.loc[
                df["betting_house"] == house, columns[drop_index + 1]
            ].values[0]
            if recovery < df.loc[df["betting_house"] == house, to_month].values[0]:
                recoveries.append(
                    {
                        "betting_house": house,
                        "drop_month": to_month,
                        "recovery_month": columns[drop_index + 1],
                        "position_drop": row["significant_drop"],
                        "position_recovered": df.loc[
                            df["betting_house"] == house, to_month
                        ].values[0]
                        - recovery,
                    }
                )
    return pd.DataFrame(recoveries)


def plot_recoveries(
    df: pd.DataFrame, title: str = "Betting Houses with Successful Recoveries"
) -> None:
    """
    Plots a horizontal bar chart showing the recoveries of betting houses after a significant drop.

    :param df: DataFrame containing betting houses and their recoveries.
    :param title: Title of the plot.
    """
    if df.empty:
        print("No recoveries to plot.")
        return

    df["recovery"] = df["position_recovered"]
    plt.figure(figsize=(12, 8))
    plt.barh(df["betting_house"], df["recovery"], color="lightblue")
    plt.xlabel("Recovered Positions")
    plt.ylabel("Betting House")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def calculate_position_and_visit_variation(
    df: pd.DataFrame, ranking_columns: list, visit_columns: list
) -> pd.DataFrame:
    """
    Calculates the variation in positions and visits for betting houses between all consecutive months.

    :param df: DataFrame containing betting houses, rankings, and visits over time.
    :param ranking_columns: List of columns representing rankings over time.
    :param visit_columns: List of columns representing visits over time.
    :return: DataFrame with betting houses, position variation, and visit variation for all consecutive months.
    """
    df_variation = df.copy()

    # Calcular variação de posição entre todos os meses consecutivos
    for i in range(len(ranking_columns) - 1):
        df_variation[
            f"position_variation_{ranking_columns[i]}_{ranking_columns[i+1]}"
        ] = (df[ranking_columns[i]] - df[ranking_columns[i + 1]])

    # Calcular variação percentual de visitas entre todos os meses consecutivos
    for i in range(len(visit_columns) - 1):
        df_variation[f"visit_variation_{visit_columns[i]}_{visit_columns[i+1]}"] = (
            (df[visit_columns[i + 1]] - df[visit_columns[i]])
            / df[visit_columns[i]]
            * 100
        )

    return df_variation


def plot_position_vs_visits(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "Position vs Visits Variation",
    xlabel: str = "Position Variation",
    ylabel: str = "Visit Variation (%)",
    figsize: tuple = (8, 4),
    fontfamily: str = "monospace",
    point_color: str = "blue",
) -> None:
    """
    Plots the relationship between position variation and visit variation for betting houses.

    :param df: DataFrame containing betting houses, position variations, and visit variations.
    :param x_column: Column name for the x-axis (position variation).
    :param y_column: Column name for the y-axis (visit variation).
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param fontfamily: Font family for text in the plot.
    :param point_color: Color for all points in the scatter plot.
    """
    plt.figure(figsize=figsize)
    sns.scatterplot(
        x=x_column,
        y=y_column,
        data=df,
        color=point_color,
        s=100,
    )
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.title(title, fontsize=15, fontweight="bold", fontfamily=fontfamily)
    plt.axhline(0, color="gray", linestyle="--", alpha=0.5)
    plt.axvline(0, color="gray", linestyle="--", alpha=0.5)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend([], [], frameon=False)
    plt.tight_layout()
    plt.show()


def plot_position_vs_visits_simple(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "Position vs Visits Variation",
) -> None:
    """
    Plots the relationship between position variation and visit variation for betting houses.

    :param df: DataFrame containing betting houses, position variations, and visit variations.
    :param x_column: Column name for the x-axis (position variation).
    :param y_column: Column name for the y-axis (visit variation).
    :param title: Title of the plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_column, y=y_column, data=df, hue="betting_house")
    plt.xlabel("Position Variation")
    plt.ylabel("Visit Variation (%)")
    plt.title(title)
    plt.axhline(0, color="gray", linestyle="--", alpha=0.5)
    plt.axvline(0, color="gray", linestyle="--", alpha=0.5)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def get_top_position_variations(
    df: pd.DataFrame, ranking_columns: list, top_n: int = 5
) -> pd.DataFrame:
    """
    Identifies betting houses with the highest positive and negative position variations between consecutive months.

    :param df: DataFrame containing betting houses and their rankings over time.
    :param ranking_columns: List of columns representing rankings over consecutive months.
    :param top_n: Number of top gainers and losers to return.
    :return: DataFrame with betting houses and their position variations.
    """
    variation_df = pd.DataFrame()

    for i in range(len(ranking_columns) - 1):
        df_temp = df.copy()
        df_temp["position_change"] = df[ranking_columns[i]] - df[ranking_columns[i + 1]]
        df_temp["from_month"] = ranking_columns[i]
        df_temp["to_month"] = ranking_columns[i + 1]
        df_temp["variation_type"] = df_temp["position_change"].apply(
            lambda x: "positive" if x > 0 else "negative"
        )

        # Selecionar as maiores variações positivas e negativas
        top_positive = df_temp[df_temp["variation_type"] == "positive"].nlargest(
            top_n, "position_change"
        )
        top_negative = df_temp[df_temp["variation_type"] == "negative"].nsmallest(
            top_n, "position_change"
        )

        variation_df = pd.concat([variation_df, top_positive, top_negative])

    return variation_df.reset_index(drop=True)


def calculate_visit_variation(df: pd.DataFrame, visit_columns: list) -> pd.DataFrame:
    """
    Calculates the percentage variation in visits for the identified betting houses.

    :param df: DataFrame containing betting houses and their position variations.
    :param visit_columns: List of columns representing visits over consecutive months.
    :return: DataFrame with betting houses, visit variations, and position variations.
    """
    df_visit_variation = df.copy()
    visit_variations = []

    for index, row in df.iterrows():
        from_month = row["from_month"].replace("rank_", "")
        to_month = row["to_month"].replace("rank_", "")

        # Identificar as colunas de visita correspondentes
        visit_from = f"{from_month}"
        visit_to = f"{to_month}"

        # Calcular variação percentual de visitas
        if visit_from in visit_columns and visit_to in visit_columns:
            initial_visit = df.loc[index, visit_from]
            final_visit = df.loc[index, visit_to]
            visit_variation = ((final_visit - initial_visit) / initial_visit) * 100
            visit_variations.append(visit_variation)
        else:
            visit_variations.append(None)

    df_visit_variation["visit_variation_percent"] = visit_variations

    return df_visit_variation


def display_position_and_visit_changes(df: pd.DataFrame) -> None:
    """
    Displays the betting houses with the highest positive and negative position variations,
    along with their visit variations.

    :param df: DataFrame containing betting houses, position variations, and visit variations.
    """
    for _, row in df.iterrows():
        print(f"{row['betting_house']}:")
        print(
            f"  De {row['from_month'].replace('rank_', '').capitalize()} para {row['to_month'].replace('rank_', '').capitalize()}:"
        )
        print(
            f"  Mudança de posição: {row['position_change']} posições {'positivas' if row['position_change'] > 0 else 'negativas'}"
        )
        print(f"  Variação de visitas: {row['visit_variation_percent']:.2f}%\n")


def plot_monthly_visits_sum(
    df: pd.DataFrame,
    month_columns: list,
    bar_color: str = "skyblue",
    title: str = "Total Monthly Visits",
    xlabel: str = "Month",
    ylabel: str = "Total Visits",
    figsize: tuple = (10, 6),
    fontfamily: str = FONTFAMILY,
    title_padding: int = TITLE_PADDING,
    x_label_color: str = "gray",
    y_label_color: str = "gray",
    x_ticks_fontsize: int = 12,
    y_ticks_fontsize: int = 12,
    y_min: float = None,
    y_max: float = None,
    show_values: bool = True,
    value_fontsize: int = 10,
    value_color: str = "black",
    value_offset: tuple = (0, 5),
) -> None:
    """
    Plots the total visits for each month as a bar chart with rounded values and a single bar color.

    :param df: Input DataFrame containing the monthly visit columns.
    :param month_columns: List of columns representing the months.
    :param bar_color: Color of the bars in the chart (default is "skyblue").
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param figsize: Tuple representing the size of the figure (width, height).
    :param fontfamily: Font family for text in the plot.
    :param title_padding: Padding for the title.
    :param x_label_color: Color for x-axis label.
    :param y_label_color: Color for y-axis label.
    :param x_ticks_fontsize: Font size for x-axis ticks.
    :param y_ticks_fontsize: Font size for y-axis ticks.
    :param y_min: Minimum value for the y-axis.
    :param y_max: Maximum value for the y-axis.
    :param show_values: Boolean to show or hide values on top of bars.
    :param value_fontsize: Font size for values displayed on top of bars.
    :param value_color: Color of the values displayed on top of bars.
    :param value_offset: Offset for the values displayed on top of bars (x, y).
    """
    # Calcular a soma das visitas para cada mês
    monthly_visits_sum = df[month_columns].sum()

    # Função para formatar os números grandes
    def format_large_numbers(value):
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.1f} bilhões"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.1f} milhões"
        elif value >= 1_000:
            return f"{value / 1_000:.1f} mil"
        else:
            return str(int(value))

    # Criar o gráfico de barras com a mesma cor para todas as barras
    fig, ax = plt.subplots(figsize=figsize, facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    sns.barplot(
        x=monthly_visits_sum.index,
        y=monthly_visits_sum.values,
        color=bar_color,  # Definindo uma única cor para todas as barras
        edgecolor="black",
        ax=ax,
    )

    # Adicionar rótulos em cima das barras com formatação de números
    if show_values:
        for index, value in enumerate(monthly_visits_sum):
            ax.annotate(
                format_large_numbers(value),
                (index, value),
                ha="center",
                va="bottom",
                fontfamily=fontfamily,
                fontsize=value_fontsize,
                color=value_color,
                xytext=value_offset,
                textcoords="offset points",
            )

    # Ajustar limites do eixo y
    if y_min is not None or y_max is not None:
        plt.ylim(y_min, y_max)

    # Definir título e rótulos
    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=fontfamily,
        pad=title_padding,
    )
    ax.set_xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color=x_label_color)
    ax.set_ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color=y_label_color)

    plt.xticks(fontfamily=fontfamily, fontsize=x_ticks_fontsize)
    plt.yticks(fontfamily=fontfamily, fontsize=y_ticks_fontsize)
    plt.tight_layout()
    plt.show()


def generate_comparison_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a summary DataFrame comparing position and visit variations.

    :param df: DataFrame containing position and visit variations.
    :return: Summary DataFrame with average variations and stability status.
    """
    df_summary = df.copy()

    # Calcular a média das variações de posição e visitas
    position_columns = [
        col for col in df.columns if col.startswith("position_variation")
    ]
    visit_columns = [col for col in df.columns if col.startswith("visit_variation")]

    df_summary["avg_position_variation"] = df_summary[position_columns].mean(axis=1)
    df_summary["avg_visit_variation_percent"] = df_summary[visit_columns].mean(axis=1)

    # Classificar as casas como estáveis ou instáveis
    df_summary["stability_status"] = df_summary.apply(
        lambda row: "Stable" if abs(row["avg_position_variation"]) < 1 else "Unstable",
        axis=1,
    )

    # Retornar apenas colunas relevantes
    return df_summary[
        [
            "betting_house",
            "avg_position_variation",
            "avg_visit_variation_percent",
            "stability_status",
        ]
    ]


def prepare_input_for_plot_adjusted(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the input DataFrame for the position vs. visit variation plot,
    with predefined ranking and visit columns. Also includes the ranking in May
    and formats the visit variation as percentages.

    :param df: Original DataFrame containing betting houses, rankings, and visits.
    :return: Prepared DataFrame with average variations, stability status, ranking in May, and formatted visit variations.
    """
    # Definindo as colunas de ranking e visitas
    ranking_columns_example = ["rank_may", "rank_june", "rank_july", "rank_august"]
    visit_columns_example = ["may", "june", "july", "august"]

    # Step 1: Calculate position and visit variations
    df_variation = calculate_position_and_visit_variation(
        df, ranking_columns_example, visit_columns_example
    )

    # Step 2: Generate the summary DataFrame with average variations and stability status
    df_summary = generate_comparison_summary(df_variation)

    # Step 3: Add the final ranking column and initial ranking in May to the summary DataFrame
    if "rank_august" in df.columns:
        df_summary["rank_august"] = df["rank_august"]
    else:
        raise KeyError(
            "The final ranking column 'rank_august' is not present in the DataFrame."
        )

    if "rank_may" in df.columns:
        df_summary["rank_may"] = df["rank_may"]
    else:
        raise KeyError(
            "The initial ranking column 'rank_may' is not present in the DataFrame."
        )

    # Step 4: Format the avg_visit_variation_percent as percentages
    df_summary["avg_visit_variation_percent"] = df_summary[
        "avg_visit_variation_percent"
    ].apply(lambda x: f"{x:.1f}%")
    df_summary = df_summary[
        [
            "betting_house",
            "rank_may",
            "rank_august",
            "stability_status",
            "avg_visit_variation_percent",
        ]
    ]

    return df_summary


def plot_position_vs_visits_comparison(
    df: pd.DataFrame,
    title: str = "Comparison of Position and Visit Variations",
    figsize: tuple = (10, 6),
    point_color_stable: str = "green",
    point_color_unstable: str = "red",
    fontfamily: str = "monospace",
    grid_style: str = "--",
    grid_alpha: float = 0.6,
    xlabel: str = "Average Visit Variation (%)",
    ylabel: str = "Average Position Variation",
) -> None:
    """
    Plots the comparison of position variation and visit variation for betting houses.

    :param df: DataFrame containing average variations and stability status.
    :param title: Title of the plot.
    :param figsize: Size of the figure (width, height).
    :param point_color_stable: Color of the points for stable betting houses.
    :param point_color_unstable: Color of the points for unstable betting houses.
    :param fontfamily: Font family for text in the plot.
    :param grid_style: Line style for the grid.
    :param grid_alpha: Transparency level for the grid lines.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    """
    plt.figure(figsize=figsize, facecolor=BACKGROUND_COLOR)
    plt.gca().set_facecolor(BACKGROUND_COLOR)

    # Plotar casas de apostas estáveis
    stable_df = df[df["stability_status"] == "Stable"]
    unstable_df = df[df["stability_status"] == "Unstable"]

    plt.scatter(
        stable_df["avg_visit_variation_percent"],
        stable_df["avg_position_variation"],
        color=point_color_stable,
        label="Stable",
        s=100,
        alpha=0.7,
    )

    # Plotar casas de apostas instáveis
    plt.scatter(
        unstable_df["avg_visit_variation_percent"],
        unstable_df["avg_position_variation"],
        color=point_color_unstable,
        label="Unstable",
        s=100,
        alpha=0.7,
    )

    # Adicionar legendas e texto ao gráfico
    for i, row in df.iterrows():
        plt.text(
            row["avg_visit_variation_percent"],
            row["avg_position_variation"],
            row["betting_house"],
            fontsize=9,
            fontfamily=fontfamily,
            ha="right" if row["avg_visit_variation_percent"] > 0 else "left",
        )

    plt.axhline(0, color="gray", linestyle=grid_style, alpha=grid_alpha)
    plt.axvline(0, color="gray", linestyle=grid_style, alpha=grid_alpha)
    plt.title(title, fontsize=15, fontweight="bold", fontfamily=fontfamily, pad=15)
    plt.xlabel(xlabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.ylabel(ylabel, fontfamily=fontfamily, fontsize=12, color="gray")
    plt.grid(True, linestyle=grid_style, alpha=grid_alpha)
    plt.xticks(fontfamily=fontfamily)
    plt.yticks(fontfamily=fontfamily)
    plt.legend(title="Stability", loc="upper right", fontsize=10)
    plt.tight_layout()
    plt.show()
