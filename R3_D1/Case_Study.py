# 选择几个好的Instance和几个差的Instance，对比结果
# question answer Instance answer
import json
import os
import pandas as pd
from evalut import eval_hr_topk
from evalut import eval_f1
import tqdm
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.patches import Patch
# from matplotlib.font_manager import FontProperties
# from MergeGeneration import MergeGeneration
# 写一个字典，把原来的方法映射到论文中的名称
# newnamedic ={
#     "PPR+GSR":"SBE-PPR+SBR-SPR",
#     "PPR+OSR-EEMS":"SBE-PPR+OSAR-EEMs",
#     "PPR+OSR-LLMS":"SBE-PPR+OSAR-LLMs",
#     "PPR+ISR-EEMs":"SBE-PPR+ISAR-EEMs",
#     "PPR+ISR-LLMs":"SBE-PPR+ISAR-LLMs",
#     "EMB-edge+GSR":"SAE-EEMs+SBR-SPR",
#     "EMB-edge+OSR-EEMS":"SAE-EEMs+OSAR-EEMs",
#     "EMB-edge+OSR-LLMS":"SAE-EEMs+OSAR-LLMs",
#     "EMB-edge+ISR-EEMs":"SAE-EEMs+ISAR-EEMs",
#     "EMB-edge+ISR-LLMs":"SAE-EEMs+ISAR-LLMs",
#     "LLM-EMB-edge+GSR":"SAE-LLMs+SBR-SPR",
#     "LLM-EMB-edge+OSR-EEMS":"SAE-LLMs+OSAR-EEMs",
#     "LLM-EMB-edge+OSR-LLMS":"SAE-LLMs+OSAR-LLMs",
#     "LLM-EMB-edge+ISR-EEMs":"SAE-LLMs+ISAR-EEMs",
#     "LLM-EMB-edge+ISR-LLMs":"SAE-LLMs+ISAR-LLMs",
# }
# newnamedic ={
#     "SBE-PPR+SBR-SPR":"PPR+GSR",
#     "SBE-PPR+OSAR-EEMs":"PPR+OSR-EEMS",
#     "SBE-PPR+OSAR-LLMs":"PPR+OSR-LLMS",
#     "SBE-PPR+ISAR-EEMs":"PPR+ISR-EEMs",
#     "SBE-PPR+ISAR-LLMs":"PPR+ISR-LLMs",
#     "SAE-EEMs+SBR-SPR":"EMB-edge+GSR",
#     "SAE-EEMs+OSAR-EEMs":"EMB-edge+OSR-EEMS",
#     "SAE-EEMs+OSAR-LLMs":"EMB-edge+OSR-LLMS",
#     "SAE-EEMs+ISAR-EEMs":"EMB-edge+ISR-EEMs",
#     "SAE-EEMs+ISAR-LLMs":"EMB-edge+ISR-LLMs",
#     "SAE-LLMs+SBR-SPR":"LLM-EMB-edge+GSR",
#     "SAE-LLMs+OSAR-EEMs":"LLM-EMB-edge+OSR-EEMS",
#     "SAE-LLMs+OSAR-LLMs":"LLM-EMB-edge+OSR-LLMS",
#     "SAE-LLMs+ISAR-EEMs":"LLM-EMB-edge+ISR-EEMs",
#     "SAE-LLMs+ISAR-LLMs":"LLM-EMB-edge+ISR-LLMs",
# }
newnamelist = [
    "SBR-PPR+SBR-SPR",  # 最差的 N0.1
    "SAE-EEMs+ISAR-EEMs", # 最差的 N0.6
    "SAE-EEMs+OSAR-EEMs", # 最好的 No.2
    "SAE-EEMs+OSAR-LLMs", # 最好的 No.3
]
# newnamelist = [
#     "Method",
#     "SBE-PPR+SBR-SPR",

#     "SAE-EEMs+OSAR-EEMs",
#     "SAE-EEMs+OSAR-LLMs",
#     "SAE-LLMs+OSAR-EEMs",
#     "SAE-LLMs+OSAR-LLMs",
#     "SAE-EEMs+ISAR-EEMs",
#     "SAE-EEMs+ISAR-LLMs",
#     "SAE-LLMs+ISAR-EEMs",
#     "SAE-LLMs+ISAR-LLMs",

#     "SAE-EEMs+SBR-SPR",
#     "SAE-LLMs+SBR-SPR",

#     "SBE-PPR+OSAR-EEMs",
#     "SBE-PPR+OSAR-LLMs",
#     "SBE-PPR+ISAR-EEMs",
#     "SBE-PPR+ISAR-LLMs",
# ]
def processSingleJson(jsonpath,idlist):
    # 需要算出F1@PATHNUM和Hit@PATHNUM
    F1 =0
    Hit = 0
    count = 0
    with open(jsonpath, "r") as f:
        infos = json.load(f)
        for i in range(len(infos["eval_info"])):
            data = infos["eval_info"][i]
            answers = data["answers"]
            id = str(data["id"])
            if id not in idlist:
                continue
            F1 += data["F1"]
            Hit += data["HR"]
            count += 1
    F1 = F1/count
    Hit = Hit/count
    return F1, Hit
def getidlist(dataset):
    txtPath = f"/back-up/gzy/dataset/VLDB/Pipeline/PathRetrieval/Result/Instance_1000_{dataset}_sampleID.txt"
    idlist = []
    with open(txtPath, "r") as f:
        for line in f:
            idlist.append(line.strip())
    return idlist
def casestudy(PATHNUM,dataset):
    idlist = getidlist(dataset)
    numindexdic = {
        0:1,
        1:2,
        2:8,
        3:10,
        4:11,
        5:12,
        6:14,
    }
    for llm in llmlist:
        data = [["Method",f"F1",f"HR"]]
        result = []
        templist = []
        for i in tqdm.tqdm(range(500)):
            temp = {}
            temp = {
                "case_id":i
            }
            for index,instance in enumerate(Instancelist):
                # beforeinstance = newnamedic[instance]
                se = instance.split("+")[0]
                pr = instance.split("+")[1]
                sepath = sedic[se]
                prpath = prdic[pr]
                modelpath = f"/back-up/gzy/dataset/VLDB/Instance/NewGeneration/{dataset}/{sepath}"
                jsonpath = f"{modelpath}/{prpath}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
                with open(jsonpath,"r",encoding="utf-8") as f:
                    infos = json.load(f)
                    data = infos["eval_info"][i]
                    id = data["id"]
                    if id not in idlist:
                        continue
                    # print(id)
                    llm_answer = data["llm_answer"]
                    ReasoningPaths = data["ReasoningPaths"]
                    f1 = data["F1"]
                    Hr = data["HR"]
                numindex = numindexdic[index]
                temp[f"No. {numindex}. "+instance] = {
                    "llm_answer":llm_answer,
                    "F1":f1,
                    "HR":Hr,
                    # "ReasoningPaths":ReasoningPaths
                }
                templist.append(f1)
            
            temp["id"] = data["id"]
            temp["question"] = data["question"]
            temp["answer"] = data["answers"]
            if templist[0]==0 and templist[1]==0 and templist[2]==1 and templist[3]==1:
                # temp["best"] = "best"
                result.append(temp)
        # 写入json文件中
            llm = llm.replace("70b","72B")
            with open(f"{dataset}-{llm}-casestudy-notion.json","w") as f:
                f.write(json.dumps(result, indent=4,ensure_ascii=False))

            
            

if __name__ == "__main__":
    # llmlist = ["qwen2-7b","llama3-8b","qwen2-70b","qwen2-7b","llama3-8b","qwen2-70b"]
    # llmlist = ["qwen2-7b","glm4-9b","qwen2-70b","llama3.3-70b","qwen2-7b","glm4-9b","qwen2-70b","llama3.3-70b"]
    llmlist = ["qwen2-7b"]
    # datasetlist = ["CWQ","webqsp","GrailQA","WebQuestion"]
    datasetlist = ["WebQuestion"]
    prdic = {
        "SBR-SPR":"SPR",
        "OSAR-EEMs":"SPR/EMB",
        "OSAR-LLMs":"SPR/LLM/qwen2-70b/EMB_v2",
        "ISAR-EEMs":"BeamSearch/EMB",
        "ISAR-LLMs":"BeamSearch/LLM/qwen2-70b/EMB_v2"
    }
    sedic = {
        "SAE-EEMs":"EMB/edge",
        "SAE-LLMs":"LLM/qwen2-70b/EMB/ppr_1000_edge_64",
        "SBE-PPR":"PPR"
    }
    Instancelist = [
        "SBE-PPR+SBR-SPR",  # Group 1  N0.1
        "SAE-EEMs+OSAR-EEMs", # Group 2 最好的 No.2
        "SAE-LLMs+ISAR-EEMs", # Group 2 最差的 No.8
        "SAE-EEMs+SBR-SPR", # Group 3 最好的 No.10
        "SAE-LLMs+SBR-SPR", # Group 3 最差的 No.11
        "SBE-PPR+OSAR-EEMs", # Group 4 最好的 No.12
        "SBE-PPR+ISAR-EEMs", # Group 4 最差的 No.14
    ]
    # shotsNUMlist = ["zero-shot","one-shot","few-shot"]
    shotsnum = "zero_shot"
    # modedic = {
    #     "PPR"
    # }
    # ["PPR","EMB/edge","LLM/qwen2-70b/EMB/ppr_1000_edge_64"]
    PATHNUMlist = [32]
    PATHNUM = 32
    for PATHNUM in PATHNUMlist:
        for dataset in datasetlist:
            casestudy(PATHNUM,dataset)
    print("全部处理完成！")