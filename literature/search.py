# encoding=utf8
import sys
from turtle import tilt

from matplotlib.pyplot import title
import csv

# reload(sys)
# sys.setdefaultencoding("utf8")

import os
import json

CONFERENCES = [
    "AAAI",
    "ACL",
    "EMNLP",
    "COLING",
    "NAACL",
    "IJCAI",
    "CVPR",
    "ICCV",
    "NIPS",
    "ICML",
    # "Interspeech",
]


def search(conference, year, keywords):
    files = [
        os.path.join(conference, file_name)
        for file_name in os.listdir(conference)
        if file_name.startswith(str(year)) and file_name.endswith(".json")
    ]
    res = []
    for file_path in files:
        with open(file_path, "r") as fp:
            literature = json.load(fp)
            for paper in literature:
                abstract = paper["abstract"]
                title = paper["title"]
                if abstract:
                    abstract = (
                        abstract.replace("\n", " ")
                        .encode("ascii", "ignore")
                        .decode("ascii")
                    )
                if title:
                    title = title.lower()
                flag = False
                if isinstance(keywords, list):
                    for keyword in keywords:
                        if keyword in paper["title"].lower():
                            flag = True
                            break
                        elif (abstract is not None) and (keyword in abstract.lower()):
                            flag = True
                            break
                    if flag:
                        print(abstract)
                        res.append(
                            (
                                paper["title"],
                                paper["url"],
                                abstract,
                            )
                        )
                else:
                    if keywords(title or "", abstract or ""):
                        print(abstract)
                        res.append(
                            (
                                paper["title"],
                                paper["url"],
                                abstract,
                            )
                        )
    return res


def search_all(conferences=None, years=None, keywords=None):
    res = {}
    if conferences is None:
        conferences = CONFERENCES
    if years is None:
        years = list(range(2012, 2022))
    if keywords is None:
        keywords = [""]

    if isinstance(conferences, str):
        conferences = [conferences]
    if isinstance(years, int):
        years = [years]
    if isinstance(keywords, str):
        keywords = [keywords]

    for conference in conferences:
        for year in years:
            search_res = search(conference, year, keywords)
            if len(search_res) > 0:
                res[str(year) + str(conference)] = search_res
    return res


def judge_ner(title, abstract):
    ner_key = ["(ner)", " ner ", "named entity recognition", "entity extract"]
    for k in ner_key:
        if k in title or k in abstract:
            return True
    return False


def main():
    ans = search_all(None, list(range(2022 - 4, 2022)), judge_ner)
    count = 0
    for _, value in ans.items():
        count += len(value)
    print(count)

    file_name = "ner"

    with open("%s.csv" % file_name, "w") as fp:
        f_csv = csv.writer(fp)
        for year_conf, value in ans.items():
            year = int(year_conf[:4])
            conference = year_conf[4:]
            for paper in value:
                f_csv.writerow([year, conference] + list(paper))


if __name__ == "__main__":
    main()
