from django.contrib import admin

from lizard_datasource import augmented_datasource
from lizard_datasource import models

from django.utils.translation import ugettext_lazy as _


def run_cache_script_next_time(modeladmin, request, queryset):
    queryset.update(script_run_next_opportunity=True)

run_cache_script_next_time.short_description = _(
    "Run the cache-latest-values script at the next opportunity")


def create_proximity_mapping(modeladmin, request, queryset):
    for data_source in queryset:
        augmented_datasource.fill_mapping_with_closest_locations(data_source)
create_proximity_mapping.short_description = _(
    "Fill the identifier mapping of extra graph lines using closest locations")


class DatasourceModelAdmin(admin.ModelAdmin):
    list_display = ['visible', 'originating_app', 'identifier']
    list_display_links = ['originating_app', 'identifier']
    list_editable = ['visible']
    actions = [run_cache_script_next_time]
    fieldsets = (
        (None, {
                'fields': ['originating_app', 'identifier', 'visible']
                }),
        ('Cache script', {
                'fields': ['script_times_to_run_per_day',
                           'script_last_run_started',
                           'script_run_next_opportunity'
                           ]
                }))
    readonly_fields = [
        'originating_app', 'identifier', 'script_last_run_started']


class DatasourceLayerAdmin(admin.ModelAdmin):
    list_display = [
        'nickname', 'unit_cache', 'choices_made', 'datasource_model']
    list_display_links = ['choices_made', 'datasource_model']
    list_editable = ['nickname', 'unit_cache']


class ColorFromLatestValueInline(admin.TabularInline):
    model = models.ColorFromLatestValue


class ExtraGraphLineInline(admin.TabularInline):
    model = models.ExtraGraphLine


class PercentileInline(admin.TabularInline):
    model = models.PercentileLayer


class AugmentedDataSourceAdmin(admin.ModelAdmin):
    inlines = [
        ColorFromLatestValueInline,
        ExtraGraphLineInline,
        PercentileInline,
        ]
    actions = [create_proximity_mapping]


class ColorMapLineInline(admin.TabularInline):
    model = models.ColorMapLine


class ColorMapAdmin(admin.ModelAdmin):
    inlines = [ColorMapLineInline]


class IdentifierMappingLineInline(admin.TabularInline):
    model = models.IdentifierMappingLine


class IdentifierMappingAdmin(admin.ModelAdmin):
    inlines = [IdentifierMappingLineInline]


admin.site.register(models.DatasourceModel, DatasourceModelAdmin)
admin.site.register(models.DatasourceLayer, DatasourceLayerAdmin)
admin.site.register(models.AugmentedDataSource, AugmentedDataSourceAdmin)
admin.site.register(models.ColorMap, ColorMapAdmin)
admin.site.register(models.IdentifierMapping, IdentifierMappingAdmin)
