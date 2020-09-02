import DBcm


config = {
    'host': 'localhost',
    'user': 'gameUser',
    'password': 'gamePassword',
    'database': 'gameDB',
}


def add_scores(name: str, score: float, sourceword: str) -> None:
    _SQL = """Insert into leaderboard
                (name, score, sourceword)
                values
                (%s, %s, %s)"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_SQL, (name, score, sourceword))


def retrieve_sorted_leaderboard() -> list:
    _SQL = """Select score, name, sourceword From leaderboard
                order By score"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_SQL)
        data = cursor.fetchall()
        return [(float(row[0]), row[1], row[2]) for row in data]
