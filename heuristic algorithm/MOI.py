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