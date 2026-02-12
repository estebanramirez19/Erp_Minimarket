from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='codigo_descuento',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='compra',
            name='notas',
            field=models.TextField(blank=True),
        ),
    ]
