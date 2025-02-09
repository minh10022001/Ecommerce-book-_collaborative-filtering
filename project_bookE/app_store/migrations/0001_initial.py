# Generated by Django 4.1.7 on 2023-12-24 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(db_column='ID_product', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, null=True)),
                ('price', models.FloatField(null=True)),
                ('short_description', models.TextField(null=True)),
                ('author', models.CharField(max_length=500, null=True)),
                ('slug', models.CharField(max_length=500, null=True)),
                ('is_authenic', models.CharField(max_length=500, null=True)),
                ('publisher', models.CharField(max_length=500, null=True)),
                ('publication_year', models.CharField(max_length=500, null=True)),
                ('dimensions', models.CharField(max_length=1000, null=True)),
                ('book_cover', models.CharField(max_length=500, null=True)),
                ('numpage', models.CharField(max_length=500, null=True)),
                ('manufacturer', models.CharField(max_length=500, null=True)),
                ('image', models.ImageField(max_length=500, upload_to='download/')),
                ('stock', models.IntegerField(null=True)),
                ('count_review', models.IntegerField(null=True)),
                ('avg_rating', models.FloatField(null=True)),
                ('is_upload', models.BooleanField(default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(db_column='ID_category', primary_key=True, serialize=False)),
                ('slug_category', models.CharField(max_length=200, null=True)),
                ('category_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlistline',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('create_at', models.DateField(default=None, null=True)),
                ('id_customer', models.ForeignKey(blank=True, db_column='ID_customer', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_user.customer')),
                ('id_product', models.ForeignKey(blank=True, db_column='ID_product', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_store.book')),
            ],
        ),
        migrations.CreateModel(
            name='RatingBook',
            fields=[
                ('id', models.IntegerField(db_column='ID_rating', primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=20000, null=True)),
                ('rating', models.IntegerField(null=True)),
                ('create_at', models.DateField(default=None, null=True)),
                ('id_customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_user.customer')),
                ('id_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_store.book')),
            ],
        ),
        migrations.CreateModel(
            name='ImportBook',
            fields=[
                ('id', models.IntegerField(db_column='ID_import', primary_key=True, serialize=False)),
                ('price_import', models.FloatField(null=True)),
                ('price_sale', models.FloatField(null=True)),
                ('create_at', models.DateField(default=None, null=True)),
                ('num', models.IntegerField(null=True)),
                ('is_sale', models.BooleanField(default=True, null=True)),
                ('id_product', models.ForeignKey(blank=True, db_column='ID_product', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_store.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='id_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_store.category'),
        ),
    ]
