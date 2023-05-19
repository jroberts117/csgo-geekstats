
from django.http import HttpResponse
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


from .geekmodels import Maps, MapRating, Geek, TiersData, Season
from .serializers import MapSerializer, MapImageSerializer, DataSerializer, MapRequestSerializer, AIRequestSerializer

import os, openai

@api_view(['GET','POST'])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))

def map_rating(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = MapSerializer(data=request.data)
        if serializer.is_valid():
            try:
                map_id = Maps.objects.get(idmap=serializer.data['map_id'])
                user_id = Geek.objects.get(geek_id=serializer.data['user_id'])
            except:
                return Response('Map or Geek is invalid', status=status.HTTP_400_BAD_REQUEST)                
            map_rating = serializer.data['rating']
            try:
                check_rating = MapRating.objects.get(map_id=map_id, geek_id=user_id)
                check_rating.rating = map_rating
                check_rating.save()
                return Response("Map has been updated", status=status.HTTP_201_CREATED)
            except:
                MapRating.objects.create(map=map_id, geek=user_id, rating=map_rating)
                return Response("Map created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def upload_image(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = MapImageSerializer(data=request.data)
        if serializer.is_valid():
            mid = serializer.data['mid']
            print('map is:'+str(mid))
            print('field is:'+serializer.data['type'])
            # mid = request.POST.get('mid')
            map_update = Maps.objects.get(idmap=mid)
            if  serializer.data['type'] == 'hero':
                map_update.hero_image  =  request.FILES.get('image')
            elif serializer.data['type'] == 'radar':
                map_update.radar  =  request.FILES.get('image')
            elif serializer.data['type'] == 'image2':
                map_update.image2  =  request.FILES.get('image')
            elif serializer.data['type'] == 'thumb':
                map_update.thumbnail  =  request.FILES.get('image')
            else:
                map_update.image3  =  request.FILES.get('image')

            # map_update.image2 = request.FILES.get('image2') if request.FILES.get('image2') else map_update.image2
            # map_update.thumbnail = request.FILES.get('thumb') if request.FILES.get('thumb') else map_update.thumbnail
            # print(dataMap[0])
            try:
                map_update.save()
            except:
                print('save failed:'+str(request.FILES.get('image')))
            return Response("map image has been updated", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def update_data(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            field = serializer.data['field']
            value = serializer.data['value']
            curr_user = serializer.data['uid']
            if field =='theme' or  field =='description' or field =='workshop_link':
                edit_map = Maps.objects.get(idmap=serializer.data['did'])
                setattr(edit_map, field, value)
                # edit_map[field] = value
                try:
                    edit_map.save()
                    return Response("Map updated", status=status.HTTP_200_OK)
                except:
                    print('update failed: '+serializer.data[field]+' = '+serializer.data[value])
                    return Response("invalid update", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_image(request):
    if request.method == 'POST':
        return HttpResponse("Not Implemented")
    elif request.method == 'GET':
        print("data",request.query_params)
        serializer = MapRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            mid = serializer.data['mid']
            map_name = serializer.data['map']
            if serializer.data['type'] == 'thumb':
                print('map is:'+map_name)
                print('field is:'+serializer.data['type'])
                map_image = Maps.objects.get(map=map_name)
                if map_image.thumbnail:
                    return Response(map_image.thumbnail.url, status=status.HTTP_200_OK)
                else :
                    return Response("No Map Image", status=status.HTTP_200_OK)
            else :
                return Response("Not Implemented", status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def ai_request(request):
    # Write me an api that processes input for an api call to openai
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        ai_response = 'Unknown error'
        Task = 'Recap the following "DataSet" data as a sportscaster. '
        Tone = 'Be very sacrcastic.  Use an accent like a New Yorker.  '
        Instructions = 'Call the "West1: Master" tier "Master" tier.  '
        if request.data['type'] == 'recap':
            serializer = AIRequestSerializer(data=request.data)
            Season_data = Season.objects.get(name=request.data['season_name'])
            dataset = serializers.serialize('json', TiersData.objects.values('player','tier','matchdate','kills','deaths','assists','kdr','alltime_kdr').filter(matchdate__gte=Season_data.start_date,matchdate__lte=Season_data.end_date))
            print(dataset)
            aiPrompt = []
            if serializer.is_valid():
                aiPrompt = [{"prompt": Task + Tone + Instructions + serializer.data['spec_inst'] + "\nDataSet: \n"}]
                aiPrompt.append(dataset)
                print('AI Prompt: ',aiPrompt)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No valid action requested", status=status.HTTP_400_BAD_REQUEST)
            
        openai.api_key = os.getenv("OPEN_AI_KEY")
        ai_response = openai.Completion.create(
        # model="text-davinci-001", # Best ,most expensive model
        #   model="text-curie-001",  # Good, reasonably priced model
            model="text-babbage-001", # Stupid but cheap
            # model="text-ada-001", # Stupid and fast but the cheapest model
            prompt=aiPrompt,
            temperature=0.7,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print('AI Response: ',ai_response)
    else:
        ai_response = 'unknown post error'
    return Response(ai_response, status=status.HTTP_200_OK)
        

