from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Menu, MenuProducts, MenuCategories
from .serializers import MenuSerializer, MenuProductSerializer, MenuCategorySerializer

class GetMenuItems(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class AddMenuItem(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class EditMenuItem(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'id'

class DeleteMenuItem(generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'id'

class AddMenuProduct(APIView):
    def post(self, request, id):
        menu = generics.get_object_or_404(Menu, id=id)
        serializer = MenuProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(menu=menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteMenuProduct(APIView):
    def delete(self, request, id, productId):
        menu_product = generics.get_object_or_404(MenuProducts, menu_id=id, product_id=productId)
        menu_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetMenuCategories(generics.ListAPIView):
    queryset = MenuCategories.objects.all()
    serializer_class = MenuCategorySerializer

class AddMenuCategory(generics.CreateAPIView):
    queryset = MenuCategories.objects.all()
    serializer_class = MenuCategorySerializer
