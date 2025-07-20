
import frappe
from frappe.model.document import Document

class Developer(Document):
	def after_insert(self):
		if not frappe.db.exists("User", self.developer_email):
			user = frappe.new_doc("User")
			user.first_name = self.developer_name
			user.email = self.developer_email
			user.send_welcome_email = 1
			user.append("roles", {"role": "Developer"})
			user.save(ignore_permissions=True)

			self.user_id = user.name
			self.save(ignore_permissions=True)

			frappe.get_doc({
				"doctype": "User Permission",
				"user": self.developer_email,
				"allow": "Developer",
				"for_value": self.name
			}).insert(ignore_permissions=True)