from django.shortcuts import get_object_or_404
from rest_framework.views import Request, Response, status

from rest_framework.pagination import PageNumberPagination



class ListBaseView(PageNumberPagination):
    def list(self, request: Request) -> Response:
        queryset = self.view_queryset.all()
        result_page = self.paginate_queryset(queryset, request)
        serializer = self.view_serializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
    
class CreateBaseView:
    def create(self, request: Request) -> Response:
        serializer = self.view_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    
class RetrieveBaseView:
    def retrieve(
        self, request: Request, *args: tuple, **kwargs: dict
    ) -> Response:
        url_param = kwargs.get(self.url_params_name)
        obj = get_object_or_404(self.view_queryset, pk=url_param)
        serializer = self.view_serializer(obj)

        return Response(serializer.data, status.HTTP_200_OK)


class UpdateBaseView:
    def update(
        self, request: Request, *args: tuple, **kwargs: dict
    ) -> Response:
        url_param = kwargs.get(self.url_params_name)
        obj = get_object_or_404(self.view_queryset, pk=url_param)

        serializer = self.view_serializer(obj, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class DestroyBaseView:
    def destroy(
        self, request: Request, *args: tuple, **kwargs: dict
    ) -> Response:
        url_param = kwargs.get(self.url_params_name)

        obj = get_object_or_404(self.view_queryset, pk=url_param)
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)