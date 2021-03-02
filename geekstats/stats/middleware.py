from django.http import HttpResponse
import stats.query as qry
import sys
import datetime

class state:
    def __init__(self):
        self.start_date = '2019-01-01'
        self.end_date = '2030-12-31'
        self.compare = 'date(eventTime)'
        self.value = 0
        self.operator = '='
        self.clause = ''
        self.page = ''
        self.season = ''
        
class EventData(object):
    def __init__(self, get_response):
        self.get_response = get_response
        return(None)
        
    def __call__(self, request):
#        print("hello middleware", file=sys.stderr)
        newstate = state()
        eventdates = []
        #Get Date picklist info
        eventdates.append('Overall')
        eventdates.append('------ Seasons')
        data = qry.get_query('seasons',state)
        for i in data:
            eventdates.append(str(i[0]))
        eventdates.append('------ Individual Dates')
        dates = qry.get_query('values',newstate)
        dates.sort(reverse=True)
        for i in dates:
            eventdates.append(str(i[0]))
        if request.method == 'POST':
            try:
                request.session['selector'] = request.POST['dateList']
                try:
                    print('POST and the selector is a date')
                    temp = datetime.datetime.strptime(request.POST['dateList'], '%Y-%m-%d')
                    request.session['start_date'] = request.POST['dateList']
                    request.session['end_date'] = request.POST['dateList']
                except:
                    print('POST and the selector is NOT a date')
                    data = []
                    data = qry.get_query('seasons',state)
                    if request.POST['dateList'] == 'Overall':
                        request.session['start_date'] = eventdates[-1]
                        request.session['end_date'] = '2100-01-01'
                    else:
                        for i in data:
                            if i[0] == request.POST['dateList']:
                                print('we are processing')
                                request.session['start_date'] = str(i[1])
                                request.session['end_date'] = str(i[2])
                                request.session['season'] = i[0]
            except:
                print('we are not in the stats so skip this stuff')
        else:
            try:
                print('NOT a POST and the start date is already set')
                test = request.session['start_date']

            except:
                print('NOT a POST and the start date is NOT already set')
                request.session['start_date'] = str(dates[0][0])
                request.session['end_date'] = str(dates[0][0])
                request.session['selector'] = str(dates[0][0])

                
        request.session['eventdates'] = eventdates

        if request.method == 'GET':
            if request.GET.get('pid') != None:
                request.session['playerid'] = request.GET.get('pid')
            else:
                request.session['playerid'] = ''
            if request.GET.get('wid') != None:
                request.session['weaponid'] = request.GET.get('wid')
            else:
                request.session['weaponid'] = ''
            if request.GET.get('mid') != None:
                request.session['mapid'] = request.GET.get('mid')
            else:
                request.session['mapid'] = ''
            if request.GET.get('oid') != None:
                request.session['opponentid'] = request.GET.get('oid')
            else:
                request.session['opponentid'] = ''

                
            
        response = self.get_response(request)
        return(response)
        
