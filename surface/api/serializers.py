from rest_framework.serializers import ModelSerializer
from ..models import ModelSurface

class SurfaceSerializer(ModelSerializer):
    class Meta:
        model = ModelSurface
        fields = ('id, name')