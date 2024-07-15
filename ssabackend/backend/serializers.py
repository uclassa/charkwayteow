from rest_framework import serializers
from . import models as m


class EventSerializer(serializers.ModelSerializer):
    """
    Event serializer for admin use
    Honestly not really needed anymore since we're now using django admin
    """
    participants = serializers.SlugRelatedField(
        many=True,
        queryset=m.Member.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = m.Event
        fields = '__all__'
        read_only_fields = ('image_id',)


class EventPublicSerializer(serializers.ModelSerializer):
    """
    This is the read only serializer for the website and telebot
    The image field pulls from the cached url on the model so google drive storage is not called
    Otherwise api calls will be very very slowwwwwwww
    """
    image = serializers.CharField(source='image_id')

    class Meta:
        model = m.Event
        fields = ('title', 'start_date', 'end_date', 'venue', 'description', 'image', 'link')
        read_only_fields = fields


class FamilySerializer(serializers.ModelSerializer):
    """
    TODO: Make this into a read only serializer without members for the telebot
    """

    class Meta:
        model = m.Family
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer for admin use
    Also not really needed anymore since we're now using django admin
    """
    events = serializers.SlugRelatedField(
        many=True,
        queryset=m.Event.objects.all(),
        slug_field='title'
    )

    family = serializers.SlugRelatedField(
        queryset=m.Family.objects.all(),
        slug_field='fam_name'
    )
    
    class Meta:
        model = m.Member
        fields = '__all__'
        read_only_fields = ('image_id',)


class PhotoSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the photo submission model
    """
    class Meta:
        model = m.PhotoSubmission
        fields = ('member', 'description', 'number_of_people', 'image')