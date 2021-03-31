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

######################### SETUP THE DATE AND SEASON PICKLIST FOR EVERY PAGE ##########################################################
        
        eventdates = []                                                         # eventdates is the pick list of dates and seasons
        eventdates.append('Overall')
        eventdates.append('------ Seasons')
        data = list(Season.objects.values().order_by('-start_date'))            # Gets all the season date ranges
        for i in data:
            eventdates.append(i['name'])                                        # Adds the season names to the picklist
        eventdates.append('------ Individual Dates')
        dates = list(TiersData.objects.values('matchdate').order_by('-matchdate').distinct())
        for i in dates:
            eventdates.append(str(i['matchdate']))                              # Adds the individual dates to the picklist
        request.session['eventdates'] = eventdates                              # Set the session to have all the dates for the ddlb

######################### PROCESS REQUEST IF A DATE OR SEASON WAS SELECTED AND SET SESSION INFO ##########################################
        
        if request.method == 'POST':                                            # If a date or season was picked
            if request.session.get('selector',False) and request.POST.get('dateList',False):
                request.session['selector'] = request.POST['dateList']          # Set a session object for the item selected
                if validate(request.POST['dateList']):                          # catch if it is a date or not
##                    temp = datetime.datetime.strptime(request.POST['dateList'], '%Y-%m-%d')  # Test to see if it is a date
                    request.session['start_date'] = request.POST['dateList']    # Set the session date ranges to the same thing
                    request.session['end_date'] = request.POST['dateList']
                else:                                                           # If they picked text
                    if request.POST['dateList'] == 'Overall':                   # If they want everything get the max range from the db
                        request.session['start_date'] = eventdates[-1]
                        request.session['end_date'] = '2100-01-01'
                    else:                                                       # If it's a season, then work with that
##                        print('we received '+request.POST['dateList']+' and will try and look it up')
                        data = list(Season.objects.values().filter(name=request.POST['dateList']))
                        request.session['start_date'] = data[0]['start_date'].strftime('%Y-%m-%d')   # Set the dates
                        request.session['end_date'] = data[0]['end_date'].strftime('%Y-%m-%d')
                        request.session['season'] = data[0]['name']
##            except:
##                print('we are not in the stats so skip this stuff')     # If that fails, it's a page not working with data range data

################ PROCESS THE PAGE IF NO DATE OR SEASON WAS SELECTED CAPTURE OTHER SESSION DATA  #######################################
        else:
            if not request.session.get('start_date',False):                     # If we don'thave a start date, this is the first load so default to the last play date
##                print('NOT a POST and the start date is NOT already set')
                request.session['start_date'] = str(dates[0]['matchdate'])
                request.session['end_date'] = str(dates[0]['matchdate'])
                request.session['selector'] = str(dates[0]['matchdate'])

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
        
