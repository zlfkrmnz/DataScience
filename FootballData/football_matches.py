import requests
import pandas as pd
import json

class FootballData:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}

    def fetch_matches(self, league_code):
        url = f"{self.base_url}/competitions/{league_code}/matches"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def process_matches(self, matches_data):
        matches = matches_data.get('matches', [])
        processed_data = []
        for match in matches:
            match_info = {
                'Match ID': match.get('id'),
                'Season': match.get('season', {}).get('startDate'),
                'Matchday': match.get('matchday'),
                'Home Team': match.get('homeTeam', {}).get('name'),
                'Away Team': match.get('awayTeam', {}).get('name'),
                'Home Score': match.get('score', {}).get('fullTime', {}).get('home'),
                'Away Score': match.get('score', {}).get('fullTime', {}).get('away'),
                'Status': match.get('status'),
                'Date': match.get('utcDate')
            }
            processed_data.append(match_info)
        return processed_data

    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    API_KEY = '4bb655ea5f314b1a90d22e18963d4d4b'  # Buraya kendi API anahtarınızı girin
    LEAGUE_CODE = 'PL'  # Premier League için örnek kod; diğer ligler için kodları kontrol edin

    football_data = FootballData(API_KEY)
    matches_data = football_data.fetch_matches(LEAGUE_CODE)
    if matches_data:
        processed_data = football_data.process_matches(matches_data)
        football_data.save_to_csv(processed_data, 'matches.csv')
