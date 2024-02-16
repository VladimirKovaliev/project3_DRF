from rest_framework import serializers

from vehicle.models import Car, Moto, Milage
from vehicle.valitdators import TitleValidator


class MilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milage
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    # first нужнен, тк в модели ordering стоит -year, и для получения первого нужно писать first
    last_milage = serializers.IntegerField(source='milage.all.first.milage', read_only=True)
    milage = MilageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = '__all__'  # либо ('title', 'description')


class MotoSerializer(serializers.ModelSerializer):
    last_milage = serializers.SerializerMethodField()

    class Meta:
        model = Moto
        fields = '__all__'  # либо ('title', 'description')

    def get_last_milage(self, instance):
        if instance.milage.all().first():
            return instance.milage.all().first().milage
        return 0


class MotoMilageSerializer(serializers.ModelSerializer):
    moto = MotoSerializer()

    class Meta:
        model = Milage
        fields = ('milage', 'year', 'moto',)


class MotoCreateSerializer(serializers.ModelSerializer):
    milage = MilageSerializer(many=True)

    class Meta:
        model = Moto
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Moto.objects.all())
        ]

    def create(self, validated_data):
        milage = validated_data.pop('milage')

        moto_item = Moto.objects.create(**validated_data)

        for m in milage:
            Milage.objects.create(**m, moto=moto_item)

        return moto_item
