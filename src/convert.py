import json
import datetime
import scrap
import csv
from lib import target as t
from lib import term as e

idToFaculty = {
    # 学部・学科
    "0": "共通",
    # 学士課程
    "1": "国際",
    "2": "情報",
    "3": "芸術",
    # 修士・博士課程（研究科）
    "5": "国際",
    "6": "情報",
    "7": "芸術",
    "8": "平和",
}


def generateJSON(path="../public/csv/sample.csv"):
    content = []
    with open(path, encoding="utf8", newline="") as raw:
        rows = csv.reader(raw)
        next(rows)
        for row in rows:
            target, detail = t.unifyTargetArray(rawStr=row[5], id=row[9][-13:-5])
            dict = {
                "id": row[9][-13:-5],
                "year": row[9][-18:-14],
                "subject": row[0],
                "teacher": row[1],
                "role": row[2],
                "unit": row[3],
                "faculty": idToFaculty.get(row[9][-13], "不明"),
                "target": target,
                "require": row[4],
                "semester": e.termReturn(row[6]),
                "pw": row[7],
                "url": row[9],
                "detail": detail,
            }
            content.append(dict)
    return content


if __name__ == "__main__":
    scrapResult = scrap.summarizeSyllabus()
    path = "../public/ichipiro-syllabus.json"
    with open(path, "w") as f:
        json.dump(
            {"date": str(datetime.date.today()), "contents": generateJSON(scrapResult)},
            f,
            indent=2,
            ensure_ascii=False,
        )
