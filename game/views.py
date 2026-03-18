from rest_framework import viewsets
from .models import Player, Route, Checkpoint, GameSession
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated



class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class CheckpointViewSet(viewsets.ModelViewSet):
    queryset = Checkpoint.objects.all()
    serializer_class = CheckpointSerializer


class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    nickname = request.data.get('nickname')

    if not username or not password or not nickname:
        return Response({'error': 'Username, password and nickname are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    Player.objects.create(user=user, nickname=nickname)

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_race(request):
    route_id = request.data.get('route_id')
    
    player = Player.objects.get(user=request.user)
    route = Route.objects.get(id=route_id)
    
    session = GameSession.objects.create(player=player, route=route, start_time=timezone.now())
    serializer = GameSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_race(request):
    session_id = request.data.get('session_id')
    deliveries = request.data.get('deliveries', 0)
    time_taken = request.data.get('time_taken', 0)
    
    session = GameSession.objects.get(id=session_id, player__user=request.user)
    
    session.completed = True
    session.end_time = timezone.now()
    session.deliveries_made = deliveries
    
    #Scoring logic 
    session.score = (deliveries * 100) - int(time_taken)  # Example: 100 points per delivery minus time penalty
    session.save()
    
    return Response({'message': 'Race completed!', 'score': session.score}, status=status.HTTP_200_OK)  
