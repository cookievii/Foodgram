from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from core.mixins import AttributesForRecipe
from core.validaters import validate_ingredients, validate_tags
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredientRelations
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class RecipeIngredientRelationsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredients.id")
    name = serializers.ReadOnlyField(source="ingredients.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredients.measurement_unit"
    )

    class Meta:
        model = RecipeIngredientRelations
        fields = ("id", "name", "measurement_unit", "amount")


class SimpleRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")


class RecipeSerializer(AttributesForRecipe, SimpleRecipeSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientRelationsSerializer(
        read_only=True, many=True, source="recipeingredientrelations"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def create_ingredient_amount(self, valid_ingredients, recipe):
        objects = []
        for data in valid_ingredients:
            amount = data.get("amount")
            ingredients = get_object_or_404(Ingredient, id=data["id"])
            objects.append(
                RecipeIngredientRelations(
                    recipe=recipe, ingredients=ingredients, amount=amount
                )
            )
        RecipeIngredientRelations.objects.bulk_create(objects)

    def create(self, validated_data):
        pop_ingredients = validated_data.pop("ingredients")
        pop_tags = validated_data.pop("tags")

        recipe = Recipe.objects.create(**validated_data)

        tags = Tag.objects.filter(id__in=pop_tags)
        recipe.tags.set(tags)

        self.create_ingredient_amount(pop_ingredients, recipe)
        return recipe

    def validate(self, data):
        get_ingredients = self.initial_data.get("ingredients")
        validated_ingredients = validate_ingredients(get_ingredients)
        data["ingredients"] = validated_ingredients

        get_tags = self.initial_data.get("tags")
        validated_tags = validate_tags(get_tags)
        data["tags"] = validated_tags
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )

        instance.tags.clear()
        tags_data = self.initial_data.get("tags")
        instance.tags.set(tags_data)
        RecipeIngredientRelations.objects.filter(
            recipe=instance
        ).all().delete()

        valid_ingredients = validated_data.get(
            "ingredients", instance.ingredients
        )
        self.create_ingredient_amount(valid_ingredients, instance)
        instance.save()
        return instance
