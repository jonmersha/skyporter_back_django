from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        # Added phone_number to the registration fields
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone_number']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        # Added phone_number to the profile view fields
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']