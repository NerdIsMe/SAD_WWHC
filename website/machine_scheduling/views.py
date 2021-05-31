from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Document, StrongMachineInfo, WeakMachineInfo
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