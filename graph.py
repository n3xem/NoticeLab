import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime
matplotlib.use('Agg')

lab_limit_dict = {
    "小坂": 9,
    "中島": 9,
    "高橋": 9,
    "鉄谷": 9,
    "川澄": 9,
    "寺田": 9,
    "増田": 9,
    "岩井": 9,
    "大野": 9,
    "森谷": 9,
    "竜田": 2,
    "山田": 2,
    "池田": 2,
    "井ノ上": 2
}


def make_graph(dict, filename):
    plt.rcParams["font.family"] = "meiryo"
    fig = plt.figure()

    overlimit_dict = {}

    for keys in dict.keys():
        if dict[keys] > lab_limit_dict[keys]:
            overlimit_dict[keys] = dict[keys] - lab_limit_dict[keys]
            dict[keys] = lab_limit_dict[keys]
        else:
            overlimit_dict[keys] = 0

    left = np.array(list(dict.keys()))
    height1 = np.array(list(dict.values()))
    height2 = np.array(list(overlimit_dict.values()))
    plt.bar(left, height1, width=0.5, color="green")
    plt.bar(left, height2, width=0.5, bottom=height1, color="orange")
    plt.title("希望人数:" + str(np.sum(height1) + np.sum(height2)) +
              "人 " + str(datetime.datetime.now()))
    fig.savefig(filename)
    plt.close()


def make_sorted_graph(tuple_list, filename):
    plt.rcParams["font.family"] = "meiryo"
    fig = plt.figure()
    overlimit_list = []

    listed_list = []
    for item in tuple_list:
        listed_list.append(list(item))
    for item in listed_list:
        if lab_limit_dict[item[0]] < item[1]:
            overlimit_list.append(item[1] - lab_limit_dict[item[0]])
            item[1] = lab_limit_dict[item[0]]
        else:
            overlimit_list.append(0)
    left = np.array([item[0] for item in listed_list])
    height1 = np.array([item[1] for item in listed_list])
    height2 = np.array(overlimit_list)
    plt.bar(left, height1, width=0.5, color="green")
    plt.bar(left, height2, width=0.5, bottom=height1, color="orange")
    plt.title("希望人数:" + str(np.sum(height1) + np.sum(height2)) +
              "人 " + str(datetime.datetime.now()))
    fig.savefig(filename)
    plt.close()


if __name__ == "__main__":
    make_graph
