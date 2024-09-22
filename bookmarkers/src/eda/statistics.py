import pandas as pd


def calculate_mean_visits(row: pd.Series) -> float:
    """
    Calculates the mean visits for a row, excluding zeros and null
    values.

    :param row: A row of the DataFrame.
    :return: The mean of the valid visit values.
    """
    valid_visits = row[["may", "june", "july", "august"]].replace(-1, pd.NA).dropna()
    return valid_visits.mean()


def format_visits(value: float) -> str:
    """
    Formats the visit number into a readable string.

    :param value: A float representing the average number of visits.
    :return: A formatted string representing the value.
    """
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f} milhões"
    elif value >= 1_000:
        return f"{value / 1_000:.1f} mil"
    else:
        return f"{value:.0f}"


def get_avg_visits(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame with initial and final ranks, along with the
    average visits.

    :param df: Input DataFrame with ranking and visit data.
    :return: A new DataFrame with formatted ranks and average visits.
    """
    df_new = df[["betting_house", "rank_may", "rank_august"]].copy()
    df_new.rename(
        columns={"rank_may": "initial_rank", "rank_august": "final_rank"}, inplace=True
    )
    df_new["initial_rank"] = df_new["initial_rank"].astype(int)
    df_new["final_rank"] = df_new["final_rank"].astype(int)
    df_new["average_visits"] = df.apply(calculate_mean_visits, axis=1)
    df_new["average_visits"] = df_new["average_visits"].apply(format_visits)

    return df_new
