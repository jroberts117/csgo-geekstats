from django.http import HttpResponse
import stats.query as qry
import sys
import datetime
from .geekmodels import TiersData, Season

## State is used in the middleware as a way to track default values 
class state:
    def __init__(self):
        self.start_date = '2019-01-01'
        self.end_date = '2030-12-31'
        self.compare = 'date(eventTime)'
        self.dateType = 'season'
        self.value = 0
        self.operator = '='
        self.clause = ''
        self.page = ''
        self.season = ''

def validate(date_text):
    try:
        temp = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False

## EventData object is called on each request by Django        
class EventData(object):
    def __init__(self, get_response):
        self.get_response = get_response
        return(None)
        
    def __call__(self, request):
        if request.method == 'POST' and 'dateType' in request.POST:                                            # If a date or season was picked or range
            if request.POST['dateType'] == 'season':
                season_dates = (Season.objects.values('name','start_date','end_date').filter(name=request.POST['dateList']))
                request.session['start_date'] = season_dates[0]['start_date'].strftime('%Y-%m-%d')    # Set the session date ranges to be the season selected
                request.session['end_date'] = season_dates[0]['end_date'].strftime('%Y-%m-%d')
                request.session['selector'] = request.POST['dateList']
            elif request.POST['dateType'] == 'match':
                request.session['start_date'] = (datetime.datetime.strptime(request.POST['dateList'], '%m-%d-%Y')).strftime('%Y-%m-%d')    # Set the session date ranges to the match date selected
                request.session['end_date'] = (datetime.datetime.strptime(request.POST['dateList'], '%m-%d-%Y')).strftime('%Y-%m-%d')
                request.session['selector'] = request.POST['dateList']
            elif request.POST['dateType'] == 'range':
                request.session['start_date'] = request.POST['start_date']    # Set the session date ranges to the range selected
                request.session['end_date'] = request.POST['end_date']
            request.session['datetype'] = request.POST['dateType']
            
                
################ PROCESS THE PAGE IF NO DATE OR SEASON WAS SELECTED CAPTURE OTHER SESSION DATA  #######################################
        else:
            if not request.session.get('start_date',False):                     # If we don'thave a start date, this is the first load so default to the last play date
                last_date = list(SeasonMatch.objects.aggregate(Max('match_date')))
                request.session['start_date'] = str(last_date[0]['match_date'])
                request.session['end_date'] = str(last_date[0]['match_date'])
                request.session['datetype'] = 'season'


            if request.GET.get('pid') != None:
                request.session['playerid'] = request.GET.get('pid')    #  Capture the playerid
            else:
                request.session['playerid'] = ''
            if request.GET.get('wid') != None:
                request.session['weaponid'] = request.GET.get('wid')    # Capture the weaponid
            else:
                request.session['weaponid'] = ''
            if request.GET.get('mid') != None:
                request.session['mapid'] = request.GET.get('mid')       # Capture the mapid
            else:
                request.session['mapid'] = ''
            if request.GET.get('oid') != None:                          # Capture the opponentid
                request.session['opponentid'] = request.GET.get('oid')
            else:
                request.session['opponentid'] = ''
            
        response = self.get_response(request)
        return(response)
        
