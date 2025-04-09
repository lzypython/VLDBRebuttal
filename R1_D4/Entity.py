
import json
from evalut import normalize
datasetlist = ["CWQ","webqsp","GrailQA","WebQuestion"]
model = "LLM/qwen2-70b/EMB/ppr_1000_edge_64"
shotsnum = "zero_shot"
PATHNUM = 32
llm = "qwen2-7b"
resultlist = {
    "GSR":"SPR",
}
prtype = "GSR"
datasetlist = ["CWQ"]
datasetrootpath = "/home/gzy/graphrag/src/local_data"
id2hop = {}
questin2hop = {}
for dataset in datasetlist:
    datasetpath = f"{datasetrootpath}/{dataset}_hop.json"
    if dataset=="WebQuestion":
        # 根据question找hop
        with open(datasetpath, "r") as f:
            hopinfo = json.load(f)
            for data in hopinfo:
                question = normalize(data["question"])
                questin2hop[question] = data["hop"]
    else:
        # 根据id找hop
        with open(datasetpath, "r") as f:
            hopinfo = json.load(f)
            for data in hopinfo:
                id2hop[str(data["id"])] = data["hop"]

def entity():
    entitydict ={}
    for dataset in datasetlist:
        modelpath = f"/back-up/gzy/dataset/VLDB/Pipeline/Generation/{dataset}/{model}"
        jsonpath = f"{modelpath}/{resultlist[prtype]}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
        F1_1 = 0
        F1_2 = 0
        F1_3 = 0
        HR_1 = 0
        HR_2 = 0
        HR_3 = 0
        count1 =0
        count2 =0
        count3 =0
        with open(jsonpath, "r") as f:
            infos = json.load(f)
            print("len(infos):",len(infos["eval_info"]))
            for i in range(len(infos["eval_info"])):
                data = infos["eval_info"][i]
                entity = data["entities"]
                id = str(data["id"])
                f1 = data["F1"]
                hr = data["HR"]
                lenentity = len(entity)
                if lenentity == 1:
                    F1_1 += f1
                    HR_1 += hr
                    count1 += 1
                elif lenentity == 2:
                    F1_2 += f1
                    HR_2 += hr
                    count2 += 1
                elif lenentity > 2:
                    F1_3 += f1
                    HR_3 += hr
                    count3 += 1
                # if lenentity not in entitydict:
                #     entitydict[lenentity] = 1
                # else:
                #     entitydict[lenentity] += 1
        print(F1_1/count1,F1_2/count2,F1_3/count3)
        print(HR_1/count1,HR_2/count2,HR_3/count3)
    # answerdict = dict(sorted(entitydict.items(), key=lambda x: x[0], reverse=False))
    # # print("answerdict:",answerdict)
    # # 转化成百分比
    # allkey = 0
    # for key in answerdict:
    #     allkey += answerdict[key]
    # for key in answerdict:
    #     answerdict[key] = round(answerdict[key]*100/allkey,2)
    # print("answerdict:",answerdict)
    # # 写入到json文件中
    # jsonpath = f"entity.json"
    # with open(jsonpath, "w") as f:
    #     json.dump(answerdict, f, indent=4)
entity()