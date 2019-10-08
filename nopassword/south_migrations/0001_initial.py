# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration

from .utils import AUTH_USER_MODEL


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LoginCode'
        db.create_table('nopassword_logincode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='login_codes', to=orm[AUTH_USER_MODEL]
            )),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('next', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('nopassword', ['LoginCode'])

    def backwards(self, orm):
        # Deleting model 'LoginCode'
        db.delete_table('nopassword_logincode')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {
                'unique': 'True', 'max_length': '80'
            }),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {
                'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'
            })
        },
        'auth.permission': {
            'Meta': {
                'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'
            },
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {
                'to': "orm['contenttypes.ContentType']"
            }),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {
                'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                'object_name': 'ContentType', 'db_table': "'django_content_type'"
            },
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nopassword.logincode': {
            'Meta': {'object_name': 'LoginCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {
                'related_name': "'login_codes'", 'to': "orm[" + AUTH_USER_MODEL + "]"
            })
        }
    }

    complete_apps = ['nopassword']
