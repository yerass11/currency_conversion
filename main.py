import requests
from bs4 import BeautifulSoup
import csv

url = "https://nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Ошибка при подключении к {url}: {e}")
else:
    soup = BeautifulSoup(response.text, "html.parser")
    

    currency_table = soup.find("table")  
    if currency_table:
        data = []
        for row in currency_table.find_all("tr")[1:]:  
            columns = row.find_all("td")

            if len(columns) >= 3:
                currency_name = columns[1].text.strip() if columns[1] else ""
                currency_code = columns[2].text.strip() if columns[2] else ""
                currency_rate = columns[3].text.strip() if columns[3] else ""
                

                if currency_rate.replace('.', '', 1).isdigit():
                    data.append({
                        "Валюта": currency_name,
                        "Код": currency_code,
                        "Курс": currency_rate
                    })

    
        with open("currency_rates.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Валюта", "Код", "Курс"])
            writer.writeheader()
            writer.writerows(data)

        print("Данные сохранены в файл currency_rates.csv")
    else:
        print("Не удалось найти таблицу с курсами валют.")