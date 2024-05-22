from bs4 import BeautifulSoup
import requests

# Fetch the HTML content
url = "https://id-mpl.com/team/ae"
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
    matches.append({
        "team1": team1, 
        "team2": team2,
        "score": score,
        "status": status,
        # "week": week,
        # "date": date
        })

# Print the extracted data
print("Team Information:")
print("Name:", team_name)
print("Logo URL:", team_logo_url)
print("Social Media Links:", social_media_links)

print("\nRoster for Season 13:")
for player in roster:
    print(player)

print("\nMatch Details for Season 13:")
for match in matches:
    print(match)
