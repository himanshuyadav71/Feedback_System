from rest_framework import serializers
from django.utils import timezone

class UserInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    date_of_birth = serializers.DateField(required=True, input_formats=['%Y-%m-%d'])

    def validate_email(self, value):
        # only allow emails at acropolis.in
        try:
            domain = value.split('@', 1)[1].lower()
        except IndexError:
            raise serializers.ValidationError("Enter a valid email address.")
        if domain != "acropolis.in":
            raise serializers.ValidationError("Email must be at @acropolis.in domain.")
        return value

    def validate_date_of_birth(self, value):
        today = timezone.localdate()
        if value >= today:
            raise serializers.ValidationError("date_of_birth must be in the past.")
        age_years = (today - value).days // 365
        if age_years < 15:
            raise serializers.ValidationError("age must be at least 15 years.")
        return value