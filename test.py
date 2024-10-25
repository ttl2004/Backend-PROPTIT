import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import time
import csv
# Thiết lập mã hóa UTF-8 cho đầu ra
sys.stdout.reconfigure(encoding='utf-8')

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


# Hàm cào dữ liệu lấy thông tin cầu thủ của từng đội bóng
def Crawl_data_for_each_team(players_data):
    # Lấy thông tin cầu thủ của mỗi đội
    for team in team_data:
        team_name = team[0]
        team_url = team[1]

        print(f"Đang cào dữ liệu cầu thủ của đội {team_name}... ")
        # Cào url của từng đội bóng
        r_tmp = requests.get(team_url)
        soup_tmp = BeautifulSoup(r_tmp.content, 'html.parser')

        with open("F:/Python BTL/hi.html", "w", encoding="utf-8") as file:
            file.write(soup_tmp.prettify())

        player_table = soup_tmp.find('table', {
            'class': 'stats_table sortable min_width',
            'id': 'stats_standard_9'
        })

        if player_table:
            # Tìm thẻ <tbody> trong <table>
            tbody = player_table.find('tbody')

            if tbody:
                # Lấy tất cả các thẻ <a> có định dạng như yêu cầu trong <tbody>
                players = tbody.find_all('a', href=True)

                for player in players:
                    if "players" in player['href']:
                        # Lấy tên cầu thủ
                        player_name = player.get_text(strip=True)
                        if player_name != "Matches": 
                            players_data.append([team_name, player_name])

                print(f"Đã cào xong dữ liệu cầu thủ của đội {team_name}.")

            else:
                print(f"Không tìm thấy thẻ <tbody> trong trang của đội {team_name}.")
        else:
            print(f"Không tìm thấy thẻ <div> chứa cầu thủ trong trang của đội {team_name}.")

        # Tạm nghỉ trước khi cào đội tiếp theo
        time.sleep(5)

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

    #         # Chuyển dữ liệu thành DataFrame và lưu thành file CSV
    #         # df = pd.DataFrame(team_data, columns=["Tên Đội", "URL"])
    #         # df.to_csv("F:/Python BTL/Team.csv", index=False, encoding='utf-8-sig')
    #         # print("Đã lưu thông tin các đội bóng vào file Team.csv")
    #     else:
    #         print("Không tìm thấy thẻ <tbody>.")
    # else:
    #     print("Không tìm thấy thẻ <table>.")

    # Đọc dữ liệu từ file CSV
    team_data = read_csv(team_data)

    for team in team_data:
        print(team)

    #  Danh sach chứa từng cầu thủ của đội bóng
    players_data = []
    players_data = Crawl_data_for_each_team(players_data)



    # Chuyển dữ liệu thành DataFrame và lưu thành file CSV
    df_players = pd.DataFrame(players_data, columns=["Tên Đội", "Tên Cầu Thủ"])
    df_players.to_csv("F:/Python BTL/Players.csv", index=False, encoding='utf-8-sig')
    print("Đã lưu thông tin các cầu thủ vào file Players.csv")