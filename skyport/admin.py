from django.contrib import admin
from django.db.models import Sum


from .models.partners import Partner
from .models.core import Factory, ParentCompany, Warehouse, Product
from .models.inventory import Inventory, StockMovement
from .models.procurement import (
    PurchaseOrder,
    PurchaseReceipt,
    PurchaseReceiptItem,
)
from .models.sales import (
    SalesOrder,
    SalesDispatch,
    SalesDispatchItem,
)

# =========================
# Base Admin
# =========================

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        "tracking_id",
        "created_at",
        "updated_at",
        "authorization_time",
        "authorized_by",
    )
    list_filter = ("is_authorized", "created_at")
    search_fields = ("tracking_id",)


# =========================
# PARTNERS
# =========================

@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    list_display = (
        "tracking_id",
        "company_name",
        "partner_type",
        "user",
        "is_authorized",
    )
    list_filter = ("partner_type", "is_authorized")
    search_fields = ("tracking_id", "company_name", "user__username")


# =========================
# CORE LOGISTICS
# =========================
@admin.register(ParentCompany)
class ParentCompanyAdmin(admin.ModelAdmin):
    list_display = ("tracking_id", "name", "country", "city")
    search_fields = ("name",)

@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ("tracking_id", "name", "parent_company", "site_address")
    list_filter = ("parent_company",)
    search_fields = ("name",)


@admin.register(Warehouse)
class WarehouseAdmin(BaseAdmin):
    list_display = ("tracking_id", "name", "factory", "is_authorized")
    list_filter = ("factory",)
    search_fields = ("tracking_id", "name")


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("tracking_id", "name", "is_authorized")
    search_fields = ("tracking_id", "name")


# =========================
# INVENTORY
# =========================

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity")
    list_filter = ("warehouse", "product")
    search_fields = ("product__name", "warehouse__name")
    readonly_fields = ("product", "warehouse")

    def has_add_permission(self, request):
        return False  # inventory updated only via movements


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
        "authorization_time",
        "authorized_by",
    )

    list_display = (
        "created_at",
        "product",
        "movement_type",
        "quantity",
        "source_warehouse",
        "destination_warehouse",
        "reference",
    )

    list_filter = (
        "movement_type",
        "source_warehouse",
        "destination_warehouse",
    )

    search_fields = ("reference", "product__name")
    ordering = ("-created_at",)


# =========================
# PROCUREMENT
# =========================

class PurchaseReceiptItemInline(admin.TabularInline):
    model = PurchaseReceiptItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(BaseAdmin):
    list_display = ("tracking_id", "supplier", "is_authorized", "created_at")
    list_filter = ("supplier", "is_authorized")
    search_fields = ("tracking_id", "supplier__company_name")


@admin.register(PurchaseReceipt)
class PurchaseReceiptAdmin(BaseAdmin):
    list_display = ("tracking_id", "purchase_order", "warehouse", "received_at")
    list_filter = ("warehouse",)
    inlines = [PurchaseReceiptItemInline]

    def save_model(self, request, obj, form, change):
        if not obj.authorized_by:
            obj.authorized_by = request.user
            obj.is_authorized = True
        super().save_model(request, obj, form, change)


# =========================
# SALES
# =========================

class SalesDispatchItemInline(admin.TabularInline):
    model = SalesDispatchItem
    extra = 1


@admin.register(SalesOrder)
class SalesOrderAdmin(BaseAdmin):
    list_display = ("tracking_id", "customer", "is_authorized", "created_at")
    list_filter = ("customer", "is_authorized")
    search_fields = ("tracking_id", "customer__company_name")


@admin.register(SalesDispatch)
class SalesDispatchAdmin(BaseAdmin):
    list_display = ("tracking_id", "sales_order", "warehouse", "dispatched_at")
    list_filter = ("warehouse",)
    inlines = [SalesDispatchItemInline]

    def save_model(self, request, obj, form, change):
        if not obj.authorized_by:
            obj.authorized_by = request.user
            obj.is_authorized = True
        super().save_model(request, obj, form, change)
