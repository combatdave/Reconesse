# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.birthYear'
        db.add_column(u'past_article', 'birthYear',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Article.deathYear'
        db.add_column(u'past_article', 'deathYear',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Article.content'
        db.alter_column(u'past_article', 'content', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Deleting field 'Article.birthYear'
        db.delete_column(u'past_article', 'birthYear')

        # Deleting field 'Article.deathYear'
        db.delete_column(u'past_article', 'deathYear')


        # Changing field 'Article.content'
        db.alter_column(u'past_article', 'content', self.gf('django.db.models.fields.CharField')(max_length=10000))

    models = {
        u'past.article': {
            'Meta': {'object_name': 'Article'},
            'birthYear': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'deathYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['past']