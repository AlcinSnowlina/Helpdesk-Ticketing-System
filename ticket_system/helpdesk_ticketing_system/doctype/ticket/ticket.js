frappe.ui.form.on("Ticket", {
    onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value("from_date", frappe.datetime.get_today());
        }
    },

    refresh: function(frm) {
        if (frm.doc.status !== "Closed") {
            frm.add_custom_button("Mark as Completed", function () {
                frappe.call({
                    method: "frappe.client.set_value",
                    args: {
                        doctype: "Ticket",
                        name: frm.doc.name,
                        fieldname: "status",
                        value: "Closed"
                    },
                    callback: function() {
                        frm.reload_doc();
                    }
                });
            }, __("Actions"));
        }

        frm.add_custom_button("Add Comment", function () {
            frappe.call({
                method: 'ticket_system.helpdesk_ticketing_system.doctype.ticket.ticket.get_user_role_for_ticket',
                callback: function(r) {
                    const userRole = r.message || "Unknown";

                    let d = new frappe.ui.Dialog({
                        title: 'Add Comment',
                        fields: [
                            {
                                label: 'Comment',
                                fieldname: 'comment_text',
                                fieldtype: 'Text Editor',
                                reqd: 1
                            },
                            {
                                label: 'Role',
                                fieldname: 'role',
                                fieldtype: 'Select',
                                options: ['Client', 'Developer', 'Manager'],
                                default: userRole,
                                read_only: 1
                            }
                        ],
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            if (!values.comment_text) {
                                frappe.msgprint("Comment cannot be empty");
                                return;
                            }

                            // Step 3: Send to backend
                            frappe.call({
                                method: 'ticket_system.helpdesk_ticketing_system.doctype.ticket.ticket.add_comment_and_notify',
                                args: {
                                    ticket: frm.doc.name,
                                    comment_text: values.comment_text,
                                    role: values.role
                                },
                                callback: function() {
                                    d.hide();
                                    frappe.msgprint("Comment added successfully");
                                    frm.reload_doc();
                                }
                            });
                        }
                    });

                    d.show();
                }
            });
        });
    }
});
