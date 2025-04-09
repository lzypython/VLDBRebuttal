import os
import json
def processJson(file):
    HR_0_0 =0
    HR_0_1 =0
    HR_1_0 =0
    HR_1_1 =0
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        eval_info = data["eval_info"]
        for item in eval_info:
            if item["HR"]==0 and item["HR2"]==0:
                HR_0_0 += 1
            elif item["HR"]==0 and item["HR2"]==1:
                HR_0_1 += 1
            elif item["HR"]==1 and item["HR2"]==0:
                HR_1_0 += 1
            elif item["HR"]==1 and item["HR2"]==1:
                HR_1_1 += 1
    return HR_0_0, HR_0_1, HR_1_0, HR_1_1
    # 返回[HR=0 HR2=0,
    #     HR=0 HR2=1,
    #      HR=1 HR2=0,
    #       HR=1 HR2=1]个数
    return []
def traverse_json_files(root_dir):
    # 遍历根目录下的所有文件和子目录
    All_HR_0_0 =0
    All_HR_0_1 =0
    All_HR_1_0 =0
    All_HR_1_1 =0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # 检查文件是否是 JSON 文件
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                print(f"Found JSON file: {file_path}")
                hr_0_0,hr_0_1,hr_1_0,hr_1_1 = processJson(file_path)
                All_HR_0_0+=hr_0_0
                All_HR_0_1+=hr_0_1
                All_HR_1_0+=hr_1_0
                All_HR_1_1+=hr_1_1
    print("HR_0_0",All_HR_0_0)
    print("HR_0_1",All_HR_0_1)
    print("HR_1_0",All_HR_1_0)
    print("HR_1_1",All_HR_1_1)
    acc_rate = (All_HR_0_0+All_HR_1_1)/(All_HR_0_0+All_HR_0_1+All_HR_1_0+All_HR_1_1)
    print("Accuracy rate：",round(acc_rate,4)*100,"%")
    return All_HR_0_0,All_HR_0_1,All_HR_1_0,All_HR_1_1
def drawImage(All_HR_0_0,All_HR_0_1,All_HR_1_0,All_HR_1_1):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import confusion_matrix

    # 定义混淆矩阵的值
    conf_matrix = np.array([[All_HR_0_0, All_HR_1_0],
                            [All_HR_0_1, All_HR_1_1]])

    # 绘制混淆矩阵
    plt.figure(figsize=(24, 6))
    sns.set(font_scale=3)  # 设置字体大小
    # 设置xtick和ytick的字体大小
    plt.xticks(fontsize=30,fontweight='bold')
    plt.yticks(fontsize=30,fontweight='bold')
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Hits@1_0', 'Hits@1_1'], 
                yticklabels=['Judge@1_0', 'Judge@1_1'])

    # 添加标题和标签
    # plt.title('Confusion Matrix')
    # 加粗
    plt.xlabel('Hits@1',fontsize=46,fontweight='bold')
    plt.ylabel('Judge@1',fontsize=46,fontweight='bold')

    # 显示图形
    # plt.show()
    plt.savefig("Hits@1_Judge@1_confusionMatrix.pdf",format="pdf",bbox_inches='tight')
# 指定根目录
root_directory = '/back-up/gzy/dataset/VLDB/Instance/Judgement/CWQ'

# 开始遍历
HR_0_0,HR_0_1,HR_1_0,HR_1_1 = traverse_json_files(root_directory)
drawImage(HR_0_0,HR_0_1,HR_1_0,HR_1_1)