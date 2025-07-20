# Copyright (c) 2025, snow and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Count",
            "fieldname": "count",
            "fieldtype": "Int",
            "width": 100
        }
    ]

    data = frappe.db.sql("""
        SELECT status, COUNT(*) AS count
        FROM `tabTicket`
        GROUP BY status
    """, as_dict=True)

    return columns, data
