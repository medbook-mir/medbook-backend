from django.db import models
from drf_spectacular.utils import (
    extend_schema, 
    OpenApiResponse, 
    OpenApiExample, 
    OpenApiParameter, 
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework import serializers



def image_upload_schema(operation_id, summary, description, tag, response_properties):
    """
    Decorator for image upload methods (not classes)
    """
    return extend_schema(
        operation_id=operation_id,
        summary=summary,
        description=description,
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'The image file to upload (jpg, jpeg, png, gif, webp)'
                    }
                },
                'required': ['image']
            }
        },
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': response_properties
                },
                description=f'{summary} successful',
                examples=[
                    OpenApiExample(
                        'Successful Upload',
                        value={
                            'id': 1,
                            'image': '/media/images/doctor_123.jpg',
                            f'{tag.lower()}_id': 1
                        }
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'image': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'example': ['This field is required.']
                        }
                    }
                },
                description='Validation errors'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string', 
                            'example': 'Authentication credentials were not provided.'
                        }
                    }
                },
                description='Authentication required'
            )
        },
        tags=[tag]
    )


def document_upload_schema(**kwargs):
    """
    Dynamic schema decorator for document upload views.
    
    Args:
        model_name (str): Name of the model (e.g., 'doctor', 'clinic')
        model_display_name (str): Display name for the model (e.g., 'Doctor', 'Clinic')
        additional_fields (dict): Additional fields specific to the model
        tag (str): Tag name for swagger grouping
    """
    model_name = kwargs.get('model_name', 'document')
    model_display_name = kwargs.get('model_display_name', model_name.title())
    additional_fields = kwargs.get('additional_fields', {})
    tag = kwargs.get('tag', f'{model_display_name}s')
    
    base_response_properties = {
        'id': {'type': 'integer', 'description': f'ID of the {model_name} document'},
        'name': {'type': 'string', 'description': 'Name of the document'},
        'file': {'type': 'string', 'description': 'URL of the uploaded file'},
        'file_size': {'type': 'integer', 'description': 'File size in bytes'},
        'mime_type': {'type': 'string', 'description': 'MIME type of the file'},
        'max_file_size_mb': {'type': 'integer', 'description': 'Maximum file size in MB'},
        'allowed_file_types': {'type': 'string', 'description': 'Allowed file types'},
        'is_active': {'type': 'boolean', 'description': 'Whether the document is active'},
        'created_at': {'type': 'string', 'format': 'date-time', 'description': 'Creation timestamp'},
        'updated_at': {'type': 'string', 'format': 'date-time', 'description': 'Last update timestamp'},
    }
    
    response_properties = {**base_response_properties, **additional_fields}
    
    base_request_properties = {
        'file': {
            'type': 'string',
            'format': 'binary',
            'description': f'The {model_name} document file to upload (pdf, jpg, jpeg, png, doc, docx)'
        },
        'name': {
            'type': 'string',
            'description': 'Name of the document',
            'example': f'{model_name}_license.pdf'
        },
        'max_file_size_mb': {
            'type': 'integer',
            'description': 'Maximum file size in MB',
            'default': 10
        }
    }
    
    additional_request_fields = kwargs.get('additional_request_fields', {})
    request_properties = {**base_request_properties, **additional_request_fields}
    
    base_example_data = {
        'id': 1,
        'name': f'{model_name}_license.pdf',
        'file': f'/media/documents/{model_name}/license.pdf',
        'file_size': 2048576,
        'mime_type': 'application/pdf',
        'max_file_size_mb': 10,
        'allowed_file_types': 'pdf,jpg,jpeg,png,doc,docx',
        'is_active': True,
        'created_at': '2025-08-07T10:38:00+05:00',
        'updated_at': '2025-08-07T10:38:00+05:00',
    }
    
    additional_example_data = kwargs.get('additional_example_data', {})
    example_data = {**base_example_data, **additional_example_data}
    
    def decorator(view_class):
        view_class.get = extend_schema(
            operation_id=f'{model_name}_document_list',
            summary=f'List {model_display_name} Documents',
            description=f'Retrieve a list of all active documents for {model_display_name.lower()}s',
            responses={
                200: OpenApiResponse(
                    response={
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': response_properties
                        }
                    },
                    description=f'List of {model_name} documents',
                    examples=[
                        OpenApiExample(
                            'Example Response',
                            value=[example_data]
                        )
                    ]
                ),
                401: OpenApiResponse(
                    response={
                        'type': 'object',
                        'properties': {
                            'detail': {'type': 'string', 'example': 'Authentication credentials were not provided.'}
                        }
                    },
                    description='Authentication required'
                )
            },
            tags=[tag]
        )(view_class.get)
        
        view_class.get_single = extend_schema(
            operation_id=f'{model_name}_document_retrieve',
            summary=f'Retrieve {model_display_name} Document',
            description=f'Retrieve a specific {model_name} document by ID',
            parameters=[
                OpenApiParameter(
                    name='pk',
                    type=int,
                    location=OpenApiParameter.PATH,
                    description=f'{model_display_name} document ID'
                )
            ],
            responses={
                200: OpenApiResponse(
                    response={
                        'type': 'object',
                        'properties': response_properties
                    },
                    description=f'{model_display_name} document details',
                    examples=[
                        OpenApiExample(
                            'Example Response',
                            value=example_data
                        )
                    ]
                ),
                404: OpenApiResponse(
                    response={
                        'type': 'object',
                        'properties': {
                            'error': {'type': 'string', 'example': f'{model_display_name}Document not found'}
                        }
                    },
                    description='Document not found'
                ),
                401: OpenApiResponse(description='Authentication required')
            },
            tags=[tag]
        )(view_class.get_single)
        
        view_class.post = extend_schema(
            operation_id=f'{model_name}_document_create',
            summary=f'Upload {model_display_name} Document',
            description=f'Upload a new document for {model_display_name.lower()}. Requires authentication.',
            request={
                'multipart/form-data': {
                    'type': 'object',
                    'properties': request_properties,
                    'required': ['file', 'name']
                }
            },
            responses={
                201: OpenApiResponse(
                    response={
                        'type': 'object',
                        'properties': response_properties
                    },
                    description=f'{model_display_name} document uploaded successfully',
                    examples=[
                        OpenApiExample(
                            'Example Response',
                            value=example_data
                        )
                    ]
                ),
                400: OpenApiResponse(
                    response={
                        'type': 'object',
                        'properties': {
                            'field_name': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'example': ['This field is required.']
                            }
                        }
                    },
                    description='Validation errors'
                ),
                401: OpenApiResponse(description='Authentication required')
            },
            tags=[tag]
        )(view_class.post)
        
        view_class.patch = extend_schema(
            operation_id=f'{model_name}_document_update',
            summary=f'Update {model_display_name} Document',
            description=f'Partially update an existing {model_name} document',
            parameters=[
                OpenApiParameter(
                    name='pk',
                    type=int,
                    location=OpenApiParameter.PATH,
                    description=f'{model_display_name} document ID'
                )
            ],
            request={
                'multipart/form-data': {
                    'type': 'object',
                    'properties': {k: v for k, v in request_properties.items() if k != 'file'},
                    'additionalProperties': {
                        'file': {
                            'type': 'string',
                            'format': 'binary',
                            'description': 'New file (optional)'
                        }
                    }
                }
            },
            responses={
                200: OpenApiResponse(
                    response={
                        'type': 'object',
                        'properties': response_properties
                    },
                    description=f'{model_display_name} document updated successfully',
                    examples=[
                        OpenApiExample(
                            'Example Response',
                            value={**example_data, 'updated_at': '2025-08-07T10:45:00+05:00'}
                        )
                    ]
                ),
                400: OpenApiResponse(description='Validation errors'),
                404: OpenApiResponse(description='Document not found'),
                401: OpenApiResponse(description='Authentication required')
            },
            tags=[tag]
        )(view_class.patch)
        
        return view_class
    
    return decorator


class BaseSwaggerDocs:
    def __init__(self, model_class, serializer_class, model_name=None):
        self.model_class = model_class
        self.serializer_class = serializer_class
        self.model_name = model_name or model_class._meta.verbose_name.title()
        self._cached_serializers = {}

    def _clean_model_name(self):
        return ''.join(x.title() for x in self.model_name.replace('_', ' ').split())

    def _make_ref_name(self, suffix: str) -> str:
        return f"{self._clean_model_name()}{suffix}"

    def _pluralize_model_name(self):
        """Smart pluralization that avoids double plurals."""
        model_name = self.model_name
        
        if model_name.lower().endswith('s'):
            return model_name
        
        if model_name.lower().endswith('y'):
            return model_name[:-1] + 'ies'
        elif model_name.lower().endswith(('ch', 'sh', 'x', 'z')):
            return model_name + 'es'
        else:
            return model_name + 's'

    def _resolve_serializer_class(self):
        sc = self.serializer_class
        if isinstance(sc, str):
            try:
                from django.utils.module_loading import import_string
                sc = import_string(sc)
            except Exception as e:
                raise RuntimeError(f"Could not resolve serializer class '{self.serializer_class}': {e}")
        return sc

    def get_model_fields_params(self):
        """Generate OpenAPI query parameters based on model fields"""
        
        params = []
        for field in self.model_class._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)):
                params.append(OpenApiParameter(
                    name=field.name,
                    description=f"Filter by {field.verbose_name or field.name}",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    required=False
                ))
            elif isinstance(field, (models.IntegerField, models.BigIntegerField)):
                params.append(OpenApiParameter(
                    name=field.name,
                    description=f"Filter by {field.verbose_name or field.name}",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    required=False
                ))
            elif isinstance(field, models.BooleanField):
                params.append(OpenApiParameter(
                    name=field.name,
                    description=f"Filter by {field.verbose_name or field.name}",
                    type=OpenApiTypes.BOOL,
                    location=OpenApiParameter.QUERY,
                    required=False
                ))
            elif isinstance(field, models.DateTimeField):
                params.extend([
                    OpenApiParameter(
                        name=f"{field.name}__gte",
                        description=f"Filter {field.verbose_name or field.name} from date",
                        type=OpenApiTypes.DATETIME,
                        location=OpenApiParameter.QUERY,
                        required=False
                    ),
                    OpenApiParameter(
                        name=f"{field.name}__lte",
                        description=f"Filter {field.verbose_name or field.name} to date",
                        type=OpenApiTypes.DATETIME,
                        location=OpenApiParameter.QUERY,
                        required=False
                    )
                ])
            elif isinstance(field, models.ForeignKey):
                params.append(OpenApiParameter(
                    name=f"{field.name}_id",
                    description=f"Filter by {field.verbose_name or field.name} ID",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    required=False
                ))

        params.extend([
            OpenApiParameter(name='page', description="Page number", type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter(name='page_size', description="Number of items per page", type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter(name='search', description="Search term", type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter(name='ordering', description="Field to order by (prefix with '-' for descending)",
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, required=False),
        ])

        return params

    def get_list_response_serializer(self):
        """Return a cached List response serializer for this model."""
        
        key = "list"
        if key in self._cached_serializers:
            return self._cached_serializers[key]

        serializer_class = self._resolve_serializer_class()
        ref_name = self._make_ref_name("ListResponse")

        attrs = {
            "success": serializers.BooleanField(default=True, help_text="Request success status"),
            "message": serializers.CharField(default="Resources retrieved successfully", help_text="Response message"),
            "data": serializers.ListSerializer(child=serializer_class(), help_text="List of resources"),
            "count": serializers.IntegerField(help_text="Total count of resources"),
            "Meta": type("Meta", (), {"ref_name": ref_name})
        }
        Dyn = type(f"{ref_name}Serializer", (serializers.Serializer,), attrs)
        self._cached_serializers[key] = Dyn
        return Dyn

    def get_detail_response_serializer(self):
        """Return a cached Detail response serializer for this model."""
        
        key = "detail"
        if key in self._cached_serializers:
            return self._cached_serializers[key]

        serializer_class = self._resolve_serializer_class()
        ref_name = self._make_ref_name("DetailResponse")

        attrs = {
            "success": serializers.BooleanField(default=True, help_text="Request success status"),
            "message": serializers.CharField(default="Resource retrieved successfully", help_text="Response message"),
            "data": serializer_class(help_text="Resource data"),
            "Meta": type("Meta", (), {"ref_name": ref_name})
        }
        Dyn = type(f"{ref_name}Serializer", (serializers.Serializer,), attrs)
        self._cached_serializers[key] = Dyn
        return Dyn

    def get_error_response_serializer(self, status_code=400):
        """Return an Error response serializer for a specific HTTP status."""
        
        cache_key = f"error_{status_code}"
        if cache_key in self._cached_serializers:
            return self._cached_serializers[cache_key]

        ref_name = self._make_ref_name(f"ErrorResponse{status_code}")

        error_examples = {
            400: {
                "success": False,
                "message": "Validation failed",
                "errors": {
                    "field_name": ["This field is required."],
                    "email": ["Enter a valid email address."]
                }
            },
            401: {
                "success": False,
                "message": "Authentication credentials were not provided",
                "errors": {
                    "detail": ["Authentication credentials were not provided."]
                }
            },
            403: {
                "success": False,
                "message": "Permission denied",
                "errors": {
                    "detail": ["You do not have permission to perform this action."]
                }
            },
            404: {
                "success": False,
                "message": "Not found",
                "errors": {
                    "detail": ["Not found."]
                }
            },
            409: {
                "success": False,
                "message": "Conflict",
                "errors": {
                    "detail": ["Resource already exists."]
                }
            },
            500: {
                "success": False,
                "message": "Internal server error",
                "errors": {
                    "detail": ["An error occurred while processing your request."]
                }
            }
        }

        example = error_examples.get(status_code, error_examples[400])
        
        attrs = {
            "success": serializers.BooleanField(
                default=example["success"], 
                help_text="Request success status (always false for errors)"
            ),
            "message": serializers.CharField(
                default=example["message"], 
                allow_blank=True, 
                help_text="Error message describing what went wrong"
            ),
            "errors": serializers.DictField(
                child=serializers.ListField(child=serializers.CharField()),
                default=example["errors"],
                help_text="Detailed error information organized by field"
            ),
            "Meta": type("Meta", (), {"ref_name": ref_name})
        }

        Dyn = type(f"{ref_name}Serializer", (serializers.Serializer,), attrs)
        self._cached_serializers[cache_key] = Dyn
        return Dyn

    def get_create_response_serializer(self):
        """Return a cached Create response serializer for this model."""
        
        key = "create"
        if key in self._cached_serializers:
            return self._cached_serializers[key]

        serializer_class = self._resolve_serializer_class()
        ref_name = self._make_ref_name("CreateResponse")

        attrs = {
            "success": serializers.BooleanField(default=True, help_text="Request success status"),
            "message": serializers.CharField(default="Resource created successfully", help_text="Response message"),
            "data": serializer_class(help_text="Created resource data"),
            "Meta": type("Meta", (), {"ref_name": ref_name})
        }
        Dyn = type(f"{ref_name}Serializer", (serializers.Serializer,), attrs)
        self._cached_serializers[key] = Dyn
        return Dyn

    def get_delete_response_serializer(self):
        """Return a cached Delete response serializer for this model."""
        
        key = "delete"
        if key in self._cached_serializers:
            return self._cached_serializers[key]

        serializer_class = self._resolve_serializer_class()
        ref_name = self._make_ref_name("DeleteResponse")
        
        attrs = {
            "success": serializers.BooleanField(default=True, help_text="Request success status"),
            "message": serializers.CharField(default="Resource deleted successfully", help_text="Response message"),
            "data": serializer_class(help_text="Deleted resource data"),
            "Meta": type("Meta", (), {"ref_name": ref_name})
        }
        Dyn = type(f"{ref_name}Serializer", (serializers.Serializer,), attrs)
        self._cached_serializers[key] = Dyn
        return Dyn

    def get_common_error_responses(self):
        """Return mapping for 400, 401, 403, 404, 500 with unique serializers."""
        return {
            400: self.get_error_response_serializer(400),
            401: self.get_error_response_serializer(401),
            403: self.get_error_response_serializer(403),
            404: self.get_error_response_serializer(404),
            409: self.get_error_response_serializer(409),
            500: self.get_error_response_serializer(500),
        }

    def list_docs(self):
        common_errors = self.get_common_error_responses()
        tags = [self._pluralize_model_name()]
        return extend_schema(
            summary=f"List {self._pluralize_model_name()}",
            description=f"Retrieve a list of {self.model_name.lower()} with optional filtering and pagination",
            parameters=self.get_model_fields_params(),
            responses={
                200: self.get_list_response_serializer(),
                400: common_errors[400],
                401: common_errors[401],
                403: common_errors[403],
            },
            tags=tags
        )

    def create_docs(self):
        common_errors = self.get_common_error_responses()
        tags = [self._pluralize_model_name()]
        return extend_schema(
            summary=f"Create {self.model_name}",
            description=f"Create a new {self.model_name.lower()}",
            responses={
                201: self.get_create_response_serializer(),
                400: common_errors[400],
                401: common_errors[401],
                403: common_errors[403],
                409: common_errors[409],
            },
            tags=tags
        )

    def retrieve_docs(self):
        common_errors = self.get_common_error_responses()
        tags = [self._pluralize_model_name()]
        return extend_schema(
            summary=f"Retrieve {self.model_name}",
            description=f"Retrieve details of a specific {self.model_name.lower()}",
            responses={
                200: self.get_detail_response_serializer(),
                401: common_errors[401],
                403: common_errors[403],
                404: common_errors[404],
            },
            tags=tags
        )

    def update_docs(self):
        common_errors = self.get_common_error_responses()
        tags = [self._pluralize_model_name()]
        return extend_schema(
            summary=f"Update {self.model_name}",
            description=f"Update a specific {self.model_name.lower()}",
            responses={
                200: self.get_detail_response_serializer(),
                400: common_errors[400],
                401: common_errors[401],
                403: common_errors[403],
                404: common_errors[404],
                409: common_errors[409],
            },
            tags=tags
        )

    def partial_update_docs(self):
        common_errors = self.get_common_error_responses()
        tags = [self._pluralize_model_name()]
        return extend_schema(
            summary=f"Partial Update {self.model_name}",
            description=f"Partially update a specific {self.model_name.lower()}",
            responses={
                200: self.get_detail_response_serializer(),
                400: common_errors[400],
                401: common_errors[401],
                403: common_errors[403],
                404: common_errors[404],
                409: common_errors[409],
            },
            tags=tags
        )

    def delete_docs(self):
        common_errors = self.get_common_error_responses()
        tags = [self._pluralize_model_name()]
        return extend_schema(
            summary=f"Delete {self.model_name}",
            description=f"Delete a specific {self.model_name.lower()}",
            responses={
                200: self.get_delete_response_serializer(),
                401: common_errors[401],
                403: common_errors[403],
                404: common_errors[404],
            },
            tags=tags
        )

