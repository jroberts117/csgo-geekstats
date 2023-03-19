
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


from .geekmodels import Maps, MapRating, Geek
from .serializers import MapSerializer, MapImageSerializer, DataSerializer, MapRequestSerializer

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
