import requests


RESULT = {}

def list_vacancy():
    #languages = ["JS", "Python", "Java", "Ruby", "PHP", "C++", "C#", "C", "GO", "Kotlin"]
    languages = ["JS"]
    for language in languages:
        hh(language)


def hh(language):
    page = 1
    pages_number = 2
    url = "https://api.hh.ru/vacancies"
    vacancy_info = {}
    vacancies_processed = 0
    average_salary = 0
    while page <= pages_number:
        vacancy_name = "Программист {0}".format(language)
        payload = {
            "area": "1",
            "search_field": "name",
            "text": vacancy_name,
            "page": page,
            "period": "30"
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        response = response.json()
        pages_number = response['pages']
        vacancy_info["vacancies_found"] = response["found"]
        for salary in response["items"]:
            predict = predict_rub_salary(salary["salary"])
            predict = int(predict)
            if predict != 0:
                vacancies_processed = vacancies_processed + 1
                average_salary = int(average_salary) + predict
        if vacancies_processed != 0:
            average_salary_all = average_salary / vacancies_processed
        vacancy_info["vacancies_processed"] = vacancies_processed
        vacancy_info["average_salary"] = int(average_salary_all)
        RESULT[vacancy_name] = vacancy_info
        page += 1
    print (RESULT)


def predict_rub_salary(vacancy):
    result = 0
    if vacancy != None and vacancy["currency"] == "RUR":
        if vacancy["from"] is not None and vacancy["to"] is not None:
            result =  ((int(vacancy["from"]) + int(vacancy["to"])) / 2)
        elif vacancy["from"] is not None and vacancy["to"] is None:
            result = (int(vacancy["from"]) * 1.2)
        elif vacancy["from"] is None and vacancy["to"] is not None:
            result = (int(vacancy["to"]) * 0.8)
    return result


if __name__ == '__main__':
    list_vacancy()
