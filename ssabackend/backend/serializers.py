from rest_framework import serializers
from .models import Event, Family, Member


class EventSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        many=True,
        queryset=Member.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Event
        fields = '__all__'


class EventPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('id', 'participants')


class FamilySerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True,
        queryset=Member.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Family
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    events = serializers.SlugRelatedField(
        many=True,
        queryset=Event.objects.all(),
        slug_field='title'
    )

    family = serializers.SlugRelatedField(
        queryset=Family.objects.all(),
        slug_field='fam_name'
    )
    
    class Meta:
        model = Member
        fields = '__all__'