from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('payment', '0002_rename_address1_shippingaddress_shipping_address1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_address2',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_country',
        ),
    ]
