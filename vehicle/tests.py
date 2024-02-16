from rest_framework import status
from rest_framework.test import APITestCase

from vehicle.models import Car


class VehicleTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_car(self):
        """ Тестирование создания машины """
        data = {
            'title': 'Test',
            'description': 'Test'
        }
        response = self.client.post(
            '/cars/',
            data=data
        )
        #сразу проверка на статус (при созданиии статутс 201)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # на этом этапе можно запустить тест командой python3 manage.py test
        # далее сравниваем результат
        self.assertEqual(
            response.json(),
            # следующую строку можно скопировать из вывода запуска теста
            {'id': 1, 'milage': [], 'title': 'Test', 'description': 'Test', 'owner': None}
        )

        # и финальный тест чтобы убедиться, что всё сохраняется в базу
        self.assertTrue(
            Car.objects.all().exists()
        )

    def test_list_car(self):
        """ Тестирование вывода списка машин """

        Car.objects.create(
            title='list test',
            description='list test'
        )

        response = self.client.get(
            '/cars/'
        )
        #сразу проверка 200 статус или нет
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        #сравниваем
        self.assertEqual(
            response.json(),
            [{'id': 1, 'milage': [], 'title': 'list test', 'description': 'list test', 'owner': None}]
        )


