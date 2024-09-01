# Generated by Django 5.0.3 on 2024-08-31 15:42

import django.db.models.deletion
import django.utils.timezone
import fitness_app.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('created_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('modified_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('city_name', models.TextField(max_length=256)),
                ('street_name', models.TextField(max_length=256)),
                ('house_number', models.IntegerField(validators=[fitness_app.models.check_positive])),
                ('apartment_number', models.IntegerField(blank=True, null=True, validators=[fitness_app.models.check_positive])),
                ('body', models.TextField(blank=True, null=True, validators=[fitness_app.models.check_body])),
            ],
            options={
                'verbose_name': 'address',
                'db_table': '"address"',
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('created_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('modified_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('spec', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'coach',
                'db_table': '"coach"',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('net_worth', models.DecimalField(decimal_places=2, default=1000, max_digits=9, validators=[fitness_app.models.check_money])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': '"client"',
            },
        ),
        migrations.CreateModel(
            name='ClientSub',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.client')),
            ],
            options={
                'db_table': '"client_sub"',
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('created_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('modified_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('certf_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.coach')),
            ],
            options={
                'db_table': '"certf"',
            },
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('created_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('modified_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gym_name', models.CharField(max_length=100)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fitness_app.address')),
            ],
            options={
                'verbose_name': 'gym',
                'db_table': '"gym"',
            },
        ),
        migrations.CreateModel(
            name='GymCoach',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.coach')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.gym')),
            ],
            options={
                'db_table': '"gym_coach"',
                'unique_together': {('gym', 'coach')},
            },
        ),
        migrations.AddField(
            model_name='gym',
            name='coaches',
            field=models.ManyToManyField(through='fitness_app.GymCoach', to='fitness_app.coach'),
        ),
        migrations.AddField(
            model_name='coach',
            name='gyms',
            field=models.ManyToManyField(through='fitness_app.GymCoach', to='fitness_app.gym'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('modified_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fitness_app.models.check_datetime])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.IntegerField(validators=[fitness_app.models.check_money])),
                ('expire_date', models.DateField(validators=[fitness_app.models.check_date])),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('clients', models.ManyToManyField(through='fitness_app.ClientSub', to='fitness_app.client')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.gym')),
            ],
            options={
                'db_table': '"subscription"',
            },
        ),
        migrations.AddField(
            model_name='clientsub',
            name='sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.subscription'),
        ),
        migrations.AddField(
            model_name='client',
            name='subs',
            field=models.ManyToManyField(through='fitness_app.ClientSub', to='fitness_app.subscription'),
        ),
        migrations.AlterUniqueTogether(
            name='clientsub',
            unique_together={('sub', 'client')},
        ),
    ]
