from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
from tqdm.std import tqdm

base_url = "https://icml.cc/"

annual_url = {
    2021: ["https://proceedings.mlr.press/v139/"],
    2020: ["https://proceedings.mlr.press/v119/"],
    2019: ["https://proceedings.mlr.press/v97/"],
    2018: ["https://proceedings.mlr.press/v80/"],
    2017: ["https://proceedings.mlr.press/v70/"],
    2016: ["http://proceedings.mlr.press/v48/"],
    2015: ["http://proceedings.mlr.press/v37/"],
    2014: ["http://proceedings.mlr.press/v32/"],
    2013: ["http://proceedings.mlr.press/v28/"],
    # speific
    2012: ["https://icml.cc/2012/papers.1.html"],
}


def get_abstract(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    abstract = soup.find("div", {"id": "abstract"}).get_text()
    return abstract.strip()


def get_paper_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    paper_list = soup.find_all("div", {"class": "paper"})
    paper_info_list = []

    for paper in tqdm(paper_list):
        paper_title = paper.find("p", {"class": "title"}).get_text()
        abstract_url = paper.find("p", {"class": "links"}).a.attrs["href"]
        abstract = get_abstract(abstract_url)
        paper_info_list.append(
            {
                "url": abstract_url,
                "abstract": abstract,
                "title": paper_title,
            }
        )
        print(paper_info_list[-1])

    return paper_info_list


def get_paper_list_2012(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    paper_list = soup.find_all("div", {"class": "paper"})
    paper_info_list = []

    for paper in tqdm(paper_list):
        paper_title = paper.h2.get_text()
        abstract = paper.find("p", {"class": "abstract"}).get_text().strip()
        abstract_url = url
        paper_info_list.append(
            {
                "url": abstract_url,
                "abstract": abstract,
                "title": paper_title,
            }
        )
        print(paper_info_list[-1])
    return paper_info_list


def save_paper_basic_info():
    for year, url_lists in annual_url.items():
        if year > 2013:
            continue
        url_name = str(year)
        paper_info_list = []
        for url in url_lists:
            if year >= 2013:
                paper_info_list.extend(get_paper_list(url))
            else:
                paper_info_list.extend(get_paper_list_2012(url))
        with open(url_name + ".json", "w") as fp:
            json.dump(paper_info_list, fp)
            print(url_name, "collects paper num: ", len(paper_info_list))


# get_paper_list_2012(annual_url[2012][0])
save_paper_basic_info()
