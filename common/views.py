from .models import (
    WalletAddress,
    Coin
)
from .serializers import (
    WalletAddressSerializer,
    ErrorSerializer,
    SuccessSerializer
)
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied


class WalletAddressApiView(GenericAPIView):
    """
    Spot prices.

    Get or set the current spot price.
    """

    model = WalletAddress
    serializer_class = WalletAddressSerializer
    error_serializer_class = ErrorSerializer
    queryset = WalletAddress.objects.all()

    def get_object(self):
        """Get latest spot price."""
        username = self.kwargs['username']
        coin = self.kwargs['coin']
        filters = {
            'coin__code': coin,
            'username': username,
            'is_active': True
        }
        return self.get_queryset().get(**filters)

    @swagger_auto_schema(responses={200: WalletAddressSerializer(), 404: ErrorSerializer()})
    def get(self, request, *args, **kwargs):
        """
        Get an address.

        Get the crypto wallet address for a uniquely-identified user and crypto pair.
        """
        try:
            wallet_address = self.get_object()
        except self.model.DoesNotExist:
            output_data = {
                'status': 'error',
                'error': 'User / crypto pairing not found'
            }
            output_serializer = self.error_serializer_class(data=output_data)
            output_serializer.is_valid()
            raise NotFound(output_serializer.data)
        output_serializer = self.serializer_class(wallet_address)
        return Response(output_serializer.data)

    @swagger_auto_schema(responses={200: SuccessSerializer(), 403: ErrorSerializer()})
    def delete(self, request, *args, **kwargs):
        """
        Delete an address.

        Delete the crypto wallet address for a uniquely-identified user and crypto pair.
        """
        self.permission_classes = ['rest_framework_api_key.permissions.HasAPIKey']
        try:
            self.get_object().delete()
        except self.model.DoesNotExist:
            output_data = {
                'status': 'error',
                'error': 'User / crypto pairing not found'
            }
            output_serializer = self.error_serializer_class(data=output_data)
            output_serializer.is_valid()
            raise NotFound(output_serializer.data)
        output_data = {'status': 'success'}
        output_serializer = SuccessSerializer(data=output_data)
        output_serializer.is_valid()
        return Response(output_serializer.data)

    @swagger_auto_schema(request_body=WalletAddressSerializer(), responses={200: SuccessSerializer(), 403: ErrorSerializer()})
    def post(self, request, *args, **kwargs):
        """
        Add or update address.

        Add or update a crypto address for a username and crypto pair.
        """
        self.permission_classes = ['rest_framework_api_key.permissions.HasAPIKey']
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = self.kwargs['username']
        coin_code = self.kwargs['coin']
        coin, _ = Coin.objects.get_or_create(code=coin_code)
        serializer.save(serializer.validated_data, username, coin)

        output_data = {'status': 'success'}
        output_serializer = SuccessSerializer(data=output_data)
        output_serializer.is_valid()
        return Response(output_serializer.validated_data, status=status.HTTP_201_CREATED)
