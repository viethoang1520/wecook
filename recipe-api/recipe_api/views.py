from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Recipe
from .serializers import RecipeSerializer
from .services import RecipeService
from rest_framework.views import APIView

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['POST'])
    def upload_video(self, request):
        try:
            video_file = request.FILES.get('video')
            if not video_file:
                return Response(
                    {'error': 'No video file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create recipe instance
            recipe = Recipe.objects.create(video=video_file)
            
            # Process video
            service = RecipeService(recipe)
            service.process_video()
            
            # Return response
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello"})
