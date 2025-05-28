from django.contrib import admin

from apps.catalog.models import Book, Category

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
            "title",
        # "campaign_goals",
        # "social_platforms",
        # "budget_range",
        # "timeline",
        # "target_age_range",
        # "target_gender",
        # # "target_locations",
        # # "target_interests",
        # "preferred_platforms",
        # "product_category",
        # "product_description",
    ]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
            "name",
        # "campaign_goals",
        # "social_platforms",
        # "budget_range",
        # "timeline",
        # "target_age_range",
        # "target_gender",
        # # "target_locations",
        # # "target_interests",
        # "preferred_platforms",
        # "product_category",
        # "product_description",
    ]
