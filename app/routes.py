from flask import Blueprint, jsonify
from .scraper import (
    fetch_standings, fetch_trending_videos, fetch_highlight_news, 
    fetch_sub_news, fetch_game_highlights, fetch_teams, fetch_team_data
)

bp = Blueprint('api', __name__, url_prefix='/api')

def fetch_and_respond(fetch_function, url):
    """Fetch data from the provided URL using the specified function and return a JSON response."""
    data = fetch_function(url)
    return jsonify(data), 200

@bp.route('/standings', methods=['GET'])
def standings():
    """
    Fetch and return MPL standings.
    """
    url = 'https://id-mpl.com/'
    return fetch_and_respond(fetch_standings, url)

@bp.route('/trending', methods=['GET'])
def trending():
    """
    Fetch and return trending videos.
    """
    url = 'https://id-mpl.com/'
    return fetch_and_respond(fetch_trending_videos, url)

@bp.route('/highlight-news', methods=['GET'])
def highlight_news():
    """
    Fetch and return highlight news.
    """
    url = 'https://id-mpl.com/'
    return fetch_and_respond(fetch_highlight_news, url)

@bp.route('/sub-news', methods=['GET'])
def sub_news():
    """
    Fetch and return sub-news.
    """
    url = 'https://id-mpl.com/'
    return fetch_and_respond(fetch_sub_news, url)

@bp.route('/game-highlights', methods=['GET'])
def game_highlights():
    """
    Fetch and return game highlights.
    """
    url = 'https://id-mpl.com/'
    return fetch_and_respond(fetch_game_highlights, url)

@bp.route('/teams', methods=['GET'])
def teams():
    """
    Fetch and return a list of teams.
    """
    url = 'https://id-mpl.com/teams'
    return fetch_and_respond(fetch_teams, url)

@bp.route('/team/<team_id>', methods=['GET'])
def team(team_id):
    """
    Fetch and return data for a specific team based on team_id.
    """
    base_url = 'https://id-mpl.com/team/'
    url = f"{base_url}{team_id}"
    return fetch_and_respond(fetch_team_data, url)
