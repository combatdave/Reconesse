# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'past_country')


        # Renaming column for 'Article.country' to match new field type.
        db.rename_column(u'past_article', 'country_id', 'country')
        # Changing field 'Article.country'
        db.alter_column(u'past_article', 'country', self.gf('django_countries.fields.CountryField')(max_length=2))
        # Removing index on 'Article', fields ['country']
        db.delete_index(u'past_article', ['country_id'])


    def backwards(self, orm):
        # Adding index on 'Article', fields ['country']
        db.create_index(u'past_article', ['country_id'])

        # Adding model 'Country'
        db.create_table(u'past_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'past', ['Country'])


        # Renaming column for 'Article.country' to match new field type.
        db.rename_column(u'past_article', 'country', 'country_id')
        # Changing field 'Article.country'
        db.alter_column(u'past_article', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['past.Country']))

    models = {
        u'past.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['past']