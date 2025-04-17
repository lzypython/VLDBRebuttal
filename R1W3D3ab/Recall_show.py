import json
import matplotlib.pyplot as plt  
Rootpath = "/back-up/gzy/dataset/VLDB/Rebuttal/Generation/CWQ/"
the_list = [0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
modellist = ["SPR/EMB"]
# LLMlist = ["glm4-9b","qwen2-7b","qwen2-70b"]
LLMlist = ["qwen2-7b","qwen2-70b","qwen2-1.5b","qwen2-0.5b","llama2-7b","llama3-8b","llama3-70b","llama3.2-1b","llama3.2-3b","llama3.1-70b","llama3.3-70b","llama3.3-70b-awq","mistral-12b","glm4-9b"]

# idlist
# with open(f"/back-up/lzy/Rebuttal/D2/3.ISAR-CWQ_250_sampleID.txt", "r") as f:
#     for line in f:
#         idlist.append(line.strip())
def getjson():
    for model in modellist:
        result_dic = {}
        for LLM in LLMlist:
            llm_dic = {}
            for the in the_list:
                jsonpath = Rootpath +str(the) +"/"+ model + "/" +LLM + "_32_256_zero_shot_answers" + ".json"
                with open(jsonpath, "r") as f:
                    data = json.load(f)
                HR_all = 0
                for i in range(len(data["eval_info"])):
                    HR_all += data["eval_info"][i]["HR"]
                HR = HR_all/len(data["eval_info"])
                llm_dic[the] = HR
            result_dic[LLM] = llm_dic
        with open("Recall_the_256.json", "w") as f:
            json.dump(result_dic, f, indent=4)


def getimage():
    with open("/back-up/lzy/Rebuttal/R1W3D3ab/Recall_the_256.json", "r", encoding="utf-8") as f:  
        data = json.load(f)  

    x = [float(k) for k in sorted(data["qwen2-70b"].keys())]  

    plt.figure(figsize=(8, 6))  

    markers = ['o', 's', '^','*', 'D', 'P', 'X', 'H', 'v', '<', '>']  # 自定义标记
    #使用不同的线段样式
    linestyles = [':','--','-','-','-.','-','--',':','-','--',':','-.']
    i =0
    for (model, recalls), marker in zip(data.items(), markers):  
        y = [recalls[str(xi)] for xi in x]  
        plt.plot(x, y, marker=marker,markersize=20, label=model.replace("qwen","Qwen"), linewidth=5, linestyle=linestyles[i])  
        i+=1

    # plt.title("Recall vs Threshold for Different LLMs", fontsize=16)  
    plt.xlabel("Recall Threshold", fontsize=35, fontweight='bold')  
    plt.ylabel("Hits@1", fontsize=35,  fontweight='bold')  
    plt.xticks(x, fontsize=30)
    plt.yticks(fontsize=30)  
    # plt.grid(True, linestyle='--', alpha=0.6)  
    # 顶端 三列 自定义位置
    plt.subplots_adjust(wspace=0.1, hspace=0.15)
    plt.legend(fontsize=22, loc='upper left', bbox_to_anchor=(0.03, 1.3),ncol=3, title_fontsize='25',labelspacing=0,columnspacing=0.5)
    # plt.tight_layout()  
    plt.subplots_adjust(top=0.8, left=0.2, right=0.95,bottom=0.2)

    plt.savefig("recall_vs_threshold_256.pdf")   
getjson()
getimage()