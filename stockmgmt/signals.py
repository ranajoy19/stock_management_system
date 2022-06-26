from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StockHistory, Stock


@receiver(post_save, sender=Stock)
def add_item_on_stock_history_after_stock_update(sender, instance, created, **kwargs):
    if not created:
        # Stock object updated
        id = instance.id
        category = instance.category
        item_name = instance.item_name
        quantity = instance.quantity
        issue_quantity = instance.issue_quantity
        receive_quantity = instance.receive_quantity
        last_updated = instance.last_updated
        receive_by = instance.receive_by
        issue_by = instance.issue_by
        issue_to = instance.issue_to
        phone_number = instance.phone_number
        created_by = instance.created_by
        reorder_level = instance.reorder_level

        StockHistory.objects.create(id=id, category=category, item_name=item_name, quantity=quantity,
                                    issue_quantity=issue_quantity, receive_quantity=receive_quantity,
                                    last_updated=last_updated,receive_by=receive_by,issue_by=issue_by,
                                    issue_to=issue_to,phone_number=phone_number,created_by=created_by,
                                    reorder_level=reorder_level)
