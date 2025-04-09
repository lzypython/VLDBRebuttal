import json
with open("/back-up/lzy/Rebuttal/R1_D4/hop.json", "r") as f:
    hop = json.load(f)
    # 统计hop =1 hop=2 hop>2的百分比，保留两位小数
    hop1 = 0
    hop2 = 0
    hop3 = 0
    # 格式如下
    #     {
    #     "0": 0.47,
    #     "1": 46.69,
    #     "2": 28.85,
    #     "3": 7.36,
    #     "4": 5.36,
    #     "5": 3.2,
    #     "6": 1.83,
    #     "7": 0.71,
    #     "8": 0.41,
    #     "9": 0.08,
    #     "10": 0.05,
    #     "11": 0.14,
    #     "14": 0.02,
    #     "999": 4.83
    # }
    total = 0
    for i in hop.keys():
        total += hop[i]
        if i == '1':
            hop1 = hop[i]
        elif i == '2':
            hop2 = hop[i]
        else:
            hop3 += hop[i]
    
    hop1 = round(hop1 / total * 100, 2)
    hop2 = round(hop2 / total * 100, 2)
    hop3 = round(hop3 / total * 100, 2)
    print("hop=1: {}%".format(hop1))
    print("hop=2: {}%".format(hop2))
    print("hop>2: {}%".format(hop3))
with open("/back-up/lzy/Rebuttal/R1_D4/answer.json", "r") as f:
    answer = json.load(f)
    # 统计answer =1 answer=2 answer>2的百分比，保留两位小数
    answer1 = 0
    answer2 = 0
    answer3 = 0
    # 格式如下
    total = 0
    for i in answer.keys():
        total += answer[i]
        if i == '1':
            answer1 = answer[i]
        elif i == '2':
            answer2 = answer[i]
        else:
            answer3 += answer[i]
    answer1 = round(answer1 / total * 100, 2)
    answer2 = round(answer2 / total * 100, 2)
    answer3 = round(answer3 / total * 100, 2)
    print("answer=1: {}%".format(answer1))
    print("answer=2: {}%".format(answer2))
    print("answer>2: {}%".format(answer3))
with open("/back-up/lzy/Rebuttal/R1_D4/entity.json", "r") as f:
    entity = json.load(f)
    # 统计entity =1 entity=2 entity>2的百分比，保留两位小数
    entity1 = 0
    entity2 = 0
    entity3 = 0
    # 格式如下
    total = 0
    for i in entity.keys():
        total += entity[i]
        if i == '1':
            entity1 = entity[i]
        elif i == '2':
            entity2 = entity[i]
        else:
            entity3 += entity[i]
    entity1 = round(entity1 / total * 100, 2)
    entity2 = round(entity2 / total * 100, 2)
    entity3 = round(entity3 / total * 100, 2)
    print("entity=1: {}%".format(entity1))
    print("entity=2: {}%".format(entity2))
    print("entity>2: {}%".format(entity3))