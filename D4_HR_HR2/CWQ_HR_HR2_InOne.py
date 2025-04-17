import json
import os
import pandas as pd
from evalut import eval_hr_topk
from evalut import eval_f1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.font_manager import FontProperties

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
                modelpath = f"{datspath}/{model}"
                jsonpath = f"{modelpath}/{resultlist[prtype]}/{llm}_{PATHNUM}_{shotsnum}_answers.json"
                f1, hit32 = processSingleJson(jsonpath,idlist,HRtype)
                F1 += f1
                Hit32 += hit32
                data.append([aftername,F1,Hit32])
        data = sorted(data,key=lambda x:newnamelist.index(x[0]))
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_excel(f"{dataset}-{llm}-@{PATHNUM}-{HRtype}.xlsx",index=False)
            
def CombinedGenerationImage(HR_excelpath, HR2_excelpath, saveImgpath):
    custom_colors = [
        "#293844",
        "#FAF0EB","#FCDCC6","#f79767","#f87349","#f64c29","#d32912","#DEBC33","#720909",
        "#42CFFE", "#0487e2",
        "#C8EAD1","#73C088","#397D54", "#3D4F2F"
    ]
    
    # 创建1行2列的图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 8))
    
    # 读取HR数据
    df_hr = pd.read_excel(HR_excelpath)
    Hitlist_hr = df_hr["HR"].tolist()
    methodlist = df_hr["Method"].tolist()
    
    # 读取HR2数据
    df_hr2 = pd.read_excel(HR2_excelpath)
    Hitlist_hr2 = df_hr2["HR2"].tolist()
    
    # 共同的x轴设置
    x = np.arange(len(Hitlist_hr), dtype=float)
    x[1:] += 1 
    x[9:] += 1 
    x[11:] += 1 
    x[15:] += 1 
    
    # 绘制HR图表
    ax1.set_ylim(0.32, 0.7)
    ax1.set_yticks(np.arange(0.3, 0.75, 0.2))
    ax1.axvspan(-1, 0.7, facecolor='#B2B3B0', alpha=0.1)
    ax1.axvspan(0.7, x[8] + 0.7, facecolor='#fee3ce', alpha=0.3)
    ax1.axvspan(x[8] + 0.7, x[10] + 0.8, facecolor='#B7A368', alpha=0.1)
    ax1.axvspan(x[10] + 0.8, x[-1]+1, facecolor='#E3E9D7', alpha=0.3)
    
    for j in range(len(Hitlist_hr)):
        ax1.bar(
            x[j], Hitlist_hr[j], width=0.8, 
            color=custom_colors[j], edgecolor='black', 
            linewidth=4, alpha=1
        )
    
    ax1.set_xticks(x)
    tempname = "qwen2-70b"
    tempname = tempname[0].upper() + tempname[1:]
    tempname = tempname.replace("Qwen2-70b","Qwen2-72B")
    tempname = tempname.replace("b","B")
    ax1.set_xlabel(tempname, fontsize=45, fontweight='bold')
    ax1.set_ylabel("Hits@1", fontsize=45, fontweight='bold')
    ax1.tick_params(axis='x', which='both', length=0)
    ax1.set_xticklabels(range(1,16))
    ax1.tick_params(axis='x', which='major', labelsize=40, width=3,length=20,rotation=60)
    ax1.tick_params(axis='y', which='major', labelsize=50, width=3,length=20)
    ax1.xaxis.labelpad = 10
    ax1.text(-0.5, 0.2, "No.", ha='right', va='center', fontsize=40, fontweight='bold')
    ax1.tick_params(axis='both', which='minor', labelsize=50, width=3)
    
    # 绘制HR2图表
    ax2.set_ylim(0.32, 0.7)
    ax2.set_yticks(np.arange(0.3, 0.75, 0.2))
    ax2.axvspan(-1, 0.7, facecolor='#B2B3B0', alpha=0.1)
    ax2.axvspan(0.7, x[8] + 0.7, facecolor='#fee3ce', alpha=0.3)
    ax2.axvspan(x[8] + 0.7, x[10] + 0.8, facecolor='#B7A368', alpha=0.1)
    ax2.axvspan(x[10] + 0.8, x[-1]+1, facecolor='#E3E9D7', alpha=0.3)
    
    for j in range(len(Hitlist_hr2)):
        ax2.bar(
            x[j], Hitlist_hr2[j], width=0.8, 
            color=custom_colors[j], edgecolor='black', 
            linewidth=4, alpha=1
        )
    
    ax2.set_xticks(x)
    ax2.set_xlabel(tempname, fontsize=45, fontweight='bold')
    ax2.set_ylabel("Judge@1", fontsize=45, fontweight='bold')
    ax2.tick_params(axis='x', which='both', length=0)
    ax2.set_xticklabels(range(1,16))
    ax2.tick_params(axis='x', which='major', labelsize=40, width=3,length=20,rotation=60)
    ax2.tick_params(axis='y', which='major', labelsize=50, width=3,length=20)
    ax2.xaxis.labelpad = 10
    ax2.text(-0.5, 0.2, "No.", ha='right', va='center', fontsize=40, fontweight='bold')
    ax2.tick_params(axis='both', which='minor', labelsize=50, width=3)
    
    # 创建共同的图例
    temp = []
    for i,method in enumerate(methodlist):
        temp.append(f"No.{i+1}:"+method)
    methodlist = temp
    
    legend_elements = [Patch(color=color, label=method) for color, method in zip(custom_colors, methodlist)]
    plt.subplots_adjust(wspace=0.3, hspace=0.75)
    font_properties = FontProperties(weight='bold', size=35)
    
    # 将图例放在图形顶部中央
    fig.legend(handles=legend_elements, loc='upper center', ncol=3, bbox_to_anchor=(0.458, 1), prop=font_properties,labelspacing=0.05)
    
    plt.subplots_adjust(top=0.55, left=0.08, right=0.9,bottom=0.22)
    plt.savefig(saveImgpath, format='pdf', bbox_inches='tight')
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
    shotsnum = "zero_shot"
    modelist = ["PPR","EMB/edge","LLM/qwen2-70b/EMB/ppr_1000_edge_64"]
    PATHNUMlist = [32]
    
    # 生成合并图表
    CombinedGenerationImage(
        f"CWQ-qwen2-70b-@32-HR.xlsx",
        f"CWQ-qwen2-70b-@32-HR2.xlsx",
        f"CWQ-Hits1-Judge1-combined.pdf"
    )