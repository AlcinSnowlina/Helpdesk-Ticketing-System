# Copyright (c) 2025, snow and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Manager(Document):
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'

	def after_insert(self):
		if not frappe.db.exists("User", self.manager_email):
			user = frappe.get_doc({
	            "doctype": "User",
	            "email": self.manager_email,
	            "first_name": self.first_name,
	            "last_name": self.last_name,
	            "role_profile_name": "Manager", 
	            "send_welcome_email": 1
	        })
			user.insert(ignore_permissions=True)
		else:
			frappe.msgprint(f"User {self.manager_email} already exists.")
