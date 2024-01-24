from rest_framework import viewsets, \
    generics  # по дефолту импортируется rest_framework.serializers import ModelSerializer, но я оставил так для единобразия

from vehicle.models import Car, Moto, Milage
from vehicle.serliazers import CarSerializer, MotoSerializer, MilageSerializer, MotoMilageSerializer, \
    MotoCreateSerializer


class CarViewSet(viewsets.ModelViewSet):  # ТУТ СОЗДАЕМ ВЬЮСЕТ, А ДАЛЬШЕ ДЖЕНЕРИКИ
    serializer_class = CarSerializer  # Обязательное поле
    queryset = Car.objects.all()  # указывается для того, чтобы objects работал корректно


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer  # Обязательное поле


class MotoListAPIView(generics.ListAPIView):  # Для просмотра всех мотоциклов
    serializer_class = MotoSerializer  # Обязательное поле
    queryset = Moto.objects.all()  # Обязательное поле


class MotoRetrieveAPIView(generics.RetrieveAPIView):  # Для просмотра одного мотоцикла
    serializer_class = MotoSerializer  # Обязательное поле
    queryset = Moto.objects.all()  # Обязательное поле


class MotoUpdateAPIView(generics.UpdateAPIView):  # Для обновления мото
    serializer_class = MotoSerializer  # Обязательное поле
    queryset = Moto.objects.all()  # Обязательное поле


class MotoDestroyAPIView(generics.DestroyAPIView):  # Для удаления мото
    queryset = Moto.objects.all()  # Обязательное поле


class MilageCreateAPIView(generics.CreateAPIView):
    serializer_class = MilageSerializer


class MotoMilageListAPIView(generics.ListAPIView):
    queryset = Milage.objects.filter(moto__isnull=False)
    serializer_class = MotoMilageSerializer
