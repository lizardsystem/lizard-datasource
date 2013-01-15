from django.contrib import admin

from lizard_datasource import models


class DatasourceModelAdmin(admin.ModelAdmin):
    pass


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
