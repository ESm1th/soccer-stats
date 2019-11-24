

def process_league_title(values: list) -> str:
    return ''.join(values).strip().lower()


def strip_string(values: list) -> str:
    return values.pop().strip().lower()


def convert_to_integer(values: list) -> int:
    return int(values.pop())


def process_season(values: list) -> int:
    seasons = values.pop().strip().split('/')
    return int(seasons[0])


def process_end_season(values: list) -> int:
    seasons = values.pop().strip().split('/')
    if len(seasons) == 2:
        return int(seasons.pop())


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


def process_post_match_data(values: list) -> list:
    return [int(value.strip()) for value in values]