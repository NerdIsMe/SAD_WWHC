finc By_car_length(data, by):    # data 為訂單資料（ DataFrame ）， by = 0 or 1( 0: ascending, 1: descending )

    overlap_back(machineBoil, start, end):    # 自 machineBoil 中由前向後檢查最近可安排 Stage 3 的時間區段，start, end 為該 Stage 原本的開始及結束時間
        if start < 0 or end <0 then
            return -1, -1

        將 machineBoil 由小排到大

        for i (machineBoil 中所有時間區段) do :
            if start 與 end 覆蓋到 i then
                將 start 與 end 平移修正至緊鄰 i 後
        end for

    return start, end

    overlap_front(machineBoil, start, end):    # 自 machineBoil 中由後向前檢查最近可安排 Stage 1 的時間區段，start, end 為該 Stage 原本的開始及結束時間
        if start < 0 or end <0 then
            return -1, -1

        將 machineBoil 由大排到小

        for i (machineBoil 中所有時間區段) do :
            if start 與 end 覆蓋到 i then
                將 start 與 end 平移修正至緊鄰 i 前
        end for

    return start, end


    df <- data

    if by = 0 then
        將 data 以截止時間由小排到大排序，訂單截止時間相同者再以單車所需總時間由小至大排序
    if by = ㄅ then
        將 data 以截止時間由小排到大排序，訂單截止時間相同者再以單車所需總時間由大至小排序

    將 df 中所有訂單 Stage 2 加上清潔時間

    將 df 中所有訂單拆成以車為單位（一車為一列）

    machineBoil <- []   # machine_0 被佔用的時間段，存放值為 pair
    machineNormal <- [0, 0, 0, 0]    # machine_1 至 machine_4 最後被佔用的時間

    for i (df 中的每車訂單資料) do:

        index_temp = machineNormal 中最後被佔用時間最早的機器編號
        
        if 該訂單有 Stage 1 與 Stage 3 then
            s_b_2 <- machineNormal[index_temp] - i 之 Stage 1 所需時間  # s_b_2 即為 i 之 Stage 1 最晚可開始時間
            e_b_2 <- machineNormal[index_temp]  # e_b_2 即為 i 之 Stage 1 最晚結束時間

            new_s_b_2, new_e_b_2 <- overlap_front(machineBoil, s_b_2, e_b_2)  # 自 machineBoil 中由後向前檢查最近可安排 Stage 1 的時間區段，存入 new_s_b_2, new_e_b_2

            if (new_s_b_2 > 0) and (new_e_b_2 > 0) and (new_s_b_2 與 s_b_2 差距小於 i 之 Stage 1 所需時間) then  # machine_0 可以接納 i 的 Stage 1
                將 i 之 Stage 1 派至 machine_0，以 new_s_b_2 為開始時間， new_e_b_2 為結束時間
                將 i 之其他所有 Stage 派至 machine_(index_temp)，以 machineNormal[index_temp] 為開始時間

            
            else    # machine_0 無法接納 i 的 Stage 1
                s_b <- machineNormal[index_temp] + i 所有 Stage 需所有時間 - i 之 Stage 3 所需時間  # s_b 即為i 之 Stage 3 最早可開始時間
                e_b <- machineNormal[index_temp] + i 所有 Stage 需所有時間 # e_b 即為 i 之 Stage 3 最早可結束時間
                
                new_s_b, new_e_b <- overlap_back(machineBoil, s_b, e_b)    ＃  自 machineBoil 中由前向後檢查最近可安排 Stage 3 的時間區段，存入 new_s_b, new_e_b
                
                if (new_s_b > 0) and (new_e_b > 0) and (new_s_b 與 s_b 差距小於 i 之 Stage 3 所需時間) and (new_e_b <= 此訂單 due time) then  # machine_0 可以接納 i 的 Stage 3
                    將 i 之 Stage 3 派至 machine_0，以 new_s_b 為開始時間， new_e_b 為結束時間
                    將 i 之其他所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間

                else    # machine_0 亦無法接納 i 的 Stage 3
                    將 i 之所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間
        
        elif 該訂單只有 Stage 1 then
            s_b <- 0
            e_b <- 0 + i 之 Stage 1 所需時間

            new_s_b, new_e_b <- overlap_back(machineBoil, s_b, e_b)   # 自 machineBoil 中由最前向後檢查最近可安排 Stage 1 的時間區段，存入 new_s_b, new_e_b

            if (將 Stage 1 安排至 machine_0 的 (new_s_b, new_e_b) 不會使 makespan 增大) and (new_e_b <= 此訂單 due time) then
                將 i 之 Stage 1 派至 machine_0 ，以 new_s_b 為開始時間， new_e_b 為結束時間
                將 i 之其他所有 Stage 派至 machine_(index_temp)，以 machineNormal[index_temp] 為開始時間
            else
                將 i 之所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間


        
        elif 該訂單有 Stage 1 沒有 Stage 3 then
            s_b_2 <- machineNormal[index_temp] - i 之 Stage 1 所需時間  # s_b_2 即為 i 之 Stage 1 最晚可開始時間
            e_b_2 <- machineNormal[index_temp]  # e_b_2 即為 i 之 Stage 1 最晚結束時間

            new_s_b_2, new_e_b_2 <- overlap_front(machineBoil, s_b_2, e_b_2)   # 自 machineBoil 中由後向前檢查最近可安排 Stage 1 的時間區段，存入 new_s_b_2, new_e_b_2

            if (new_s_b_2 > 0) and (new_e_b_2 > 0) and (new_s_b_2 與 s_b_2 差距小於 i 之 Stage 1 所需時間) then  # machine_0 可以接納 i 的 Stage 1
                將 i 之 Stage 1 派至 machine_0 ，以 new_s_b_2 為開始時間， new_e_b_2 為結束時間
                將 i 之其他所有 Stage 派至 machine_(index_temp)，以 machineNormal[index_temp] 為開始時間
            
            else   # machine_0 無法已接納 i 的 Stage 1
                將 i 之所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間

            
        elif 該訂單有 Stage 3 沒有 Stage 1 then
            s_b <- machineNormal[index_temp] + i 所有 Stage 需所有時間 - i 之 Stage 3 所需時間  # s_b 即為i 之 Stage 3 最早可開始時間
            e_b <- machineNormal[index_temp] + i 所有 Stage 需所有時間 # e_b 即為 i 之 Stage 3 最早可結束時間
                
            new_s_b, new_e_b <- overlap_back(machineBoil, s_b, e_b)     ＃  自 machineBoil 中由前向後檢查最近可安排 Stage 3 的時間區段，存入 new_s_b, new_e_b
                
            if (new_s_b > 0) and (new_e_b > 0) and (new_s_b 與 s_b 差距小於 i 之 Stage 3 所需時間) and (new_e_b <= 此訂單 due time) then  # machine_0 可以接納 i 的 Stage 3
                將 i 之 Stage 3 派至 machine_0，以 new_s_b 為開始時間， new_e_b 為結束時間
                將 i 之其他所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間

            else    # machine_0 無法已接納 i 的 Stage 3
                將 i 之所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間

        
        else    #該訂單沒有 Stage 1 與 Stage 1，只有 Stage 2
            將 i 之所有 Stage 派至 machine_(index_temp)，machineNormal[index_temp] 為開始時間

    
    end for

            
            







