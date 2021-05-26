import pandas as pd
import numpy as np
import datetime as dt
import sys
import math

def Preprocess(excelPath, by):# by == 0: ascending, by == 1: descending

    xls = pd.ExcelFile(excelPath)
    products = pd.read_excel(xls, sheet_name=None)
    productUsed = {}
    for productName in products:
        productUsed[productName] = products[productName].columns[2]
    products = pd.read_excel(xls, sheet_name=None, skiprows=1)
    final = pd.DataFrame(columns=["orderIndex", "carIndex", "phaseIndex",
                                    "stageOne", "stageTwo", "stageThree",
                                    "cleanTime", "phaseBefore",
                                    "carTotal", "orderTotal"])


    orderIndex = 1
    for productName in list(products.keys()):
        # print(productName, productUsed[productName])
        tempIndex = 0
        temp = pd.DataFrame(columns=["orderIndex", "carIndex", "phaseIndex",
                                    "stageOne", "stageTwo", "stageThree",
                                    "cleanTime", "phaseBefore",
                                    "carTotal", "orderTotal"])
        products[productName]["是否佔機台"] = products[productName]["是否佔機台"] == "是"
        n = products[productName].shape[0]
        stage = 1
        phaseIndex = 1
        carIndex = 1
        stageOne = 0
        stageTwo = 0
        stageThree = 0
        cleanTime = 0
        phaseBefore = 0
        carTotal = products[productName]["時間"].sum()
        orderTotal = productUsed[productName] * carTotal
        for i in range(n):
            if (products[productName]["是否佔機台"][i] or products[productName]["時間"][i] < 30) and products[productName]["製程"][i] != "清潔":
                if products[productName]["製程"][i] == "煮" and stage == 1:
                    stageOne += products[productName]["時間"][i]
                elif products[productName]["製程"][i] == "煮" and stage == 2:
                    stageThree += products[productName]["時間"][i]
                elif products[productName]["製程"][i] != "煮":
                    if stage != 2:
                        stage = 2
                    stageTwo += products[productName]["時間"][i]
                    stageTwo += stageThree
                    stageThree = 0
                
                if i == (n-1):
                    temp.loc[tempIndex] = [orderIndex, carIndex, phaseIndex,
                                        stageOne, stageTwo, stageThree,
                                        cleanTime, phaseBefore,
                                        carTotal, orderTotal]
            elif not products[productName]["是否佔機台"][i]:
                if products[productName]["製程"][i] == "清潔":
                    cleanTime = products[productName]["時間"][i]
                temp.loc[tempIndex] = [orderIndex, carIndex, phaseIndex,
                                    stageOne, stageTwo, stageThree,
                                    cleanTime, phaseBefore,
                                    carTotal, orderTotal]
                tempIndex += 1
                if i == (n-1):
                    continue

                stage = 1
                phaseIndex = 2
                stageOne = 0
                stageTwo = 0
                stageThree = 0
                cleanTime = 0
                phaseBefore = products[productName]["時間"][i]
            
        temp = pd.DataFrame(np.repeat(temp.values, productUsed[productName], axis=0), columns=temp.columns)
        carIndex = 2
        for j in range(1, temp.shape[0]):
            if temp.at[j, 'phaseIndex'] != temp.at[j-1, 'phaseIndex']:
                carIndex = 1
            temp.at[j, 'carIndex'] = carIndex
            carIndex += 1
        # display(temp)
        final = pd.concat([final, temp])
        orderIndex += 1
    if by == 0:
        final = final.sort_values(['carTotal', 'carIndex', 'phaseIndex'],
                                 ascending=[True, True, True]).reset_index(drop = True)
    elif by == 1:
        final = final.sort_values(['carTotal', 'carIndex', 'phaseIndex'],
                                 ascending=[False, True, True]).reset_index(drop = True)
    # print("final")
    # display(final)
    return final

def Apply(excelPath, num_of_machineNormal = 4, start_time_list = [0, 0, 0, 0, 0]):
    from .our_alg import WHILE, StageTwoFirst, MachineOneInsert, StageTwoFirstInsert

    # read excel
    xls = pd.ExcelFile(excelPath)
    products = pd.read_excel(xls, sheet_name=None, skiprows=1)
    productsName = list(products.keys())
    ascend = Preprocess(excelPath, 0)
    descend = Preprocess(excelPath, 1)

    # apply all algorithms
    all_algor = []

    try:
        WHILE_a = WHILE(ascend, num_of_machineNormal, start_time_list) # ascending
        all_algor.append((WHILE_a, WHILE_a["endTime"].max()))
    except:
        pass

    try:
        WHILE_d = WHILE(descend, num_of_machineNormal, start_time_list) # descending
        all_algor.append((WHILE_d, WHILE_d["endTime"].max()))
    except:
        pass

    try:
        STFI_a = StageTwoFirstInsert(ascend, num_of_machineNormal, start_time_list) # ascending
        all_algor.append((STFI_a, STFI_a["endTime"].max()))
    except:
        pass

    try:
        STFI_d = StageTwoFirstInsert(descend, num_of_machineNormal, start_time_list) # desscending
        all_algor.append((STFI_d, STFI_d["endTime"].max()))
    except:
        pass

    try:
        STF_a = StageTwoFirst(ascend, num_of_machineNormal, start_time_list) # ascending
        all_algor.append((STF_a, STF_a["endTime"].max()))
    except:
        pass

    try:
        STF_d = StageTwoFirst(descend, num_of_machineNormal, start_time_list) # desscending
        all_algor.append((STF_d, STF_d["endTime"].max()))
    except:
        pass

    for OSOMO in [True, False]:
        model = MachineOneInsert(ascend, num_of_machineNormal, OSOMO, start_time_list)
        for method in ['carTotal', 'orderTotal']:
            for method_ascending in [True, False]:
                for start_with_shortest_stageOne in [True, False]:
                    try:
                        result = model.schedule(method, method_ascending, start_with_shortest_stageOne)
                        all_algor.append((result, result["endTime"].max()))
                    except:
                        pass

    all_algor = sorted(all_algor, key=lambda x: x[1])

    # concat with raw data
    results = []
    for algor in all_algor[0:3]:
        newIndex = 0
        newDf = pd.DataFrame(columns=["機台", "產品", "車", "製程", "溫度", "程式步驟", "備註", "開始時間", "結束時間"])
        nowDf = algor[0].sort_values(by=['orderIndex', 'carIndex', 'phaseIndex', 'stage']).reset_index(drop = True).copy()
        lastJ = 0
        for i in range(len(nowDf)):
            nowRow = nowDf.iloc[i]
            machine = str(int(nowRow["machineIndex"]))
            order = productsName[int(nowRow["orderIndex"]) - 1]
            car = str(int(nowRow["carIndex"]))
            startTime = nowRow["startTime"]
            endTime = nowRow["endTime"]

            nowProduct = products[order]
            lastStart = startTime
            

            for j in range(lastJ, len(nowProduct)):
                process = nowProduct.iloc[j]["製程"]
                temperature = nowProduct.iloc[j]["溫度"]
                step = nowProduct.iloc[j]["程式步驟"]
                remark = nowProduct.iloc[j]["備註"]
                start = lastStart
                end = start + nowProduct.iloc[j]["時間"]
                lastStart = end

                if math.isnan(temperature):
                    newDf.loc[newIndex] = ["0", order, car,
                                            process, temperature,
                                            step, remark, start, end]
                else:
                    newDf.loc[newIndex] = [machine, order, car,
                                            process, temperature,
                                            step, remark, start, end]
                newIndex += 1
                if end == endTime:
                    if i != (len(nowDf) - 1):
                        if nowDf.iloc[i]["orderIndex"] == nowDf.iloc[i+1]["orderIndex"] and nowDf.iloc[i]["carIndex"] == nowDf.iloc[i+1]["carIndex"]:
                            if nowDf.iloc[i]["phaseIndex"] != nowDf.iloc[i+1]["phaseIndex"]:
                                j += 1
                                process = nowProduct.iloc[j]["製程"]
                                temperature = nowProduct.iloc[j]["溫度"]
                                step = nowProduct.iloc[j]["程式步驟"]
                                remark = nowProduct.iloc[j]["備註"]
                                start = lastStart
                                end = start + nowProduct.iloc[j]["時間"]
                                newDf.loc[newIndex] = ["0", order, car,
                                                        process, temperature,
                                                        step, remark, start, end]
                                newIndex += 1
                    if j == len(nowProduct)-1:
                        lastJ = 0
                    else:
                        lastJ = j+1
                    break
        results.append(newDf)
                
    return results

def Save(resultDf, location, powerTime = dt.time(7,0,0)):

    result = resultDf.copy()
    result["機台"] = "機台" + result["機台"]
    result["機台"] = result["機台"].replace("機台0", "機台外")
    result["車"] = "第" + result["車"] + "車"

    powerTime = dt.datetime.combine(dt.datetime.min, powerTime) - dt.datetime.min
    result["開始時間"] = (result["開始時間"].astype(int) // 60).astype(str)+":"+(result["開始時間"].astype(int) % 60).astype(str)
    result["開始時間"] = pd.to_datetime(result["開始時間"], format="%H:%M")
    result["開始時間"] = (result["開始時間"] + powerTime).dt.time
    result["結束時間"] = (result["結束時間"].astype(int) // 60).astype(str)+":"+(result["結束時間"].astype(int) % 60).astype(str)
    result["結束時間"] = pd.to_datetime(result["結束時間"], format="%H:%M")
    result["結束時間"] = (result["結束時間"] + powerTime).dt.time

    machines = sorted(result["機台"].unique().tolist())
    writer = pd.ExcelWriter(location + '機台排程資訊.xlsx', engine='xlsxwriter')
    for machine in machines:
        # print(machine)
        temp = result[result["機台"] == machine].drop(columns = ["機台"]).sort_values(by = ["開始時間"])
        if machine == "機台0":
            machine = "機台外"
        temp.to_excel(writer, sheet_name=machine, index = False, encoding = 'utf-8')
    writer.save()

    orders = sorted(result["產品"].unique().tolist())
    writer = pd.ExcelWriter(location + '產品排程資訊.xlsx', engine='xlsxwriter')
    for order in orders:
        # print(order)
        temp = result[result["產品"] == order].drop(columns = ["產品"]).sort_values(by = ["車","開始時間"])
        temp = temp[["車", "機台", "製程", "溫度", "程式步驟", "備註", "開始時間", "結束時間"]]
        temp.to_excel(writer, sheet_name=order, index = False, encoding = 'utf-8')
    writer.save()