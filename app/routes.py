from flask import Blueprint, jsonify
from .scraper import fetch_standings, fetch_trending_videos, fetch_highlight_news, fetch_sub_news, fetch_game_highlights, fetch_teams, fetch_team_ae

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/standings', methods=['GET'])
def standings():
    url = 'https://id-mpl.com/'
    data = fetch_standings(url)
    return jsonify(data), 200

@bp.route('/trending', methods=['GET'])
def trending():
    url = 'https://id-mpl.com/'
    data = fetch_trending_videos(url)
    return jsonify(data), 200

@bp.route('/highlight-news', methods=['GET'])
def highlight_news():
    url = 'https://id-mpl.com/'
    data = fetch_highlight_news(url)
    return jsonify(data), 200

@bp.route('/sub-news', methods=['GET'])
def sub_news():
    url = 'https://id-mpl.com/'
    data = fetch_sub_news(url)
    return jsonify(data), 200

@bp.route('/game-highlights', methods=['GET'])
def game_highlights():
    url = 'https://id-mpl.com/'
    data = fetch_game_highlights(url)
    return jsonify(data), 200

@bp.route('/teams', methods=['GET'])
def teams():
    url = 'https://id-mpl.com/teams'
    data = fetch_teams(url)
    return jsonify(data), 200

@bp.route('/team/ae', methods=['GET'])
def team_ae():
    url = 'https://id-mpl.com/team/ae'
    data = fetch_team_ae(url)
    return jsonify(data), 200