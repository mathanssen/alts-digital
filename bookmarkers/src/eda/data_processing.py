import pandas as pd


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the input DataFrame by renaming columns, ensuring
    numeric values, and filtering out rows with null or zero values in
    the specified months. Converts specified columns to integer type.

    :param df: Original DataFrame to be preprocessed.
    :return: Preprocessed DataFrame.
    """
    months = ["may", "june", "july", "august"]

    df = df.rename(
        columns={
            "Casa de apostas": "betting_house",
            "Março": "march",
            "Abril": "april",
            "Maio": "may",
            "Junho": "june",
            "Julho": "july",
            "Agosto": "august",
        }
    ).drop(["Top"], axis=1, errors="ignore")

    # Garantir que as colunas dos meses sejam numéricas
    df[months] = df[months].apply(pd.to_numeric, errors="coerce")

    # Remover colunas de março e abril
    df = df.drop(columns=["march", "april"], errors="ignore")

    # Remover linhas com valores nulos ou zero nos meses restantes
    df = df.dropna(subset=months)
    df = df[(df[months] > 0).all(axis=1)].reset_index(drop=True)

    # Calcular o ranking de cada mês
    df["rank_may"] = df["may"].rank(method="min", ascending=False).astype(int)
    df["rank_june"] = df["june"].rank(method="min", ascending=False).astype(int)
    df["rank_july"] = df["july"].rank(method="min", ascending=False).astype(int)
    df["rank_august"] = df["august"].rank(method="min", ascending=False).astype(int)

    # Calcular a mudança de ranking entre os meses
    df["rank_change_may_june"] = abs(df["rank_june"] - df["rank_may"]).astype(int)
    df["rank_change_june_july"] = abs(df["rank_july"] - df["rank_june"]).astype(int)
    df["rank_change_july_august"] = abs(df["rank_august"] - df["rank_july"]).astype(int)

    # Calcular o crescimento percentual
    df["growth_percentage"] = ((df["august"] - df["may"]) / df["may"]) * 100

    return df
