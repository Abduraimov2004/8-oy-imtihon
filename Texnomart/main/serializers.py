from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Product, Image, Comment, ProductAttribute, AttributeKey, AttributeValue




class CategorySerializer(serializers.ModelSerializer):
    full_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'full_image_url', 'slug']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def get_full_image_url(self, instance):
        if instance.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(instance.image.url)
        return None





class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        exclude = ('id','product','attr_key','attr_value')

    def to_representation(self, instance):
        context = super(ProductAttributeSerializer, self).to_representation(instance)
        context['key_id'] = instance.attr_key.id
        context['key_name'] = instance.attr_key.key_name

        context['value_id'] = instance.attr_value.id
        context['value_name'] = instance.attr_value.value_name
        return context


class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'primary_image']

    def get_primary_image(self, obj):
        primary_image_instance = obj.images.filter(is_primary=True).first()
        if primary_image_instance and primary_image_instance.image:
            request = self.context.get('request')
            return request.build_absolute_uri(primary_image_instance.image.url)
        return None



class ProductDetailSerializer(serializers.ModelSerializer):
    all_images = serializers.SerializerMethodField()


    def get_all_images(self, instance):
        request = self.context.get('request')
        if instance.images.exists():
            return [request.build_absolute_uri(image.image.url) for image in instance.images.all()]
        return []

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'all_images', ]



    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)

        if validated_data.get('image'):
            instance.image = validated_data['image']

        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True,read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    all_images = serializers.SerializerMethodField()
    users_like = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, instance):
        instance = instance.comments.all().aggregate(avg_rating=Avg('rating', default=0))
        return round(instance['avg_rating'])

    def get_users_like(self, product):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        if user in product.users_like.all():
            return True

        return False

    def get_all_images(self, instance):
        request = self.context.get('request')
        if request:
            images = [request.build_absolute_uri(image.image.url) for image in instance.images.all()]
            return images
        return []

    def to_representation(self, product):
        context = super(ProductSerializer, self).to_representation(product)
        context['comments_count'] = product.comments.count()
        return context

    class Meta:
        model = Product
        fields = '__all__'


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = ['id', 'key_name']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value_name']










