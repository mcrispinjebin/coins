# Generated by Django 3.2.8 on 2021-10-24 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('t', 'Transgender')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('title', models.CharField(choices=[('mr', 'Mr'), ('ms', 'Miss'), ('mrs', 'Mrs'), ('dr', 'Dr')], max_length=4)),
                ('email', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('deactivated', 'De - Activated')], max_length=15)),
                ('created_at', models.DateField()),
                ('created_by', models.CharField(max_length=50)),
                ('updated_at', models.DateField(blank=True, default=None, null=True)),
                ('updated_by', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.AutoField(primary_key=True, serialize=False)),
                ('wallet_type', models.CharField(choices=[('food', 'Food Wallet'), ('premium', 'Premium Wallet')], max_length=10)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency_type', models.CharField(choices=[('inr', 'Indian Rupees'), ('usd', 'US Dollars')], default='usd', max_length=3)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linked_account', to='wallet.account')),
            ],
            options={
                'db_table': 'wallet',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('payin', 'Payin'), ('payout', 'Payout')], max_length=10)),
                ('status', models.CharField(choices=[('success', 'Success'), ('failure', 'Failure')], max_length=10)),
                ('created_at', models.DateField()),
                ('created_by', models.CharField(max_length=50)),
                ('updated_at', models.DateField(blank=True, default=None, null=True)),
                ('updated_by', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('referenced_wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_wallet', to='wallet.wallet')),
                ('wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_wallet', to='wallet.wallet')),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
    ]
