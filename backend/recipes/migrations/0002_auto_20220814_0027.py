# Generated by Django 2.2.16 on 2022-08-13 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("recipes", "0001_initial"),
        ("tags", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ingredients", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shoppingcart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="recipetag",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipetag",
                to="recipes.Recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="recipetag",
            name="tags",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipetag",
                to="tags.Tag",
                verbose_name="Тег",
            ),
        ),
        migrations.AddField(
            model_name="recipeingredientrelations",
            name="ingredients",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipeingredientrelations",
                to="ingredients.Ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AddField(
            model_name="recipeingredientrelations",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipeingredientrelations",
                to="recipes.Recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="recipes.RecipeIngredientRelations",
                to="ingredients.Ingredient",
                verbose_name="Ингредиенты",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipe",
                through="recipes.RecipeTag",
                to="tags.Tag",
                verbose_name="Теги",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite",
                to="recipes.Recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddConstraint(
            model_name="shoppingcart",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_shoppingcart"
            ),
        ),
        migrations.AddConstraint(
            model_name="recipetag",
            constraint=models.UniqueConstraint(
                fields=("tags", "recipe"), name="unique_recipetag"
            ),
        ),
        migrations.AddConstraint(
            model_name="recipeingredientrelations",
            constraint=models.UniqueConstraint(
                fields=("recipe", "ingredients"),
                name="unique_recipe_ingredients",
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_favorite"
            ),
        ),
    ]
