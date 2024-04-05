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
        read_only_fields = ('image_url',)


class EventPublicSerializer(serializers.ModelSerializer):
    # This is the read only serializer for the website and telebot
    # The image field pulls from the cached url on the model so google drive storage is not called
    # Otherwise api calls will be very very slowwwwwwww
    image = serializers.URLField(source='image_url')

    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'venue', 'description', 'image', 'link')


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
        read_only_fields = ('profile_image_url',)


'''
TODO: Since the only editable data by users is their profile, only the member serializer needs to be modified to output the image url but take in an image. Cross that bridge when we get there.
'''