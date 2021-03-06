# Generated by Django 2.1.7 on 2019-04-29 12:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=50)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='kolvo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='myOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Единица заказа',
                'verbose_name_plural': 'Единицы заказов',
            },
        ),
        migrations.CreateModel(
            name='myOrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.myOrderItem')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='needforvideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('img', models.FileField(blank=True, upload_to='')),
            ],
            options={
                'verbose_name': 'видео для главной страницы',
                'verbose_name_plural': 'Видео',
            },
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('content', models.TextField()),
                ('price', models.IntegerField()),
                ('img', models.FileField(blank=True, upload_to='')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edinica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.kolvo')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name': 'группу продуктов',
                'verbose_name_plural': 'Группы продуктов',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Type'),
        ),
        migrations.AddField(
            model_name='myorderitem',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.product'),
        ),
    ]
