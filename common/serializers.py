from .models import WalletAddress
from rest_framework import serializers


class WalletAddressSerializer(serializers.ModelSerializer):
    """Wallet Serializer."""

    class Meta:
        """Meta information."""

        model = WalletAddress
        fields = [
            'address'
        ]

    def save(self, validated_data, username, coin):
        """Save the address."""
        wallet_data = {
            'address': validated_data.get('address'),
            'username': username,
            'coin': coin
        }
        wallet_address = WalletAddress(**wallet_data)
        wallet_address.save()
        return wallet_address


class ErrorSerializer(serializers.Serializer):
    """Error Serializer."""

    status = serializers.CharField()
    error = serializers.CharField()


class SuccessSerializer(serializers.Serializer):
    """Success mesasge."""

    status = serializers.CharField()
