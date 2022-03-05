from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
from tqdm.std import tqdm

base_url = "https://openaccess.thecvf.com/"

annual_url = {
    2021: ["https://www.isca-speech.org/archive/interspeech_2021/index.html"],
    2020: ["https://www.isca-speech.org/archive/interspeech_2020/index.html"],
    2019: ["https://www.isca-speech.org/archive/interspeech_2019/index.html"],
    2018: ["https://www.isca-speech.org/archive/interspeech_2018/index.html"],
    2017: ["https://www.isca-speech.org/archive/interspeech_2017/index.html"],
    2016: ["https://www.isca-speech.org/archive/interspeech_2016/index.html"],
    2015: ["https://www.isca-speech.org/archive/interspeech_2015/index.html"],
    2014: ["https://www.isca-speech.org/archive/interspeech_2014/index.html"],
    2013: ["https://www.isca-speech.org/archive/interspeech_2013/index.html"],
    2012: ["https://www.isca-speech.org/archive/interspeech_2012/index.html"],
}


def get_abstract(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.find("h3", {"class": "w3-center"})
    if title is None:
        return None, None
    title = title.get_text().strip()
    abstract = (
        soup.find("div", {"class": "w3-container w3-card w3-padding-large w3-white"})
        .p.get_text()
        .strip()
    )
    return title, abstract


def get_paper_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    paper_list = soup.find_all("a", {"class": "w3-text"})
    paper_info_list = []
    for paper in tqdm(paper_list):
        abstract_url = urljoin(url[: -len("index.html")], paper.attrs["href"])
        paper_title, abstract = get_abstract(abstract_url)
        if paper_title is None:
            paper_title = paper.get_text()
            abstract_url = None
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
        if year > 2019:
            continue
        url_name = str(year)
        paper_info_list = []
        for url in url_lists:
            paper_info_list.extend(get_paper_list(url))
        with open(url_name + ".json", "w") as fp:
            json.dump(paper_info_list, fp)
            print(url_name, "collects paper num: ", len(paper_info_list))


save_paper_basic_info()
