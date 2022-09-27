# Generated by Django 4.1.1 on 2022-09-23 11:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Vardas')),
                ('last_name', models.CharField(max_length=100, verbose_name='Pavarde')),
                ('description', models.TextField(default='Zinomas autorius.', max_length=2000, verbose_name='Aprasymas')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Pavadinimas')),
                ('summary', models.TextField(help_text='Trumpas knygos aprašymas', max_length=1000, verbose_name='Aprasymas')),
                ('isbn', models.CharField(max_length=13, verbose_name='ISBN')),
                ('cover', models.ImageField(null=True, upload_to='covers', verbose_name='Virselis')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='library.author')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Iveskite knygos žanrą(pvz. detektyvas)', max_length=200, verbose_name='Pavadinimas')),
            ],
            options={
                'verbose_name': 'Žanras',
                'verbose_name_plural': 'Žanrai',
            },
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unikalus ID knygos kopijai', primary_key=True, serialize=False)),
                ('due_back', models.DateField(blank=True, null=True, verbose_name='Bus prieinama')),
                ('status', models.CharField(blank=True, choices=[('a', 'Administruojama'), ('p', 'Paimta'), ('g', 'Galima paimti'), ('r', 'Rezervuota')], default='a', help_text='Statusas', max_length=1)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.book')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Išrinkite žanrą(us) šiai knygai', to='library.genre'),
        ),
    ]
