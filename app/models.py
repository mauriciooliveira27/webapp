from django.db import models


class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'user'



class RegistroPlaca(models.Model):

    cod_placa = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=20)
    ip = models.TextField()

    class Meta:
        managed = False
        db_table = 'registro_placas'


class RegistroCordoes(models.Model):

    id = models.IntegerField(primary_key=True)
    cod_placa = models.IntegerField()
    cordao_fisico = models.CharField(max_length=255)
    canal_placa = models.IntegerField()
    sensor_placa = models.IntegerField()
    placa = models.ForeignKey(RegistroPlaca, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'registro_cordoes'


class Servicos(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=55)

    class Meta:
        managed = False
        db_table = 'servicos'

