from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Product, Category
import os
import json
from datetime import datetime

DELETED_ITEMS_DIR = 'deleted_items'

if not os.path.exists(DELETED_ITEMS_DIR):
    os.makedirs(DELETED_ITEMS_DIR)


def serialize_datetime(obj):
    """Convert datetime objects to string format."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def save_deleted_item_to_json(instance, item_type):
    file_name = f'{DELETED_ITEMS_DIR}/{item_type}_{instance.id}.json'

    data = instance.__dict__.copy()

    data.pop('created_at', None)
    data.pop('updated_at', None)

    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()

    with open(file_name, 'w') as file:
        json.dump(data, file, default=serialize_datetime, indent=4)


@receiver(pre_delete, sender=Product)
def save_deleted_product(sender, instance, **kwargs):
    save_deleted_item_to_json(instance, 'product')


@receiver(pre_delete, sender=Category)
def save_deleted_category(sender, instance, **kwargs):
    save_deleted_item_to_json(instance, 'category')
