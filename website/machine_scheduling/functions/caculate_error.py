def Calculate_error(testing_data, gurobi_result, algori_result):
    import pandas as pd
    gurobi_result = gurobi_result[gurobi_result.startTime != gurobi_result.endTime]
    algori_result = algori_result[algori_result.startTime != algori_result.endTime]
    # merge result and order_data
    testing_data = testing_data.rename(columns = {'order':'order_index'})
    gurobi_result = gurobi_result.merge(testing_data[['order_index', 'finish']]).sort_values(by = ['finish','order_index'], ascending = [True, True])#.sort_index(kind='mergesort')
    algori_result = algori_result.merge(testing_data[['order_index', 'finish']]).sort_values(by = ['finish','order_index'], ascending = [True, True])#.sort_index(kind='mergesort')
    # count number of delay orders
    gurobi_order_end_times = gurobi_result.groupby('order_index').max()   
    algori_order_end_times = algori_result.groupby('order_index').max()    
    gurobi_num_of_delay = ((gurobi_order_end_times.endTime - gurobi_order_end_times.finish) > 0.0001).sum()
    algori_num_of_delay = ((algori_order_end_times.endTime - algori_order_end_times.finish) > 0.0001).sum()
    return (algori_num_of_delay - gurobi_num_of_delay)/len(testing_data)