from django_filters import rest_framework as filters
from .models import Part

class PartFilter(filters.FilterSet):
    category = filters.ChoiceFilter(choices=Part.PART_CATEGORIES, required=False)
    team_name = filters.CharFilter(field_name='team__name', lookup_expr='icontains', required=False)
    aircraft_name = filters.CharFilter(field_name='aircraft__name', lookup_expr='icontains', required=False)
    min_stock = filters.NumberFilter(field_name="stock_quantity", lookup_expr='gte', required=False)
    is_active = filters.BooleanFilter(field_name="is_active", required=False)

    class Meta:
        model = Part
        fields = []