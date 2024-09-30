from rest_framework import serializers
from . import models as m


class EventPublicSerializer(serializers.ModelSerializer):
    """
    This is the read only serializer for the website and telebot
    The image field pulls from the cached url on the model so google drive storage is not called
    Otherwise api calls will be very very slowwwwwwww
    """
    image = serializers.CharField(source='image_url')

    class Meta:
        model = m.Event
        fields = ('title', 'start_date', 'end_date', 'venue', 'description', 'image', 'link')
        read_only_fields = fields


class FamilySerializer(serializers.ModelSerializer):
    """
    Read only serializer for the family model used for leaderboard
    """

    class Meta:
        model = m.Family
        fields = ('id', 'fam_name', 'points')


class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer
    TODO: Implement proper image handling
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


class GroupChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the group chat model
    """
    class Meta:
        model = m.GroupChat
        fields = '__all__'
