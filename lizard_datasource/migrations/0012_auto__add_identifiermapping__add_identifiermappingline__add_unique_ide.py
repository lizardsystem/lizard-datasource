# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IdentifierMapping'
        db.create_table('lizard_datasource_identifiermapping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('lizard_datasource', ['IdentifierMapping'])

        # Adding model 'IdentifierMappingLine'
        db.create_table('lizard_datasource_identifiermappingline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mapping', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_datasource.IdentifierMapping'])),
            ('identifier_from', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('identifier_to', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('lizard_datasource', ['IdentifierMappingLine'])

        # Adding unique constraint on 'IdentifierMappingLine', fields ['mapping', 'identifier_from']
        db.create_unique('lizard_datasource_identifiermappingline', ['mapping_id', 'identifier_from'])


    def backwards(self, orm):
        # Removing unique constraint on 'IdentifierMappingLine', fields ['mapping', 'identifier_from']
        db.delete_unique('lizard_datasource_identifiermappingline', ['mapping_id', 'identifier_from'])

        # Deleting model 'IdentifierMapping'
        db.delete_table('lizard_datasource_identifiermapping')

        # Deleting model 'IdentifierMappingLine'
        db.delete_table('lizard_datasource_identifiermappingline')


    models = {
        'lizard_datasource.augmenteddatasource': {
            'Meta': {'object_name': 'AugmentedDataSource'},
            'augmented_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.DatasourceModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lizard_datasource.colorfromlatestvalue': {
            'Meta': {'object_name': 'ColorFromLatestValue'},
            'augmented_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.AugmentedDataSource']"}),
            'colormap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.ColorMap']"}),
            'hide_from_layer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer_to_add_color_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'colors_from'", 'to': "orm['lizard_datasource.DatasourceLayer']"}),
            'layer_to_get_color_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'colors_used_by'", 'null': 'True', 'to': "orm['lizard_datasource.DatasourceLayer']"})
        },
        'lizard_datasource.colormap': {
            'Meta': {'object_name': 'ColorMap'},
            'defaultcolor': ('colorful.fields.RGBColorField', [], {'max_length': '7', 'null': 'True'}),
            'defaultdescription': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lizard_datasource.colormapline': {
            'Meta': {'ordering': "[u'minvalue', u'maxvalue']", 'object_name': 'ColorMapLine'},
            'color': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'colormap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.ColorMap']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "(u'nickname', u'datasource_model', u'choices_made')", 'object_name': 'DatasourceLayer'},
            'choices_made': ('django.db.models.fields.TextField', [], {}),
            'datasource_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.DatasourceModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'lizard_datasource.datasourcemodel': {
            'Meta': {'ordering': "(u'originating_app', u'identifier')", 'object_name': 'DatasourceModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'originating_app': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'script_last_run_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'script_run_next_opportunity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'script_times_to_run_per_day': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'lizard_datasource.extragraphline': {
            'Meta': {'object_name': 'ExtraGraphLine'},
            'augmented_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.AugmentedDataSource']"}),
            'hide_from_layer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer_to_add_line_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'extra_graph_line_from'", 'to': "orm['lizard_datasource.DatasourceLayer']"}),
            'layer_to_get_line_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'extra_graph_line_to'", 'to': "orm['lizard_datasource.DatasourceLayer']"})
        },
        'lizard_datasource.identifiermapping': {
            'Meta': {'object_name': 'IdentifierMapping'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'lizard_datasource.identifiermappingline': {
            'Meta': {'unique_together': "((u'mapping', u'identifier_from'),)", 'object_name': 'IdentifierMappingLine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier_from': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'identifier_to': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mapping': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.IdentifierMapping']"})
        },
        'lizard_datasource.percentilelayer': {
            'Meta': {'object_name': 'PercentileLayer'},
            'augmented_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_datasource.AugmentedDataSource']"}),
            'hide_from_layer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer_to_add_percentile_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'percentiles_from'", 'to': "orm['lizard_datasource.DatasourceLayer']"}),
            'layer_to_get_percentile_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'percentiles_used_by'", 'to': "orm['lizard_datasource.DatasourceLayer']"}),
            'percentile': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['lizard_datasource']