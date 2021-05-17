import numpy as np
import pandas as pd

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