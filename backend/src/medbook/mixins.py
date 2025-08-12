import logging
from django.http import Http404
from django.db.models import Q
from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated

from .swagger_docs import BaseSwaggerDocs
from .paginations import StandardPagination


logger = logging.getLogger(__name__)


class SwaggerMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        swagger_model = getattr(cls, "swagger_model", None) or getattr(cls, "model", None)
        if not swagger_model:
            return

        serializer_for_docs = getattr(cls, "serializer_class", None)
        if not serializer_for_docs:
            return

        model_name = getattr(cls, "swagger_model_name", None)
        if not model_name:
            model_name = swagger_model.__name__

        swagger_docs = BaseSwaggerDocs(swagger_model, serializer_for_docs, model_name)

        crud_methods = {
            'list': swagger_docs.list_docs(),
            'create': swagger_docs.create_docs(),
            'retrieve': swagger_docs.retrieve_docs(),
            'update': swagger_docs.update_docs(),
            'partial_update': swagger_docs.partial_update_docs(),
            'destroy': swagger_docs.delete_docs(),
        }

        for method_name, decorator in crud_methods.items():
            if hasattr(cls, method_name):
                original_method = getattr(cls, method_name)
                if callable(original_method):
                    decorated_method = decorator(original_method)
                    setattr(cls, method_name, decorated_method)


class ResponseMixin:
    def success_response(self, data=None, message=None, code=None, count=None, **kwargs):
        status_code = code or status.HTTP_200_OK
        response_message = message or "Operation completed successfully"
        
        response_data = {
            "success": True,
            "code": status_code,
            "message": response_message,
            "data": data if data is not None else []
        }
        
        if count is not None:
            response_data["count"] = count
        
        response_data.update(kwargs)
        
        return Response(response_data, status=status_code)
    
    def error_response(self, message=None, errors=None, code=None, **kwargs):
        status_code = code or status.HTTP_400_BAD_REQUEST
        response_message = message or "An error occurred"
        
        response_data = {
            "success": False,
            "code": status_code,
            "message": response_message,
            "errors": errors if errors is not None else {}
        }
        
        response_data.update(kwargs)
        
        return Response(response_data, status=status_code)
    
    def handle_exception(self, exc):
        try:
            if isinstance(exc, Http404):
                return self.error_response(
                    message="Resource not found",
                    errors={"detail": ["The requested resource was not found."]},
                    code=status.HTTP_404_NOT_FOUND
                )
            elif isinstance(exc, ValidationError):
                return self.error_response(
                    message="Validation failed",
                    errors=exc.detail if hasattr(exc, 'detail') else {"detail": [str(exc)]},
                    code=status.HTTP_400_BAD_REQUEST
                )
            elif isinstance(exc, PermissionDenied):
                return self.error_response(
                    message="Permission denied",
                    errors={"detail": ["You do not have permission to perform this action."]},
                    code=status.HTTP_403_FORBIDDEN
                )
            elif isinstance(exc, NotAuthenticated):
                return self.error_response(
                    message="Authentication required",
                    errors={"detail": ["Authentication credentials were not provided."]},
                    code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                response = super().handle_exception(exc)
                
                if hasattr(response, 'data') and hasattr(response, 'status_code'):
                    return self.error_response(
                        message="An error occurred",
                        errors=response.data if isinstance(response.data, dict) else {"detail": [str(response.data)]},
                        code=response.status_code
                    )
                
                return response
                
        except Exception as e:
            logger.error(f"Error in exception handler: {str(e)}", exc_info=True)
            return self.error_response(
                message="Internal server error",
                errors={"detail": ["An unexpected error occurred."]},
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FilterMixin:
    def get_filter_params(self):
        return {
            key: value for key, value in self.request.query_params.items()
            if key not in ['page', 'page_size', 'ordering', 'search']
        }
    
    def apply_filters(self, queryset):
        filter_params = self.get_filter_params()
        
        for param, value in filter_params.items():
            if not value:
                continue
                
            if hasattr(self, f'filter_{param}'):
                queryset = getattr(self, f'filter_{param}')(queryset, value)
            else:
                queryset = self._apply_field_filter(queryset, param, value)
        
        return queryset
    
    def _apply_field_filter(self, queryset, param, value):
        try:
            return queryset.filter(**{param: value})
        except (models.FieldDoesNotExist, ValueError, TypeError):
            pass
        
        if param.endswith('_id'):
            field_name = param.replace('_id', '')
            try:
                return queryset.filter(**{field_name: value})
            except (models.FieldDoesNotExist, ValueError, TypeError):
                pass
    
    def _has_field(self, model, field_name):
        try:
            model._meta.get_field(field_name)
            return True
        except models.FieldDoesNotExist:
            return False
    
    def apply_search(self, queryset):
        search_term = self.request.query_params.get('search')
        if search_term and hasattr(self, 'search_fields'):
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f"{field}__icontains": search_term})
            queryset = queryset.filter(search_query)
        return queryset
    
    def apply_ordering(self, queryset):
        ordering = self.request.query_params.get('ordering')
        if ordering:
            ordering_fields = [field.strip() for field in ordering.split(',')]
            valid_fields = []
            for field in ordering_fields:
                field_name = field.lstrip('-')
                if self._has_field(queryset.model, field_name):
                    valid_fields.append(field)
            
            if valid_fields:
                return queryset.order_by(*valid_fields)
        
        if hasattr(self, 'ordering'):
            return queryset.order_by(*self.ordering)
        
        return queryset.order_by('-created_at')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.apply_filters(queryset)
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)
        return queryset
    

class BaseController(SwaggerMixin, ResponseMixin, FilterMixin):
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset() if hasattr(super(), 'get_queryset') else self.queryset
        queryset = self.apply_filters(queryset)
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)
        
        return queryset


class BaseViewSet(BaseController, viewsets.ModelViewSet):
    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["pk"])
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                count=queryset.count(),
                message="Resources retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(
                data=serializer.data,
                message="Resource retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            if hasattr(self, 'create'):
                self.create(serializer.validated_data)
            
            self.perform_create(serializer)
            
            return self.success_response(
                data=serializer.data,
                message="Resource created successfully",
                code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            
            if hasattr(self, 'update'):
                self.update(instance, serializer.validated_data)
            
            self.perform_update(serializer)
            
            return self.success_response(
                data=serializer.data,
                message="Resource updated successfully"
            )
        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if hasattr(self, 'delete'):
                self.delete(instance)
            
            instance_data = self.get_serializer(instance).data
            self.perform_destroy(instance)
            
            return self.success_response(
                data=instance_data,
                message="Resource deleted successfully",
                code=status.HTTP_200_OK
            )
        except Exception as e:
            return self.handle_exception(e)


class ReadOnlyViewSet(BaseController, viewsets.ReadOnlyModelViewSet):
    
    def list(self, request, *args, **kwargs):
        """List resources with pagination"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                count=queryset.count(),
                message="Resources retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single resource"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(
                data=serializer.data,
                message="Resource retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)


class BaseListViewSet(BaseController, mixins.ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                count=queryset.count(),
                message="Resources retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)


class BaseCreateViewSet(BaseController, viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            if hasattr(self, 'create'):
                self.create(serializer.validated_data)
            
            self.perform_create(serializer)
            
            return self.success_response(
                data=serializer.data,
                message="Resource created successfully",
                code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)


class BaseRetrieveViewSet(BaseController, viewsets.ViewSet):
    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["pk"])
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response(
                data=serializer.data,
                message="Resource retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)


class BaseUpdateAPIViewSet(BaseController, viewsets.ViewSet):
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            
            if hasattr(self, 'update'):
                self.validate_update(instance, serializer.validated_data)
            
            self.perform_update(serializer)
            
            return self.success_response(
                data=serializer.data,
                message="Resource updated successfully"
            )
        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class BaseDestroyAPIView(BaseController, viewsets.ViewSet):
    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["pk"])
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if hasattr(self, 'delete'):
                self.validate_delete(instance)
            
            instance_data = self.serializer_class(instance).data
            self.perform_destroy(instance)
            
            return self.success_response(
                data=instance_data,
                message="Resource deleted successfully"
            )
        except Exception as e:
            return self.handle_exception(e)


class BaseCreateRetrieveViewSet(BaseController, viewsets.ViewSet):
    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["pk"])
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            if hasattr(self, 'create'):
                self.create(serializer.validated_data)
            
            self.perform_create(serializer)
            
            return self.success_response(
                data=serializer.data,
                message="Resource created successfully",
                code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)
        
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response(
                data=serializer.data,
                message="Resource retrieved successfully"
            )
        except Exception as e:
            return self.handle_exception(e)

