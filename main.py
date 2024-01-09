import requests


def main():
    
    languages = ["JS", "Python", "Java", "Ruby", "PHP", "C++", "C#", "C", "GO", "Kotlin"]
    url = "https://api.hh.ru/vacancies"
    result = {}
    for language in languages:
        vacancy_info = {}
        vacancies_processed = 0
        average_salary = 0
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
        #result[vacancy_name] = response["found"]
        vacancy_info["vacancies_found"] = response["found"]
        for salary in response["items"]:
            predict = predict_rub_salary(salary["salary"])
            #print (predict)
            if predict != 0:
                vacancies_processed = vacancies_processed + 1
                average_salary = average_salary + predict
        average_salary = average_salary / vacancies_processed
        vacancy_info["vacancies_processed"] = vacancies_processed
        vacancy_info["average_salary"] = int(average_salary)
        result[vacancy_name] = vacancy_info
    print (result)


def predict_rub_salary(vacancy):
    result = 0
    if vacancy != None:
        if vacancy["from"] is not None and vacancy["to"] is not None:
            result =  ((int(vacancy["from"]) + int(vacancy["to"])) / 2)
        elif vacancy["from"] is not None and vacancy["to"] is None:
            result = (int(vacancy["from"]) * 1.2)
        elif vacancy["from"] is None and vacancy["to"] is not None:
            result = (int(vacancy["to"]) * 0.8)
    return result


if __name__ == '__main__':
    main()



