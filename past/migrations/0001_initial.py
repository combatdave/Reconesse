# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'past_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'past', ['Country'])

        # Adding model 'Article'
        db.create_table(u'past_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['past.Country'])),
        ))
        db.send_create_signal(u'past', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'past_country')

        # Deleting model 'Article'
        db.delete_table(u'past_article')


    models = {
        u'past.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['past.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'past.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['past']