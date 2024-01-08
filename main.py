import requests


def main():
    
    languages = ["JS", "Python", "Java", "Ruby", "PHP", "C++", "CSS", "C#", "C", "GO"]
    url = "https://api.hh.ru/vacancies"
    result = {}
    for language in languages:
        vacancy_name = "Программист {0}".format(language)
        payload = {
            "area": "1",
            "search_field": "name",
            "text": vacancy_name,
            "page": "1",
            "period": "30"
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        response = response.json()
        result[vacancy_name] = response["found"]
        if language == "Python":
            for salary in response["items"]:
                predict_rub_salary(salary["salary"])


def predict_rub_salary(vacancy):
    if vacancy != None:
        print(vacancy)
        if vacancy["from"] is not None and vacancy["to"] is not None:
            print ((int(vacancy["from"]) + int(vacancy["to"])) / 2)
        elif vacancy["from"] is not None and vacancy["to"] is None:
            print (int(vacancy["from"]) * 1.2)
        elif vacancy["from"] is None and vacancy["to"] is not None:
            print (int(vacancy["to"]) * 0.8)


if __name__ == '__main__':
    main()



