'''
Views for recipe APIs.
'''
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    '''View for manage recipe APIs.'''
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Retreive recipes for authenticated user.'''
        # protip: override method, return recipes only for authenticated user
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''Return the serializer class for request.'''
        # protip: override method, return diff serializer based on endpoint
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''Create new recipe.'''
        # when we create a new recipe through this viewset, we call this
        # method which updates user value to authenticated user
        serializer.save(user=self.request.user)
