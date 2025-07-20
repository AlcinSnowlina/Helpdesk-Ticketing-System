# Copyright (c) 2025, snow and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Client(Document):
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'

	def after_insert(self):
		if not frappe.db.exists("User", self.email_id):
			user = frappe.new_doc("User")
			user.email = self.email_id
			user.first_name = self.full_name
			user.send_welcome_email = 1
			user.append("roles", {"role": "Client"})
			user.save(ignore_permissions=True)

            # Link user to client
			self.user_id = user.name
			self.save(ignore_permissions=True)

            # User permission
			frappe.get_doc({
                "doctype": "User Permission",
                "user": self.email_id,
                "allow": "Client",
                "for_value": self.name
            }).insert(ignore_permissions=True)