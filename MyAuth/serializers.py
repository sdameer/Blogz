from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class Usercreateserialzer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'email', 'password']