
# 🏆 Club World Cup 2025 – Data Analysis Project

Este projeto realiza uma análise dos clubes, jogadores, treinadores e confrontos históricos relacionados ao **Mundial de Clubes da FIFA 2025**, incluindo também edições anteriores.

## 📚 Descrição

O projeto foi desenvolvido com o objetivo de:

- Consolidar dados de clubes campeões e seus títulos nacionais e continentais.
- Analisar o desempenho de clubes por continente ("Europa vs. Resto do Mundo").
- Listar os jogadores mais valiosos dos clubes participantes.
- Consolidar estatísticas de técnicos e suas conquistas.

As saídas são geradas em arquivos Excel para análise posterior.

---

## 🛠️ Estrutura do Projeto

```
club-world-cup-2025/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── world_club_titles.json
│   │   ├── curated/
│   │       ├── teams_manual.json
│   │       ├── coaches_manual.json
│   │       └── fixtures/  # Diversos arquivos JSON por edição
│   ├── processed/
│       ├── players.xlsx
│       ├── coaches.xlsx
│       ├── club_performance.xlsx
│       ├── club_titles.xlsx
├── src/
│   ├── constants.py
│   ├── loaders.py
│   ├── utils.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── leagues.py
│   │   ├── teams.py
│   │   ├── coaches.py
│   │   ├── players.py
│   │   └── fixtures.py
│   └── processing/
│       ├── __init__.py
│       ├── fixtures.py
│       ├── enrichment.py
│       ├── statistics.py
│       └── players.py
```

---

## 📈 Resultados Gerados

Os principais outputs do projeto, gerados em **`data/processed/`**, são:

- `club_titles.xlsx`: Quantidade de títulos nacionais e internacionais de cada clube participante.
- `club_performance.xlsx`: Desempenho consolidado dos clubes (vitórias, derrotas, gols, edições disputadas).
- `players.xlsx`: Lista de jogadores mais valiosos de cada clube.
- `club_players_summary.xlsx`: Resumo dos jogadores por clube (número de jogadores e valor de mercado total).
- `coaches.xlsx`: Informações e estatísticas de carreira dos treinadores.

---

## 🚀 Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/club-world-cup-2025.git
cd club-world-cup-2025
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o script principal:

```bash
python src/main.py
```

Os arquivos Excel serão gerados na pasta `data/processed/`.

