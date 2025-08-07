from rest_framework import serializers
from .models import TopUpOrder, TopUpProduct, Game

class TopUpOrderSerializer(serializers.ModelSerializer):
    gamename = serializers.CharField(write_only=True)
    game_id = serializers.CharField(write_only=True)
    product_name = serializers.CharField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    class Meta:
        model = TopUpOrder
        fields = [
            'gamename', 'game_id', 'product_name', 'product_id', 'product_price',
            'user_email', 'status', 'created_at'
        ]
        read_only_fields = ('status', 'created_at')

    def validate(self, data):
        try:
            game = Game.objects.get(name=data['gamename'], game_id=data['game_id'])
        except Game.DoesNotExist:
            raise serializers.ValidationError("Game does not exist.")

        if not game.is_active:
            raise serializers.ValidationError("Game is not active.")

        try:
            product = TopUpProduct.objects.get(id=data['product_id'], name=data['product_name'], game=game)
        except TopUpProduct.DoesNotExist:
            raise serializers.ValidationError("Product not found for this game.")

        if product.price != data['product_price']:
            raise serializers.ValidationError("Product price mismatch.")

        data['product'] = product
        return data

    def create(self, validated_data):
        validated_data.pop('gamename')
        validated_data.pop('game_id')
        validated_data.pop('product_name')
        validated_data.pop('product_id')
        validated_data.pop('product_price')
        return TopUpOrder.objects.create(**validated_data)
