from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from webapi.serializers import UserSerializer, GroupSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from ddtrace import tracer, patch_all, context

class home(APIView):

    def get(self, request):
        print(request)
        return Response({'data': 'get'})

    def post(self, request):
        data = request.data
        para = data['paragraph_details']
        parent_span_details = data.get('parent_span_details')
        print({'parent_span_details': parent_span_details})
        parent_span = None
        if parent_span_details:
            parent_span_id = parent_span_details.get("span_id")
            parent_trace_id = parent_span_details.get("trace_id")
            parent_span = context.Context(span_id=parent_span_id, trace_id=parent_trace_id)
        print(parent_span)
        span = tracer.start_span(
            name='post_method', service='django_api', child_of=parent_span, activate=True
            )
        time.sleep(2)
        
        span.finish()
        return Response({'data': 'post'})
    # return JsonResponse({'status': 'success'})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]