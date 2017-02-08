# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Location(models.Model):
    pathname = models.CharField(max_length=32, primary_key=True, db_column='PATHNAME') # Field name made lowercase.
    filesize = models.IntegerField(db_column='FILESIZE') # Field name made lowercase.
    class Meta:
        db_table = u'LOCATION'

class Word(models.Model):
    code = models.CharField(max_length=128, primary_key=True, db_column='CODE') # Field name made lowercase.
    numberofarticles = models.BigIntegerField(db_column='NUMBEROFARTICLES') # Field name made lowercase.
    amount = models.BigIntegerField(db_column='AMOUNT') # Field name made lowercase.
    class Meta:
        db_table = u'WORD'

class Wordfile(models.Model):
    word = models.CharField(max_length=255, db_column='WORD') # Field name made lowercase.
    path_id = models.CharField(max_length=64, db_column='PATH_ID') # Field name made lowercase.
    amount = models.IntegerField(db_column='AMOUNT') # Field name made lowercase.
    class Meta:
        db_table = u'WORDFILE'

class Wordpath(models.Model):
    word = models.CharField(max_length=255, primary_key=True, db_column='WORD') # Field name made lowercase.
    path_id = models.CharField(max_length=64, db_column='PATH_ID') # Field name made lowercase.
    amount = models.IntegerField(db_column='AMOUNT') # Field name made lowercase.
    class Meta:
        db_table = u'WORDPATH'

