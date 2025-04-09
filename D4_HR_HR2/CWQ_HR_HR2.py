import json
import os
import pandas as pd
from evalut import eval_hr_topk
from evalut import eval_f1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.font_manager import FontProperties
# from MergeGeneration import MergeGeneration
# 写一个字典，把原来的方法映射到论文中的名称
newnamedic ={
    "PPR+GSR":"SBE-PPR+SBR-SPR",
    "PPR+OSR-EEMS":"SBE-PPR+OSAR-EEMs",
    "PPR+OSR-LLMS":"SBE-PPR+OSAR-LLMs",
    "PPR+ISR-EEMs":"SBE-PPR+ISAR-EEMs",
    "PPR+ISR-LLMs":"SBE-PPR+ISAR-LLMs",
    "EMB-edge+GSR":"SAE-EEMs+SBR-SPR",
    "EMB-edge+OSR-EEMS":"SAE-EEMs+OSAR-EEMs",
    "EMB-edge+OSR-LLMS":"SAE-EEMs+OSAR-LLMs",
    "EMB-edge+ISR-EEMs":"SAE-EEMs+ISAR-EEMs",
    "EMB-edge+ISR-LLMs":"SAE-EEMs+ISAR-LLMs",
    "LLM-EMB-edge+GSR":"SAE-LLMs+SBR-SPR",
    "LLM-EMB-edge+OSR-EEMS":"SAE-LLMs+OSAR-EEMs",
    "LLM-EMB-edge+OSR-LLMS":"SAE-LLMs+OSAR-LLMs",
    "LLM-EMB-edge+ISR-EEMs":"SAE-LLMs+ISAR-EEMs",
    "LLM-EMB-edge+ISR-LLMs":"SAE-LLMs+ISAR-LLMs",
}
newnamelist = [
    "Method",
    "SBE-PPR+SBR-SPR",

    "SAE-EEMs+OSAR-EEMs",
    "SAE-EEMs+OSAR-LLMs",
    "SAE-LLMs+OSAR-EEMs",
    "SAE-LLMs+OSAR-LLMs",
    "SAE-EEMs+ISAR-EEMs",
    "SAE-EEMs+ISAR-LLMs",
    "SAE-LLMs+ISAR-EEMs",
    "SAE-LLMs+ISAR-LLMs",

    "SAE-EEMs+SBR-SPR",
    "SAE-LLMs+SBR-SPR",

    "SBE-PPR+OSAR-EEMs",
    "SBE-PPR+OSAR-LLMs",
    "SBE-PPR+ISAR-EEMs",
    "SBE-PPR+ISAR-LLMs",
]
def processSingleJson(jsonpath,idlist,HRtype):
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
            Hit += data[HRtype]
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
def generation(PATHNUM,dataset,HRtype,datspath):
    idlist = getidlist(dataset)
    for llm in llmlist:
        data = [["Method",f"F1",HRtype]]
        for model in modelist:
            for prtype,result in resultlist.items():
                F1 = 0
                Hit32 = 0
                beforename = namedic[model]+"+"+prtype
                aftername = newnamedic[beforename]
                # try:
                # print("使用新数据：")
                modelpath = f"{datspath}/{model}"
                # modelpath = f"/back-up/gzy/dataset/VLDB/Instance/NewGeneration/{dataset}/{model}"
                jsonpath = f"{modelpath}/{resultlist[prtype]}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
                f1, hit32 = processSingleJson(jsonpath,idlist,HRtype)
                # print("使用新数据成功！")
                F1 += f1
                Hit32 += hit32
                data.append([aftername,F1,Hit32])
                # print(f"{prtype}处理完成！")
        # 按照aftername排序,排序规则参考newnamelist
        data = sorted(data,key=lambda x:newnamelist.index(x[0]))
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_excel(f"{dataset}-{llm}-@{PATHNUM}-{HRtype}.xlsx",index=False)
            
            
def GenerationImage(excelpath, saveImgpath,HRtype):
    custom_colors = [
        "#293844",
        "#FAF0EB","#FCDCC6","#f79767","#f87349","#f64c29","#d32912","#DEBC33","#720909",
        "#42CFFE", "#0487e2",
        "#C8EAD1","#73C088","#397D54", "#3D4F2F"
    ]
    # 读取Excel数据
    # df = pd.read_excel(rootpath)
    # F1list = df[f"F1"].tolist()
    # Hitlist = df[f"HR"].tolist()
    # methodlist = df["Method"].tolist()
    # 一行两列的图,控制间隔
    fig, ax = plt.subplots(1, 1, figsize=(30, 20))
    excelpath = f"CWQ-qwen2-70b-@{PATHNUM}-{HRtype}.xlsx"
    df = pd.read_excel(excelpath)
    Hitlist = df[HRtype].tolist()
    x = np.arange(len(Hitlist), dtype=float)
    x[1:] += 1 
    x[9:] += 1 
    x[11:] += 1 
    x[15:] += 1 
    methodlist = df["Method"].tolist()
    # x = np.arange(len(Hitlist))
    # 设置坐标轴刻度，a为最小值，b为最大值
    ax.set_ylim(0.32, 0.7)
    ax.set_yticks(np.arange(0.3, 0.75, 0.2))
    ax.axvspan(-1, 0.7, facecolor='#B2B3B0', alpha=0.1)
    ax.axvspan(0.7, x[8] + 0.7, facecolor='#fee3ce', alpha=0.3)
    ax.axvspan(x[8] + 0.7, x[10] + 0.8, facecolor='#B7A368', alpha=0.1)
    ax.axvspan(x[10] + 0.8, x[-1]+1, facecolor='#E3E9D7', alpha=0.3)
    for j in range(len(Hitlist)):
        ax.bar(
            x[j], Hitlist[j], width=0.8, 
            color=custom_colors[j], edgecolor='black', 
            linewidth=4, alpha=1
        )
    ax.set_xticks(x)
    tempname = "qwen2-70b"
    tempname = tempname[0].upper() + tempname[1:]
    tempname = tempname.replace("Qwen2-70b","Qwen2-72B")
    tempname = tempname.replace("b","B")
    ax.set_xlabel(tempname, fontsize=45, fontweight='bold')
    # if i == 0:
    ax.set_ylabel(HRtype, fontsize=45, fontweight='bold')
    # 隐藏 X 轴刻度和标签
    ax.tick_params(axis='x', which='both', length=0)
    # ax[k][i].tick_params(axis='x', which='both', length=0)  # 隐藏刻度短线
    ax.set_xticklabels(range(1,16))  # 隐藏 X 轴标签
    ax.tick_params(axis='x', which='major', labelsize=40, width=3,length=20,rotation=60)
    ax.tick_params(axis='y', which='major', labelsize=50, width=3,length=20)
    ax.xaxis.labelpad = 10
    # if dataset == "CWQ":
    ax.text(-0.5, 0.24, "No.", ha='right', va='center', fontsize=40, fontweight='bold')
    ax.tick_params(axis='both', which='minor', labelsize=50, width=3)
            
            
    
    temp = []
    for i,method in enumerate(methodlist):
        temp.append(f"No.{i+1}:"+method)
    methodlist = temp
    # methodlist = ["No."+i for i in methodlist]
    legend_elements = [Patch(color=color, label=method) for color, method in zip(custom_colors, methodlist)]
    plt.subplots_adjust(wspace=0.3, hspace=0.75)  # 设置行和列之间的间隔
    font_properties = FontProperties(weight='bold', size=37)
    # plt.title(f"{dataset} Generation", fontsize=60, fontweight='bold')
    plt.legend(handles=legend_elements, loc='upper center', ncol=3, bbox_to_anchor=(0.54, 330), prop=font_properties,labelspacing=0.05)
    plt.subplots_adjust(top=0.87, left=0.08, right=0.99,bottom=0.1)
    plt.savefig(saveImgpath, format='pdf')
    # plt.tight_layout()
    print("画图保存成功：", saveImgpath)
if __name__ == "__main__":
    llmlist = ["qwen2-70b"]
    datasetlist = ["CWQ"]

    resultlist = {
        "GSR":"SPR",
        "OSR-EEMS":"SPR/EMB",
        "OSR-LLMS":"SPR/LLM/qwen2-70b/EMB_v2",
        "ISR-EEMs":"BeamSearch/EMB",
        "ISR-LLMs":"BeamSearch/LLM/qwen2-70b/EMB_v2"
    }
    namedic = {
        "EMB/edge":"EMB-edge",
        "LLM/qwen2-70b/EMB/ppr_1000_edge_64":"LLM-EMB-edge",
        "PPR":"PPR"
    }
    # shotsNUMlist = ["zero-shot","one-shot","few-shot"]
    shotsnum = "zero_shot"
    modelist = ["PPR","EMB/edge","LLM/qwen2-70b/EMB/ppr_1000_edge_64"]
    PATHNUMlist = [32]
    # for PATHNUM in PATHNUMlist:
    #     for dataset in datasetlist:
    #         generation(PATHNUM,dataset,"HR",f"/back-up/gzy/dataset/VLDB/Instance/NewGeneration/{dataset}")
    #         generation(PATHNUM,dataset,"HR2",f"/back-up/gzy/dataset/VLDB/Instance/Judgement/{dataset}")


    GenerationImage(f"CWQ-qwen2-70b-@32-HR.xlsx",f"CWQ-HR.pdf","HR")
    GenerationImage(f"CWQ-qwen2-70b-@32-HR2.xlsx",f"CWQ-HR2.pdf","HR2")
    