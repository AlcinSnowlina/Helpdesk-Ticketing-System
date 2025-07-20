# Copyright (c) 2025, snow and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters:
        filters = {}

    conditions = ["docstatus < 2"]
    params = {}

    if filters.get("status"):
        conditions.append("status = %(status)s")
        params["status"] = filters["status"]

    if filters.get("priority"):
        conditions.append("priority = %(priority)s")
        params["priority"] = filters["priority"]

    if filters.get("from_date"):
        conditions.append("creation >= %(from_date)s")
        params["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        # Include full to_date day
        to_date = datetime.strptime(filters["to_date"], "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
        conditions.append("creation <= %(to_date)s")
        params["to_date"] = to_date

    where_clause = "WHERE " + " AND ".join(conditions)

    columns = [
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Ticket Count", "fieldname": "count", "fieldtype": "Int", "width": 100}
    ]

    data = frappe.db.sql(f"""
        SELECT 
            priority, 
            status, 
            COUNT(*) AS count
        FROM `tabTicket`
        {where_clause}
        GROUP BY priority, status
        ORDER BY priority, status
    """, params, as_dict=True)

    return columns, data