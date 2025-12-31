from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.inventory import Inventory, StockMovement
from .models.procurement import PurchaseReceipt
from .models.sales import SalesDispatch


def update_inventory(product, warehouse, quantity):
    inventory, _ = Inventory.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={"quantity": 0}
    )
    inventory.quantity += quantity
    inventory.save()


@receiver(post_save, sender=StockMovement)
def apply_stock_movement(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.destination_warehouse:
        update_inventory(
            instance.product,
            instance.destination_warehouse,
            instance.quantity
        )

    if instance.source_warehouse:
        update_inventory(
            instance.product,
            instance.source_warehouse,
            -instance.quantity
        )


@receiver(post_save, sender=PurchaseReceipt)
def stock_in_from_receipt(sender, instance, created, **kwargs):
    if not created:
        return

    for item in instance.items.all():
        StockMovement.objects.create(
            product=item.product,
            movement_type=StockMovement.MovementType.SUPPLIER_TO_WAREHOUSE,
            quantity=item.quantity,
            destination_warehouse=instance.warehouse,
            reference=instance.tracking_id
        )


@receiver(post_save, sender=SalesDispatch)
def stock_out_from_dispatch(sender, instance, created, **kwargs):
    if not created:
        return

    for item in instance.items.all():
        StockMovement.objects.create(
            product=item.product,
            movement_type=StockMovement.MovementType.WAREHOUSE_TO_CUSTOMER,
            quantity=item.quantity,
            source_warehouse=instance.warehouse,
            reference=instance.tracking_id
        )
