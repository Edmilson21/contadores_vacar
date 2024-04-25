# Generated by Django 3.2.24 on 2024-04-24 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_empresa', models.CharField(max_length=100, unique=True, verbose_name='Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Vacar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_agua', models.IntegerField()),
                ('valor_P1', models.IntegerField()),
                ('valor_P2', models.IntegerField()),
                ('valor_P3', models.IntegerField()),
                ('valor_gas_derecho', models.IntegerField()),
                ('valor_gas_izquierdo', models.IntegerField()),
                ('valor_gas_casa', models.IntegerField()),
                ('gas', models.IntegerField()),
                ('fecha_registro', models.DateField()),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medidor.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Cruce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_agua', models.IntegerField()),
                ('agua1', models.IntegerField()),
                ('agua2', models.IntegerField()),
                ('bombero', models.IntegerField()),
                ('valor_luz', models.IntegerField()),
                ('valor_gas', models.IntegerField()),
                ('fecha_registro', models.DateField()),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medidor.empresa')),
            ],
        ),
    ]