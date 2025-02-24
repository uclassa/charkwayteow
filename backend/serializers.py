from rest_framework import serializers
from . import models as m


class EventPublicSerializer(serializers.ModelSerializer):
    """
    This is the read only serializer for the website
    The image field pulls from the cached url on the model so google drive storage is not called
    Otherwise api calls will be very very slowwwwwwww
    """
    image = serializers.CharField(source='image_url')

    class Meta:
        model = m.Event
        fields = ('title', 'start_date', 'end_date', 'venue', 'description', 'image', 'link')
        read_only_fields = fields


class EventAPISerializer(serializers.ModelSerializer):
    """
    This is the read only serializer for the telebot.
    """
    class Meta:
        model = m.Event
        fields = ('title', 'start_date', 'end_date', 'venue', 'description', 'link', 'event_image_folder_url')
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


class PhotoSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the photo submission model
    """
    class Meta:
        model = m.PhotoSubmission
        fields = ('member', 'description', 'number_of_people', 'image', 'score')


class GroupChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the group chat model
    """
    class Meta:
        model = m.GroupChat
        fields = '__all__'


class ExcoSerializer(serializers.ModelSerializer):
    """
    Serializer for the exco member model
    """
    class Meta:
        model = m.ExcoMember
        fields = ("id", "name", "role", "year", "major", "photo", "alt_photo", "alt")
