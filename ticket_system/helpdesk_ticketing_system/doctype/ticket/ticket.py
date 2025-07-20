# Copyright (c) 2025, snow and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Ticket(Document):
    
    def after_insert(self):
         self.set_deadline()
         self.send_confirmation_email()
        
    def before_save(self):
        self.sendmail()
        # self.deadline()
        
    def set_deadline(self):
        self.from_date = frappe.utils.nowdate()
        today = frappe.utils.nowdate()
        summ=0
        if self.priority == "High":
            self.dead_line = frappe.utils.add_days(today, 1)
        if self.priority == "Medium":
            self.dead_line = frappe.utils.add_days(today, 3)
        if self.priority == "Low":
            self.dead_line = frappe.utils.add_days(today, 5)
        self.save()
        
    def send_confirmation_email(self):

        developer_email = self.developer_email
        customer_email = self.client_email
        print("Developer Email:", developer_email)
        print("Customer Email:", customer_email)
        
        if customer_email:
            frappe.sendmail(
                recipients=[customer_email],

                subject=f"Ticket Confirmation - {self.name}",
                message=f"Dear {self.client},\n\nYour ticket has been submitted successfully.\n\nThanks,\nSupport Team"
            )

            frappe.sendmail(
                recipients=[developer_email],
                subject=f"Customer Raised an Ticket - {self.name}",
                message=f"Dear {self.developer},\n\nCustomer has submitted an Ticket.\n\nThanks,\nSupport Team"
            )

            frappe.log_error(frappe.get_traceback(), f"Ticket Sent successfully: {self.name}")
        
        else:
            frappe.log_error("No valid email found to send confirmation for Ticket: " + self.name)

    def sendmail(self):
        developer_email = self.developer_email
        customer_email = self.client_email
        manager = "alcinsnowlina@gmail.com"
        state=self.status
        if state == "In Progress":
            frappe.sendmail(
                recipients=[customer_email],
                subject=f"Ticket Confirmation - {self.name}",
                message=f"Dear {self.client},\n\nYour ticket has been In Progress.\n\nThanks,\nSupport Team"
            )

            frappe.sendmail(
                recipients=[manager],
                subject=f"Customer Raised a Ticket - {self.name}",
                message=f"Dear {manager},\n\n ticket has been In Progress.\n\nThanks,\nSupport Team"
            )
        elif state == "Closed":
            frappe.sendmail(
                recipients=[customer_email],
                subject=f"Ticket Closed - {self.name}",
                message=f"Dear {self.client},\n\nYour ticket has been Completed successfully.\n\nThanks,\nSupport Team"
            )

            frappe.sendmail(
                recipients=[manager],
                subject=f"Ticket Closed - {self.name}",
                message=f"Dear {manager},\n\nThe ticket has been Completed successfully.\n\nThanks,\nSupport Team"
            )
            
    
@frappe.whitelist()
def add_comment_and_notify(ticket, comment_text, role):
    manager = "alcinsnowlina@gmail.com"
    doc = frappe.get_doc("Ticket", ticket)
    if doc.status == "Closed":
        frappe.throw("You cannot comment on a closed ticket.")

    if role == "Client":
        client = doc.get("client_email")
        recipient_email = doc.get("developer_email")
        doc.status = "In Progress"
    else:
        client = doc.get("developer_email")
        recipient_email = doc.get("client_email")
        doc.status = "In Progress"

    timestamp = frappe.utils.now_datetime()
    doc.append("ticket_comments", {
        "comment_text": comment_text,
        "commented_by": client,
        "role": role,
        "timestamp": timestamp
    })

    doc.flags.ignore_validate_update_after_submit = True
    doc.flags.ignore_permissions = True
    doc.flags.ignore_version = True
    doc.save()

    if recipient_email:
        frappe.sendmail(
            recipients=[recipient_email],
            subject=f"New comment on Ticket {ticket}",
            message=comment_text,
            sender="alcinsnowlinars@gmail.com"  
        )

@frappe.whitelist()
def get_user_role_for_ticket():
    user = frappe.session.user

    developer = frappe.get_value("Developer", {"user_id": user}, "name")
    if developer:
        return "Developer"

    client = frappe.get_value("Client", {"user_id": user}, "name")
    if client:
        return "Client"
    
    return "Manager"

def deadline(self):
        frappe.log_error("Deadline Check", "Checking deadline for ticket")
        print("Checking deadline for ticket")
        manager="alcinsnowlina@gmail.com"
        from_date = self.get("from_date")
        deadline = self.get("deadline")

        if not from_date or not deadline:
            return

        if isinstance(from_date, str):
            from_date = frappe.utils.get_datetime(from_date)
        if isinstance(deadline, str):
            deadline = frappe.utils.get_datetime(deadline)

        if from_date > deadline:
            self.status = "Failed"
            frappe.sendmail(
                recipients=[manager],
                subject=f"Deadline Error for Ticket {self.name}",
                message=f"Dear Manager,<br><br>The From Date for Ticket {self.name} is after the Deadline.<br><br>Thanks,<br>Support Team"
            )
            frappe.sendmail(
                recipients=[self.client_email],
                subject=f"Deadline Error for Ticket {self.name}",
                message=f"Dear {self.client},<br><br>The From Date for your Ticket {self.name} is after the Deadline.<br><br>Thanks,<br>Support Team"
            )
        if self.docstatus == 1 and self.status == "Failed":
            self.cancel()


# # Copyright (c) 2025, snow and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class Ticket(Document):

#     def after_insert(self):
#         self.set_deadline()
#         self.send_confirmation_email()

#     def before_save(self):
#         self.sendmail()

#     def set_deadline(self):
#         self.from_date = frappe.utils.nowdate()
#         today = frappe.utils.nowdate()

#         if self.priority == "High":
#             self.dead_line = frappe.utils.add_days(today, 1)
#         elif self.priority == "Medium":
#             self.dead_line = frappe.utils.add_days(today, 3)
#         elif self.priority == "Low":
#             self.dead_line = frappe.utils.add_days(today, 5)

#         self.save()

#     def send_confirmation_email(self):
#         developer_email = self.developer_email
#         customer_email = self.client_email

#         client_msg = f"""
#         <p>Dear {self.client},</p>
#         <p>Your ticket has been successfully submitted. Our developer will address it shortly.</p>
#         <table style="border-collapse: collapse; width: 100%;">
#             <tr><td><strong>Ticket ID:</strong></td><td>{self.name}</td></tr>
#             <tr><td><strong>Subject:</strong></td><td>{self.subject}</td></tr>
#             <tr><td><strong>Priority:</strong></td><td>{self.priority}</td></tr>
#             <tr><td><strong>Expected Deadline:</strong></td><td>{self.dead_line}</td></tr>
#         </table>
#         <p>Thank you,<br><strong>Support Team</strong></p>
#         """

#         dev_msg = f"""
#         <p>Dear {self.developer},</p>
#         <p>A new ticket has been assigned to you.</p>
#         <table style="border-collapse: collapse; width: 100%;">
#             <tr><td><strong>Ticket ID:</strong></td><td>{self.name}</td></tr>
#             <tr><td><strong>Client:</strong></td><td>{self.client}</td></tr>
#             <tr><td><strong>Subject:</strong></td><td>{self.subject}</td></tr>
#             <tr><td><strong>Priority:</strong></td><td>{self.priority}</td></tr>
#         </table>
#         <p>Regards,<br><strong>Support Team</strong></p>
#         """

#         if customer_email:
#             frappe.sendmail(
#                 recipients=[customer_email],
#                 subject=f"Ticket Confirmation - {self.name}",
#                 message=client_msg
#             )
#             frappe.sendmail(
#                 recipients=[developer_email],
#                 subject=f"New Ticket Assigned - {self.name}",
#                 message=dev_msg
#             )
#             frappe.log_error("Confirmation emails sent", self.name)
#         else:
#             frappe.log_error("No customer email found", self.name)

#     def sendmail(self):
#         developer_email = self.developer_email
#         customer_email = self.client_email
#         manager_email = "alcinsnowlinars@gmail.com"

#         if self.status == "In Progress":
#             message = f"""
#             <p>Dear {self.client},</p>
#             <p>Your ticket <strong>{self.name}</strong> is now <strong>In Progress</strong>.</p>
#             <p>Thank you,<br>Support Team</p>
#             """
#             frappe.sendmail(recipients=[customer_email], subject=f"Ticket Update - {self.name}", message=message)

#             manager_msg = f"""
#             <p>Dear Manager,</p>
#             <p>Ticket <strong>{self.name}</strong> is now being worked on by the developer.</p>
#             <p>Regards,<br>System</p>
#             """
#             frappe.sendmail(recipients=[manager_email], subject=f"Ticket In Progress - {self.name}", message=manager_msg)

#         elif self.status == "Closed":
#             message = f"""
#             <p>Dear {self.client},</p>
#             <p>Your ticket <strong>{self.name}</strong> has been successfully <strong>closed</strong>.</p>
#             <p>We hope your issue was resolved.</p>
#             <p>Thanks,<br>Support Team</p>
#             """
#             manager_msg = f"""
#             <p>Dear Manager,</p>
#             <p>The ticket <strong>{self.name}</strong> has been closed by the developer.</p>
#             <p>Regards,<br>System</p>
#             """
#             frappe.sendmail(recipients=[customer_email], subject=f"Ticket Closed - {self.name}", message=message)
#             frappe.sendmail(recipients=[manager_email], subject=f"Ticket Closed - {self.name}", message=manager_msg)


# @frappe.whitelist()
# def add_comment_and_notify(ticket, comment_text, role):
#     manager_email = "alcinsnowlinars@gmail.com"
#     doc = frappe.get_doc("Ticket", ticket)

#     if doc.status == "Closed":
#         frappe.throw("You cannot comment on a closed ticket.")

#     if role == "Client":
#         sender = doc.get("client_email")
#         recipient = doc.get("developer_email")
#         doc.status = "In Progress"
#     else:
#         sender = doc.get("developer_email")
#         recipient = doc.get("client_email")
#         doc.status = "In Progress"

#     timestamp = frappe.utils.now_datetime()

#     doc.append("ticket_comments", {
#         "comment_text": comment_text,
#         "commented_by": sender,
#         "role": role,
#         "timestamp": timestamp
#     })

#     doc.flags.ignore_validate_update_after_submit = True
#     doc.flags.ignore_permissions = True
#     doc.flags.ignore_version = True
#     doc.save()

#     if recipient:
#         message = f"""
#         <p>Dear User,</p>
#         <p>You have a new comment on Ticket <strong>{ticket}</strong>:</p>
#         <blockquote style="border-left: 3px solid #ccc; padding-left: 10px;">{comment_text}</blockquote>
#         <p>Regards,<br>Support Team</p>
#         """
#         frappe.sendmail(
#             recipients=[recipient],
#             subject=f"New Comment on Ticket {ticket}",
#             message=message,
#             sender="support@yourcompany.com"
#         )


# @frappe.whitelist()
# def get_user_role_for_ticket():
#     user = frappe.session.user

#     developer = frappe.get_value("Developer", {"user_id": user}, "name")
#     if developer:
#         return "Developer"

#     client = frappe.get_value("Client", {"user_id": user}, "name")
#     if client:
#         return "Client"

#     return "Manager"


# def deadline(self):
#     manager_email = "alcinsnowlinars@gmail.com"
#     from_date = self.get("from_date")
#     deadline = self.get("deadline")

#     if not from_date or not deadline:
#         return

#     if isinstance(from_date, str):
#         from_date = frappe.utils.get_datetime(from_date)
#     if isinstance(deadline, str):
#         deadline = frappe.utils.get_datetime(deadline)

#     if from_date > deadline:
#         self.status = "Failed"

#         error_message = f"""
#         <p>Dear Manager,</p>
#         <p>The <strong>from date</strong> for Ticket <strong>{self.name}</strong> is after its deadline.</p>
#         <p>This may indicate incorrect ticket setup or delay in action.</p>
#         <p>Regards,<br>System</p>
#         """
#         frappe.sendmail(recipients=[manager_email], subject=f"Deadline Issue - Ticket {self.name}", message=error_message)

#         client_msg = f"""
#         <p>Dear {self.client},</p>
#         <p>Your ticket <strong>{self.name}</strong> has encountered a deadline issue. Please contact support.</p>
#         <p>Thanks,<br>Support Team</p>
#         """
#         frappe.sendmail(recipients=[self.client_email], subject=f"Deadline Issue - Ticket {self.name}", message=client_msg)

#     if self.docstatus == 1 and self.status == "Failed":
#         self.cancel()
