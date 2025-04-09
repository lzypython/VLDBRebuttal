
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
datasetlist = ["CWQ","webqsp","GrailQA","WebQuestion"]
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
def hop():
    hopdict ={}
    for dataset in datasetlist:
        modelpath = f"/back-up/gzy/dataset/VLDB/Pipeline/Generation/{dataset}/{model}"
        jsonpath = f"{modelpath}/{resultlist[prtype]}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
        
        with open(jsonpath, "r") as f:
            infos = json.load(f)
            print("len(infos):",len(infos["eval_info"]))
            for i in range(len(infos["eval_info"])):
                data = infos["eval_info"][i]
                answers = data["answers"]
                id = str(data["id"])
                if dataset=="WebQuestion":
                    question = normalize(data["question"])
                    hop = questin2hop[question]
                    if hop not in hopdict:
                        hopdict[hop] = 1
                    else:
                        hopdict[hop] += 1
                else:
                    hop = id2hop[id]
                    if hop not in hopdict:
                        hopdict[hop] = 1
                    else:
                        hopdict[hop] += 1
        # 输出hopdict
        # print("dataset:",dataset)
    # 把hop按键排序
    hopdict = dict(sorted(hopdict.items(), key=lambda x: x[0], reverse=False))
    # 转化成百分比
    allkey = 0
    for key in hopdict:
        allkey +=hopdict[key]
    for key in hopdict:
        hopdict[key] = round(hopdict[key]*100/allkey,2)

    print("hopdict:",hopdict)
    # 写入到json文件中
    jsonpath = f"hop.json"
    with open(jsonpath, "w") as f:
        json.dump(hopdict, f, indent=4)
def answer():
    answerdict ={}
    for dataset in datasetlist:
        modelpath = f"/back-up/gzy/dataset/VLDB/Pipeline/Generation/{dataset}/{model}"
        jsonpath = f"{modelpath}/{resultlist[prtype]}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
        
        with open(jsonpath, "r") as f:
            infos = json.load(f)
            print("len(infos):",len(infos["eval_info"]))
            for i in range(len(infos["eval_info"])):
                data = infos["eval_info"][i]
                answers = data["answers"]
                id = str(data["id"])
                lenans = len(answers)
                if lenans not in answerdict:
                    answerdict[lenans] = 1
                else:
                    answerdict[lenans] += 1
    answerdict = dict(sorted(answerdict.items(), key=lambda x: x[0], reverse=False))
    # print("answerdict:",answerdict)
    # 转化成百分比
    allkey = 0
    for key in answerdict:
        allkey += answerdict[key]
    for key in answerdict:
        answerdict[key] = round(answerdict[key]*100/allkey,2)

    print("answerdict:",answerdict)
    # 写入到json文件中
    jsonpath = f"answer.json"
    with open(jsonpath, "w") as f:
        json.dump(answerdict, f, indent=4)
def entity():
    entitydict ={}
    for dataset in datasetlist:
        modelpath = f"/back-up/gzy/dataset/VLDB/Pipeline/Generation/{dataset}/{model}"
        jsonpath = f"{modelpath}/{resultlist[prtype]}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
        with open(jsonpath, "r") as f:
            infos = json.load(f)
            print("len(infos):",len(infos["eval_info"]))
            for i in range(len(infos["eval_info"])):
                data = infos["eval_info"][i]
                entity = data["entities"]
                id = str(data["id"])
                lenentity = len(entity)
                if lenentity not in entitydict:
                    entitydict[lenentity] = 1
                else:
                    entitydict[lenentity] += 1
    answerdict = dict(sorted(entitydict.items(), key=lambda x: x[0], reverse=False))
    # print("answerdict:",answerdict)
    # 转化成百分比
    allkey = 0
    for key in answerdict:
        allkey += answerdict[key]
    for key in answerdict:
        answerdict[key] = round(answerdict[key]*100/allkey,2)
    print("answerdict:",answerdict)
    # 写入到json文件中
    jsonpath = f"entity.json"
    with open(jsonpath, "w") as f:
        json.dump(answerdict, f, indent=4)
hop()
answer()
entity()