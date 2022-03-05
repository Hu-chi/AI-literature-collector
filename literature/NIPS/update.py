from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
from tqdm.std import tqdm

base_url = "https://nips.cc/"

annual_url = {
    2021: ["https://nips.cc/Conferences/2021/Schedule?type=Poster"],
    2020: ["https://nips.cc/Conferences/2020/Schedule?type=Poster"],
    2019: ["https://nips.cc/Conferences/2019/Schedule?type=Poster"],
    2018: ["https://nips.cc/Conferences/2018/Schedule?type=Poster"],
    2017: ["https://nips.cc/Conferences/2017/Schedule?type=Poster"],
    2016: ["https://nips.cc/Conferences/2016/Schedule?type=Poster"],
    2015: ["https://nips.cc/Conferences/2015/Schedule?type=Poster"],
    2014: ["https://nips.cc/Conferences/2014/Schedule?type=Poster"],
    2013: ["https://nips.cc/Conferences/2013/Schedule?type=Poster"],
    2012: ["https://nips.cc/Conferences/2012/Schedule?type=Poster"],
}


def get_abstract(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    abstract = soup.find("div", {"class": "abstractContainer"})
    if abstract is None:
        return None
    else:
        abstract = abstract.get_text()
    return abstract.strip()


def get_paper_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    paper_list = soup.find_all("div", {"class": "maincard narrower poster"})
    paper_info_list = []
    for paper in tqdm(paper_list):
        paper_title = paper.find("div", {"class": "maincardBody"}).get_text()
        id = paper.parent.attrs["onclick"].split("(")[-1].strip(")")
        abstract_url = url[: -len("type=Poster")] + "showEvent=%s" % id
        # abstract = None
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
        if year not in [2019]:
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
