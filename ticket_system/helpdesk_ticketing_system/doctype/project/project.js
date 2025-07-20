// Copyright (c) 2025, snow and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project", {
    onload: function(frm) {
        if (frm.is_new()) {
            // Step 1: Get current user email
            let email = frappe.session.user;

            // Step 2: Find matching Client by email_id
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Client',
                    filters: {
                        email_id: email
                    },
                    fields: ['name', 'first_name', 'last_name', 'email_id'],
                    limit_page_length: 1
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let client = r.message[0];
                        let full_name = `${client.first_name} ${client.last_name || ''}`.trim();

                        frm.set_value('client', full_name);     // Assuming you have a client_name field
                        frm.set_value('client_email', client.email_id);
                    }
                }
            });
        }
    }
});
