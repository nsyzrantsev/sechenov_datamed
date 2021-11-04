# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DdiFact(models.Model):
    id_fact = models.IntegerField(primary_key=True)
    id_task = models.ForeignKey('Task', models.DO_NOTHING, db_column='id_task')
    id_doc = models.IntegerField()
    sentence_txt = models.TextField()
    parsing_txt = models.TextField()
    numb_sentence_in_doc = models.IntegerField()
    ddi_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'ddi_fact'


class DdiResult(models.Model):
    id_fact = models.OneToOneField(DdiFact, models.DO_NOTHING, db_column='id_fact', primary_key=True)
    id_task = models.IntegerField()
    id_doc = models.IntegerField()
    sentence_txt = models.CharField(max_length=1024)
    parsing_txt = models.CharField(max_length=1024)
    numb_sentence_in_doc = models.IntegerField()
    ddi_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ddi_result'


class DdiXFact(models.Model):
    id_fact = models.IntegerField(primary_key=True)
    id_task = models.IntegerField()
    id_doc = models.IntegerField()
    sentence_txt = models.CharField(max_length=4096)
    parsing_txt = models.CharField(max_length=4096)
    numb_sentence_in_doc = models.IntegerField()
    ddi_type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'ddi_x_fact'


class DrugLink(models.Model):
    id_fact = models.ForeignKey(DdiFact, models.DO_NOTHING, db_column='id_fact')
    drug_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'drug_link'


class DrugXLink(models.Model):
    id_fact = models.IntegerField()
    drug_name = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'drug_x_link'


class DvaDdi(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    ddi_text = models.TextField()
    pmid = models.IntegerField(db_column='PMID')  # Field name made lowercase.
    sentencenumb = models.IntegerField(db_column='SentenceNumb')  # Field name made lowercase.
    finddate = models.DateField(db_column='FindDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dva_ddi'


class DvaGisz(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    rus = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)
    eng = models.TextField(blank=True, null=True)
    atx = models.TextField(blank=True, null=True)
    snomed = models.TextField(blank=True, null=True)
    gr = models.IntegerField(blank=True, null=True)
    mnn = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dva_gisz'


class DvaXGisz(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    rus = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)
    eng = models.TextField(blank=True, null=True)
    atx = models.TextField(blank=True, null=True)
    snomed = models.TextField(blank=True, null=True)
    gr = models.IntegerField(blank=True, null=True)
    mnn = models.TextField(blank=True, null=True)
    query_time = models.DateTimeField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dva_x_gisz'


class ExportPkgDesc(models.Model):
    id = models.IntegerField(primary_key=True)
    setid = models.TextField(db_column='SETID', blank=True, null=True)  # Field name made lowercase.
    spl_version = models.IntegerField(db_column='SPL_VERSION', blank=True, null=True)  # Field name made lowercase.
    product_name = models.TextField(db_column='PRODUCT_NAME', blank=True, null=True)  # Field name made lowercase.
    product_code = models.TextField(db_column='PRODUCT_CODE', blank=True, null=True)  # Field name made lowercase.
    ndc = models.TextField(db_column='NDC', blank=True, null=True)  # Field name made lowercase.
    package_description = models.TextField(db_column='PACKAGE_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    form_code = models.TextField(db_column='FORM_CODE', blank=True, null=True)  # Field name made lowercase.
    product_number = models.IntegerField(db_column='PRODUCT_NUMBER', blank=True, null=True)  # Field name made lowercase.
    part_yn = models.TextField(db_column='PART_YN', blank=True, null=True)  # Field name made lowercase.
    total_product_quantity = models.IntegerField(db_column='TOTAL_PRODUCT_QUANTITY', blank=True, null=True)  # Field name made lowercase.
    strength = models.TextField(db_column='STRENGTH', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_pkg_desc'


class Rls(models.Model):
    regnumb = models.CharField(db_column='RegNumb', max_length=255, blank=True, null=True)  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enddata = models.CharField(db_column='EndData', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stopdate = models.CharField(db_column='StopDate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=255, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)  # Field name made lowercase.
    torgname = models.CharField(db_column='TorgName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    chemname = models.CharField(db_column='ChemName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    forms = models.CharField(db_column='Forms', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enterprise = models.CharField(db_column='Enterprise', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scancode = models.CharField(db_column='ScanCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    docum = models.CharField(db_column='Docum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pharmgroup = models.CharField(db_column='PharmGroup', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rls'


class Source(models.Model):
    source_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'source'


class Task(models.Model):
    id_task = models.IntegerField(primary_key=True)
    source = models.ForeignKey(Source, models.DO_NOTHING)
    query_text = models.CharField(max_length=45, blank=True, null=True)
    query_time = models.DateTimeField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'
