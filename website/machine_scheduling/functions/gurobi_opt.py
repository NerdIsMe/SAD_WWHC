def GurobiOptimization(data, time_limit = 60):
    import gurobipy as gp
    import pandas as pd
# constant 
    # machines
    M = 5
    Clean = 1/6
    Only_Cook = 0

    # orders
    N = len(data["order"])
    F = list(data["finish"])
    Car = list(data["car"].astype('int64'))
    S = list(data["smoke"]*Clean)
    ST = []
    for i in range(N):
        stage = [[], data["timeOne"][i], (data["timeTwo"]+S)[i], data["timeThree"][i]]
        ST.append(stage)

    # infinity
    inf = 1000
    
    # Create a new model
    model = gp.Model("mip1")

    # Create variables
    # 第n個訂單、第c車、第i階段，被丟給第m台機器
    x={}
    for n in range(0, N):
        x[n] = {}
        for c in range(0, Car[n]):
            x[n][c] = {}
            for i in range(1, 3+1):
                x[n][c][i] = {}
                for m in range(0, M):
                    x[n][c][i][m] = model.addVar(lb = 0, ub = 1, vtype=gp.GRB.BINARY, name='x_{}_{}_{}_{}'.format(n, c, i, m))

    # 訂單是否準時 d_n
    d = {}
    for n in range(0, N):
        d[n] = model.addVar(lb = 0, ub = 1, vtype=gp.GRB.BINARY, name='d_{}'.format(n))

    # z_{ncijkl} = 1 if uet_{nci} 比 uet_{jkl} 早進入 machine_m
    z={}
    z_added = {}
    for n in range(0, N):
        z[n] = {}
        z_added[n] = {}
        for c in range(0, Car[n]):
            z[n][c] = {}
            z_added[n][c] = {}
            for i in range(1, 3+1):
                z[n][c][i] = {}
                z_added[n][c][i] = {}
                for j in range(0, N):
                    z[n][c][i][j] = {}
                    z_added[n][c][i][j] = {}
                    for k in range(0, Car[j]):
                        z[n][c][i][j][k] = {}
                        z_added[n][c][i][j][k] = {}
                        for l in range(1, 3+1):
                            z_added[n][c][i][j][k][l] = False
                            z[n][c][i][j][k][l] = {}
                            for m in range(M):
                                z[n][c][i][j][k][l][m] = model.addVar(lb = 0, ub = 1, vtype=gp.GRB.BINARY, name='z_{}_{}_{}_{}_{}_{}_{}'.format(n, c, i, j, k, l, m))

    # 每車每階段的完成時間
    uet = {}
    for n in range(0, N):
        uet[n] = {}
        for c in range(0, Car[n]):
            uet[n][c] = {}
            for i in range(1, 3+1):
                uet[n][c][i] = model.addVar(lb=0, vtype=gp.GRB.CONTINUOUS, name='uet_{}_{}_{}'.format(n, c, i))

    # 訂單最後完成時間
    ft = {}
    for n in range(0, N):
        ft[n] = model.addVar(lb=0, vtype=gp.GRB.CONTINUOUS, name='ft_{}'.format(n))

    # Integrate new variables
    model.update()

# Set objective
    model.setObjective(gp.quicksum((inf * d[n] + (F[n] - ft[n]))  for n in range(0, N)), gp.GRB.MAXIMIZE) 
#         model.setObjective(quicksum(d[n]  for n in range(0, N)), GRB.MAXIMIZE) 

# Add constraint:

    # 每車的結束時間
    for n in range(0, N):
        model.addConstr(ft[n] == gp.max_(uet[n][c][3] for c in range(Car[n])), "FinishTime_{}".format(n))

    # 時間內完成訂單與否
    for n in range(0, N):
        model.addConstr(d[n] * (F[n] - ft[n]) >= 0, "NotDelay_{}".format(n))

    # 每車 stage 之間的先後順序
    for n in range(0, N):
        for c in range(0, Car[n]):
            model.addConstr(float(ST[n][1]) <= uet[n][c][1], "StageOne_{}_{}".format(n, c))
            model.addConstr(uet[n][c][1] + float(ST[n][2]) <= uet[n][c][2], "StageTwo_{}_{}".format(n, c))
            model.addConstr(uet[n][c][2] + float(ST[n][3]) <= uet[n][c][3], "StageThree_{}_{}".format(n, c))
            model.addConstr(uet[n][c][3] <= 24, "FinishTime24_{}_{}".format(n, c))

    # 讓訂單的順序正常
    '''
    for n in range(0, N):
        for c in range(0, Car[n]- 1):
            model.addConstr(uet[n][c][1] <= uet[n][c+1][1], "StageOne_{}_{}".format(n, c))
            model.addConstr(uet[n][c][2] <= uet[n][c+1][2], "StageTwo_{}_{}".format(n, c))
            model.addConstr(uet[n][c][3] <= uet[n][c+1][3], "StageThree_{}_{}".format(n, c))
    '''
    # 每車 stage_i 若為空訂單，跟在上一個訂單後面結束?
    for n in range(0, N):
        for c in range(0, Car[n]):
            for i in range(1, 3):
                model.addConstr(uet[n][c][i+1] - uet[n][c][i] <= inf * ST[n][i+1],
                                "Stage_{}_{}_{}".format(n, c, i))

    # 一個階段只能使用一台機器            
    for n in range(0, N):
        for c in range(0, Car[n]):
            for i in range(1, 3+1):
                model.addConstr(gp.quicksum(x[n][c][i][m] for m in range(0, M)) == 1,
                                "OneMachine_{}_{}_{}".format(n, c, i))

    # 最多只能換一次機器且只能換到第0機台
    for n in range(0, N):
        for c in range(0, Car[n]):
#             model.addConstr(gp.quicksum(x[n][c][1][0] * x[n][c][2][m] for m in range(1, M)) +
#                             gp.quicksum(x[n][c][2][m] * x[n][c][3][0] for m in range(1, M)) <= 1)
            model.addConstr(gp.quicksum(gp.quicksum(x[n][c][i][m] * x[n][c][i+1][m] for m in range(1, M)) for i in range(1, 3)) 
                            + gp.quicksum(x[n][c][i][0] for i in range(1,4))== 2,
                            "TwoMachine_{}_{}_{}".format(n, c, i))
            model.addConstr(x[n][c][1][0] + x[n][c][3][0] <= 1) 

    # 如果 stage 之間沒有換機器，則要接續上一個 stage 做
    for n in range(0, N):
        for c in range(0, Car[n]):
            for i in range(1, 3):
                model.addConstr(uet[n][c][i+1] - uet[n][c][i] - ST[n][i+1] <= 
                                inf * (1 - gp.quicksum(x[n][c][i][m] * x[n][c][i+1][m] for m in range(0, M)))
                                , "ChangeMachine_{}_{}_{}".format(n, c, i))

    # 判斷任兩個車 stage 之間的先後順序 
    for n in range(0, N):
        for c in range(0, Car[n]):
            for i in range(1, 3+1):
                for j in range(0, N):
                    for k in range(0, Car[j]):
                        for l in range(1, 3+1): 
                            if (n != j or c != k or i != l) and (z_added[j][k][l][n][c][i] == False):
                                z_added[n][c][i][j][k][l] = True
                                for m in range(0, M):
                                    model.addConstr(x[n][c][i][m] * uet[n][c][i] + ST[j][l] - uet[j][k][l] <= inf * (1 - z[n][c][i][j][k][l][m])
                                                    , "SameMachine1_{}_{}_{}_{}_{}_{}_{}".format(n, c, i, j, k, l, m))
                                    model.addConstr(x[j][k][l][m] * uet[j][k][l] + ST[n][i] - uet[n][c][i] <= inf * z[n][c][i][j][k][l][m]
                                                    , "SameMachine2_{}_{}_{}_{}_{}_{}_{}".format(n, c, i, j, k, l, m))

    # stage_2 的生產不能進入 machine 0
    for n in range(0, N):
        for c in range(0, Car[n]):
            model.addConstr(x[n][c][2][Only_Cook] == 0
                            , "CantCook_{}_{}".format(n, c))

#         model.params.MIPGAP = 0.15
    model.setParam("OutputFlag",0)
    model.Params.TimeLimit = time_limit
    model.update()
    model.optimize()
    #print('model.objval: %d' %model.objval)

    # showing result
    result = pd.DataFrame()
    row_index = 0
    for n in range(N):
        for c in range(Car[n]):
            for i in range(1, 4):
                result.loc[row_index, 'order_index'] = n
                result.loc[row_index, 'car_index'] = c
                result.loc[row_index, 'stage'] = i
                result.loc[row_index, 'startTime'] = uet[n][c][i].x - ST[n][i]
                result.loc[row_index, 'endTime'] = uet[n][c][i].x
                for m in range(M):
                    if round(x[n][c][i][m].x, 1) == 1:
                        result.loc[row_index, 'machine_index'] = m
                row_index += 1

    # model for linear relaxation
#         model_re = model.relax()
#         model_re.Params.NonConvex = 2
#         model_re.optimize()
#         print('model_re.objval: %d' %model_re.objval)

    return result