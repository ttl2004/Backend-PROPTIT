import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import time
import csv
# Thiết lập mã hóa UTF-8 cho đầu ra
sys.stdout.reconfigure(encoding='utf-8')

def read_html_file(html_content):
    # Đọc file HTML
    with open("F:/Python BTL/MC.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    return html_content


def read_csv(team_data):
    # Mở file CSV để đọc
    with open('F:/Python BTL/Team.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Bỏ qua dòng tiêu đề
        next(reader)
        
        # Đọc từng dòng và thêm vào danh sách
        for row in reader:
            team_name = row[0]
            team_url = row[1]
            team_data.append((team_name, team_url))
    
    return team_data


def Xu_ly_du_lieu_cau_thu(tmp_tr, team_name, player_data_tmp, mp):
    # Lấy thông tin cầu thủ
    player_name = tmp_tr.find('th', {'data-stat': 'player'}).get_text(strip=True)
    player_national = tmp_tr.find('td', {'data-stat': 'nationality'}).find('a')['href'].split('/')[-1].replace('-Football', ' ') if tmp_tr.find('td', {'data-stat': 'nationality'}).find('a') else "N/a"
    player_position = tmp_tr.find('td', {'data-stat': 'position'}).get_text(strip=True)
    player_age = tmp_tr.find('td', {'data-stat': 'age'}).get_text(strip=True)
    #Playing time
    player_games = tmp_tr.find('td', {'data-stat': 'games'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'games'}).get_text(strip=True) else "N/a"
    player_games_starts = tmp_tr.find('td', {'data-stat': 'games_starts'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'games_starts'}).get_text(strip=True) else "N/a"
    player_minutes = tmp_tr.find('td', {'data-stat': 'minutes'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'minutes'}).get_text(strip=True) else "N/a"

    # Performance
    player_goals_pens = tmp_tr.find('td', {'data-stat': 'goals_pens'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'goals_pens'}).get_text(strip=True) else "N/a"
    player_pens_made = tmp_tr.find('td', {'data-stat': 'pens_made'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'pens_made'}).get_text(strip=True) else "N/a"
    player_assists = tmp_tr.find('td', {'data-stat': 'assists'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'assists'}).get_text(strip=True) else "N/a"
    player_cards_yellow = tmp_tr.find('td', {'data-stat': 'cards_yellow'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'cards_yellow'}).get_text(strip=True) else "N/a"
    player_cards_red = tmp_tr.find('td', {'data-stat': 'cards_red'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'cards_red'}).get_text(strip=True) else "N/a"

    # Expected 
    player_xg = tmp_tr.find('td', {'data-stat': 'xg'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'xg'}).get_text(strip=True) else "N/a"
    player_npxg = tmp_tr.find('td', {'data-stat': 'npxg'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'npxg'}).get_text(strip=True) else "N/a"
    player_xg_assist = tmp_tr.find('td', {'data-stat': 'xg_assist'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'xg_assist'}).get_text(strip=True) else "N/a"

    # Progression
    player_progressive_carries = tmp_tr.find('td', {'data-stat': 'progressive_carries'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'progressive_carries'}).get_text(strip=True) else "N/a"
    player_progressive_passes = tmp_tr.find('td', {'data-stat': 'progressive_passes'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'progressive_passes'}).get_text(strip=True) else "N/a"
    player_progressive_passes_received = tmp_tr.find('td', {'data-stat': 'progressive_passes_received'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'progressive_passes_received'}).get_text(strip=True) else "N/a"

    # Per 90 minutes
    player_goals_per90 = tmp_tr.find('td', {'data-stat': 'goals_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'goals_per90'}).get_text(strip=True) else "N/a"
    player_assists_per90 = tmp_tr.find('td', {'data-stat': 'assists_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'assists_per90'}).get_text(strip=True) else "N/a"
    player_goals_assists_per90 = tmp_tr.find('td', {'data-stat': 'goals_assists_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'goals_assists_per90'}).get_text(strip=True) else "N/a"
    player_goals_pens_per90 = tmp_tr.find('td', {'data-stat': 'goals_pens_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'goals_pens_per90'}).get_text(strip=True) else "N/a"
    player_goals_assists_pens_per90 = tmp_tr.find('td', {'data-stat': 'goals_assists_pens_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'goals_assists_pens_per90'}).get_text(strip=True) else "N/a"
    player_xg_per90 = tmp_tr.find('td', {'data-stat': 'xg_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'xg_per90'}).get_text(strip=True) else "N/a"
    player_xg_assist_per90 = tmp_tr.find('td', {'data-stat': 'xg_assist_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'xg_assist_per90'}).get_text(strip=True) else "N/a"
    player_xg_xg_assist_per90 = tmp_tr.find('td', {'data-stat': 'xg_xg_assist_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'xg_xg_assist_per90'}).get_text(strip=True) else "N/a"
    player_npxg_per90 = tmp_tr.find('td', {'data-stat': 'npxg_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'npxg_per90'}).get_text(strip=True) else "N/a"
    player_npxg_xg_assist_per90 = tmp_tr.find('td', {'data-stat': 'npxg_xg_assist_per90'}).get_text(strip=True) if tmp_tr.find('td', {'data-stat': 'npxg_xg_assist_per90'}).get_text(strip=True) else "N/a"

    # Thêm thông tin cầu thủ vào danh sách
    tmp = [
        player_name, player_national, team_name, player_position, player_age, player_games, player_games_starts, player_minutes, 
        player_goals_pens, player_pens_made, player_assists, player_cards_yellow, player_cards_red, player_xg, 
        player_npxg, player_xg_assist, player_progressive_carries, player_progressive_passes, 
        player_progressive_passes_received, player_goals_per90, player_assists_per90, player_goals_assists_per90, 
        player_goals_pens_per90, player_goals_assists_pens_per90, player_xg_per90, player_xg_assist_per90, player_xg_xg_assist_per90,
        player_npxg_per90, player_npxg_xg_assist_per90
    ]
    player_data_tmp.append(tmp)
    mp[player_name] = player_data_tmp[-1]

    return player_data_tmp

def Xu_ly_du_lieu_thu_mon(player):
    player_GA = player.find('td', {'data-stat': 'gk_goals_against'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_goals_against'}).get_text(strip=True) else "N/a"
    player_GA90 = player.find('td', {'data-stat': 'gk_goals_against_per90'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_goals_against_per90'}).get_text(strip=True) else "N/a"
    player_SoTA = player.find('td', {'data-stat': 'gk_shots_on_target_against'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_shots_on_target_against'}).get_text(strip=True) else "N/a"
    player_Saves = player.find('td', {'data-stat': 'gk_saves'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_saves'}).get_text(strip=True) else "N/a"
    player_SaveP = player.find('td', {'data-stat': 'gk_save_pct'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_save_pct'}).get_text(strip=True) else "N/a"
    player_W = player.find('td', {'data-stat': 'gk_wins'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_wins'}).get_text(strip=True) else "N/a"
    player_D = player.find('td', {'data-stat': 'gk_ties'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_ties'}).get_text(strip=True) else "N/a"
    player_L = player.find('td', {'data-stat': 'gk_losses'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_losses'}).get_text(strip=True) else "N/a"
    player_CS = player.find('td', {'data-stat': 'gk_clean_sheets'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_clean_sheets'}).get_text(strip=True) else "N/a"
    player_CSP = player.find('td', {'data-stat': 'gk_clean_sheets_pct'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_clean_sheets_pct'}).get_text(strip=True) else "N/a"
    player_PKatt = player.find('td', {'data-stat': 'gk_pens_att'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_pens_att'}).get_text(strip=True) else "N/a"
    player_PKA = player.find('td', {'data-stat': 'gk_pens_allowed'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_pens_allowed'}).get_text(strip=True) else "N/a"
    player_PKsv = player.find('td', {'data-stat': 'gk_pens_saved'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_pens_saved'}).get_text(strip=True) else "N/a"
    player_PKm = player.find('td', {'data-stat': 'gk_pens_missed'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_pens_missed'}).get_text(strip=True) else "N/a"
    player_SaveP = player.find('td', {'data-stat': 'gk_pens_save_pct'}).get_text(strip=True) if player.find('td', {'data-stat': 'gk_pens_save_pct'}).get_text(strip=True) else "N/a"
    
    # Trả về list chỉ số thủ môn
    return [player_GA, player_GA90, player_SoTA, player_Saves, player_SaveP, player_W, player_D, player_L, player_CS, player_CSP, player_PKatt, player_PKA, player_PKsv, player_PKm, player_SaveP]

def Xu_ly_du_lieu_shooting(player):
    player_Gls = player.find('td', {'data-stat': 'goals'}).get_text(strip=True) if player.find('td', {'data-stat': 'goals'}).get_text(strip=True) else "N/a"
    player_Sh = player.find('td', {'data-stat': 'shots'}).get_text(strip=True) if player.find('td', {'data-stat': 'shots'}).get_text(strip=True) else "N/a"
    player_SoT = player.find('td', {'data-stat': 'shots_on_target'}).get_text(strip=True) if player.find('td', {'data-stat': 'shots_on_target'}).get_text(strip=True) else "N/a"
    player_SoTP = player.find('td', {'data-stat': 'shots_on_target_pct'}).get_text(strip=True) if player.find('td', {'data-stat': 'shots_on_target_pct'}).get_text(strip=True) else "N/a"
    player_Sh90 = player.find('td', {'data-stat': 'shots_per90'}).get_text(strip=True) if player.find('td', {'data-stat': 'shots_per90'}).get_text(strip=True) else "N/a"
    player_Sot90 = player.find('td', {'data-stat': 'shots_on_target_per90'}).get_text(strip=True) if player.find('td', {'data-stat': 'shots_on_target_per90'}).get_text(strip=True) else "N/a"
    player_GSh = player.find('td', {'data-stat': 'goals_per_shot'}).get_text(strip=True) if player.find('td', {'data-stat': 'goals_per_shot'}).get_text(strip=True) else "N/a"
    player_GSoT = player.find('td', {'data-stat': 'goals_per_shot_on_target'}).get_text(strip=True) if player.find('td', {'data-stat': 'goals_per_shot_on_target'}).get_text(strip=True) else "N/a"
    player_Dist = player.find('td', {'data-stat': 'average_shot_distance'}).get_text(strip=True) if player.find('td', {'data-stat': 'average_shot_distance'}).get_text(strip=True) else "N/a"
    player_FK = player.find('td', {'data-stat': 'shots_free_kicks'}).get_text(strip=True) if player.find('td', {'data-stat': 'shots_free_kicks'}).get_text(strip=True) else "N/a"
    player_PK = player.find('td', {'data-stat': 'pens_made'}).get_text(strip=True) if player.find('td', {'data-stat': 'pens_made'}).get_text(strip=True) else "N/a"
    player_PKatt = player.find('td', {'data-stat': 'pens_att'}).get_text(strip=True) if player.find('td', {'data-stat': 'pens_att'}).get_text(strip=True) else "N/a"
    player_xG = player.find('td', {'data-stat': 'xg'}).get_text(strip=True) if player.find('td', {'data-stat': 'xg'}).get_text(strip=True) else "N/a"
    player_npxG = player.find('td', {'data-stat': 'npxg'}).get_text(strip=True) if player.find('td', {'data-stat': 'npxg'}).get_text(strip=True) else "N/a"
    player_npxGSh = player.find('td', {'data-stat': 'npxg_per_shot'}).get_text(strip=True) if player.find('td', {'data-stat': 'npxg_per_shot'}).get_text(strip=True) else "N/a"
    player_GxG = player.find('td', {'data-stat': 'xg_net'}).get_text(strip=True) if player.find('td', {'data-stat': 'xg_net'}).get_text(strip=True) else "N/a"
    player_npGxG = player.find('td', {'data-stat': 'npxg_net'}).get_text(strip=True) if player.find('td', {'data-stat': 'npxg_net'}).get_text(strip=True) else "N/a"

    # Trả về list chỉ số shooting
    return [player_Gls, player_Sh, player_SoT, player_SoTP, player_Sh90, player_Sot90, player_GSh, player_GSoT, player_Dist, player_FK, player_PK, player_PKatt, player_xG, player_npxG, player_npxGSh, player_GxG, player_npGxG]

def Xu_ly_du_lieu_passing(player):
    player_Cmp = player.find('td', {'data-stat': 'passes_completed'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_completed'}).get_text(strip=True) else "N/a"
    player_Att = player.find('td', {'data-stat': 'passes'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes'}).get_text(strip=True) else "N/a"
    player_CmpP = player.find('td', {'data-stat': 'passes_pct'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_pct'}).get_text(strip=True) else "N/a"
    player_TotDist = player.find('td', {'data-stat': 'passes_total_distance'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_total_distance'}).get_text(strip=True) else "N/a"
    player_PrgDist = player.find('td', {'data-stat': 'passes_progressive_distance'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_progressive_distance'}).get_text(strip=True) else "N/a"
    player_Short_Cmp = player.find('td', {'data-stat': 'passes_completed_short'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_completed_short'}).get_text(strip=True) else "N/a"
    player_Short_Att = player.find('td', {'data-stat': 'passes_short'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_short'}).get_text(strip=True) else "N/a"
    plaer_Short_CmpP = player.find('td', {'data-stat': 'passes_pct_short'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_pct_short'}).get_text(strip=True) else "N/a"
    player_Medium_Cmp = player.find('td', {'data-stat': 'passes_completed_medium'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_completed_medium'}).get_text(strip=True) else "N/a"
    player_Medium_Att = player.find('td', {'data-stat': 'passes_medium'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_medium'}).get_text(strip=True) else "N/a"
    player_Medium_CmpP = player.find('td', {'data-stat': 'passes_pct_medium'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_pct_medium'}).get_text(strip=True) else "N/a"
    player_Long_Cmp = player.find('td', {'data-stat': 'passes_completed_long'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_completed_long'}).get_text(strip=True) else "N/a"
    player_Long_Att = player.find('td', {'data-stat': 'passes_long'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_long'}).get_text(strip=True) else "N/a"
    player_Long_CmpP = player.find('td', {'data-stat': 'passes_pct_long'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_pct_long'}).get_text(strip=True) else "N/a"
    player_Ast = player.find('td', {'data-stat': 'assists'}).get_text(strip=True) if player.find('td', {'data-stat': 'assists'}).get_text(strip=True) else "N/a"
    player_xAG = player.find('td', {'data-stat': 'xg_assist'}).get_text(strip=True) if player.find('td', {'data-stat': 'xg_assist'}).get_text(strip=True) else "N/a"
    player_xA = player.find('td', {'data-stat': 'pass_xa'}).get_text(strip=True) if player.find('td', {'data-stat': 'pass_xa'}).get_text(strip=True) else "N/a"
    palyer_AxAG = player.find('td', {'data-stat': 'xg_assist_net'}).get_text(strip=True) if player.find('td', {'data-stat': 'xg_assist_net'}).get_text(strip=True) else "N/a"
    player_KP = player.find('td', {'data-stat': 'assisted_shots'}).get_text(strip=True) if player.find('td', {'data-stat': 'assisted_shots'}).get_text(strip=True) else "N/a"
    player_1div3 = player.find('td', {'data-stat': 'passes_into_final_third'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_into_final_third'}).get_text(strip=True) else "N/a"
    player_PPA = player.find('td', {'data-stat': 'passes_into_penalty_area'}).get_text(strip=True) if player.find('td', {'data-stat': 'passes_into_penalty_area'}).get_text(strip=True) else "N/a"
    player_CrsPA = player.find('td', {'data-stat': 'crosses_into_penalty_area'}).get_text(strip=True) if player.find('td', {'data-stat': 'crosses_into_penalty_area'}).get_text(strip=True) else "N/a"
    player_PrgP = player.find('td', {'data-stat': 'progressive_passes'}).get_text(strip=True) if player.find('td', {'data-stat': 'progressive_passes'}).get_text(strip=True) else "N/a"

    # Trả về list chỉ số passing
    return [player_Cmp, player_Att, player_CmpP, player_TotDist, player_PrgDist, player_Short_Cmp, player_Short_Att, plaer_Short_CmpP, player_Medium_Cmp, player_Medium_Att, player_Medium_CmpP, player_Long_Cmp, player_Long_Att, player_Long_CmpP, player_Ast, player_xAG, player_xA, palyer_AxAG, player_KP, player_1div3, player_PPA, player_CrsPA, player_PrgP]

# Hàm cào dữ liệu lấy thông tin cầu thủ của từng đội bóng
def Crawl_data_for_each_team_tmp(players_data, team_data):
    # Lấy thông tin cầu thủ của mỗi đội
    for team in team_data:
        team_name = team[0]
        team_url = team[1]

        print(f"Đang cào dữ liệu cầu thủ của đội {team_name}... {team_url}")
        # Cào url của từng đội bóng
        #r_tmp = requests.get(team_url)
        r_tmp = ""
        r_tmp = read_html_file(r_tmp)
        soup_tmp = BeautifulSoup(r_tmp, 'html.parser')

        # Danh sách tạm thời chứa thông tin cầu thủ
        player_data_tmp = []
        mp = {}

        player_table = soup_tmp.find('table', {
            'class': 'stats_table sortable min_width',
            'id': 'stats_standard_9'
        })

        if player_table:
            # Tìm thẻ <tbody> trong <table>
            tbody = player_table.find('tbody')

            if tbody:
                players = tbody.find_all('tr')
                for player in players:
                    player_data_tmp = Xu_ly_du_lieu_cau_thu(player, team_name, player_data_tmp, mp) 

            else:
                print(f"<Không tìm thấy thẻ <tbody> trong bảng cầu thủ>")
        else:
            print(f"<Không tìm thấy thẻ <table> chứa cầu thủ trong trang của đội {team_name}.>")
            
        #Tìm bảng chứa thông tin các thủ môn
        Goalkeeper_table = soup_tmp.find('table', {
            'class': 'stats_table sortable min_width',
            'id': 'stats_keeper_9'
        })

        if Goalkeeper_table:
            # Tìm thẻ <tbody> trong <table>
            tbody = Goalkeeper_table.find('tbody')

            if tbody:
                players = tbody.find_all('tr')
                # Danh sách lưu tạm thời tên các thủ môn
                list_tmp = []

                for player in players:
                    player_name = player.find('th', {'data-stat': 'player'}).get_text(strip=True) 
                    mp[player_name] += Xu_ly_du_lieu_thu_mon(player)
                    list_tmp.append(player_name)

                for player in player_data_tmp:
                    if player[0] not in list_tmp:
                        player += ["N/a"] * 15
            else:
                print(f"<Không tìm thấy thẻ <tbody> bảng thủ môn.>")
        else:
            print(f"<Không tìm thấy thẻ <table> chứa thủ môn trong trang của đội {team_name}.>")

        # Tìm bảng chứa thông tin Shooting của các cầu thủ
        Shooting_table = soup_tmp.find('table', {
            'class': 'stats_table sortable min_width',
            'id': 'stats_shooting_9'
        })

        if Shooting_table:
            # Tìm thẻ <tbody> trong <table>
            tbody = Shooting_table.find('tbody')

            if tbody:
                players = tbody.find_all('tr')
                # Danh sách lưu tạm thời tên các cầu thủ
                list_tmp = []

                for player in players:
                    player_name = player.find('th', {'data-stat': 'player'}).get_text(strip=True)
                    mp[player_name] += Xu_ly_du_lieu_shooting(player)
                    list_tmp.append(player_name)

                for player in player_data_tmp:
                    if player[0] not in list_tmp:
                        player += ["N/a"] * 17

            else:
                print(f"<Không tìm thấy thẻ <tbody> bảng Shooting.>")
        else:
            print(f"<Không tìm thấy thẻ <table> chứa thông tin Shooting trong trang của đội {team_name}.>")

        # Tìm bảng chứa thông tin Passing của các cầu thủ
        Passing_table = soup_tmp.find('table', {
            'class': 'stats_table sortable min_width',
            'id': 'stats_passing_9'
        })

        if Passing_table:
            # Tìm thẻ <tbody> trong <table>
            tbody = Passing_table.find('tbody')

            if tbody:
                players = tbody.find_all('tr')
                # Danh sách lưu tạm thời tên các cầu thủ
                list_tmp = []

                for player in players:
                    player_name = player.find('th', {'data-stat': 'player'}).get_text(strip=True)
                    mp[player_name] += Xu_ly_du_lieu_passing(player)
                    list_tmp.append(player_name)
                
                for player in player_data_tmp:
                    if player[0] not in list_tmp:
                        player += ["N/a"] * 23

            else:
                print(f"<Không tìm thấy thẻ <tbody> bảng Passing.>")
        else:
            print(f"<Không tìm thấy thẻ <table> chứa thông tin Passing trong trang của đội {team_name}.>")


        for player in player_data_tmp:
            print(*player)
        break
        # Tạm nghỉ trước khi cào đội tiếp theo
        time.sleep(10)

    return players_data

if __name__ == "__main__":
    # # URL to fetch
    # url = 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats'
    # r = requests.get(url)
    # soup = BeautifulSoup(r.content, 'html.parser')
    # # print(soup.prettify())

    # # Ghi vào file hmtl
    # # with open("F:/Python BTL/hi.html", "w", encoding="utf-8") as file:
    # #     file.write(soup.prettify())

    # # Tìm bảng chứa thông tin các đội bóng trong mùa giải 2023-2024
    # table = soup.find('table', {
    #     'class': 'stats_table sortable min_width force_mobilize',
    #     'id': 'results2023-202491_overall'
    # })

     # Danh sách chứa dữ liệu đội bóng và URL
    team_data = []

    # if table:
    #     # Tìm thẻ <tbody> trong <table>
    #     tbody = table.find('tbody')
        
    #     if tbody:
    #         # Lấy tất cả các thẻ <a> có định dạng như yêu cầu trong <tbody>
    #         teams = tbody.find_all('a', href=True)

    #         for team in teams:
    #             if "squads" in team['href']:  # Kiểm tra nếu "squads" có trong href
    #                 team_name = team.get_text(strip=True)
    #                 team_url = "https://fbref.com" + team['href']
    #                 team_data.append([team_name, team_url])
    #     else:
    #         print("Không tìm thấy thẻ <tbody>.")
    # else:
    #     print("Không tìm thấy thẻ <table>.")

    # Đọc dữ liệu từ file CSV
    team_data = read_csv(team_data)

    # for team in team_data:
    #     print(team)

    #  Danh sach chứa từng cầu thủ của đội bóng
    players_data = []
    players_data = Crawl_data_for_each_team_tmp(players_data, team_data)
    
    # for player in players_data:
    #     print(*player)



    # # Chuyển dữ liệu thành DataFrame và lưu thành file CSV
    # df_players = pd.DataFrame(players_data, columns=["Player Name", "Nation", "Team", "Position", "Age", "Matches Played", "Starts", "Minutes", 
    #                                                  "Non-Penalty Goals", "Penalties Made", "Assists", "Yellow Cards", "Red Cards", "xG", 
    #                                                  "npxG", "xAG", "PrgC", "PrgP", "PrgR",
    #                                                  "Gls/90", "Ast/90", "G+A/90", "G-PK/90", "G+A-PK/90", "xG/90", "xAG/90",
    #                                                  "xG+xAG/90", "npxG/90", "npxG+xAG/90"])
    # df_players.to_csv("F:/Python BTL/Players.csv", index=False, encoding='utf-8-sig')
    # print("Đã lưu thông tin các cầu thủ vào file Players.csv")