from django.contrib import admin

from lizard_datasource import models


class DatasourceModelAdmin(admin.ModelAdmin):
    pass


class DatasourceLayerAdmin(admin.ModelAdmin):
    pass


class AugmentedDataSourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.DatasourceModel, DatasourceModelAdmin)
admin.site.register(models.DatasourceLayer, DatasourceLayerAdmin)
admin.site.register(models.AugmentedDataSource, AugmentedDataSourceAdmin)
