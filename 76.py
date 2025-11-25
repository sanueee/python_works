import requests
import matplotlib.pyplot as plt
from datetime import datetime
from statistics import mean

def load_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        data = []
        for i, line in enumerate(lines):
            if i == 0:
                continue
            parts = line.split(',')
            if len(parts) == 4:
                data.append(parts)

        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
        return []

def filter_pension_data(data, region, year):
    try:
        filtered = []
        year_str = str(year)
        for row in data:
            name, reg, date, value = row
            if 'пенси' in name.lower() and reg == region and year_str in date:
                filtered.append(row)

        return filtered

    except Exception as e:
        print(f"Ошибка при фильтрации данных - {e}")
        return []

def calculate_average_pension(filtered_data):
    try:
        if not filtered_data:
            print("Нет данных для расчета средней пенсии")
            return None
        values = []
        for row in filtered_data:
            try:
                value = float(row[3])
                values.append(value)
            except ValueError:
                print(f"Не удалось преобразовать значение - {row[3]}")
                continue

        if not values:
            print("Нет корректных числовых значений")
            return None

        avg = mean(values)
        return avg

    except Exception as e:
        print(f"Ошибка при расчете средней пенсии: {e}")
        return None

def plot_pension_dynamics(filtered_data, region, year):
    try:
        if not filtered_data:
            print("Нет данных для построения графика")
            return

        dates = []
        values = []

        for row in filtered_data:
            try:
                date_str = row[2]
                value = float(row[3])
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                dates.append(date_obj)
                values.append(value)
            except (ValueError, IndexError) as e:
                print(f"Ошибка обработки строки {row}: {e}")
                continue
        if not dates or not values:
            print("Нет корректных данных для графика")
            return

        sorted_data = sorted(zip(dates, values))
        dates, values = zip(*sorted_data)

        plt.figure(figsize=(12, 6))
        plt.plot(dates, values, marker='o', linewidth=2, markersize=6)
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Пенсия (руб.)', fontsize=12)
        plt.title(f'Динамика пенсии в {region} за {year} год', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.show()

    except Exception as e:
        print(f"Ошибка при построении графика: {e}")

def main():
    url = "https://raw.githubusercontent.com/dm-fedorov/python_basic/master/data/opendata.stat"
    region = "Забайкальский край"
    year = 2018

    data = load_data_from_url(url)
    if not data:
        print("Не удалось загрузить данные")
        return

    filtered_data = filter_pension_data(data, region, year)
    plot_pension_dynamics(filtered_data, region, year)
    if not filtered_data:
        print(f"Данные о пенсии в {region} за {year} год не найдены")
        return

    avg_pension = calculate_average_pension(filtered_data)
    if avg_pension is not None:
        print(f"\nСредняя пенсия в регионе '{region}' за {year} год: {avg_pension:.2f} рублей")

if __name__ == "__main__":
    main()