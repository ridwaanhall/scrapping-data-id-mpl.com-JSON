import requests
from bs4 import BeautifulSoup

def fetch_standings(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the tab content containing the table
    tab_content = soup.find('div', id='standing-regular-season')

    if not tab_content:
        return {'error': 'No tab content found'}

    # Find the table within the tab content
    table = tab_content.find('table', {'class': 'table table-sm table-standings'})

    if not table:
        return {'error': 'No data table found'}

    standings = []
    team_rows = table.select('tbody tr')

    for row in team_rows:
        team_info = row.select_one('.team-info')
        columns = row.find_all('td')

        team_name_element = team_info.select_one('.team-name')
        # print(team_name_element)
        
        team_name = columns[0].find('div', class_='team-name').text.strip()
        
        team_rank = team_info.select_one('.team-rank')
        if team_rank:
            team_rank = team_rank.get_text(strip=True)
        else:
            team_rank = ''

        team_logo = team_info.select_one('.team-logo img')
        if team_logo:
            team_logo = team_logo['src']
        else:
            team_logo = ''

        match_point = row.select_one('td:nth-of-type(2)').get_text(strip=True)
        match_record = row.select_one('td:nth-of-type(3)').get_text(strip=True).replace('\n                                                -\n                                                ', ' - ')
        net_game_win = row.select_one('td:nth-of-type(4)').get_text(strip=True)
        game_record = row.select_one('td:nth-of-type(5)').get_text(strip=True).replace('\n                                                -\n                                                ', ' - ')
        # print("game record", game_record)
        game_win, game_lose = map(int, game_record.split(' - '))
        
        game_rate = game_win / (game_win + game_lose)

        standings = {
            'team_name': team_name.replace('\n                                                    \n\n                                                        ', ' - '),
            'team_rank': int(team_rank),
            'team_logo': team_logo,
            'match_point': int(match_point),
            'match_record': match_record,
            'net_game_win': int(net_game_win),
            'game_record': game_record,
            'game_rate': game_rate
        }
        standings.append(standings)

    return standings


def fetch_trending_videos(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container holding the trending videos
    trending_section = soup.find('div', class_='shorts-slider')
    if not trending_section:
        return {'error': 'No trending section found'}

    trending = []
    for item in trending_section.find_all('div', class_='shorts-item'):
        onclick_attr = item.find('a')['onclick']
        video_link = onclick_attr.split("'")[1]
        thumbnail_url = item.find('img')['src']
        
        trending.append({
            'video_link': video_link,
            'thumbnail_url': thumbnail_url
        })

    return trending


def fetch_highlight_news(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container holding the highlight news
    highlight_news_section = soup.find('div', class_='highlight-news')
    if not highlight_news_section:
        return {'error': 'No highlight news section found'}

    highlight_news = []
    for link in highlight_news_section.find_all('a', href=True):
        url = link['href']
        image_style = link.find('div', class_='image-outer')['style']
        background_image_url = image_style.split("url('")[1].split("')")[0]
        date = link.find('div', class_='news-date').text.strip()
        title = link.find('div', class_='news-title').text.strip()

        highlight_news.append({
            'url': url,
            'image_url': background_image_url,
            'date': date,
            'title': title
        })

    return highlight_news


def fetch_sub_news(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}

    soup = BeautifulSoup(response.text, 'html.parser')

    sub_news_section = soup.find('div', class_='sub-news')
    if not sub_news_section:
        return {'error': 'No sub-news section found'}

    sub_news = []
    for link in sub_news_section.find_all('a', href=True):
        url = link['href']
        left_style = link.find('div', class_='left')['style']
        left_image_url = left_style.split("url('")[1].split("')")[0]
        date = link.find('div', class_='news-date').text.strip()
        title = link.find('div', class_='news-title').text.strip()

        sub_news.append({
            'url': url,
            'image_url': left_image_url,
            'date': date,
            'title': title
        })

    return sub_news


def fetch_game_highlights(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}

    soup = BeautifulSoup(response.text, 'html.parser')

    video_playlist_section = soup.find('div', id='video-playlist')
    if not video_playlist_section:
        return {'error': 'No video playlist section found'}

    highlights = []
    for link in video_playlist_section.find_all('a', class_='video-item', href=True):
        onclick_attr = link['onclick']
        video_url = onclick_attr.split("'")[1]
        thumbnail_url = link.find('div', class_='thumbnail').find('img')['src']
        title = link.find('div', class_='text').text.strip()
        
        highlights.append({
            'video_url': video_url,
            'thumbnail_url': thumbnail_url,
            'title': title
        })

    return highlights


def fetch_teams(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}

    soup = BeautifulSoup(response.text, 'html.parser')

    team_section = soup.find('div', class_='d-flex flex-column justify-content-center align-items-center flex-lg-row mt-xl-4')
    if not team_section:
        return {'error': 'No team section found'}

    teams = []
    for team_card_outer in team_section.find_all('div', class_='team-card-outer'):
        link = team_card_outer.find('a', href=True)
        team_url = link['href']
        team_name = link.find('div', class_='team-name').text.strip()
        team_image_url = link.find('img')['src']

        teams.append({
            'team_url': team_url,
            'team_name': team_name,
            'team_image_url': team_image_url
        })

    return teams


def fetch_team_ae(url: str):
    # response = requests.get(url)
    # if response.status_code != 200:
    #     return {'error': 'Failed to fetch data'}

    # soup = BeautifulSoup(response.text, 'html.parser')

    # team_data = {}

    # # Find team name and social media links
    # team_info = soup.find('div', class_='col-lg-8 offset-lg-2')
    # if team_info:
    #     team_name = team_info.find('h4').text.strip()
    #     team_data['team_name'] = team_name

    #     social_media_links = team_info.find('div', class_='icon-socmed')
    #     if social_media_links:
    #         social_media = {}
    #         for link in social_media_links.find_all('a'):
    #             platform = link['href'].split('/')[-1]
    #             social_media[platform] = link['href']
    #         team_data['social_media'] = social_media

    # # Find player and coach information
    # roster_section = soup.find('div', {'data-ga-impression': 'Section Roster Team Detail'})
    # if roster_section:
    #     roster_data = []
    #     for player_info in roster_section.find_all('div', class_='col-md-3 col-6'):
    #         player_name = player_info.find('div', class_='player-name').text.strip()
    #         player_role = player_info.find('div', class_='player-role').text.strip()
    #         roster_data.append({'player_name': player_name, 'player_role': player_role})
    #     team_data['roster'] = roster_data

    # # Find match details
    # match_section = soup.find('div', {'data-ga-impression': 'Section Match Team Detail'})
    # if match_section:
    #     match_data = []
    #     for match_info in match_section.find_all('div', class_='match-team'):
    #         match_detail = {}
    #         match_detail['opponent'] = match_info.find_all('div', class_='match-logo')[-1].text.strip()
    #         match_detail['score'] = match_info.find('div', class_='score').text.strip()
    #         # match_detail['date'] = match_info.find('div', style='font-weight: 400;').text.strip()
    #         match_detail['result'] = match_info.find('div', class_='match-status-wl').text.strip()
    #         match_data.append(match_detail)
    #     team_data['matches'] = match_data

    # return team_data
    
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract team information
    team_name = soup.find("h4", class_="d-flex").text.strip()
    team_logo_url = soup.find("img", class_="team-logo")["src"]

    # Extract social media links
    social_media_links = {}
    social_media_div = soup.find("div", class_="icon-socmed")
    for link in social_media_div.find_all("a"):
        social_media_links[link["href"]] = link.find("i")["class"][0].split("-")[-1]

    # Extract roster for Season 13
    roster = []
    roster_div = soup.find("div", {"data-ga-impression": "Section Roster Team Detail"})
    for player_div in roster_div.find_all("div", class_="col-md-3"):
        player_name = player_div.find("div", class_="player-name").text.strip()
        player_role = player_div.find("div", class_="player-role").text.strip()
        player_image_url = player_div.find("img")["src"]
        roster.append({"name": player_name, "role": player_role, "image_url": player_image_url})

    # Extract match details for Season 13
    matches = []
    matches_div = soup.find("div", {"data-ga-impression": "Section Match Team Detail"})
    for match_div in matches_div.find_all("div", class_="match-team"):
        teams = match_div.find_all("div", class_="match-logo")
        team1 = teams[0].text.strip()
        team2 = teams[1].text.strip()
        score = match_div.find("div", class_="score").text.strip()
        status = match_div.find("div", class_="match-status-wl").text.strip()
        date_info = match_div.find_all("div", class_="col-12")
        # week = date_info[0].text.strip()
        # date = date_info[1].text.strip()
        matches.append({"team1": team1, "team2": team2, "score": score, "status": status, 
                        })

    # Return the extracted data
    return {
        "team_name": team_name,
        "team_logo_url": team_logo_url,
        "social_media_links": social_media_links,
        "roster": roster,
        "matches": matches
    }