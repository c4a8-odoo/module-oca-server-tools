import logging

from odoo.upgrade import util

# from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

_install_modules = [
    "purchase_shipping",
]

_delete_modules = [
    "stock_user_default_warehouse_purchase",
    "stock_user_default_warehouse_sale",
    "stock_user_default_warehouse_mrp",
    "stock_user_default_warehouse_base",
    "stock_dropshipping",
    "stock_sms",
    "product_state_stock_base",
    "stock_accountant",
    "approvals_purchase_stock",
    "spreadsheet_dashboard_stock",
    "spreadsheet_dashboard_purchase_stock",
    "stock_maintenance",
    "stock_enterprise",
    "spreadsheet_dashboard_stock_account",
    "project_purchase_stock",
    "sale_purchase_stock",
    "approval_purchase_stock",
    "sale_stock_margin",
    "sale_project_stock",
    "sale_subscription_stock",
    "sale_project_stock_account",
    "project_stock_account",
    "project_stock",
    "sale_purchase_stock_inter_company_rules",
    "purchase_stock",
    "sale_stock",
    "stock_account",
    "stock",
]


def migrate(cr, version):
    """
    Don't request an env for the base pre-migration as flushing the env in
    odoo/modules/registry.py will break on the 'base' module not yet having
    been instantiated.
    """
    _logger.info("Start stock pre-migration script")
    # env = api.Environment(cr, SUPERUSER_ID, {})
    # openupgrade.rename_fields(env, _fields_renames)

    for module in _install_modules:
        _logger.info("Installing module %s", module)
        util.force_install_module(cr, module)

    # stock cleanup
    cr.execute("DELETE FROM sale_order_line_stock_route_rel;")

    cr.execute(
        """
        ALTER TABLE purchase_order ADD COLUMN IF NOT EXISTS partner_shipping_id INT4;
        UPDATE purchase_order SET partner_shipping_id=dest_address_id
        WHERE dest_address_id IS NOT NULL;
        """
    )

    for module in _delete_modules:
        _logger.info("Uninstalling module %s", module)
        util.uninstall_module(cr, module)
