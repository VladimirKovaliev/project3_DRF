from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, \
    generics  # по дефолту импортируется rest_framework.serializers import ModelSerializer, но я оставил так для единобразия
from rest_framework.permissions import IsAuthenticated, AllowAny

from vehicle.models import Car, Moto, Milage
from vehicle.paginators import VehiclePaginator
from vehicle.permissions import IsOwnerOrStaff
from vehicle.serliazers import CarSerializer, MotoSerializer, MilageSerializer, MotoMilageSerializer, \
    MotoCreateSerializer
from vehicle.tasks import check_milage


class CarViewSet(viewsets.ModelViewSet):  # ТУТ СОЗДАЕМ ВЬЮСЕТ, А ДАЛЬШЕ ДЖЕНЕРИКИ
    serializer_class = CarSerializer  # Обязательное поле
    queryset = Car.objects.all()  # указывается для того, чтобы objects работал корректно
    permission_classes = [AllowAny]


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer  # Обязательное поле
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()


class MotoListAPIView(generics.ListAPIView):  # Для просмотра всех мотоциклов
    serializer_class = MotoSerializer  # Обязательное поле
    queryset = Moto.objects.all()  # Обязательное поле
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):  # Для просмотра одного мотоцикла
    serializer_class = MotoSerializer  # Обязательное поле
    queryset = Moto.objects.all()  # Обязательное поле


class MotoUpdateAPIView(generics.UpdateAPIView):  # Для обновления мото
    serializer_class = MotoSerializer  # Обязательное поле
    queryset = Moto.objects.all()  # Обязательное поле
    permission_classes = [IsOwnerOrStaff]


class MotoDestroyAPIView(generics.DestroyAPIView):  # Для удаления мото
    queryset = Moto.objects.all()  # Обязательное поле


class MilageCreateAPIView(generics.CreateAPIView):
    serializer_class = MilageSerializer

    def perform_create(self, serializer):
        new_milage = serializer.save()
        if new_milage.car:
            check_milage.delay(new_milage.car_id, 'Car')
        else:
            check_milage.delay(new_milage.moto_id, 'Moto')


class MilageListAPIView(generics.ListAPIView):
    serializer_class = MilageSerializer
    queryset = Milage.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('car', 'moto')
    ordering_fields = ('year',)


class MotoMilageListAPIView(generics.ListAPIView):
    queryset = Milage.objects.filter(moto__isnull=False)
    serializer_class = MotoMilageSerializer
