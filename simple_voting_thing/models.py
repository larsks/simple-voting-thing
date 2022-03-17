# type: ignore

import datetime
from pony import orm

db = orm.Database()


class Session(db.Entity):
    session_id = orm.PrimaryKey(int, auto=True)
    session_created = orm.Required(datetime.datetime, default=datetime.datetime.now)
    vote = orm.Optional("Vote")


class Vote(db.Entity):
    vote_id = orm.PrimaryKey(int, auto=True)
    session_id = orm.Required(Session)
    vote_choice = orm.Required(str)


def initdb(path=None):
    if path is None:
        path = "votes.db"

    db.bind(provider="sqlite", filename=path, create_db=True)
    db.generate_mapping(create_tables=True)
