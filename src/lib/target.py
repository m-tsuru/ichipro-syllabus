import re

translateDict = {
    "、": ",",
    "，": ",",
    "・": ",",
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "(": "（",
    ")": "）",
}

baseRoleMaximum = {"B": 4, "M": 2, "D": 3}


def roleReturn(rawStr: str, res: dict, BaseRole: str, NoneAllTrue: bool = False):
    min = 0
    if "1" in rawStr:
        res[f"{BaseRole}1"] = True
        min = 1
    if "2" in rawStr:
        res[f"{BaseRole}2"] = True
        min = 2
    if "3" in rawStr:
        res[f"{BaseRole}3"] = True
        min = 3
    if "4" in rawStr:
        res[f"{BaseRole}4"] = True
        min = 4
    if "以上" in rawStr or "above" in rawStr:
        if min == 0:
            min = 1
        for i in range(min, baseRoleMaximum[BaseRole] + 1, 1):
            res[f"{BaseRole}{i}"] = True
    if any(res) and NoneAllTrue == True and min == 0:
        for i in range(1, baseRoleMaximum[BaseRole] + 1, 1):
            res[f"{BaseRole}{i}"] = True
    return res


def unifyTargetArray(rawStr, id):
    success = False
    res = {
        "B1": False,
        "B2": False,
        "B3": False,
        "B4": False,
        "M1": False,
        "M2": False,
        "D1": False,
        "D2": False,
        "D3": False,
        "parseError": False,
    }
    description = ""

    # 1. 文字列辞書に沿って置換処理
    rawStr = (
        rawStr.translate(str.maketrans(translateDict))
        .replace("First", "1st")
        .replace("Second", "2nd")
        .replace("Third", "3rd")
        .replace("fourth", "4th")
        .replace("次", "")
        .replace("生", "")
    )

    # 2. "(前期|後期)博士" などの文字列を含むものは 数字を切り取って M1, D1 などに誘導
    # a. 修士
    if "修士" in rawStr:
        res = roleReturn(rawStr, res, "M", True)
        success = True
    # b. 前期
    if "前期" in rawStr and success != True:
        res = roleReturn(rawStr, res, "M", True)
        success = True
    # c. 後期
    if "後期" in rawStr and success != True:
        res = roleReturn(rawStr, res, "D", True)
        success = True
    # d. 院
    if ("院" in rawStr or "Graduate" in rawStr) and success != True:
        res = roleReturn(rawStr, res, "D", True)
        res = roleReturn(rawStr, res, "M", True)
        success = True

    # 3. 特徴が数字のみのものは、idToFaculty を参照する
    if (
        ("1" in rawStr or "2" in rawStr or "3" in rawStr or "4" in rawStr)
        and (id[0] == "5" or id[0] == "6" or id[0] == "7" or id[0] == "8")
        and success != True
    ):
        res = roleReturn(rawStr, res, "M")
        success = True

    if (
        ("1" in rawStr or "2" in rawStr or "3" in rawStr or "4" in rawStr)
        and (id[0:3] == "00M")
        and success != True
    ):
        res = roleReturn(rawStr, res, "M")
        success != True

    if (
        ("1" in rawStr or "2" in rawStr or "3" in rawStr or "4" in rawStr)
        and (id[0] == "0" or id[0] == "1" or id[0] == "2" or id[0] == "3")
        and success != True
    ):
        res = roleReturn(rawStr, res, "B")
        success = True

    # 4. 1~3 の処理が正常に終了した場合、括弧を抜き出して、備考欄に括弧内のコメントを代入
    if success == True:
        reg = "(?<=（).+?(?=\）)"
        if len(re.findall(reg, rawStr)) != 0:
            description = re.findall(reg, rawStr)[0]
        else:
            pass

    # 5. 全てが成功しなければ、parseError フラグを立てて、備考欄に文字列をそのまま代入し、終了。
    if success == False:
        res["parseError"] = True
        description = rawStr

    return res, description


if __name__ == "__main__":
    array = [
        "Second year and above",
        "3rd year students",
        "Graduate Students",
        "１・２年次",
        "博士前期課程１、２年",
        "2年次以上",
        "１年（情報科学部・芸術学部対象）",
        "博士前期課程絵画研究 日本画１年",
        "芸術学研究科博士後期課程１・２年次",
        "💩",
    ]
    for i in array:
        print("# " + i)
        print(unifyTargetArray(i))
