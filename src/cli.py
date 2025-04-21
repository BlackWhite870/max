from db import (
    save_weather_to_db,
    delete_weather_by_city,
    get_all_weather,
    search_city_weather,
)


def menu():
    while True:
        print("\n=== Меню ===")
        print("1. Просмотреть все записи")
        print("2. Добавить погоду вручную")
        print("3. Удалить город")
        print("4. Найти город")
        print("0. Выход")
        choice = input("Выберите пункт: ")

        if choice == "1":
            records = get_all_weather()
            if not records:
                print("Нет данных.")
            else:
                for row in records:
                    print(f"{row[0]}: {row[1]}°C, {row[2]}, обновлено: {row[3]}")
        elif choice == "2":
            city = input("Введите название города: ")
            temp = float(input("Температура (°C): "))
            desc = input("Описание погоды: ")
            save_weather_to_db(city, temp, desc)
            print("Запись добавлена.")
        elif choice == "3":
            city = input("Введите название города для удаления: ")
            delete_weather_by_city(city)
        elif choice == "4":
            city = input("Введите название города для поиска: ")
            result = search_city_weather(city)
            if result:
                print(
                    f"{result[0]}: {result[1]}°C, {result[2]}, обновлено: {result[3]}"
                )
            else:
                print("Город не найден.")
        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    menu()
