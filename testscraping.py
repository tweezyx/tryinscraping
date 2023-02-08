import requests
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36"
}

#получаем адрес и обрабатываем его
def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response.text)

#забираем из него json
def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(response.json(),file,indent=4,ensure_ascii=False)

def collect_data():
    s = requests.Session()
    response = s.get(url = 'https://career.habr.com/api/frontend/vacancies?q=python&sort=date&type=all&qid=3&currency=RUR',
                     headers=headers)
    data = response.json()
    all_pages = data.get("meta").get("totalPages")

    result_data = []
    for page_count in range(1,all_pages+1):
        url=f"https://career.habr.com/api/frontend/vacancies?q=python&sort=date&type=all&qid=3&currency=RUR&page={page_count}"
        r = s.get(url=url, headers=headers)
        data = r.json()
        vacancies = data.get("list")
        for vacancy in vacancies:
            vacancy_title = vacancy.get("title")
            vacancy_qualification = vacancy.get("salaryQualification").get("title")
            vacancy_salary = vacancy.get("salary").get("formatted")
            if vacancy_salary == "":
                vacancy_salary = 'Не указана'
            adding_time = vacancy.get("publishedDate").get("date")
            result_data.append(
                {
                "title": vacancy_title,
                "qualification": vacancy_qualification,
                "salary": vacancy_salary,
                "adding_time": adding_time,
                #"skills": skills,
                "link": "https://career.habr.com"+vacancy.get("href")
                }
            )
        print(f"{page_count}/{all_pages}")
        with open("result_data.json", "w", encoding="utf-8") as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)
def main():
    #get_page(url="https://career.habr.com/vacancies?type=all")
    #get_json(url="https://career.habr.com/api/frontend/vacancies?q=python&sort=relevance&type=all&qid=3&currency=RUR&page=1")
    collect_data()

if __name__ == "__main__":
    main()