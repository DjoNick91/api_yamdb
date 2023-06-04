from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response


from .models import CustomUser
from .serializers import CreateUserSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    lookup_url_kwarg = "username"

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def me_about(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == "PATCH":
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@action(url_path="signup", detail=True)
@permission_classes([permissions.AllowAny])
def new_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
