from rest_framework.viewsets import ModelViewSet
from ..models import ModelSurface
from .serializers import SurfaceSerializer
from rest_framework.response import Response

from ..Calculate.scraping import create_data_for_db
from ..Calculate.calculate import ExpressionParse

import json

class SurfaceViewSet(ModelViewSet):
    queryset = ModelSurface.objects.all()
    serializer_class = SurfaceSerializer
   
    calcs: list[ExpressionParse] = [] # экземпляры калькуляторов для latex-выражений

    def list(self, request):

        indx = int(request.GET.get('indx', -1))
        if indx == -1:
            # Парсинг и добавление данных в бд (если бд пустая)
            len_mod = len(ModelSurface.objects.all())
            if not len_mod:
                for row in create_data_for_db():
                    new_surface = ModelSurface(**row)
                    new_surface.save()
            
            # Извлечение latex-выражений из бд в класс-калькулятор
            for row in ModelSurface.objects.all():
                self.calcs.append(ExpressionParse(row.latex_expr))

            def create_response(attrs=['name', 'latex_img', 'img', 'text', 'link']) -> dict[str, list[str]]:
                # Получение общей информации о поверхностях из бд
                response = {attr: [] for attr in attrs}
                for row in ModelSurface.objects.all():
                    for attr in attrs:
                        response[attr].append(getattr(row, attr))
                return response

            return Response(create_response())
        else:
            return Response({'points': self.calcs[indx].calculate_points(), 
                             'parameters': self.calcs[indx].parameters})
        
    def create(self, request):
        indx = int(request.GET.get('indx', -1))
        parameters: dict[str, float] = {k: float(v) for k, v in json.loads(request.body).items()}

        return Response({'points': self.calcs[indx].calculate_points(**parameters)})