from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style ={'input_style':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_keywords = {
            'password': {'write_only': True}
        }
        
    def save(self):
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        
        if password != password_confirm:
            raise serializers.ValidationError({'errors':'Password and Confirm password doesn\'t match'})
        
        userquery_set = User.objects.filter(email=self.validated_data['email'])
        
        if userquery_set.exists():
            raise serializers.ValidationError({'errors':'Email already exists'})
        
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account