from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
from tqdm.std import tqdm

base_url = "https://openaccess.thecvf.com/"

annual_url = {
    2021: ["https://openaccess.thecvf.com/CVPR2021?day=all"],
    2020: [
        "https://openaccess.thecvf.com/CVPR2020?day=2020-06-16",
        "https://openaccess.thecvf.com/CVPR2020?day=2020-06-17",
        "https://openaccess.thecvf.com/CVPR2020?day=2020-06-18",
    ],
    2019: [
        "https://openaccess.thecvf.com/CVPR2019?day=2019-06-18",
        "https://openaccess.thecvf.com/CVPR2019?day=2019-06-19",
        "https://openaccess.thecvf.com/CVPR2019?day=2019-06-20",
    ],
    2018: [
        "https://openaccess.thecvf.com/CVPR2018?day=2018-06-19",
        "https://openaccess.thecvf.com/CVPR2018?day=2018-06-20",
        "https://openaccess.thecvf.com/CVPR2018?day=2018-06-21",
    ],
    2017: ["https://openaccess.thecvf.com/CVPR2017?day=all"],
    2016: ["https://openaccess.thecvf.com/CVPR2016?day=all"],
    2015: ["https://openaccess.thecvf.com/CVPR2015?day=all"],
    2014: ["https://openaccess.thecvf.com/CVPR2014?day=all"],
    2013: ["https://openaccess.thecvf.com/CVPR2013?day=all"],
    # speific
    # 2012: [
    #     "http://tab.computer.org/pamitc/archive/cvpr2012/program-details/schedule.html"
    # ],
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


def get_paper_list_2012(url):
    # Todo
    pass


def save_paper_basic_info():
    for year, url_lists in annual_url.items():
        if year > 2014:
            continue
        url_name = str(year)
        paper_info_list = []
        for url in url_lists:
            if year > 2012:
                paper_info_list.extend(get_paper_list(url))
            else:
                paper_info_list.extend(get_paper_list_2012(url))
        with open(url_name + ".json", "w") as fp:
            json.dump(paper_info_list, fp)
            print(url_name, "collects paper num: ", len(paper_info_list))


# get_paper_list(annual_url[2021][0])
save_paper_basic_info()
