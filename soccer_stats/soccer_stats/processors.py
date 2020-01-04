

def process_league_title(values: list) -> str:
    return ''.join(values).strip().lower()


def strip_string(values: list) -> str:
    return values.pop().strip().lower()


def convert_to_integer(values: list) -> int:
    return int(values.pop())


def process_season_start(values: list) -> int:
    season = values.pop().strip()
    if '/' not in season:
        return int(season)
    return int(season.split('/')[0])


def process_season_end(values: list) -> int:
    season = valuse.pop().strip()
    if '/' not in season:
        return int(season)
    return int(season.split('/')[1])


def process_all_matches(values: list) -> int:
    matches = values.pop().strip().split('/')
    if len(matches) == 2:
        return int(matches.pop())


def process_timestamp(values: list) -> int:
    return int(values.pop().strip())


def process_home_result(values: list) -> int:
    return int(values[0].strip())


def process_away_result(values: list) -> int:
    return int(values.pop().strip())


def process_post_match_data_home(values: list) -> int:
    return int(values[0].strip())


def process_post_match_data_awat(values: list) -> int:
    return int(values[1].strip())