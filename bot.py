from tennis_explorer_scraper import get_te_matchlist_all, get_te_match_json, get_te_player
from pandarallel import pandarallel
import pandas as pd
from datetime import datetime
import pycountry
import flag

pandarallel.initialize()

games = get_te_matchlist_all()

def get_match_data(row):
  print(f"getting match data for {row['match_link']}")

  try:
    match_data = get_te_match_json(match_url=row['match_link'])
    row['player1_ranking'] = int(match_data['player1']['ranking_pos'].rstrip('.'))
    row['player2_ranking'] = int(match_data['player2']['ranking_pos'].rstrip('.'))
    row['surface'] = match_data['surface']
    row['event_name'] = match_data['event_name']
    row['tournament'] = match_data['tournament']
    row['round'] = match_data['round']
    row['tour'] = match_data['tour']
    row['matchtype'] = match_data['matchtype']
    row['player1_link'] =  match_data['player1']['te_link']
    row['player1_name'] =  match_data['player1']['name']
    row['player2_link'] =  match_data['player2']['te_link']
    row['player2_name'] =  match_data['player2']['name']
    row['match_date'] =  row['date']
    row['match_time'] =  row['time']
  except ValueError:
    print(f"failed to get match data for {row['match_link']}")
    pass

  return row

# to debug with breakpoint(), use apply instead of parallel_apply
# head in case I want to limit when developing locally
# get games of the day when both players have ranking position <= 50
match_data = games.head(5000).parallel_apply(get_match_data, axis=1).query('status != "complete"').query('player1_ranking <= 50 and player2_ranking <= 50')

full_games = pd.merge(games, match_data, left_on="match_link", right_on="match_link")

def get_player_data(row):
  print(f"getting player data for {row['player1_link']} and {row['player2_link']}")

  try:
    player1_data = get_te_player(player_url=row['player1_link'])
    player2_data = get_te_player(player_url=row['player2_link'])
    player1_country = player1_data['player_country'][0]
    player2_country = player2_data['player_country'][0]

    try:
      row['player1_country_emoji'] = flag.flag(
        pycountry.countries.search_fuzzy(player1_country)[0].alpha_2
      )
    except LookupError:
      print(f"couldn't find country {player1_country}")
      row['player1_country_emoji'] = player1_country

    try:
      row['player2_country_emoji'] = flag.flag(
        pycountry.countries.search_fuzzy(player2_country)[0].alpha_2
      )
    except LookupError:
      print(f"couldn't find country {player2_country}")
      row['player2_country_emoji'] = player2_country
  except:
    print(f"failed to get player data for {row}")
    pass

  row["tweet"] = f"""
  Game: {row['player1_country_emoji']} {row['player1_name']} (rank #{int(row['player1_ranking'])}) vs {row['player2_country_emoji']} {row['player2_name']} (rank #{int(row['player2_ranking'])})
  Tournament: {row['tour'].upper()} {row['tournament']} ({row['matchtype']} - {row['round']})
  Local time: {row['match_time']}
  Surface: {row['surface']}
  """

  row["tweet"] = "\n".join(line.strip() for line in row["tweet"].strip().splitlines())

  return row

# to debug with breakpoint(), use apply instead of parallel_apply
final = full_games.dropna().parallel_apply(get_player_data, axis=1)

print(final)
print(final.iloc[0]['tweet'])
