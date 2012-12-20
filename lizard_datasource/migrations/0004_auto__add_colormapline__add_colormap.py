# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ColorMapLine'
        db.create_table('lizard_datasource_colormapline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('colormap', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_datasource.ColorMap'])),
            ('minvalue', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('maxvalue', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mininclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maxinclusive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('color', self.gf('colorful.fields.RGBColorField')(max_length=7)),
        ))
        db.send_create_signal('lizard_datasource', ['ColorMapLine'])

        # Adding model 'ColorMap'
        db.create_table('lizard_datasource_colormap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('lizard_datasource', ['ColorMap'])


    def backwards(self, orm):
        # Deleting model 'ColorMapLine'
        db.delete_table('lizard_datasource_colormapline')

        # Deleting model 'ColorMap'
        db.delete_table('lizard_datasource_colormap')


    models = {
        'lizard_datasource.augmenteddatasource': {
            'Meta': {'object_name': 'AugmentedDataSource'},
            'augmented_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.DatasourceModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_datasource.colormap': {
            'Meta': {'object_name': 'ColorMap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lizard_datasource.colormapline': {
            'Meta': {'object_name': 'ColorMapLine'},
            'color': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'colormap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.ColorMap']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxinclusive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'maxvalue': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mininclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'minvalue': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_datasource.datasourcecache': {
            'Meta': {'object_name': 'DatasourceCache'},
            'datasource_layer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.DatasourceLayer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lizard_datasource.datasourcelayer': {
            'Meta': {'object_name': 'DatasourceLayer'},
            'choices_made': ('django.db.models.fields.TextField', [], {}),
            'datasource_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.DatasourceModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_datasource.datasourcemodel': {
            'Meta': {'object_name': 'DatasourceModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'originating_app': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['lizard_datasource']