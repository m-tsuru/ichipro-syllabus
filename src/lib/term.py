def termReturn(rawStr: str):
    dict = {
        "T1": False,
        "T2": False,
        "T3": False,
        "T4": False,
        "Other": False,
        "parseError": False,
    }
    if "前期授業" == rawStr:
        dict["T1"] = True
        dict["T2"] = True

    elif "後期授業" == rawStr:
        dict["T3"] = True
        dict["T4"] = True

    elif "前期前半" == rawStr:
        dict["T1"] = True

    elif "前期後半" == rawStr:
        dict["T2"] = True

    elif "後期前半" == rawStr:
        dict["T3"] = True

    elif "後期後半" == rawStr:
        dict["T4"] = True

    elif "年間授業" == rawStr:
        dict["T1"] = True
        dict["T2"] = True
        dict["T3"] = True
        dict["T4"] = True
    else:
        dict["parseError"] = True

    return dict


if __name__ == "__main__":
    array = ["前期後半", "前期授業", "年間授業", "💩"]
    for i in array:
        print("# " + i)
        print(termReturn(i))
