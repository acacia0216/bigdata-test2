import json

from collect import crawler
from analysis import analizer
from visualize import visualizer

pagename = "chosun"
from_date = "2017-01-01"
to_date = "2018-05-23"
path = "D:/javaStudy/"
f_ex = ".json"
filename = path + pagename + f_ex

if __name__ == "__main__":
    # 수집
    # postList = crawler.fb_get_post_list(pagename, from_date, to_date)
    # print(postList)

    # 분석
    dataString = analizer.json_to_str(filename, "message_str")
    count_data = analizer.count_wordfreq(dataString)


    # with open("d:/javaStudy/analysis_" + f_name + ".json", 'w', encoding='utf-8') as outfile:
    #     json_string = json.dumps(count_data, indent=4, sort_keys=True, ensure_ascii=False)
    #     outfile.write(json_string)

    print("카운트데이터 : ", count_data)

    dictWord1 = dict(count_data.most_common(20))
    dictWord2 = dict(count_data.most_common(50))

    # 그래프
    visualizer.show_graph_bar(dictWord1, pagename)
    visualizer.wordcloud(dictWord2, pagename)
