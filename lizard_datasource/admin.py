from django.contrib import admin

from lizard_datasource import models

from django.utils.translation import ugettext_lazy as _


def run_cache_script_next_time(modeladmin, request, queryset):
    queryset.update(script_run_next_opportunity=True)

run_cache_script_next_time.short_description = _(
    "Run the cache latest values script at the next opportunity")


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
    pass


class ColorFromLatestValueInline(admin.TabularInline):
    model = models.ColorFromLatestValue


class PercentileInline(admin.TabularInline):
    model = models.PercentileLayer


class AugmentedDataSourceAdmin(admin.ModelAdmin):
    inlines = [ColorFromLatestValueInline, PercentileInline]


class ColorMapLineInline(admin.TabularInline):
    model = models.ColorMapLine


class ColorMapAdmin(admin.ModelAdmin):
    inlines = [ColorMapLineInline]


admin.site.register(models.DatasourceModel, DatasourceModelAdmin)
admin.site.register(models.DatasourceLayer, DatasourceLayerAdmin)
admin.site.register(models.AugmentedDataSource, AugmentedDataSourceAdmin)
admin.site.register(models.ColorMap, ColorMapAdmin)
