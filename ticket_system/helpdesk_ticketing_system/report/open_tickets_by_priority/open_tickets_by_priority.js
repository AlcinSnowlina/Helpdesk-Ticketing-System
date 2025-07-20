// Copyright (c) 2025, snow and contributors
// For license information, please see license.txt

frappe.query_reports["Open Tickets by Priority"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            //reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date"
        },
        {
            fieldname: "priority",
            label: "Priority",
            fieldtype: "Select",
            options: ["", "High", "Medium", "Low"]
        },
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: ["", "Open", "On Process", "Completed","In Progress", "Closed", "Failed"]
        }
    ]
};
