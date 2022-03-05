from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
from tqdm.std import tqdm

base_url = "https://openaccess.thecvf.com/"

annual_url = {
    2021: ["https://openaccess.thecvf.com/ICCV2021?day=all"],
    2019: [
        "https://openaccess.thecvf.com/ICCV2019?day=2019-10-29",
        "https://openaccess.thecvf.com/ICCV2019?day=2019-10-30",
        "https://openaccess.thecvf.com/ICCV2019?day=2019-10-31",
        "https://openaccess.thecvf.com/ICCV2019?day=2019-11-01",
    ],
    2017: ["https://openaccess.thecvf.com/ICCV2017?day=all"],
    2015: ["https://openaccess.thecvf.com/ICCV2015?day=all"],
    2013: ["https://openaccess.thecvf.com/ICCV2013?day=all"],
}


def get_abstract(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    abstract = soup.find("div", {"id": "abstract"}).get_text().strip()
    return abstract


def get_paper_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    paper_list = soup.find_all("dt", {"class": "ptitle"})
    paper_info_list = []
    for paper in tqdm(paper_list):
        abstract_url = urljoin(base_url, paper.a.attrs["href"])
        paper_title = paper.a.get_text().strip()
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


def save_paper_basic_info():
    for year, url_lists in annual_url.items():
        if year != 2019:
            continue
        url_name = str(year)
        paper_info_list = []
        for url in url_lists:
            paper_info_list.extend(get_paper_list(url))
        with open(url_name + ".json", "w") as fp:
            json.dump(paper_info_list, fp)
            print(url_name, "collects paper num: ", len(paper_info_list))


# get_paper_list(annual_url[2021][0])
save_paper_basic_info()
