def PlotSchedule(result, the_date, datum_time, number_of_strongMachine, gap_minute_pass = 30):
    import pandas as pd
    from datetime import datetime, date, time, timedelta
    import plotly.express as px
    import plotly.graph_objects as go
    
    result.fillna('-', inplace = True)
    y_axis = [number_of_strongMachine + 1.5, 0.5]
    # create new pd.DataFrame for plotly
    result = result.sort_values(by = ['產品', '車', '開始時間'], ascending = [True, True, True]).reset_index(drop = True)
    work_day = datetime.combine(the_date, datum_time)
    df = pd.DataFrame()
    df['機台'] = result.機台.astype('int')#.astype('str')
    df['orderIndex'] = result.產品
    df['carIndex'] = result.車.astype('int')
    df['start'] = list(map(lambda x: work_day + timedelta(minutes = x), result.開始時間))
    df['start_minute'] = result.開始時間#list(map(lambda x,y: work_day + timedelta(minutes = (x+y)/2), result.結束時間, result.開始時間))
    df['finish_minute'] = result.結束時間
    df['finish'] = list(map(lambda x: work_day + timedelta(minutes = x), result.結束時間))
    df['hover_start'] = list(map(lambda x: x.strftime('%H:%M'), df['start']))
    df['hover_finish'] =  list(map(lambda x: x.strftime('%H:%M'), df.finish))
    df['step'] = result.製程
    df['temperature'] = list(map(lambda x: '/' if x== '-' else int(x), result.溫度))
    df = df.sort_values(by = ['orderIndex', 'carIndex', 'start_minute'], ascending = [True, True, True]).reset_index(drop = True)
    # 建立 plotly legend
    #display(order_data)
    order_plotly_legend = []
    endTimes = []
    for index in df.orderIndex:
        endTime = (work_day + timedelta(minutes = int(df[df.orderIndex == index]['finish_minute'].max()))).strftime('%H:%M')
        label = str(index) + ', 完成時間：' + endTime
        order_plotly_legend.append(label)
        endTimes.append(endTime)
        
    df['訂單'] = order_plotly_legend
    df['hover_訂單'] = df.orderIndex
    df['hover_endTime'] = endTimes
    
    plot_df = df.iloc[0:0].copy()
    # 初始值為第一筆
    accumulate = df.loc[0]
    accumulate.step = '<br>    '+ accumulate.step + ' %s度, %s ~ %s' %(accumulate.temperature, accumulate.hover_start, accumulate.hover_finish)
    for i in range(1, len(df)): 
        if df.loc[i].機台 == 0 and df.loc[i]['finish_minute'] - df.loc[i]['start_minute'] < gap_minute_pass:
            df.loc[i, '機台'] = df.loc[i-1].機台
        if accumulate.機台 == df.loc[i].機台 and accumulate.orderIndex == df.loc[i].orderIndex and accumulate.carIndex == df.loc[i].carIndex and accumulate.finish == df.loc[i].start:
            accumulate.finish = df.loc[i].finish
            accumulate.hover_finish = df.loc[i].hover_finish
            accumulate.finish_minute = df.loc[i].finish_minute
            if df.loc[i].temperature == '/':
                accumulate.step += '<br>    ' + df.loc[i].step + ', %s ~ %s' %(df.loc[i].hover_start, df.loc[i].hover_finish)
            else:
                accumulate.step += '<br>    ' + df.loc[i].step + ' %s度, %s ~ %s' %(df.loc[i].temperature, df.loc[i].hover_start, df.loc[i].hover_finish)
        else:
            plot_df.loc[len(plot_df)] = accumulate
            accumulate = df.loc[i]
            
            accumulate.step = '<br>    '+ accumulate.step + ' %s度, %s ~ %s' %(df.loc[i].temperature, df.loc[i].hover_start, df.loc[i].hover_finish)
        if i == len(df)-1:
            plot_df.loc[len(plot_df)] = accumulate
    
    
    
    #df = df.sort_values(by = 'Machine')
    fig = px.timeline(plot_df, x_start="start", x_end="finish", y="機台", color="訂單", title = '於 %s 完成所有訂單' %(max(endTimes)),
                      range_y = y_axis, custom_data = ['hover_訂單', 'carIndex', '機台', 'step', 'hover_start', 'hover_finish', 'hover_endTime'])
    # 修改 hover data
    # 第一行 order_name + 車 + machine index
    # 第二行 包含的階段與步驟(目前沒有)
    # 第三行 開始時間 ~ 結束時間
    fig.update_traces(hovertemplate = ("%{customdata[0]}-第%{customdata[1]}車, 機台%{customdata[2]}<br>"
                                        + "處理時間: %{customdata[4]} ~ %{customdata[5]}<br><br>" + "步驟: %{customdata[3]}<br>" 
                                       + "<extra></extra>"))#+ "所有車 %{customdata[6]} 完成"

    #fig.update_yaxes(autorange="reversed")
    fig.update_traces(width=0.7)
    
    # 加上car index & order_index
    plot_df['middle'] = list(map(lambda x,y: work_day + timedelta(minutes = (x+y)/2), plot_df['start_minute'], plot_df['finish_minute']))
    annots =  list(map(lambda i: dict(x=plot_df.loc[i, 'middle'],y=plot_df.loc[i, '機台'],
                                text=(plot_df.loc[i, 'orderIndex']+'-'+str(int(plot_df.loc[i, 'carIndex']))), showarrow=False, font=dict(color='white')), plot_df.index))

    # plot figure
    fig['layout']['annotations'] = annots

    fig.update_layout(yaxis_tickformat = ',d')
    # fig.show()
    return fig