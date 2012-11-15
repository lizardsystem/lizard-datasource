# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DatasourceCache'
        db.create_table('lizard_datasource_datasourcecache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datasource_layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_datasource.DatasourceLayer'])),
            ('locationid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lizard_datasource', ['DatasourceCache'])

        # Adding model 'DatasourceLayer'
        db.create_table('lizard_datasource_datasourcelayer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datasource_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_datasource.DatasourceModel'])),
            ('choices_made', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lizard_datasource', ['DatasourceLayer'])


    def backwards(self, orm):
        
        # Deleting model 'DatasourceCache'
        db.delete_table('lizard_datasource_datasourcecache')

        # Deleting model 'DatasourceLayer'
        db.delete_table('lizard_datasource_datasourcelayer')


    models = {
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
