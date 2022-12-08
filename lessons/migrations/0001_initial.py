# Generated by Django 4.1.3 on 2022-12-06 08:38

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message="Username must consist of  an '@' and a minimum of 3 alphanumericals!", regex='^@\\w{3,}$')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ID', models.CharField(max_length=4)),
                ('invoice_number', models.CharField(max_length=3)),
                ('full_invoice_number', models.CharField(max_length=8)),
                ('pay', models.PositiveIntegerField()),
                ('paid', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(choices=[('monday', 'MONDAY'), ('tuesday', 'TUESDAY'), ('wednesday', 'WEDNESDAY'), ('thursday', 'THURSDAY'), ('friday', 'FRIDAY')], default='monday', max_length=10)),
                ('number_of_lessons', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1)),
                ('interval', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2, 'Cannot request lessons for a period shorter than 2 days.'), django.core.validators.MaxValueValidator(14, 'Cannot request lessons for a period longer than 14 days.')])),
                ('duration', models.PositiveIntegerField(choices=[(30, 30), (45, 45), (60, 60)], default=30, verbose_name='Duration (mins)')),
                ('extra_info', models.CharField(blank=True, max_length=100, verbose_name='Extra information')),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lessons.request')),
                ('teacher', models.CharField(max_length=30)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]