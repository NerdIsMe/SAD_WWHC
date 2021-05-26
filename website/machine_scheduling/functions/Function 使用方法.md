# Function 使用方法
\## 兩個井字號為 python 執行檔

\### 三個井字號為 function 名稱

## plot_schedule.py
### Plot_Schedule(result, order_data, method = '',Y = 2020, M = 10, D = 21, h = 7, m = 30)
- result(pd.DataFrame): 各個方法排程的結果，包含以下 columns:
    - machine_index
    - order_index
    - car_index
    - startTime
    - endTime
- order_data(pd.DataFrame): testing_data，用來加入 order deadline & 計算 number of delay orders
- 工作開工時間 (with default value), optional:
    - Y: year
    - M: month
    - D: day
    - h: hour
    - m: minute
- method(str), optional:
    - 排程使用的方法，將會顯示在 plot title

## caculate_error.py
### caculate_error(testing_data, gurobi_result, algori_result)
- testing_data(pd.DataFrame): 用來加入 order deadline & 計算 number of delay orders
- gurobi_result(pd.DataFrame): gurobi方法排程的結果，包含以下 columns:
    - machine_index
    - order_index
    - car_index
    - startTime
    - endTime
- algori_result(pd.DataFrame): 非gurobi方法排程的結果，包含以下 columns:
    - machine_index
    - order_index
    - car_index
    - startTime
    - endTime