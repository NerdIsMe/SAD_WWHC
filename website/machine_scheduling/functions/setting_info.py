from ..models import Document, StrongMachineInfo, WeakMachineInfo

def modifyStrongMachineNum(val) :
    current_num = StrongMachineInfo.objects.count()
    if current_num < val:# 新增強機台
        for i in range(current_num, val):
            new_machine = StrongMachineInfo()
            new_machine.index = i+2
            new_machine.save()

    elif current_num > val: # 要刪除強機台
        for i in range(val, current_num):
            new_machine = StrongMachineInfo.objects.get(index = i+2)
            new_machine.delete()

def getStartTime():
    start_times = []
    start_times.append(WeakMachineInfo.objects.get(index = 1).startTime)
    for machine in StrongMachineInfo.objects.all():
        start_times.append(machine.startTime)
    return start_times

def getRelativeStartTime():# 相對開始時間
    from datetime import datetime, date
    r_start_times = []
    time_delta = datetime.combine(date.today(), WeakMachineInfo.objects.get(index = 1).startTime) - datetime.combine(date.today(), datumTime())
    time_delta_minute = time_delta.days*1440 + time_delta.seconds/60
    r_start_times.append(time_delta_minute)
    for machine in StrongMachineInfo.objects.all():
        time_delta = datetime.combine(date.today(), machine.startTime) - datetime.combine(date.today(), datumTime())
        time_delta_minute = time_delta.days*1440 + time_delta.seconds/60
        r_start_times.append(time_delta_minute)
    return r_start_times

def datumTime():# 相對開始時間的基準點：7:30
    from datetime import time
    return time(hour = 0, minute=0)

def getNormalMachineNum():
    return StrongMachineInfo.objects.count()