from requests_html import HTMLSession
from datetime import date
import pandas as pd
import time

session = HTMLSession()
data_frame = list()

def parse_page_links():
    base_url = "https://empregos.maringa.com/?area=&bairro=&cidade=&estado=&experiencia=&faixa_salarial=&text=&vagas-de-emprego={1}"
    response = session.get(base_url)
    last_element = len(response.html.find("a.page-link.rounded[href]"))
    last_page = 10#int(response.html.find("a.page-link.rounded[href]")[last_element - 1].attrs["href"][-3:])
    all_links = list()
    for page in range(1, last_page + 1):
        url = f"https://empregos.maringa.com/?area=&bairro=&cidade=&estado=&experiencia=&faixa_salarial=&text=&vagas-de-emprego={page}"
        all_links.append(url)
    return all_links

def parse_jobs(urls):
    for url in urls[0:15]:
        response = session.get(url)
        size = len(response.html.find("div.card-anuncio.mb-3"))
        for i in range(0, size):
            job =  {
                "job_title": response.html.find("b.flex-wrap")[i].text,
                "company_name": response.html.find("div.text-muted.mt-1")[i].text,
                "job_area": response.html.find("p.descricao small")[i].text,
                "publication_date": response.html.find("small.text-nowrap.ml-4")[i].text,
                "job_link": response.html.find("a.flex-wrap[href]")[i].attrs["href"]
            }
            data_frame.append(job)
        time.sleep(1)

parse_jobs(parse_page_links())
df = pd.DataFrame(data_frame).query("publication_date.str.len() > 0").reset_index(drop = True)
df["publication_date"] = pd.to_datetime(df["publication_date"]).dt.strftime("%d/%m/%Y %H:%M")
df["job_title"] = df["job_title"].str.lower()
df = df[df["job_title"].str.contains("analista|dados|dado|b.i.|b.i|power|inteligência|inteligencia|business|intelligence")]
#df.info()
df.to_excel("C:\\Users\\diogo\\Downloads\\empregos.xlsx", sheet_name = "empregos")
print(df)