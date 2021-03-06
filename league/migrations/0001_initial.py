# Generated by Django 3.2 on 2021-04-17 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('side', models.CharField(choices=[('corp', 'Corp'), ('runner', 'Runner')], max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('image_url', models.CharField(max_length=255)),
                ('faction', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('discord_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('signup', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='league.player')),
                ('player1_corp_deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1_corp', to='league.deck')),
                ('player1_runner_deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1_runner', to='league.deck')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='league.player')),
                ('player2_corp_deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2_corp', to='league.deck')),
                ('player2_runner_deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2_runner', to='league.deck')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.week')),
            ],
        ),
    ]
