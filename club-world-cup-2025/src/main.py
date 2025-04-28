import asyncio

from loaders import load_coaches_data, load_club_titles_data
from processing.fixtures import process_fixtures
from processing.players import fetch_players_data, summarize_players_by_club
from processing.statistics import generate_club_statistics

# Clubes com Mais Títulos no Mundial de Clubes FIFA 2025
titles_df = load_club_titles_data()
titles_df.to_excel("outputs/club_titles.xlsx", index=False)

# Europa vs. Resto do Mundo – Desempenho dos Continentes em Perspectiva
df_combined_fixtures, teams_combined_df = asyncio.run(process_fixtures())
club_statistics_df = generate_club_statistics(df_combined_fixtures, teams_combined_df)
club_statistics_df.to_excel("outputs/club_performance.xlsx", index=False)

# Jogadores Mais Valiosos do Mundial de Clubes 2025
players_df = fetch_players_data()
players_df.to_excel("outputs/players.xlsx", index=False)

club_summary = summarize_players_by_club(players_df)
club_summary.to_excel("outputs/club_players_summary.xlsx", index=False)

# Técnicos do Mundial: Desempenho e Conquistas
coaches_df = load_coaches_data()
coaches_df.to_excel("outputs/coaches.xlsx", index=False)
