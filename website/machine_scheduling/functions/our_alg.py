import numpy as np
import pandas as pd


def WHILE(data , num_of_machineNormal , start_time_list) :
    import pandas as pd
    import numpy as np
    data.to_csv("pc_temp.csv" , index=False)
    
    df = pd.read_csv("pc_temp.csv" , encoding='utf-8')
    for i , r in df.iterrows() :
        if(r['phaseBefore'] != 0) :
            for ii , rr in df.iterrows() :
                if(rr['orderIndex'] == r['orderIndex'] and rr['carIndex'] == r['carIndex'] and rr['phaseIndex'] == r['phaseIndex'] - 1) :
                    rr['phaseBefore'] = r['phaseBefore']
                    r['phaseBefore'] = 0
    
    df.columns = ['orderIndex', 'carIndex' , 'phaseIndex' , 'stageOne' , 'stageTwo' , 'stageThree' , 'cleanTime' , 'phaseAfter' , 'carTotal' , 'orderTotal']
    df_detail = df
    temp = [-1] * len(df_detail)
    df_detail['canStartTime'] = temp
    df_detail['changeNum'] = temp
    df_detail['completionTime'] = temp
    # print(df_detail)
    onlyMachineNum = 1
    # allMachineNum = 4
    allMachineNum = num_of_machineNormal
    onlyMachine = []
    for i in range(onlyMachineNum) :
        onlyMachine.append(pd.DataFrame([[0 , 0 , 0 , 0 , 0 , 0 , start_time_list[0]]] , columns = ['machineIndex' , 'orderIndex' , 'carIndex' ,'phaseIndex', 'stage' , 'startTime' , 'endTime']))
    allMachine = []
    for i in range(allMachineNum) :
        allMachine.append(pd.DataFrame([[i , 0 , 0 , 0 , 0 , 0 , start_time_list[i+1] ]] , columns = ['machineIndex' , 'orderIndex' , 'carIndex' ,'phaseIndex', 'stage' , 'startTime' , 'endTime']))
    
    maxPhaseNum = 5
    count = len(df_detail)
    while (count > 0) :
        rowIndex = -1
        row = pd.Series([300,300,300,300,300,300,300,300,300,300,300,300,300] , index = ['orderIndex' , 'phaseIndex' , 'carIndex' , 'stageOne' , 'stageTwo' , 'stageThree' , 'cleanTime' , 'phaseAfter' , 'carTotal' , 'orderTotal' , 'canStartTime' , 'changeNum' , 'completionTime'])
        machineTimeList = []
        for i in range(onlyMachineNum) :
            machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
        for i in range(allMachineNum) :
            machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
        for i , r in df_detail.iterrows() :
            if(r['canStartTime'] < 100000 and r['completionTime'] <= 0) :
                can = False
                for j in range(len(machineTimeList)) :
                    if(r['canStartTime'] <= machineTimeList[j]) :
                        can = True
                if(can == True) :
                    rowIndex = i
                    row = r
                    break
        if(rowIndex == -1) :
            for i , r in df_detail.iterrows() :
                if(r['canStartTime'] < 100000 and r['completionTime'] <= 0) :
                    rowIndex = i
                    row = r
                    break
            change = -1
            stage = -1
            lastFive = False
            if(count <= 5) :
                lastFive = True
            
            count = count - 1
            # Type One
            if (row['stageOne'] != 0 and row['stageTwo'] == 0 and row['stageThree'] == 0) :
                machineTimeList = []
                for i in range(onlyMachineNum) :
                    machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
                for i in range(allMachineNum) :
                    machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
                idx = -1
                val = 100000
                for i in range(len(machineTimeList)) :
                    if(machineTimeList[i] < val and machineTimeList[i] > row['canStartTime']) :
                        idx = i
                        val = machineTimeList[i]
                if(idx == -1) :
                    val = 0
                    for i in range(len(machineTimeList)) :
                        if(machineTimeList[i] > val) :
                            idx = i
                            val = machineTimeList[i]
                    val = row['canStartTime']
                stage = 1
                s = pd.Series([idx , row['orderIndex'] , row['carIndex'] , row['phaseIndex'],stage , val , val + row['stageOne'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                if idx == 0 :
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    idx = idx - 1
                    allMachine[idx] = allMachine[idx].append(s , ignore_index = True)

                row['canStartTime'] = 100000
                row['changeNum'] = 0
                row['completionTime'] = val + row['stageOne'] + row['phaseAfter']
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
                
            # Type Two
            elif (row['stageOne'] != 0 and row['stageTwo'] != 0 and row['stageThree'] == 0) :
                # Stage One
                machineTimeList = []
                for i in range(onlyMachineNum) :
                    machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
                for i in range(allMachineNum) :
                    machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
                idx = -1
                val = 100000
                for i in range(len(machineTimeList)) :
                    if(machineTimeList[i] < val and machineTimeList[i] > row['canStartTime']) :
                        idx = i
                        val = machineTimeList[i]
                if(idx == -1) :
                    val = 0
                    for i in range(len(machineTimeList)) :
                        if(machineTimeList[i] > val) :
                            idx = i
                            val = machineTimeList[i]
                    val = row['canStartTime']
                stage = 1
                s = pd.Series([idx , row['orderIndex'] , row['carIndex'] , row['phaseIndex'],stage , val , val + row['stageOne'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                idx = idx - 1
                if idx == -1 :
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    allMachine[idx] = allMachine[idx].append(s , ignore_index = True)
                
                # Stage Two
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'] - (val + row['stageOne'] + row['cleanTime']))
                if(lastFive) :
                    val2 , idx2 = min((val , idx) for (idx , val) in enumerate(machineTimeList2))
                if(not lastFive) :
                    val2 , idx2 = max((val , idx) for (idx , val) in enumerate(machineTimeList2))
                val2 = val + row['stageOne'] 
                if (idx != -1) :
                    idx2 = idx        
                if(val2 < allMachine[idx2].iloc[-1]['endTime']) :
                    val2 = allMachine[idx2].iloc[-1]['endTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                change = 0
                if idx != idx2 :
                    change = 1
                row['completionTime'] = val2 + row['stageTwo'] + row['phaseAfter']
                row['changeNum'] = change
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
            # Type Three
            elif (row['stageOne'] != 0 and row['stageTwo'] != 0 and row['stageThree'] != 0) :
                # Stage One
                machineTimeList = []
                for i in range(onlyMachineNum) :
                    machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
                for i in range(allMachineNum) :
                    machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
                idx = -1
                val = 100000
                for i in range(len(machineTimeList)) :
                    if(machineTimeList[i] < val and machineTimeList[i] > row['canStartTime']) :
                        idx = i
                        val = machineTimeList[i]
                if(idx == -1) :
                    val = 0
                    for i in range(len(machineTimeList)) :
                        if(machineTimeList[i] > val) :
                            idx = i
                            val = machineTimeList[i]
                    val = row['canStartTime']
                stage = 1
                s = pd.Series([idx , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val , val + row['stageOne'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                idx = idx - 1
                if idx == -1 :
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    allMachine[idx] = allMachine[idx].append(s , ignore_index = True)
                
                # Stage Two
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'] - (val + row['stageOne'] + row['cleanTime']))
                if(lastFive) :
                    val2 , idx2 = min((val , idx) for (idx , val) in enumerate(machineTimeList2))
                if(not lastFive) :
                    val2 , idx2 = max((val , idx) for (idx , val) in enumerate(machineTimeList2))
                val2 = val + row['stageOne'] 
                if (idx != -1) :
                    idx2 = idx        
                if(val2 < allMachine[idx2].iloc[-1]['endTime']) :
                    val2 = allMachine[idx2].iloc[-1]['endTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                change = 0
                if idx != idx2 :
                    change = 1
                
                # Stage Three
                if change == 0 :
                    idx3 = -1
                    val3 = val2 + row['stageTwo'] + row['cleanTime']
                    if(lastFive) :
                        idx3 = idx2
                    stage = 3
                    if idx3 == -1 : 
                        if(onlyMachine[0].iloc[-1]['endTime'] > val3):
                            val3 = onlyMachine[0].iloc[-1]['endTime']
                        s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                        onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True) 
                    else : 
                        s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                        allMachine[idx3] = allMachine[idx3].append(s , ignore_index = True) 
                    if idx3 != idx2 :
                        change = 1
                    row['completionTime'] = val3 + row['stageThree'] + row['phaseAfter']
                    row['changeNum'] = change
                    for k in range(1 , maxPhaseNum + 1) :
                        if(row['phaseIndex'] == k) :
                            after = False
                            for ii , rr in df_detail.iterrows() :
                                if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                    after = True
                                    rr['canStartTime'] = row['completionTime']

                elif change == 1 :
                    idx3 = idx2
                    val3 = allMachine[idx3].iloc[-1]['endTime']
                    stage = 3
                    s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                    allMachine[idx3] = allMachine[idx3].append(s , ignore_index = True)

                    row['completionTime'] = val3 + row['stageThree'] + row['phaseAfter']
                    row['changeNum'] = change
                    for k in range(1 , maxPhaseNum + 1) :
                        if(row['phaseIndex'] == k) :
                            after = False
                            for ii , rr in df_detail.iterrows() :
                                if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                    after = True
                                    rr['canStartTime'] = row['completionTime']
            # Type Four
            elif (row['stageOne'] == 0 and row['stageTwo'] != 0 and row['stageThree'] == 0) :
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'])
                idx2 = -1
                val2 = 100000
                for i in range(len(machineTimeList2)) :
                    if(machineTimeList2[i] < val2 and machineTimeList2[i] > row['canStartTime']) :
                        idx2 = i
                        val2 = machineTimeList2[i]
                if(idx2 == -1) :
                    val2 = 0
                    for i in range(len(machineTimeList2)) :
                        if(machineTimeList2[i] > val) :
                            idx2 = i
                            val2 = machineTimeList2[i]
                    val2 = row['canStartTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                change = 0
                row['completionTime'] = val2 + row['stageTwo'] + row['phaseAfter']
                row['changeNum'] = change
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
            # Type Five
            elif (row['stageOne'] == 0 and row['stageTwo'] != 0 and row['stageThree'] != 0) :
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'])
                idx2 = -1
                val2 = 100000
                for i in range(len(machineTimeList2)) :
                    if(machineTimeList2[i] < val2 and machineTimeList2[i] > row['canStartTime']) :
                        idx2 = i
                        val2 = machineTimeList2[i]
                if(idx2 == -1) :
                    val2 = 0
                    for i in range(len(machineTimeList2)) :
                        if(machineTimeList2[i] > val) :
                            idx2 = i
                            val2 = machineTimeList2[i]
                    val2 = row['canStartTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                idx3 = -1
                val3 = val2 + row['stageTwo'] + row['cleanTime']

                if(lastFive) :
                    idx3 = idx2
                stage = 3
                if idx3 == -1 :
                    if(onlyMachine[0].iloc[-1]['endTime'] > val3):
                        val3 = onlyMachine[0].iloc[-1]['endTime']
                    s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                    allMachine[idx3] = allMachine[idx3].append(s , ignore_index = True)
                change = 0
                if idx3 != idx2 :
                    change = 1
                row['completionTime'] = val3 + row['stageThree'] + row['phaseAfter']
                row['changeNum'] = change
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
            else :
                print("Wrong Input!")


        else :
            change = -1
            stage = -1
            lastFive = False
            if(count <= 5) :
                lastFive = True
            count = count - 1
            # Type One
            if (row['stageOne'] != 0 and row['stageTwo'] == 0 and row['stageThree'] == 0) :
                machineTimeList = []
                for i in range(onlyMachineNum) :
                    machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
                for i in range(allMachineNum) :
                    machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
                idx = -1
                val = 100000
                for i in range(len(machineTimeList)) :
                    if(machineTimeList[i] < val and machineTimeList[i] > row['canStartTime']) :
                        idx = i
                        val = machineTimeList[i]
                if(idx == -1) :
                    val = 0
                    for i in range(len(machineTimeList)) :
                        if(machineTimeList[i] > val) :
                            idx = i
                            val = machineTimeList[i]
                    val = row['canStartTime']
                stage = 1
                s = pd.Series([idx , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val , val + row['stageOne'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex', 'phaseIndex' , 'stage' , 'startTime' , 'endTime'])
                if idx == 0 :
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    idx = idx - 1
                    allMachine[idx] = allMachine[idx].append(s , ignore_index = True)

                row['canStartTime'] = 100000
                row['changeNum'] = 0
                row['completionTime'] = val + row['stageOne'] + row['phaseAfter']
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
                
            # Type Two
            elif (row['stageOne'] != 0 and row['stageTwo'] != 0 and row['stageThree'] == 0) :
                # Stage One
                machineTimeList = []
                for i in range(onlyMachineNum) :
                    machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
                for i in range(allMachineNum) :
                    machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
                idx = -1
                val = 100000
                for i in range(len(machineTimeList)) :
                    if(machineTimeList[i] < val and machineTimeList[i] > row['canStartTime']) :
                        idx = i
                        val = machineTimeList[i]
                if(idx == -1) :
                    val = 0
                    for i in range(len(machineTimeList)) :
                        if(machineTimeList[i] > val) :
                            idx = i
                            val = machineTimeList[i]
                    val = row['canStartTime']
                stage = 1
                s = pd.Series([idx , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val , val + row['stageOne'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex','stage' , 'startTime' , 'endTime'])
                idx = idx - 1
                if idx == -1 :
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    allMachine[idx] = allMachine[idx].append(s , ignore_index = True)
                
                # Stage Two
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'] - (val + row['stageOne'] + row['cleanTime']))
                if(lastFive) :
                    val2 , idx2 = min((val , idx) for (idx , val) in enumerate(machineTimeList2))
                if(not lastFive) :
                    val2 , idx2 = max((val , idx) for (idx , val) in enumerate(machineTimeList2))
                val2 = val + row['stageOne'] 
                if (idx != -1) :
                    idx2 = idx        
                if(val2 < allMachine[idx2].iloc[-1]['endTime']) :
                    val2 = allMachine[idx2].iloc[-1]['endTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                change = 0
                if idx != idx2 :
                    change = 1
                row['completionTime'] = val2 + row['stageTwo'] + row['phaseAfter']
                row['changeNum'] = change
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
            # Type Three
            elif (row['stageOne'] != 0 and row['stageTwo'] != 0 and row['stageThree'] != 0) :
                # Stage One
                machineTimeList = []
                for i in range(onlyMachineNum) :
                    machineTimeList.append(onlyMachine[i].iloc[-1]['endTime'])
                for i in range(allMachineNum) :
                    machineTimeList.append(allMachine[i].iloc[-1]['endTime'])
                idx = -1
                val = 100000
                for i in range(len(machineTimeList)) :
                    if(machineTimeList[i] < val and machineTimeList[i] > row['canStartTime']) :
                        idx = i
                        val = machineTimeList[i]
                if(idx == -1) :
                    val = 0
                    for i in range(len(machineTimeList)) :
                        if(machineTimeList[i] > val) :
                            idx = i
                            val = machineTimeList[i]
                    val = row['canStartTime']
                stage = 1
                s = pd.Series([idx , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val , val + row['stageOne'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                idx = idx - 1
                if idx == -1 :
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    allMachine[idx] = allMachine[idx].append(s , ignore_index = True)
                
                # Stage Two
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'] - (val + row['stageOne'] + row['cleanTime']))
                if(lastFive) :
                    val2 , idx2 = min((val , idx) for (idx , val) in enumerate(machineTimeList2))
                if(not lastFive) :
                    val2 , idx2 = max((val , idx) for (idx , val) in enumerate(machineTimeList2))
                val2 = val + row['stageOne'] 
                if (idx != -1) :
                    idx2 = idx        
                if(val2 < allMachine[idx2].iloc[-1]['endTime']) :
                    val2 = allMachine[idx2].iloc[-1]['endTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex', 'phaseIndex' , 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                change = 0
                if idx != idx2 :
                    change = 1
                
                # Stage Three
                if change == 0 :
                    idx3 = -1
                    val3 = val2 + row['stageTwo'] + row['cleanTime']
                    if(lastFive) :
                        idx3 = idx2
                    stage = 3
                    if idx3 == -1 : 
                        if(onlyMachine[0].iloc[-1]['endTime'] > val3):
                            val3 = onlyMachine[0].iloc[-1]['endTime']
                        s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                        onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True) 
                    else : 
                        s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'], row['phaseIndex'] , stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                        allMachine[idx3] = allMachine[idx3].append(s , ignore_index = True) 
                    if idx3 != idx2 :
                        change = 1
                    row['completionTime'] = val3 + row['stageThree'] + row['phaseAfter']
                    row['changeNum'] = change
                    for k in range(1 , maxPhaseNum + 1) :
                        if(row['phaseIndex'] == k) :
                            after = False
                            for ii , rr in df_detail.iterrows() :
                                if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                    after = True
                                    rr['canStartTime'] = row['completionTime']

                elif change == 1 :
                    idx3 = idx2
                    val3 = allMachine[idx3].iloc[-1]['endTime']
                    stage = 3
                    s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'], row['phaseIndex'], stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                    allMachine[idx3] = allMachine[idx3].append(s , ignore_index = True)

                    row['completionTime'] = val3 + row['stageThree'] + row['phaseAfter']
                    row['changeNum'] = change
                    for k in range(1 , maxPhaseNum + 1) :
                        if(row['phaseIndex'] == k) :
                            after = False
                            for ii , rr in df_detail.iterrows() :
                                if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                    after = True
                                    rr['canStartTime'] = row['completionTime']
            # Type Four
            elif (row['stageOne'] == 0 and row['stageTwo'] != 0 and row['stageThree'] == 0) :
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'])
                idx2 = -1
                val2 = 100000
                for i in range(len(machineTimeList2)) :
                    if(machineTimeList2[i] < val2 and machineTimeList2[i] > row['canStartTime']) :
                        idx2 = i
                        val2 = machineTimeList2[i]
                if(idx2 == -1) :
                    val2 = 0
                    for i in range(len(machineTimeList2)) :
                        if(machineTimeList2[i] > val) :
                            idx2 = i
                            val2 = machineTimeList2[i]
                    val2 = row['canStartTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                change = 0
                row['completionTime'] = val2 + row['stageTwo'] + row['phaseAfter']
                row['changeNum'] = change
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
            # Type Five
            elif (row['stageOne'] == 0 and row['stageTwo'] != 0 and row['stageThree'] != 0) :
                machineTimeList2 = []
                for i in range(allMachineNum) :
                    machineTimeList2.append(allMachine[i].iloc[-1]['endTime'])
                idx2 = -1
                val2 = 100000
                for i in range(len(machineTimeList2)) :
                    if(machineTimeList2[i] < val2 and machineTimeList2[i] > row['canStartTime']) :
                        idx2 = i
                        val2 = machineTimeList2[i]
                if(idx2 == -1) :
                    val2 = 0
                    for i in range(len(machineTimeList2)) :
                        if(machineTimeList2[i] > val) :
                            idx2 = i
                            val2 = machineTimeList2[i]
                    val2 = row['canStartTime']
                stage = 2
                s = pd.Series([idx2 + 1 , row['orderIndex'] , row['carIndex'] , row['phaseIndex'], stage , val2 , val2 + row['stageTwo'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex', 'phaseIndex' , 'stage' , 'startTime' , 'endTime'])
                allMachine[idx2] = allMachine[idx2].append(s , ignore_index = True)

                idx3 = -1
                val3 = val2 + row['stageTwo'] + row['cleanTime']

                if(lastFive) :
                    idx3 = idx2
                stage = 3
                if idx3 == -1 :
                    if(onlyMachine[0].iloc[-1]['endTime'] > val3):
                        val3 = onlyMachine[0].iloc[-1]['endTime']
                    s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'], row['phaseIndex'] , stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                    onlyMachine[0] = onlyMachine[0].append(s , ignore_index = True)
                else :
                    s = pd.Series([idx3 + 1 , row['orderIndex'] , row['carIndex'], row['phaseIndex'] , stage , val3 , val3 + row['stageThree'] + row['cleanTime']] , index = ['machineIndex' , 'orderIndex' , 'carIndex' , 'phaseIndex', 'stage' , 'startTime' , 'endTime'])
                    allMachine[idx3] = allMachine[idx3].append(s , ignore_index = True)
                change = 0
                if idx3 != idx2 :
                    change = 1
                row['completionTime'] = val3 + row['stageThree'] + row['phaseAfter']
                row['changeNum'] = change
                for k in range(1 , maxPhaseNum + 1) :
                    if(row['phaseIndex'] == k) :
                        after = False
                        for ii , rr in df_detail.iterrows() :
                            if(rr['orderIndex'] == row['orderIndex'] and rr['carIndex'] == row['carIndex'] and rr['phaseIndex'] == k + 1) :
                                after = True
                                rr['canStartTime'] = row['completionTime']
            else :
                print("Wrong Input!")
    dfList = []
    for i in range(onlyMachineNum) :
        dfList.append(onlyMachine[i])
    for i in range(allMachineNum) :
        dfList.append(allMachine[i])
    result = pd.concat(dfList)
    result = result[result.stage != 0]
    result = result.reset_index(drop = True)
    for i , r in result.iterrows() :
        r['machineIndex'] = r['machineIndex'] + 1
    
    import os
    os.remove("pc_temp.csv")
    return result



    import numpy as np
    import pandas as pd

    def overlap_back(machineBoil, start, end):
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = b
                end = b + period
        
        return start, end
    

    def overlap_front(machineBoil, start, end):
        
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        machineBoil.reverse()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = a - period
                end = a
        
        return start, end


    
    order = data.copy()
    order = order.rename(columns={"phaseIndex": "phase"})
    order['to_fill'] = False

    machineBoil = []
    machineNormal = []
    for i in range(num_of_machineNormal):
        machineNormal.append(0)

    look_up = pd.DataFrame(columns = ['orderIndex', 'carIndex', 'phase', 'finTime'])

    result = pd.DataFrame(columns = ['machineIndex', 'orderIndex', 'carIndex',                                           'phaseIndex', 'stage', 'startTime', 'endTime'])

    buffer = []

    totalOrderNum = order.shape[0]

    for i in range(totalOrderNum):
        order_temp = order.loc[i]
        if order_temp['phase'] > 1:
            s = pd.Series({'orderIndex': order_temp['orderIndex'],
                           'carIndex': order_temp['carIndex'], 
                           'phase': order_temp['phase'] - 1, 'finTime': -1})
            look_up = look_up.append(s, ignore_index = True)
            
            for j in range(totalOrderNum):
                order_temp_2 = order.loc[j]
                if order_temp_2['orderIndex'] == order_temp['orderIndex'] :
                    if order_temp_2['carIndex'] == order_temp['carIndex'] :
                        if order_temp_2['phase'] == order_temp['phase'] - 1 :
                            order.loc[j, 'to_fill'] = True

    # print('\n\n##########\n\n', order, '\n\n##########\n\n')


    
    i = 0
    last_from_buffer = False
    while i < totalOrderNum:
        
        if i % num_of_machineNormal == 1 and len(buffer) != 0                                  and last_from_buffer == False:

            order_temp = buffer[0]
            del buffer[0]
            last_from_buffer = True
        
        else:
            order_temp = order.loc[i]
            last_from_buffer = False
            i += 1
    
            
        one = order_temp['stageOne']
        two = order_temp['stageTwo']
        three = order_temp['stageThree']
        phase = order_temp['phase']
        phaseBefore = order_temp['phaseBefore']

        if three != 0:
            three += order_temp['cleanTime']
        else:
            if two != 0:
                two += order_temp['cleanTime']
            else:
                one += order_temp['cleanTime']

        need = one + two + three

        index_temp = machineNormal.index(min(machineNormal))
        cur_max = max(machineNormal)

        if (one != 0) and (three != 0):  ## 有第一、二、三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            new_s_b_2, new_e_b_2 = overlap_front(machineBoil, s_b_2, e_b_2)

            fit_2 = True
            if (new_s_b_2 < 0) or (new_e_b_2 < 0) or (abs(new_s_b_2 - s_b_2) > one):
                fit_2 = False

            if fit_2 == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b_2                                   or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer :
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b_2, new_e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three         

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 
                                'startTime': new_s_b_2,
                                'endTime':new_e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)


                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3
                                

            else: ## 一塞不進
                
                s_b = machineNormal[index_temp] + (need - three)
                e_b = machineNormal[index_temp] + need

                new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)

                fit_1 = True
                if (new_s_b < 0) or (new_e_b < 0) or ( abs(new_s_b - s_b) > three) :
                    fit_1 = False

                if fit_1 == True : ## 一塞不進、三塞得進
                    
                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += (need - three)
                        t_end = machineNormal[index_temp]
                        machineBoil.append( (new_s_b, new_e_b) )

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)
                        

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': 0, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3,
                                    'startTime': new_s_b,
                                    'endTime': new_e_b})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex'] ==                                                         look_up_temp['orderIndex']                                                    and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = new_e_b
                                


                else: ## 一塞不進、三塞不進

                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += need
                        t_end = machineNormal[index_temp]

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two
                        s_3 = e_2
                        e_3 = e_2 + three

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 
                                    'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 
                                    'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3, 
                                    'startTime': s_3, 'endTime': e_3})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex']==                                                          look_up_temp['orderIndex']                                                     and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = e_3

                                
                   
            
        elif (one!= 0) and  (two == 0) and (three == 0): ## 只有第一階段

            s_b = 0
            e_b = one

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)
            # print('\n', new_s_b, new_e_b, '\n')
            fit = True
            if new_e_b > cur_max :
                fit = False

            if fit == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b                                      or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    machineBoil.append( (new_s_b, new_e_b) )
                    
                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': new_s_b,'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b

            else: ## 一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:  
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': t_start, 'endTime': t_end})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = t_end


        elif (one!= 0) and  (two != 0) and (three == 0): ## 只有第一、二階段，沒第三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            new_s_b_2, new_e_b_2 = overlap_front(machineBoil, s_b_2, e_b_2)

            fit_2 = True
            if (new_s_b_2 <0) or (new_e_b_2 < 0) or (abs(new_s_b_2 - s_b_2) > one) :
                fit_2 = False

            if fit_2 == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b_2                                   or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b_2, new_e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 
                                'startTime': new_s_b_2,
                                'endTime':new_e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime':e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2


            else: #一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)
                
                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s_1 = t_start
                    e_1 = t_start + one
                    s_2 = e_1
                    e_2 = s_2 + two
                
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)

                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2

        elif (one == 0) and (three != 0) : ## 沒有第一，只有第二、三階段

            s_b = machineNormal[index_temp] + (need - three)
            e_b = machineNormal[index_temp] + need

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)

            fit_1 = True
            if (new_s_b < 0) or (new_e_b < 0) or ( abs(new_s_b - s_b) > three ) :
                fit_1 = False
            
            if fit_1 == True : ## 三塞得進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - three)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b, new_e_b) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 
                                'startTime': new_s_b, 
                                'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b


            else: ## 三塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three
                                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3


        else: ## 只有第二階段

            Stmp = machineNormal[index_temp]
            to_buffer = False
            if phase > 1:
                for j in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[j]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                            to_buffer = True

            if to_buffer:
                buffer.append(order_temp)

            else:
                t_start = machineNormal[index_temp]
                machineNormal[index_temp] += need
                t_end = machineNormal[index_temp]

                s_2 = t_start
                e_2 = s_2 + two
            
                s = pd.Series({'machineIndex': index_temp + 1, 
                            'orderIndex': order_temp['orderIndex'],
                            'carIndex': order_temp['carIndex'], 
                            'phaseIndex': phase,
                            'stage': 2, 'startTime': s_2, 'endTime': e_2})
                result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_2


        
        ##  處理剩下的 buffer
        if i == totalOrderNum and len(buffer) != 0:

            # print('begin ', machineNormal)
            
            while len(buffer) != 0 :
                
                order_temp = buffer[0]
                del buffer[0]
                one = order_temp['stageOne']
                two = order_temp['stageTwo']
                three = order_temp['stageThree']
                phase = order_temp['phase']
                phaseBefore = order_temp['phaseBefore']

                if three != 0:
                    three += order_temp['cleanTime']
                else:
                    if two != 0:
                        two += order_temp['cleanTime']
                    else:
                        one += order_temp['cleanTime']

                need = one + two + three

                conti = False
                for k in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[k]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] != -1:
                            beginTime = look_up_temp['finTime'] + phaseBefore
                        else:
                            buffer.append(order_temp)
                            conti = True

                if conti == True:
                    continue

                mini = -1
                best_k = -1
                for k in range(len(machineNormal)):
                    if machineNormal[k] > mini and machineNormal[k] < beginTime:
                        mini = machineNormal[k]
                        best_k = k

                if best_k != -1:
                    mini = beginTime
                else:
                    mini = min(machineNormal)
                    best_k = machineNormal.index(min(machineNormal))

                machineNormal[best_k] = mini + need


                s_1 = mini
                e_1 = mini + one
                s_2 = e_1
                e_2 = s_2 + two
                s_3 = e_2
                e_3 = s_3 + three

                
                if one != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)
                
                if two != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                if three != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for k in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[k]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_3

                # print('put ', machineNormal)

    sep = []
    for i in range(num_of_machineNormal + 1):
        sep.append(result[result['machineIndex'] == i])


    last = []
    for i in sep:
        o = list(i['orderIndex'])[-1]
        c = list(i['carIndex'])[-1]
        
        temp = result[result['orderIndex'] == o]
        temp = temp[temp['carIndex'] == c]
        last.append(temp)


    for i in last[1:num_of_machineNormal + 1]:
        for j in i.index:
            if i.loc[j,'machineIndex'] == 0:
                result.loc[j,'machineIndex'] = list(i['machineIndex'])[0]


    result['machineIndex'] = result['machineIndex'] + 1



    return result


    import numpy as np
    import pandas as pd

    def overlap_back(machineBoil, start, end):
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = b
                end = b + period
        
        return start, end
    

    def overlap_front(machineBoil, start, end):
        
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        machineBoil.reverse()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = a - period
                end = a
        
        return start, end


    
    order = data.copy()
    order = order.rename(columns={"phaseIndex": "phase"})
    order['to_fill'] = False

    machineBoil = []
    machineNormal = []
    for i in range(num_of_machineNormal):
        machineNormal.append(start_time_list[i])

    look_up = pd.DataFrame(columns = ['orderIndex', 'carIndex', 'phase', 'finTime'])

    result = pd.DataFrame(columns = ['machineIndex', 'orderIndex', 'carIndex',                                           'phaseIndex', 'stage', 'startTime', 'endTime'])

    buffer = []

    totalOrderNum = order.shape[0]

    for i in range(totalOrderNum):
        order_temp = order.loc[i]
        if order_temp['phase'] > 1:
            s = pd.Series({'orderIndex': order_temp['orderIndex'],
                           'carIndex': order_temp['carIndex'], 
                           'phase': order_temp['phase'] - 1, 'finTime': -1})
            look_up = look_up.append(s, ignore_index = True)
            
            for j in range(totalOrderNum):
                order_temp_2 = order.loc[j]
                if order_temp_2['orderIndex'] == order_temp['orderIndex'] :
                    if order_temp_2['carIndex'] == order_temp['carIndex'] :
                        if order_temp_2['phase'] == order_temp['phase'] - 1 :
                            order.loc[j, 'to_fill'] = True

    # print('\n\n##########\n\n', order, '\n\n##########\n\n')


    
    i = 0
    last_from_buffer = False
    while i < totalOrderNum:
        
        if i % num_of_machineNormal == 1 and len(buffer) != 0                                  and last_from_buffer == False:

            order_temp = buffer[0]
            del buffer[0]
            last_from_buffer = True
        
        else:
            order_temp = order.loc[i]
            last_from_buffer = False
            i += 1
    
            
        one = order_temp['stageOne']
        two = order_temp['stageTwo']
        three = order_temp['stageThree']
        phase = order_temp['phase']
        phaseBefore = order_temp['phaseBefore']

        if three != 0:
            three += order_temp['cleanTime']
        else:
            if two != 0:
                two += order_temp['cleanTime']
            else:
                one += order_temp['cleanTime']

        need = one + two + three

        index_temp = machineNormal.index(min(machineNormal))
        cur_max = max(machineNormal)

        if (one != 0) and (three != 0):  ## 有第一、二、三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            new_s_b_2, new_e_b_2 = overlap_front(machineBoil, s_b_2, e_b_2)

            fit_2 = True
            if (new_s_b_2 < 0) or (new_e_b_2 < 0) or (abs(new_s_b_2 - s_b_2) > one):
                fit_2 = False

            if fit_2 == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b_2                                   or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer :
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b_2, new_e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three         

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 
                                'startTime': new_s_b_2,
                                'endTime':new_e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)


                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3
                                

            else: ## 一塞不進
                
                s_b = machineNormal[index_temp] + (need - three)
                e_b = machineNormal[index_temp] + need

                new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)

                fit_1 = True
                if (new_s_b < 0) or (new_e_b < 0) or ( abs(new_s_b - s_b) > three) :
                    fit_1 = False

                if fit_1 == True : ## 一塞不進、三塞得進
                    
                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += (need - three)
                        t_end = machineNormal[index_temp]
                        machineBoil.append( (new_s_b, new_e_b) )

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)
                        

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': 0, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3,
                                    'startTime': new_s_b,
                                    'endTime': new_e_b})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex'] ==                                                         look_up_temp['orderIndex']                                                    and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = new_e_b
                                


                else: ## 一塞不進、三塞不進

                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += need
                        t_end = machineNormal[index_temp]

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two
                        s_3 = e_2
                        e_3 = e_2 + three

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 
                                    'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 
                                    'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3, 
                                    'startTime': s_3, 'endTime': e_3})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex']==                                                          look_up_temp['orderIndex']                                                     and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = e_3

                                
                   
            
        elif (one!= 0) and  (two == 0) and (three == 0): ## 只有第一階段

            s_b = 0
            e_b = one

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)
            # print('\n', new_s_b, new_e_b, '\n')
            fit = True
            if new_e_b > cur_max :
                fit = False

            if fit == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b                                      or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    machineBoil.append( (new_s_b, new_e_b) )
                    
                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': new_s_b,'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b

            else: ## 一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:  
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': t_start, 'endTime': t_end})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = t_end


        elif (one!= 0) and  (two != 0) and (three == 0): ## 只有第一、二階段，沒第三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            new_s_b_2, new_e_b_2 = overlap_front(machineBoil, s_b_2, e_b_2)

            fit_2 = True
            if (new_s_b_2 <0) or (new_e_b_2 < 0) or (abs(new_s_b_2 - s_b_2) > one) :
                fit_2 = False

            if fit_2 == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b_2                                   or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b_2, new_e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 
                                'startTime': new_s_b_2,
                                'endTime':new_e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime':e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2


            else: #一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)
                
                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s_1 = t_start
                    e_1 = t_start + one
                    s_2 = e_1
                    e_2 = s_2 + two
                
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)

                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2

        elif (one == 0) and (three != 0) : ## 沒有第一，只有第二、三階段

            s_b = machineNormal[index_temp] + (need - three)
            e_b = machineNormal[index_temp] + need

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)

            fit_1 = True
            if (new_s_b < 0) or (new_e_b < 0) or ( abs(new_s_b - s_b) > three ) :
                fit_1 = False
            
            if fit_1 == True : ## 三塞得進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - three)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b, new_e_b) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 
                                'startTime': new_s_b, 
                                'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b


            else: ## 三塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three
                                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3


        else: ## 只有第二階段

            Stmp = machineNormal[index_temp]
            to_buffer = False
            if phase > 1:
                for j in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[j]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                            to_buffer = True

            if to_buffer:
                buffer.append(order_temp)

            else:
                t_start = machineNormal[index_temp]
                machineNormal[index_temp] += need
                t_end = machineNormal[index_temp]

                s_2 = t_start
                e_2 = s_2 + two
            
                s = pd.Series({'machineIndex': index_temp + 1, 
                            'orderIndex': order_temp['orderIndex'],
                            'carIndex': order_temp['carIndex'], 
                            'phaseIndex': phase,
                            'stage': 2, 'startTime': s_2, 'endTime': e_2})
                result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_2


        
        ##  處理剩下的 buffer
        if i == totalOrderNum and len(buffer) != 0:

            # print('begin ', machineNormal)
            
            while len(buffer) != 0 :
                
                order_temp = buffer[0]
                del buffer[0]
                one = order_temp['stageOne']
                two = order_temp['stageTwo']
                three = order_temp['stageThree']
                phase = order_temp['phase']
                phaseBefore = order_temp['phaseBefore']

                if three != 0:
                    three += order_temp['cleanTime']
                else:
                    if two != 0:
                        two += order_temp['cleanTime']
                    else:
                        one += order_temp['cleanTime']

                need = one + two + three

                conti = False
                for k in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[k]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] != -1:
                            beginTime = look_up_temp['finTime'] + phaseBefore
                        else:
                            buffer.append(order_temp)
                            conti = True

                if conti == True:
                    continue

                mini = -1
                best_k = -1
                for k in range(len(machineNormal)):
                    if machineNormal[k] > mini and machineNormal[k] < beginTime:
                        mini = machineNormal[k]
                        best_k = k

                if best_k != -1:
                    mini = beginTime
                else:
                    mini = min(machineNormal)
                    best_k = machineNormal.index(min(machineNormal))

                machineNormal[best_k] = mini + need


                s_1 = mini
                e_1 = mini + one
                s_2 = e_1
                e_2 = s_2 + two
                s_3 = e_2
                e_3 = s_3 + three

                
                if one != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)
                
                if two != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                if three != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for k in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[k]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_3

                # print('put ', machineNormal)

    sep = []
    for i in range(num_of_machineNormal + 1):
        sep.append(result[result['machineIndex'] == i])


    last = []
    for i in sep:
        o = list(i['orderIndex'])[-1]
        c = list(i['carIndex'])[-1]
        
        temp = result[result['orderIndex'] == o]
        temp = temp[temp['carIndex'] == c]
        last.append(temp)


    for i in last[1:num_of_machineNormal + 1]:
        for j in i.index:
            if i.loc[j,'machineIndex'] == 0:
                result.loc[j,'machineIndex'] = list(i['machineIndex'])[0]


    result['machineIndex'] = result['machineIndex'] + 1


    return result

def StageTwoFirstInsert(data, num_of_machineNormal = 4,start_time_list = [0,0,0,0,0]):
    import numpy as np
    import pandas as pd

    def overlap_back(machineBoil, start, end):
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = b
                end = b + period
        
        return start, end
    

    def overlap_front(machineBoil, start, end):
        
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        machineBoil.reverse()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = a - period
                end = a
        
        return start, end



    order = data.copy()
    order = order.rename(columns={"phaseIndex": "phase"})
    order['to_fill'] = False

    machineBoil = []
    machineNormal = []
    for i in range(num_of_machineNormal):
        machineNormal.append(start_time_list[i+1])

    look_up = pd.DataFrame(columns = ['orderIndex', 'carIndex', 'phase', 'finTime'])

    result = pd.DataFrame(columns = ['machineIndex', 'orderIndex', 'carIndex',                                           'phaseIndex', 'stage', 'startTime', 'endTime'])

    buffer = []
    totalOrderNum = order.shape[0]

    for i in range(totalOrderNum):
        order_temp = order.loc[i]
        if order_temp['phase'] > 1:
            s = pd.Series({'orderIndex': order_temp['orderIndex'],
                           'carIndex': order_temp['carIndex'], 
                           'phase': order_temp['phase'] - 1, 'finTime': -1})
            look_up = look_up.append(s, ignore_index = True)
            
            for j in range(totalOrderNum):
                order_temp_2 = order.loc[j]
                if order_temp_2['orderIndex'] == order_temp['orderIndex'] :
                    if order_temp_2['carIndex'] == order_temp['carIndex'] :
                        if order_temp_2['phase'] == order_temp['phase'] - 1 :
                            order.loc[j, 'to_fill'] = True

    # print('\n\n##########\n\n', order, '\n\n##########\n\n')

    START_0 = start_time_list[0]
    
    i = 0
    last_from_buffer = False
    while i < totalOrderNum:
        
        if i % num_of_machineNormal == 1 and len(buffer) != 0                                  and last_from_buffer == False:

            order_temp = buffer[0]
            del buffer[0]
            last_from_buffer = True
        
        else:
            order_temp = order.loc[i]
            last_from_buffer = False
            i += 1
    
            
        one = order_temp['stageOne']
        two = order_temp['stageTwo']
        three = order_temp['stageThree']
        phase = order_temp['phase']
        phaseBefore = order_temp['phaseBefore']

        if three != 0:
            three += order_temp['cleanTime']
        else:
            if two != 0:
                two += order_temp['cleanTime']
            else:
                one += order_temp['cleanTime']

        need = one + two + three

        index_temp = machineNormal.index(min(machineNormal))
        cur_max = max(machineNormal)

        if (one != 0) and (three != 0):  ## 有第一、二、三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            new_s_b_2, new_e_b_2 = overlap_front(machineBoil, s_b_2, e_b_2)

            fit_2 = True
            if (new_s_b_2 < START_0) or (new_e_b_2 < START_0) or (abs(new_s_b_2 - s_b_2) > one):

                fit_2 = False

            if fit_2 == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b_2                                   or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer :
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b_2, new_e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three         

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 
                                'startTime': new_s_b_2,
                                'endTime':new_e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)


                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3
                                

            else: ## 一塞不進
                
                s_b = machineNormal[index_temp] + (need - three)
                e_b = machineNormal[index_temp] + need

                new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)

                fit_1 = True
                if (new_s_b < START_0) or (new_e_b < START_0) or ( abs(new_s_b - s_b) > three) :
                    fit_1 = False

                if fit_1 == True : ## 一塞不進、三塞得進
                    
                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += (need - three)
                        t_end = machineNormal[index_temp]
                        machineBoil.append( (new_s_b, new_e_b) )

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)
                        

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': 0, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3,
                                    'startTime': new_s_b,
                                    'endTime': new_e_b})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex'] ==                                                         look_up_temp['orderIndex']                                                    and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = new_e_b
                                


                else: ## 一塞不進、三塞不進

                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += need
                        t_end = machineNormal[index_temp]

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two
                        s_3 = e_2
                        e_3 = e_2 + three

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 
                                    'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 
                                    'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3, 
                                    'startTime': s_3, 'endTime': e_3})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex']==                                                          look_up_temp['orderIndex']                                                     and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = e_3

                                
                   
            
        elif (one!= 0) and  (two == 0) and (three == 0): ## 只有第一階段

            s_b = START_0
            e_b = s_b + one

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)
            # print('\n', new_s_b, new_e_b, '\n')
            fit = True
            if new_e_b > cur_max :
                fit = False

            if fit == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b                                      or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    machineBoil.append( (new_s_b, new_e_b) )
                    
                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': new_s_b,'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b

            else: ## 一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:  
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': t_start, 'endTime': t_end})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = t_end


        elif (one!= 0) and  (two != 0) and (three == 0): ## 只有第一、二階段，沒第三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            new_s_b_2, new_e_b_2 = overlap_front(machineBoil, s_b_2, e_b_2)

            fit_2 = True
            if (new_s_b_2 < START_0) or (new_e_b_2 < START_0) or (abs(new_s_b_2 - s_b_2) > one) :
                fit_2 = False

            if fit_2 == True : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b_2                                   or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b_2, new_e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 
                                'startTime': new_s_b_2,
                                'endTime':new_e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime':e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2


            else: #一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)
                
                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s_1 = t_start
                    e_1 = t_start + one
                    s_2 = e_1
                    e_2 = s_2 + two
                
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)

                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2

        elif (one == 0) and (three != 0) : ## 沒有第一，只有第二、三階段

            s_b = machineNormal[index_temp] + (need - three)
            e_b = machineNormal[index_temp] + need

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)

            fit_1 = True
            if (new_s_b < START_0) or (new_e_b < START_0) or ( abs(new_s_b - s_b) > three ) :
                fit_1 = False
            
            if fit_1 == True : ## 三塞得進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - three)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (new_s_b, new_e_b) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 
                                'startTime': new_s_b, 
                                'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b


            else: ## 三塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three
                                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3


        else: ## 只有第二階段

            Stmp = machineNormal[index_temp]
            to_buffer = False
            if phase > 1:
                for j in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[j]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                            to_buffer = True

            if to_buffer:
                buffer.append(order_temp)

            else:
                t_start = machineNormal[index_temp]
                machineNormal[index_temp] += need
                t_end = machineNormal[index_temp]

                s_2 = t_start
                e_2 = s_2 + two
            
                s = pd.Series({'machineIndex': index_temp + 1, 
                            'orderIndex': order_temp['orderIndex'],
                            'carIndex': order_temp['carIndex'], 
                            'phaseIndex': phase,
                            'stage': 2, 'startTime': s_2, 'endTime': e_2})
                result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_2


        
        ##  處理剩下的 buffer
        if i == totalOrderNum and len(buffer) != 0:

            # print('begin ', machineNormal)
            
            while len(buffer) != 0 :
                
                order_temp = buffer[0]
                del buffer[0]
                one = order_temp['stageOne']
                two = order_temp['stageTwo']
                three = order_temp['stageThree']
                phase = order_temp['phase']
                phaseBefore = order_temp['phaseBefore']

                if three != 0:
                    three += order_temp['cleanTime']
                else:
                    if two != 0:
                        two += order_temp['cleanTime']
                    else:
                        one += order_temp['cleanTime']

                need = one + two + three

                conti = False
                for k in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[k]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] != -1:
                            beginTime = look_up_temp['finTime'] + phaseBefore
                        else:
                            buffer.append(order_temp)
                            conti = True

                if conti == True:
                    continue

                mini = -1
                best_k = -1
                for k in range(len(machineNormal)):
                    if machineNormal[k] > mini and machineNormal[k] < beginTime:
                        mini = machineNormal[k]
                        best_k = k

                if best_k != -1:
                    mini = beginTime
                else:
                    mini = min(machineNormal)
                    best_k = machineNormal.index(min(machineNormal))

                machineNormal[best_k] = mini + need


                s_1 = mini
                e_1 = mini + one
                s_2 = e_1
                e_2 = s_2 + two
                s_3 = e_2
                e_3 = s_3 + three

                
                if one != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)
                
                if two != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                if three != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for k in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[k]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_3

                # print('put ', machineNormal)

    sep = []
    for i in range(num_of_machineNormal + 1):
        sep.append(result[result['machineIndex'] == i])


    last = []
    for i in sep:
        o = list(i['orderIndex'])[-1]
        c = list(i['carIndex'])[-1]
        
        temp = result[result['orderIndex'] == o]
        temp = temp[temp['carIndex'] == c]
        last.append(temp)


    for i in last[1:num_of_machineNormal + 1]:
        for j in i.index:
            if i.loc[j,'machineIndex'] == 0:
                result.loc[j,'machineIndex'] = list(i['machineIndex'])[0]


    result['machineIndex'] = result['machineIndex'] + 1


    return result

def StageTwoFirst(data, num_of_machineNormal = 4, start_time_list = [0, 0, 0, 0, 0]):
    import numpy as np
    import pandas as pd

    def overlap(machineBoil, start, end):
        if (start <= 0) or (end <= 0):
            return True
            
        overlap = False
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                overlap = True
                break
        return overlap

    def overlap_back(machineBoil, start, end):
        if (start < 0) or (end <= 0):
            return -1, -1
            
        machineBoil.sort()
        
        for a,b in machineBoil:
            if (start > a or end > a) and (start < b or end < b):
                period = end - start
                start = b
                end = b + period
        
        return start, end

    
    order = data.copy()
    order = order.rename(columns={"phaseIndex": "phase"})
    order['to_fill'] = False

    machineBoil = []
    machineNormal = []

    if start_time_list[0] != 0:
        machineBoil.append( (0, start_time_list[0]) )
    for i in range(num_of_machineNormal):
        machineNormal.append(start_time_list[i+1])

    look_up = pd.DataFrame(columns = ['orderIndex', 'carIndex', 'phase', 'finTime'])

    result = pd.DataFrame(columns = ['machineIndex', 'orderIndex', 'carIndex',                                           'phaseIndex', 'stage', 'startTime', 'endTime'])

    buffer = []

    totalOrderNum = order.shape[0]

    for i in range(totalOrderNum):
        order_temp = order.loc[i]
        if order_temp['phase'] > 1:
            s = pd.Series({'orderIndex': order_temp['orderIndex'],
                           'carIndex': order_temp['carIndex'], 
                           'phase': order_temp['phase'] - 1, 'finTime': -1})
            look_up = look_up.append(s, ignore_index = True)
            
            for j in range(totalOrderNum):
                order_temp_2 = order.loc[j]
                if order_temp_2['orderIndex'] == order_temp['orderIndex'] :
                    if order_temp_2['carIndex'] == order_temp['carIndex'] :
                        if order_temp_2['phase'] == order_temp['phase'] - 1 :
                            order.loc[j, 'to_fill'] = True

    # print('\n\n##########\n\n', order, '\n\n##########\n\n')

    i = 0
    last_from_buffer = False
    while i < totalOrderNum:
        
        if i % num_of_machineNormal == 1 and len(buffer) != 0                                  and last_from_buffer == False:

            order_temp = buffer[0]
            del buffer[0]
            last_from_buffer = True
        
        else:
            order_temp = order.loc[i]
            last_from_buffer = False
            i += 1
    
            
        one = order_temp['stageOne']
        two = order_temp['stageTwo']
        three = order_temp['stageThree']
        phase = order_temp['phase']
        phaseBefore = order_temp['phaseBefore']

        if three != 0:
            three += order_temp['cleanTime']
        else:
            if two != 0:
                two += order_temp['cleanTime']
            else:
                one += order_temp['cleanTime']

        need = one + two + three

        index_temp = machineNormal.index(min(machineNormal))
        cur_max = max(machineNormal)

        if (one != 0) and (three != 0):  ## 有第一、二、三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            if overlap(machineBoil, s_b_2, e_b_2) == False : ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > s_b_2                                        or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer :
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (s_b_2, e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three         

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': s_b_2, 'endTime':e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)


                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3
                                

            else: ## 一塞不進
                
                s_b = machineNormal[index_temp] + (need - three)
                e_b = machineNormal[index_temp] + need

                if overlap(machineBoil, s_b, e_b) == False: ## 一塞不進、三塞得進
                    
                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += (need - three)
                        t_end = machineNormal[index_temp]
                        machineBoil.append( (s_b, e_b) )

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)
                        

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': 0, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3, 'startTime': s_b, 'endTime': e_b})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex'] ==                                                         look_up_temp['orderIndex']                                                    and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = e_b
                                


                else: ## 一塞不進、三塞不進

                    Stmp = machineNormal[index_temp]
                    to_buffer = False
                    if phase > 1:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                                if look_up_temp['finTime'] + phaseBefore > Stmp                                        or look_up_temp['finTime'] == -1:
                                    to_buffer = True

                    if to_buffer:
                        buffer.append(order_temp)

                    else:
                        t_start = machineNormal[index_temp]
                        machineNormal[index_temp] += need
                        t_end = machineNormal[index_temp]

                        s_1 = t_start
                        e_1 = t_start + one
                        s_2 = e_1
                        e_2 = s_2 + two
                        s_3 = e_2
                        e_3 = e_2 + three

                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 1, 
                                    'startTime': s_1, 'endTime': e_1})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 2, 
                                    'startTime': s_2, 'endTime': e_2})
                        result = result.append(s, ignore_index = True)


                        s = pd.Series({'machineIndex': index_temp + 1, 
                                    'orderIndex': order_temp['orderIndex'],
                                    'carIndex': order_temp['carIndex'], 
                                    'phaseIndex': phase,
                                    'stage': 3, 
                                    'startTime': s_3, 'endTime': e_3})
                        result = result.append(s, ignore_index = True)

                        if order_temp['to_fill'] == True:
                            for j in range(look_up.shape[0]):
                                look_up_temp = look_up.loc[j]
                                if order_temp['orderIndex']==                                                          look_up_temp['orderIndex']                                                     and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                    look_up.loc[j, 'finTime'] = e_3

                                
                   
            
        elif (one!= 0) and  (two == 0) and (three == 0): ## 只有第一階段

            s_b = 0
            e_b = one

            new_s_b, new_e_b = overlap_back(machineBoil, s_b, e_b)
            # print('\n', new_s_b, new_e_b, '\n')
            fit = True
            if (new_s_b > machineNormal[index_temp]):
                fit = False

            if( fit == True ): ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > new_s_b                                      or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    machineBoil.append( (new_s_b, new_e_b) )
                    
                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': new_s_b,'endTime':new_e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = new_e_b

            else: ## 一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:  
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': t_start, 'endTime': t_end})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = t_end


        elif (one!= 0) and  (two != 0) and (three == 0): ## 只有第一、二階段，沒第三階段

            s_b_2 = machineNormal[index_temp] - one
            e_b_2 = machineNormal[index_temp]

            if overlap(machineBoil, s_b_2, e_b_2) == False: ## 一塞得進

                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > s_b_2                                        or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - one)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (s_b_2, e_b_2) )

                    s_2 = t_start
                    e_2 = s_2 + two

                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': s_b_2, 'endTime':e_b_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime':e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2


            else: #一塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)
                
                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]
                    
                    s_1 = t_start
                    e_1 = t_start + one
                    s_2 = e_1
                    e_2 = s_2 + two
                
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)

                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_2

        elif (one == 0) and (three != 0) : ## 沒有第一，只有第二、三階段

            s_b = machineNormal[index_temp] + (need - three)
            e_b = machineNormal[index_temp] + need
            
            if overlap(machineBoil, s_b, e_b) == False : ## 三塞得進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += (need - three)
                    t_end = machineNormal[index_temp]
                    machineBoil.append( (s_b, e_b) )

                    s_2 = t_start
                    e_2 = s_2 + two
                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': 0, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_b, 'endTime':e_b})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_b


            else: ## 三塞不進

                Stmp = machineNormal[index_temp]
                to_buffer = False
                if phase > 1:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                            if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                                to_buffer = True

                if to_buffer:
                    buffer.append(order_temp)

                else:
                    t_start = machineNormal[index_temp]
                    machineNormal[index_temp] += need
                    t_end = machineNormal[index_temp]

                    s_2 = t_start
                    e_2 = s_2 + two
                    s_3 = e_2
                    e_3 = e_2 + three
                                    
                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)


                    s = pd.Series({'machineIndex': index_temp + 1, 
                                'orderIndex': order_temp['orderIndex'],
                                'carIndex': order_temp['carIndex'], 
                                'phaseIndex': phase,
                                'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                    if order_temp['to_fill'] == True:
                        for j in range(look_up.shape[0]):
                            look_up_temp = look_up.loc[j]
                            if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                                look_up.loc[j, 'finTime'] = e_3


        else: ## 只有第二階段

            Stmp = machineNormal[index_temp]
            to_buffer = False
            if phase > 1:
                for j in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[j]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] + phaseBefore > Stmp                                         or look_up_temp['finTime'] == -1:
                            to_buffer = True

            if to_buffer:
                buffer.append(order_temp)

            else:
                t_start = machineNormal[index_temp]
                machineNormal[index_temp] += need
                t_end = machineNormal[index_temp]

                s_2 = t_start
                e_2 = s_2 + two
            
                s = pd.Series({'machineIndex': index_temp + 1, 
                            'orderIndex': order_temp['orderIndex'],
                            'carIndex': order_temp['carIndex'], 
                            'phaseIndex': phase,
                            'stage': 2, 'startTime': s_2, 'endTime': e_2})
                result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for j in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[j]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_2


        
        ##  處理剩下的 buffer
        if i == totalOrderNum and len(buffer) != 0:

            # print('begin ', machineNormal)
            
            while len(buffer) != 0 :
                
                order_temp = buffer[0]
                del buffer[0]
                one = order_temp['stageOne']
                two = order_temp['stageTwo']
                three = order_temp['stageThree']
                phase = order_temp['phase']
                phaseBefore = order_temp['phaseBefore']

                if three != 0:
                    three += order_temp['cleanTime']
                else:
                    if two != 0:
                        two += order_temp['cleanTime']
                    else:
                        one += order_temp['cleanTime']

                need = one + two + three

                conti = False
                for k in range(look_up.shape[0]):
                    look_up_temp = look_up.loc[k]
                    if order_temp['orderIndex'] == look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] -1 == look_up_temp['phase']:
                        if look_up_temp['finTime'] != -1:
                            beginTime = look_up_temp['finTime'] + phaseBefore
                        else:
                            buffer.append(order_temp)
                            conti = True

                if conti == True:
                    continue

                mini = -1
                best_k = -1
                for k in range(len(machineNormal)):
                    if machineNormal[k] > mini and machineNormal[k] < beginTime:
                        mini = machineNormal[k]
                        best_k = k

                if best_k != -1:
                    mini = beginTime
                else:
                    mini = min(machineNormal)
                    best_k = machineNormal.index(min(machineNormal))

                machineNormal[best_k] = mini + need


                s_1 = mini
                e_1 = mini + one
                s_2 = e_1
                e_2 = s_2 + two
                s_3 = e_2
                e_3 = s_3 + three

                
                if one != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 1, 'startTime': s_1, 'endTime': e_1})
                    result = result.append(s, ignore_index = True)
                
                if two != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 2, 'startTime': s_2, 'endTime': e_2})
                    result = result.append(s, ignore_index = True)

                if three != 0:
                    s = pd.Series({'machineIndex': best_k + 1, 
                                   'orderIndex': order_temp['orderIndex'],
                                   'carIndex': order_temp['carIndex'], 
                                   'phaseIndex': phase,
                                   'stage': 3, 'startTime': s_3, 'endTime': e_3})
                    result = result.append(s, ignore_index = True)

                if order_temp['to_fill'] == True:
                    for k in range(look_up.shape[0]):
                        look_up_temp = look_up.loc[k]
                        if order_temp['orderIndex']== look_up_temp['orderIndex']                              and order_temp['carIndex'] == look_up_temp['carIndex']                              and order_temp['phase'] == look_up_temp['phase']:
                            look_up.loc[j, 'finTime'] = e_3

                # print('put ', machineNormal)

    sep = []
    for i in range(num_of_machineNormal + 1):
        sep.append(result[result['machineIndex'] == i])


    last = []
    for i in sep:
        o = list(i['orderIndex'])[-1]
        c = list(i['carIndex'])[-1]
        
        temp = result[result['orderIndex'] == o]
        temp = temp[temp['carIndex'] == c]
        last.append(temp)


    for i in last[1:num_of_machineNormal + 1]:
        for j in i.index:
            if i.loc[j,'machineIndex'] == 0:
                result.loc[j,'machineIndex'] = list(i['machineIndex'])[0]


    result['machineIndex'] = result['machineIndex'] + 1



    return result


class MachineOneInsert:
    def __init__(self, data, M, onlyStageOnetoMachineOne, start_time_list):
        self.__process = data
        self.__M = M
        self.__due_time = 1080 # 暫時設為18小時
        self.__wait_list = np.array([[]]).reshape(-1, 2)
        self.__start_time_list = start_time_list
        self.__m1_completion_time = []
        self.__m25_completion_time = []
        self.__result = pd.DataFrame(data = {'machineIndex': [],'orderIndex': [], 'carIndex': [], 'stage':[],'startTime': [],'endTime': []})
        self.__onlyStageOnetoMachineOne = onlyStageOnetoMachineOne
        
    def __wait_list_append(self, process_index, ready_to_start):
        self.__wait_list = np.append(self.__wait_list, [[process_index, ready_to_start]], axis = 0)
        self.__wait_list = self.__wait_list[self.__wait_list[:,1].argsort(axis = 0)]
    
    def __insert(self, process_series, m_index, m_completion_time, wait_list = False):
        # stage1 insert
        if wait_list:
            if process_series.stageOne > process_series.stageThree:
                if (self.__m1_completion_time[0] + process_series.stageOne <= (m_completion_time + 0)) or ((process_series.stageTwo == 0) and ((m_completion_time ==self.__m1_completion_time[0]) or self.__onlyStageOnetoMachineOne)):
                    # stageOne:
                    self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 1, 'machineIndex': 1, 'orderIndex': process_series.orderIndex, 
                                                         'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m1_completion_time[0],
                                                         'endTime': self.__m1_completion_time[0] + process_series.stageOne})
                    self.__m1_completion_time[0] += process_series.stageOne
                    # stageTwo & stageThree:
                    if process_series.stageTwo != 0:
                        self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 2, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                             'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                             'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
                        self.__m25_completion_time[m_index] += process_series.stageTwo

                    if process_series.stageThree != 0:
                        self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 3, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                             'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                             'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
                        self.__m25_completion_time[m_index] += process_series.stageThree

                    return
        else: 
            self.__m25_completion_time[m_index] = m_completion_time

            if process_series.stageOne > process_series.stageThree:
                if (self.__m1_completion_time[0] + process_series.stageOne <= (m_completion_time + 0)) or ((process_series.stageTwo == 0) and ((m_completion_time ==self.__m1_completion_time[0]) or self.__onlyStageOnetoMachineOne)):
                    # stageOne:
                    self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 1, 'machineIndex': 1, 'orderIndex': process_series.orderIndex, 
                                                         'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m1_completion_time[0],
                                                         'endTime': self.__m1_completion_time[0] + process_series.stageOne})
                    self.__m1_completion_time[0] += process_series.stageOne
                    # stageTwo & stageThree:
                    if process_series.stageTwo != 0:
                        self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 2, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                             'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                             'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
                        self.__m25_completion_time[m_index] += process_series.stageTwo

                    if process_series.stageThree != 0:
                        self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 3, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                             'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                             'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
                        self.__m25_completion_time[m_index] += process_series.stageThree

                    return
        
        # stage3 insert
        if process_series.stageThree != 0:
            if self.__m1_completion_time[1] - process_series.stageThree >= m_completion_time + process_series.stageTwo + process_series.stageOne:
                # stageOne & stageTwo:
                if process_series.stageOne != 0:
                    self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 1, 'machineIndex': 1, 'orderIndex': process_series.orderIndex, 
                                                         'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                         'endTime': self.__m25_completion_time[m_index] + process_series.stageOne})
                    self.__m25_completion_time[m_index] += process_series.stageOne
                    
                if process_series.stageTwo != 0:
                    self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 2, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                         'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                         'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
                    self.__m25_completion_time[m_index] += process_series.stageTwo
                
                # stageThree
                self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 3, 'machineIndex': 1, 'orderIndex': process_series.orderIndex, 
                                                     'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m1_completion_time[1] - process_series.stageThree,
                                                     'endTime': self.__m1_completion_time[1]})
                self.__m1_completion_time[1] -= process_series.stageThree
                return
                    
        # else, no insert:
        # stageOne
        if process_series.stageOne != 0:
            self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 1, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                 'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                 'endTime': self.__m25_completion_time[m_index] + process_series.stageOne})
            self.__m25_completion_time[m_index] += process_series.stageOne

        # stageTwo
        if process_series.stageTwo != 0:
            self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 2, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                 'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                 'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
            self.__m25_completion_time[m_index] += process_series.stageTwo

        # stageThree
        if process_series.stageThree != 0:
            self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 3, 'machineIndex': m_index+2, 'orderIndex': process_series.orderIndex, 
                                                 'carIndex': process_series.carIndex, 'phaseIndex': process_series.phaseIndex, 'startTime': self.__m25_completion_time[m_index],
                                                 'endTime': self.__m25_completion_time[m_index] + process_series.stageTwo})
            self.__m25_completion_time[m_index] += process_series.stageThree

            
    def schedule(self, s_method, s_method_ascending, start_with_shortest_stageOne = True):
        # reset 所有的變數
        self.__wait_list = np.array([[]]).reshape(-1, 2)
        self.__m1_completion_time = [self.__start_time_list[0], self.__due_time]
        self.__m25_completion_time = self.__start_time_list[1:]
        self.__result = pd.DataFrame(data = {'machineIndex': [],'orderIndex': [], 'carIndex': [], 'phaseIndex':[], 'stage':[],'startTime': [],'endTime': []})
        # print(self.__result)
        # 選出 m 個最短的 'stageOne' 且 'phaseIndex == 1' 的 process_index，如果 'stageOne' 相同，則以 s_method 決定
        if start_with_shortest_stageOne:
            data = self.__process.sort_values(by = ['phaseIndex', 'stageOne', s_method], ascending = [True, True, s_method_ascending]).reset_index(drop = True)
            for m in range(self.__M):
                # Exception handling:
                if data.loc[m, 'phaseIndex'] > 1: 
                    break
                if len(data) == 0:#
                    break
                # 將這些 process 的 'stageOne' + 'stageTwo' 放到一般機台中
                # stage1
                if data.loc[m, 'stageOne'] != 0:
                    self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 1, 'machineIndex': m+2, 'orderIndex': data.loc[m, 'orderIndex'], 
                                                             'carIndex': data.loc[m, 'carIndex'], 'phaseIndex': data.loc[m, 'phaseIndex'], 'startTime': self.__m25_completion_time[m],
                                                             'endTime': self.__m25_completion_time[m] + data.loc[m, 'stageOne']})        
                    self.__m25_completion_time[m] += data.loc[m, 'stageOne']
                # stage2
                if data.loc[m, 'stageTwo'] != 0:
                    self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 2, 'machineIndex': m+2, 'orderIndex': data.loc[m, 'orderIndex'], 
                                                         'carIndex': data.loc[m, 'carIndex'], 'phaseIndex': data.loc[m, 'phaseIndex'], 'startTime': self.__m25_completion_time[m],
                                                         'endTime': self.__m25_completion_time[m] + data.loc[m, 'stageTwo']})
                    self.__m25_completion_time[m] += data.loc[m, 'stageTwo']
                # 如果有 'stageThree'，直接從 dueTime 往前排，不行的話就放在 'stageTwo' 後面。機台的 'completion time' 要加上清潔時間
                if data.loc[m, 'stageThree'] != 0:
                    if self.__m1_completion_time[1] - data.loc[m, 'stageThree'] > self.__m1_completion_time[0]:
                        self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 3, 'machineIndex': 1, 'orderIndex': data.loc[m, 'orderIndex'], 
                                                         'carIndex': data.loc[m, 'carIndex'], 'phaseIndex': data.loc[m, 'phaseIndex'], 'startTime': self.__m1_completion_time[1] - data.loc[m, 'stageThree'],
                                                         'endTime': self.__m1_completion_time[1]})
                        self.__m1_completion_time[1] -= data.loc[m, 'stageThree']
                    else:
                        self.__result.loc[len(self.__result)] = pd.Series(data = {'stage': 3, 'machineIndex': m+2, 'orderIndex': data.loc[m, 'orderIndex'], 
                                                         'carIndex': data.loc[m, 'carIndex'], 'phaseIndex': data.loc[m, 'phaseIndex'], 'startTime': self.__m25_completion_time[m],
                                                         'endTime': self.__m25_completion_time[m] + data.loc[m, 'stageThree']})
                        self.__m25_completion_time[m] += data.loc[m, 'stageThree']

                data.drop(m, inplace = True)
        
            # for 以 s_method 排序:
            data = data.sort_values(by = [s_method, 'phaseIndex'], ascending = [s_method_ascending, True]).reset_index(drop = True)
        
        else:
            data = self.__process.sort_values(by = [s_method, 'phaseIndex'], ascending = [s_method_ascending, True]).reset_index(drop = True)
            
        for i in range(len(data)):
            #print('orderIndex = %d, carIndex = %d, phaseIndex = %d' %(data.loc[i, 'orderIndex'], data.loc[i, 'carIndex'] , data.loc[i, 'phaseIndex']))
            # 選定一個 'completion time' 最小的機台
            ready25_time = min(self.__m25_completion_time) # 最早可開始的機台時間
            ready25_machine = self.__m25_completion_time.index(ready25_time)# 最早可開始的機台, 0~3 not 1~4
            #print('readytime = %d' %ready25_time)
            
            # if completion time' 已達 wait_list 第一個的開始時間:
            while(self.__wait_list.shape[0] != 0):
                if self.__wait_list[0, 1] <= ready25_time:
                    # 他執行 insert，並從  wait_list 刪除
                    self.__insert(data.loc[self.__wait_list[0, 0]], ready25_machine, ready25_time)
                    self.__wait_list = np.delete(self.__wait_list, (0), axis=0)
                    # 重新選定一個 'completion time' 最小的機台
                    ready25_time = min(self.__m25_completion_time) # 最早可開始的機台時間
                    ready25_machine = self.__m25_completion_time.index(ready25_time)# 最早可開始的機台, 0~3 not 1~4
                    continue
                break
                    
            #     if process 的 'phaseIndex' != 1，則檢查其 'phaseIndex' - 1 的 endTime + phaseIndex 是否小於機台的 'completion time':
            if data.loc[i, 'phaseIndex'] != 1:
                previous_process_end = self.__result[(self.__result.orderIndex == data.loc[i, 'orderIndex']) & (self.__result.carIndex == data.loc[i, 'carIndex'])]['endTime']
                ready_to_start = int(max(previous_process_end)) + data.loc[i, 'phaseBefore']
                self.__wait_list_append(i, ready_to_start)
            #         則丟進去一個以 'phaseIndex' -1   endTime + phaseIndex 排序的list(wait_list)中
            #         continue
            else:
                # 執行 insert
                self.__insert(data.loc[i], ready25_machine, ready25_time)
        
        # 將剩下 wait list 的 process 排完
        while(len(self.__wait_list) != 0):
            ready25_time = min(self.__m25_completion_time) # 最早可開始的機台時間
            ready25_machine = self.__m25_completion_time.index(ready25_time)# 最早可開始的機台, 0~3 not 1~4
            ready25_time = max(ready25_time, self.__wait_list[0, 1]) # max(最早可開始的機台時間, process 可開始的時間)
            self.__insert(data.loc[self.__wait_list[0, 0]], ready25_machine, ready25_time)
            self.__wait_list = np.delete(self.__wait_list, (0), axis=0)
            # 重新選定一個 'completion time' 最小的機台
            ready25_time = min(self.__m25_completion_time) # 最早可開始的機台時間
            ready25_machine = self.__m25_completion_time.index(ready25_time)# 最早可開始的機台, 0~3 not 1~4
        
        return(self.__result)