from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings as server_settings

from .models import Document, StrongMachineInfo, WeakMachineInfo

from .functions.setting_info import *
from .functions.merge_alg import *
import pandas as pd
import numpy as np
from pathlib import Path
# Create your views here.

def delete_file(document_date):
    import os
    data = Document.objects.get(date = document_date)
    data.file.delete()
    if data.schedule_is_done:
        os.remove(str(Path(server_settings.MEDIA_ROOT)) + data.date.strftime('\\documents\\results\\%Y-%m-%d_圖示化結果.html'))
        os.remove(str(Path(server_settings.MEDIA_ROOT)) + data.date.strftime('\\documents\\results\\%Y-%m-%d_產品排程資訊.xlsx'))
        os.remove(str(Path(server_settings.MEDIA_ROOT)) + data.date.strftime('\\documents\\results\\%Y-%m-%d_機台排程資訊.xlsx'))
    data.delete()
# Create your views here.

def home(request):
    homepage = True
    return render(request, 'home.html', locals())


def new_schedule_upload(request):
    if 'send_file' in request.POST:# and request.POST['datafile'] != '':
        # date:
        import datetime
        date_split = request.POST['schedule_date'].split('-')
        schdule_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        # data:
        datafile = request.FILES['data_file']
        if not datafile.name.endswith('.xlsx'):
            return HttpResponseRedirect('/error/檔案不正確，應上傳 excel 檔（.xlsx 結尾）/')
        datafile.name = schdule_date.strftime('%Y-%m-%d_')+'當日商品資訊.xlsx'
        raw_data = Document()
        raw_data.date = schdule_date
        raw_data.file = datafile
        raw_data.save()
        return HttpResponseRedirect('../view&check/%s/' %raw_data.date)

    return render(request, 'machine_scheduling/new_schedule/upload.html', locals())

def error_page(request, error_message):
    return render(request, 'website_error.html', locals())

def new_schedule_viewcheck(request, document_date):
    data = Document.objects.get(date = document_date)

    #try:
    xls = pd.ExcelFile(data.file)
    products_dict = pd.read_excel(xls, sheet_name=None, header=None)
    order_names = []; numbers_of_cars = []; product_tables = []
    car_processing_times = []
    for i in products_dict:
        tempt = products_dict[i]
        order_name = tempt.iloc[0, 0]; number_of_cars = tempt.iloc[0, 2] 
        tempt.columns = tempt.iloc[1, :]
        tempt.drop([0,1], inplace = True)
        tempt = tempt.fillna('-')

        order_names.append(order_name)
        numbers_of_cars.append(number_of_cars)
        product_tables.append(tempt)
        car_processing_time = tempt.iloc[:, 2].sum()/60; car_processing_times.append(car_processing_time)

    number_of_orders = len(products_dict)
    total_number_or_cars = sum(numbers_of_cars)
    order_processing_times = (list(map(lambda x, y: x*y, numbers_of_cars, car_processing_times)))

    product_info = zip(order_names, numbers_of_cars, product_tables)
    product_simple_info = zip(order_names, numbers_of_cars, car_processing_times, order_processing_times)
    
    total_processing_time = sum(order_processing_times)
    machine_startTimes = getStartTime()
    machine_names = ['機台' + str(i+1) for i in range(getNormalMachineNum()+1)]
    machine_names[0] += '(弱機台)'
    machine_info = zip(machine_names, machine_startTimes)
    if request.method == 'POST':
        print('receive request')
        if 'cancel_schedule' in request.POST:
            data.delete()
            return HttpResponseRedirect('/new_schedule/upload/')
        elif 'do_schedule' in request.POST:
            return HttpResponseRedirect('/new_schedule/schedule/%s/' %document_date)

    data.file.close()
    return render(request, 'machine_scheduling/new_schedule/viewcheck.html', locals())

    # except:
    #     data.file.close()
    #     delete_file(document_date)
    #     return HttpResponseRedirect('/error/檔案格式不正確，請檢查/')


def new_schedule_doschedule(request, document_date):

    from .functions.plot_schedule import PlotSchedule
    data = Document.objects.get(date = document_date)
    results = Apply(data.file, num_of_machineNormal = getNormalMachineNum(), start_time_list= getRelativeStartTime())
    data.file.close()
    figs = []; figs_html = []
    s = 0
    for i in results:
        s+=1
        figure = PlotSchedule(i, data.date, datumTime(), getNormalMachineNum())
        figs.append(figure)
        figs_html.append(figure.to_html(full_html=False, default_height=500, default_width=900))

    date = data.date
    #dir_path = str(Path(server_settings.MEDIA_ROOT)) + date.strftime('\\documents\\%Y\\%m\\%d\\')
    dir_path = str(Path(server_settings.MEDIA_ROOT)) + date.strftime('\\documents\\results\\%Y-%m-%d_')
    if request.method == 'POST':
        for i in range(len(results)):
            if str(i+1) in request.POST:
                Save(results[i], dir_path, powerTime = datumTime())
                figs[i].write_html(dir_path+'圖示化結果.html')
                break
        data.schedule_is_done = True
        data.save()
        return HttpResponseRedirect('/history_schedule/%s/' %(document_date))

    fig_info = zip(range(1, len(results)+1), figs_html)
    return render(request, 'machine_scheduling/new_schedule/doschedule.html', locals())


