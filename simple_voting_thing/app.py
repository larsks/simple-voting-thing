# type: ignore
import os
import flask

from pony import orm

from . import config
from . import models

app = flask.Flask(__name__)
app.secret_key = os.environ["SV_SECRET_KEY"]
models.initdb(path=os.environ["SV_DATABASE"])


def get_session():
    session = None
    session_id = flask.session.get("session_id")

    if session_id:
        session = models.Session.get(session_id=session_id)

    if not session:
        session = models.Session()
        models.db.commit()
        flask.session["session_id"] = session.session_id

    return session


@app.route("/")
@orm.db_session
def index():
    session = get_session()
    vote = models.Vote.get(session_id=session.session_id)

    return flask.render_template(
        "questions.html",
        session=session,
        vote=vote,
        page_title="Questions",
        question=config.QUESTION,
        choices=config.CHOICES,
    )


@app.route("/vote")
@orm.db_session
def vote():
    choice = flask.request.args["choice"]

    session = get_session()
    vote = models.Vote.get(session_id=session.session_id)
    if not vote:
        vote = models.Vote(session_id=session, vote_choice=choice)
    else:
        vote.vote_choice = choice

    return flask.render_template(
        "vote.html",
        session=session,
        vote=vote,
        page_title="models.Vote",
        question=config.QUESTION,
        choices=config.CHOICES,
    )


@app.route("/results")
@orm.db_session
def results():
    session = get_session()
    vote = models.Vote.get(session_id=session.session_id)
    votes = orm.select((v.vote_choice, orm.count(v)) for v in models.Vote)
    votes_total = sum(vote[1] for vote in votes)

    return flask.render_template(
        "results.html",
        session=session,
        vote=vote,
        votes=votes,
        votes_total=votes_total,
        page_title="Results",
        question=config.QUESTION,
        choices=config.CHOICES,
    )
