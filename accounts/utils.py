from drf_yasg.inspectors import SwaggerAutoSchema
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.utils import force_serializer_instance
from django.urls import reverse_lazy


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    use_update = False

    def __init__(self, view, path, method, components, request, overrides, operation_keys=None):
        print(3*'herereeee')
        if str(reverse_lazy('schema-redoc')) in request.get_full_path():
            self.use_update = True
        super(CustomSwaggerAutoSchema, self).__init__(view, path, method, components, request, overrides, operation_keys=None)

    def get_operation(self, operation_keys):
        operation = super(CustomSwaggerAutoSchema, self).get_operation(operation_keys)
        if self.use_update:
            payload = dict()
            for i in self.get_payload_parameters():
                payload[i['name']] = i['type']
            template_context = {
                "request_url": self.request._request.build_absolute_uri(self.path),
                "method": self.method,
                "payload": payload,
            }
        
            operation.update({
                'x-code-samples':[
                    {
                        "lang": "curl",
                        "source": render_to_string('curl_sample.html', template_context)
                    },
                    {
                        "lang": "python",
                        "source": render_to_string('python_sample.html', template_context)
                    }
                ]
            })
       
        return operation
    
    def get_payload_parameters(self):
        """Return the payload parameters accepted by this view.

        :rtype: list[openapi.Parameter]
        """
        serializer = force_serializer_instance(self.get_request_serializer())
        serializer_parameters = []
        if serializer is not None:
            serializer_parameters = self.serializer_to_parameters(serializer, in_=openapi.IN_FORM)

        return serializer_parameters
