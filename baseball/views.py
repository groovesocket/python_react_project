from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from .models import BaseballStats
from openai import OpenAI
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import BaseballStatsSerializer, PlayerDescriptionSerializer
from fractionProject.settings import OPENAI_API_KEY


class BaseballStatsView(generics.ListCreateAPIView):
    serializer_class = BaseballStatsSerializer

    def get_queryset(self):
        return BaseballStats.objects.all()


class PlayerDescription:
    def __init__(self, player_id):
        stat = BaseballStats.objects.get(id=player_id)
        self.player = stat.player
        self.description = "No player description available"

        # LLM generated description
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user",
                           "content": f"Write a short biography of {self.player}, a baseball player."}]
            )

            self.description = completion.choices[0].message.content
        except Exception as e:
            pass

class PlayerDescriptionView(APIView):
    def get_object(self, id):
        return PlayerDescription(player_id=id)

    # cache player description for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, id):
        player_object = self.get_object(id=id)
        serializer = PlayerDescriptionSerializer(player_object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateStatsView(APIView):
    def post(self, request, id, *args, **kwargs):
        try:
            player = BaseballStats.objects.get(id=id)
            if isinstance(request.data, dict):
                player.hits = request.data.get('hits', player.hits)
            else:
                player.hits = request.data
            player.save(update_fields=['hits'])
            serializer = BaseballStatsSerializer(player)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BaseballStats.DoesNotExist:
            return Response({"error": "Stats could not be updated."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
