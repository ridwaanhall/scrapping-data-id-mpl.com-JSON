import requests
from bs4 import BeautifulSoup
from typing import List, Dict


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

        # standings = {
        #     'team_name': team_name.replace('\n                                                    \n\n                                                        ', ' - '),
        #     'team_rank': int(team_rank),
        #     'team_logo': team_logo,
        #     'match_point': int(match_point),
        #     'match_record': match_record,
        #     'net_game_win': int(net_game_win),
        #     'game_record': game_record,
        #     'game_rate': game_rate
        # }
        # standings.append(standings)
        
        standings.append({
            'team_name': team_name.replace('\n                                                    \n\n                                                        ', ' - '),
            'team_rank': int(team_rank),
            'team_logo': team_logo,
            'match_point': int(match_point),
            'match_record': match_record,
            'net_game_win': int(net_game_win),
            'game_record': game_record,
            'game_rate': game_rate
            })

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


def fetch_team_data(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    # Extract team name and logo
    try:
        team_info = soup.find('h4', class_='d-flex flex-row justify-content-center align-items-center')
        if not team_info:
            raise ValueError("Team info not found")
        team_name = team_info.text.strip()
        team_logo_tag = team_info.find('img')
        team_logo = team_logo_tag['src'] if team_logo_tag else None
        data['team_name'] = team_name
        data['team_logo'] = team_logo
    except (AttributeError, ValueError) as e:
        data['team_info_error'] = str(e)

    # Extract social media links
    social_media_links = {}
    try:
        socmed_div = soup.find('div', class_='icon-socmed')
        if socmed_div:
            for link in socmed_div.find_all('a'):
                icon_class = link.find('i')['class'][0]
                if 'facebook' in icon_class:
                    social_media_links['facebook'] = link['href']
                elif 'instagram' in icon_class:
                    social_media_links['instagram'] = link['href']
                elif 'youtube' in icon_class:
                    social_media_links['youtube'] = link['href']
        data['social_media_links'] = social_media_links
    except AttributeError as e:
        data['social_media_error'] = str(e)

    # Extract roster data
    players = []
    try:
        roster_section = soup.find('div', {'data-ga-impression': 'Section Roster Team Detail'})
        if not roster_section:
            raise ValueError("Roster section not found")
        roster_title = roster_section.find('h5', class_='text-center').text.strip()
        player_divs = roster_section.find_all('div', class_='col-md-3 col-6')
        for player_div in player_divs:
            player_image_tag = player_div.find('img')
            player_image = player_image_tag['src'] if player_image_tag else None
            player_name = player_div.find('div', class_='player-name').text.strip()
            player_role = player_div.find('div', class_='player-role').text.strip()
            players.append({
                'name': player_name,
                'role': player_role,
                'image': player_image
            })
        data['roster'] = {
            'title': roster_title,
            'players': players
        }
    except (AttributeError, ValueError) as e:
        data['roster_error'] = str(e)

    # Extract match data
    matches = []
    try:
        match_section = soup.find('div', {'data-ga-impression': 'Section Match Team Detail'})
        if not match_section:
            raise ValueError("Match section not found")
        match_title = match_section.find('h5', class_='text-center').text.strip()
        match_divs = match_section.find_all('div', class_='match-team')
        for match_div in match_divs:
            teams = match_div.find_all('div', class_='match-logo')
            if len(teams) < 2:
                continue  # Ensure there are two teams in the match
            team1_logo_tag = teams[0].find('img')
            team1_logo = team1_logo_tag['src'] if team1_logo_tag else None
            team1 = {
                'name': teams[0].text.strip(),
                'logo': team1_logo
            }
            team2_logo_tag = teams[1].find('img')
            team2_logo = team2_logo_tag['src'] if team2_logo_tag else None
            team2 = {
                'name': teams[1].text.strip(),
                'logo': team2_logo
            }
            score = match_div.find('div', class_='score').text.strip()
            week_date = match_div.find('div', class_='col-9').text.strip().replace('\n                                                                                    \n\n                                            ', ' | ')
            
            # Split week_date into week and date
            if ' | ' in week_date:
                week, date = week_date.split(' | ')
            else:
                week = week_date
                date = None
            
            status = match_div.find('div', class_='match-status-wl').text.strip()
            matches.append({
                'team1': team1,
                'team2': team2,
                'score': score,
                # 'week_date': week_date,
                'week': week,
                'date': date,
                'status': status
            })
        data['matches'] = {
            'title': match_title,
            'matches': matches
        }
    except (AttributeError, ValueError) as e:
        data['matches_error'] = str(e)

    return data


def fetch_transfer_data(url: str) -> List[Dict[str, any]]:
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    soup = BeautifulSoup(response.text, 'html.parser')

    transfer_cards = soup.find_all('div', class_='transfer-card')

    transfer_data = []

    for card in transfer_cards:
        date = card.find('div', class_='text-center').text.strip()
        player_name_div = card.find('div', class_='col-lg-4')
        player_name_text = player_name_div.text.strip() if player_name_div else ''
        
        # Splitting player_name_text into name and role
        split_player_name = player_name_text.split('\n', 1)
        if len(split_player_name) == 2:
            player_name, player_role = map(str.strip, split_player_name)
        else:
            player_name = split_player_name[0].strip()
            player_role = ''
            
        # role_div = card.find('div', style={'font-size': '0.8rem'})
        # role = role_div.text.strip() if role_div else ''

        row = card.find('div', class_='row')
        from_team_div = row.find('div', class_='col-lg-5')
        from_team_logo = from_team_div.find('img')
        if from_team_logo:
            from_team_logo = from_team_logo['src']
        else:
            from_team_logo = ''
        from_team_name = from_team_div.find('div', class_='team-name').text.strip().replace('\n                                                                                                                                                            ', ' ')

        to_team_div = row.find_all('div', class_='col-lg-5')[1]
        to_team_logo = to_team_div.find('img')
        if to_team_logo:
            to_team_logo = to_team_logo['src']
        else:
            to_team_logo = ''
        to_team_name = to_team_div.find('div', class_='team-name').text.strip().replace('\n                                                                                                                                                            ', ' ')

        transfer_data.append({
            'date': date,
            'player_name': player_name,
            'player_role': player_role,
            'from_team': {
                'logo': from_team_logo,
                'name': from_team_name
            },
            'to_team': {
                'logo': to_team_logo,
                'name': to_team_name
            }
        })

    return transfer_data


def fetch_overview_data(url: str) -> List[Dict[str, any]]:
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    soup = BeautifulSoup(response.text, 'html.parser')
    overview_content = soup.find('div', class_='overview-content')
    if not overview_content:
        return {"error": "No overview content found"}

    left_images = overview_content.find('div', class_='left').find_all('img')
    right_images = overview_content.find('div', class_='right').find_all('img')

    left_images_data = []
    for img in left_images:
        if 'src' in img.attrs and img.attrs['class'][0] == 'd-none':
            left_images_data.append({
                'src': img['src'],
                'alt': img.get('alt', ''),
                'id': img.get('id', '')
            })

    right_images_data = []
    for img in right_images:
        if 'src' in img.attrs and img.attrs['class'][0] == 'd-none':
            right_images_data.append({
                'src': img['src'],
                'alt': img.get('alt', ''),
                'id': img.get('id', '')
            })

    overview_data = {
        'left_images': left_images_data,
        'right_images': right_images_data
    }

    return overview_data




