import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BACKGROUND_COLOR = "#f5f5f5"
FONTFAMILY = "monospace"
TITLE_PADDING = 15


def calculate_match_outcomes(
    df_results, home_team="Brazil", away_team="Colombia"
):
    matches = df_results[
        (
            (df_results["home_team"] == home_team)
            & (df_results["away_team"] == away_team)
        )
        | (
            (df_results["home_team"] == away_team)
            & (df_results["away_team"] == home_team)
        )
    ]

    outcomes = {"Brasil": 0, "Colombia": 0, "Empate": 0}

    for _, match in matches.iterrows():
        if (
            match["home_team"] == home_team
            and match["home_score"] > match["away_score"]
        ):
            outcomes["Brasil"] += 1
        elif (
            match["away_team"] == home_team
            and match["away_score"] > match["home_score"]
        ):
            outcomes["Brasil"] += 1
        elif (
            match["home_team"] == away_team
            and match["home_score"] > match["away_score"]
        ):
            outcomes["Colombia"] += 1
        elif (
            match["away_team"] == away_team
            and match["away_score"] > match["home_score"]
        ):
            outcomes["Colombia"] += 1
        else:
            outcomes["Empate"] += 1

    total_matches = sum(outcomes.values())
    outcome_distribution = {k: v / total_matches for k, v in outcomes.items()}

    outcome_df = pd.DataFrame(
        list(outcome_distribution.items()), columns=["Resultado", "Percentual"]
    )
    return outcome_df


def create_pie_chart(
    df,
    labels_col,
    values_col,
    title="",
    figsize=(8, 8),
    colors=["#ff9999", "#66b3ff", "#99ff99"],
):
    fig, ax = plt.subplots(figsize=figsize, facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    wedges, texts, autotexts = ax.pie(
        df[values_col],
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        textprops=dict(color="black", fontfamily=FONTFAMILY, fontsize=14),
    )

    for i, autotext in enumerate(autotexts):
        autotext.set_fontsize(14)
        autotext.set_fontfamily(FONTFAMILY)
        wedge_color = wedges[i].get_facecolor()
        if sum(wedge_color[:3]) / 3 > 0.5:
            autotext.set_color("black")

    for i, wedge in enumerate(wedges):
        ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        ax.annotate(
            df[labels_col][i],
            xy=(x, y),
            xytext=(1.1 * x, 1.1 * y),
            horizontalalignment=horizontalalignment,
            fontfamily=FONTFAMILY,
            fontsize=14,
            color="black",
            bbox=dict(facecolor="none", edgecolor="none", pad=5),
        )

    ax.set_title(
        title,
        fontsize=18,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )

    plt.show()


def calculate_team_performance(
    df_results, team_name, tournament=None, last_n_games=None
):
    if tournament:
        matches = df_results[
            (
                (df_results["home_team"] == team_name)
                | (df_results["away_team"] == team_name)
            )
            & (df_results["tournament"] == tournament)
        ]
    else:
        matches = df_results[
            (df_results["home_team"] == team_name)
            | (df_results["away_team"] == team_name)
        ]

    if last_n_games:
        matches = matches.sort_values(by="date", ascending=False).head(
            last_n_games
        )

    outcomes = {"Vitórias": 0, "Derrotas": 0, "Empates": 0}

    for _, match in matches.iterrows():
        if match["home_team"] == team_name:
            if match["home_score"] > match["away_score"]:
                outcomes["Vitórias"] += 1
            elif match["home_score"] < match["away_score"]:
                outcomes["Derrotas"] += 1
            else:
                outcomes["Empates"] += 1
        elif match["away_team"] == team_name:
            if match["away_score"] > match["home_score"]:
                outcomes["Vitórias"] += 1
            elif match["away_score"] < match["home_score"]:
                outcomes["Derrotas"] += 1
            else:
                outcomes["Empates"] += 1

    total_matches = sum(outcomes.values())
    outcome_distribution = {k: v / total_matches for k, v in outcomes.items()}

    outcome_df = pd.DataFrame(
        list(outcome_distribution.items()), columns=["Resultado", "Percentual"]
    )
    return outcome_df


def create_side_by_side_pie_charts(
    df1,
    df2,
    labels_col,
    values_col,
    title1="",
    title2="",
    figsize=(16, 8),
    colors=["#ff9999", "#66b3ff", "#99ff99"],
):
    fig, axs = plt.subplots(1, 2, figsize=figsize, facecolor=BACKGROUND_COLOR)
    axs[0].set_facecolor(BACKGROUND_COLOR)
    axs[1].set_facecolor(BACKGROUND_COLOR)

    wedges1, texts1, autotexts1 = axs[0].pie(
        df1[values_col],
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        textprops=dict(color="black", fontfamily=FONTFAMILY, fontsize=14),
    )

    for i, autotext in enumerate(autotexts1):
        autotext.set_fontsize(14)
        autotext.set_fontfamily(FONTFAMILY)
        wedge_color = wedges1[i].get_facecolor()
        if sum(wedge_color[:3]) / 3 > 0.5:
            autotext.set_color("black")

    for i, wedge in enumerate(wedges1):
        ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        axs[0].annotate(
            df1[labels_col][i],
            xy=(x, y),
            xytext=(1.1 * x, 1.1 * y),
            horizontalalignment=horizontalalignment,
            fontfamily=FONTFAMILY,
            fontsize=14,
            color="black",
            bbox=dict(facecolor="none", edgecolor="none", pad=5),
        )

    wedges2, texts2, autotexts2 = axs[1].pie(
        df2[values_col],
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        textprops=dict(color="black", fontfamily=FONTFAMILY, fontsize=14),
    )

    for i, autotext in enumerate(autotexts2):
        autotext.set_fontsize(14)
        autotext.set_fontfamily(FONTFAMILY)
        wedge_color = wedges2[i].get_facecolor()
        if sum(wedge_color[:3]) / 3 > 0.5:
            autotext.set_color("black")

    for i, wedge in enumerate(wedges2):
        ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        axs[1].annotate(
            df2[labels_col][i],
            xy=(x, y),
            xytext=(1.1 * x, 1.1 * y),
            horizontalalignment=horizontalalignment,
            fontfamily=FONTFAMILY,
            fontsize=14,
            color="black",
            bbox=dict(facecolor="none", edgecolor="none", pad=5),
        )

    axs[0].set_title(
        title1,
        fontsize=18,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    axs[1].set_title(
        title2,
        fontsize=18,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )

    plt.show()


def calculate_goal_percentage(
    df_results, team_name, tournament="Copa América"
):
    matches = df_results[
        (
            (df_results["home_team"] == team_name)
            | (df_results["away_team"] == team_name)
        )
        & (df_results["tournament"] == tournament)
    ]

    scored = matches[
        ((matches["home_team"] == team_name) & (matches["home_score"] > 0))
        | ((matches["away_team"] == team_name) & (matches["away_score"] > 0))
    ]

    outcomes = {
        "Marcou": len(scored),
        "Não Marcou": len(matches) - len(scored),
    }

    total_matches = sum(outcomes.values())
    outcome_distribution = {k: v / total_matches for k, v in outcomes.items()}

    outcome_df = pd.DataFrame(
        list(outcome_distribution.items()), columns=["Resultado", "Percentual"]
    )
    return outcome_df


def calculate_recent_goal_percentage(df_results, team_name, last_n_games=10):
    matches = (
        df_results[
            (df_results["home_team"] == team_name)
            | (df_results["away_team"] == team_name)
        ]
        .sort_values(by="date", ascending=False)
        .head(last_n_games)
    )

    scored = matches[
        ((matches["home_team"] == team_name) & (matches["home_score"] > 0))
        | ((matches["away_team"] == team_name) & (matches["away_score"] > 0))
    ]

    outcomes = {
        "Marcou": len(scored),
        "Não Marcou": len(matches) - len(scored),
    }

    total_matches = sum(outcomes.values())
    outcome_distribution = {k: v / total_matches for k, v in outcomes.items()}

    outcome_df = pd.DataFrame(
        list(outcome_distribution.items()), columns=["Resultado", "Percentual"]
    )
    return outcome_df


def calculate_goal_scenarios(
    df_results, home_team="Brazil", away_team="Colombia"
):
    matches = df_results[
        (
            (df_results["home_team"] == home_team)
            & (df_results["away_team"] == away_team)
        )
        | (
            (df_results["home_team"] == away_team)
            & (df_results["away_team"] == home_team)
        )
    ]

    scenarios = {
        "Ambos Marcaram": 0,
        "Ninguém Marcou": 0,
        "Só Brasil Marcou": 0,
        "Só Colombia Marcou": 0,
    }

    for _, match in matches.iterrows():
        brazil_goals = (
            match["home_score"]
            if match["home_team"] == home_team
            else match["away_score"]
        )
        colombia_goals = (
            match["away_score"]
            if match["home_team"] == home_team
            else match["home_score"]
        )

        if brazil_goals > 0 and colombia_goals > 0:
            scenarios["Ambos Marcaram"] += 1
        elif brazil_goals == 0 and colombia_goals == 0:
            scenarios["Ninguém Marcou"] += 1
        elif brazil_goals > 0 and colombia_goals == 0:
            scenarios["Só Brasil Marcou"] += 1
        elif brazil_goals == 0 and colombia_goals > 0:
            scenarios["Só Colombia Marcou"] += 1

    total_matches = sum(scenarios.values())
    scenario_distribution = {
        k: v / total_matches for k, v in scenarios.items()
    }

    scenario_df = pd.DataFrame(
        list(scenario_distribution.items()), columns=["Cenário", "Percentual"]
    )
    return scenario_df


def calculate_team_statistics(
    df_results, team_name, tournament="Copa América"
):
    matches = df_results[
        (
            (df_results["home_team"] == team_name)
            | (df_results["away_team"] == team_name)
        )
        & (df_results["tournament"] == tournament)
    ]

    stats = {
        "Marca e Vence": 0,
        "Marca e Empata": 0,
        "Marca e Perde": 0,
        "Não Marca": 0,
    }

    for _, match in matches.iterrows():
        if match["home_team"] == team_name:
            team_score = match["home_score"]
            opponent_score = match["away_score"]
        else:
            team_score = match["away_score"]
            opponent_score = match["home_score"]

        if team_score > 0:
            if team_score > opponent_score:
                stats["Marca e Vence"] += 1
            elif team_score < opponent_score:
                stats["Marca e Perde"] += 1
            else:
                stats["Marca e Empata"] += 1
        else:
            stats["Não Marca"] += 1

    total_matches = sum(stats.values())
    stats_distribution = {k: v / total_matches for k, v in stats.items()}

    stats_df = pd.DataFrame(
        list(stats_distribution.items()), columns=["Cenário", "Percentual"]
    )
    stats_df = stats_df.sort_values(by="Percentual", ascending=False)
    return stats_df


def create_horizontal_bar_plot(
    df1,
    df2,
    labels_col,
    values_col,
    title1="",
    title2="",
    figsize=(20, 8),
    colors=["#d3d3d3", "#a9a9a9", "#808080", "#696969"],
):
    fig, axs = plt.subplots(1, 2, figsize=figsize, facecolor=BACKGROUND_COLOR)
    fig.subplots_adjust(wspace=0.4)
    axs[0].set_facecolor(BACKGROUND_COLOR)
    axs[1].set_facecolor(BACKGROUND_COLOR)

    bars1 = axs[0].barh(
        df1[labels_col], df1[values_col], color=colors, edgecolor="black"
    )
    bars2 = axs[1].barh(
        df2[labels_col], df2[values_col], color=colors, edgecolor="black"
    )

    for bar in bars1:
        width = bar.get_width()
        percentage = f"{(width * 100):.1f}%"
        axs[0].annotate(
            percentage,
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(3, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )

    for bar in bars2:
        width = bar.get_width()
        percentage = f"{(width * 100):.1f}%"
        axs[1].annotate(
            percentage,
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(3, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )

    axs[0].set_title(
        title1,
        fontsize=18,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    axs[1].set_title(
        title2,
        fontsize=18,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )

    axs[0].set_xlabel(
        "Percentage",
        fontfamily=FONTFAMILY,
        loc="left",
        color="gray",
        fontsize=14,
    )
    axs[0].set_ylabel(
        "Scenario",
        fontfamily=FONTFAMILY,
        loc="bottom",
        color="gray",
        fontsize=14,
    )
    axs[1].set_xlabel(
        "Percentage",
        fontfamily=FONTFAMILY,
        loc="left",
        color="gray",
        fontsize=14,
    )
    axs[1].set_ylabel(
        "Scenario",
        fontfamily=FONTFAMILY,
        loc="bottom",
        color="gray",
        fontsize=14,
    )

    for spine in ["top", "right"]:
        axs[0].spines[spine].set_visible(False)
        axs[1].spines[spine].set_visible(False)

    plt.show()


def calculate_goal_intervals(
    df_goalscorers, df_results, tournament="Copa América"
):
    copa_matches = df_results[df_results["tournament"] == tournament]

    copa_goals = df_goalscorers.merge(
        copa_matches, on=["date", "home_team", "away_team"]
    )

    bins = [0, 15, 30, 45, 60, 75, 90]
    labels = ["0-15", "16-30", "31-45", "46-60", "61-75", "76-90"]

    copa_goals["interval"] = pd.cut(
        copa_goals["minute"], bins=bins, labels=labels, right=False
    )

    goal_counts = (
        copa_goals["interval"].value_counts(normalize=True).sort_index() * 100
    )

    return goal_counts.reset_index().rename(
        columns={"interval": "Intervalo", "proportion": "Percentual"}
    )


def create_vertical_bar_plot(
    df, x, y, title="", xlabel="", ylabel="", figsize=(12, 8), color="#244747"
):
    fig, ax = plt.subplots(figsize=figsize, facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)
    bars = ax.bar(df[x], df[y], color=color, edgecolor="black")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontfamily=FONTFAMILY,
            fontsize=12,
            color="black",
        )

    ax.set_title(
        title,
        fontsize=18,
        fontweight="bold",
        color="#323232",
        loc="left",
        fontfamily=FONTFAMILY,
        pad=TITLE_PADDING,
    )
    ax.set_xlabel(
        xlabel, fontfamily=FONTFAMILY, loc="left", color="gray", fontsize=14
    )
    ax.set_ylabel(
        ylabel, fontfamily=FONTFAMILY, loc="bottom", color="gray", fontsize=14
    )

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    plt.show()


def calculate_goal_intervals_brazil_colombia(
    df_goalscorers, df_results, home_team="Brazil", away_team="Colombia"
):
    matches = df_results[
        (
            (df_results["home_team"] == home_team)
            & (df_results["away_team"] == away_team)
        )
        | (
            (df_results["home_team"] == away_team)
            & (df_results["away_team"] == home_team)
        )
    ]

    goals_brazil_colombia = df_goalscorers.merge(
        matches, on=["date", "home_team", "away_team"]
    )

    bins = [0, 15, 30, 45, 60, 75, 90]
    labels = ["0-15", "16-30", "31-45", "46-60", "61-75", "76-90"]

    goals_brazil_colombia["interval"] = pd.cut(
        goals_brazil_colombia["minute"], bins=bins, labels=labels, right=False
    )

    goal_counts = (
        goals_brazil_colombia["interval"]
        .value_counts(normalize=True)
        .sort_index()
        * 100
    )

    return goal_counts.reset_index().rename(
        columns={"interval": "Intervalo", "proportion": "Percentual"}
    )


def calculate_goal_times(df_goalscorers, df_results, filter_matches):
    goals_data = df_goalscorers.merge(
        filter_matches, on=["date", "home_team", "away_team"]
    )

    goals_data["half"] = pd.cut(
        goals_data["minute"],
        bins=[0, 45, 90],
        labels=["1º Tempo", "2º Tempo"],
        right=False,
    )

    match_summary = goals_data.groupby(["date", "home_team", "away_team"])[
        "half"
    ].apply(lambda x: set(x))

    scenarios = {"Só 1º Tempo": 0, "Só 2º Tempo": 0, "Ambos": 0}

    matches_with_goals = set(match_summary.index)

    for match in matches_with_goals:
        halves = match_summary.loc[match]
        if len(halves) == 2:
            scenarios["Ambos"] += 1
        elif "1º Tempo" in halves:
            scenarios["Só 1º Tempo"] += 1
        elif "2º Tempo" in halves:
            scenarios["Só 2º Tempo"] += 1

    total_matches = sum(scenarios.values())
    scenario_distribution = {
        k: v / total_matches for k, v in scenarios.items()
    }

    scenario_df = pd.DataFrame(
        list(scenario_distribution.items()), columns=["Cenário", "Percentual"]
    )
    return scenario_df


def calculate_goal_distribution_brazil_colombia(
    df_results, home_team="Brazil", away_team="Colombia"
):
    matches = df_results[
        (
            (df_results["home_team"] == home_team)
            & (df_results["away_team"] == away_team)
        )
        | (
            (df_results["home_team"] == away_team)
            & (df_results["away_team"] == home_team)
        )
    ].copy()

    matches["total_goals"] = matches["home_score"] + matches["away_score"]

    bins = [0, 1, 2, 3, 4, float("inf")]
    labels = ["0", "1", "2", "3", "4 or more"]

    matches["goal_range"] = pd.cut(
        matches["total_goals"],
        bins=bins,
        labels=labels,
        right=False,
        include_lowest=True,
    )

    goal_distribution = (
        matches["goal_range"].value_counts(normalize=True).sort_index() * 100
    )

    return goal_distribution.reset_index().rename(
        columns={
            "goal_range": "Gols",
            "index": "Intervalo de Gols",
            "proportion": "Percentual",
        }
    )


def calculate_goal_distribution(df_results, tournament="Copa América"):
    matches = df_results[df_results["tournament"] == tournament]
    matches["total_goals"] = matches["home_score"] + matches["away_score"]

    bins = [0, 1, 2, 3, 4, float("inf")]
    labels = ["0", "1", "2", "3", "4 or mais"]

    matches["goal_range"] = pd.cut(
        matches["total_goals"],
        bins=bins,
        labels=labels,
        right=False,
        include_lowest=True,
    )

    goal_distribution = (
        matches["goal_range"].value_counts(normalize=True).sort_index() * 100
    )

    return goal_distribution.reset_index().rename(
        columns={
            "goal_range": "Gols",
            "index": "Intervalo de Gols",
            "proportion": "Percentual",
        }
    )
