import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	create_custom_fields(
		{
			"Bank Statement Import": [
				{
					"default": "0",
					"fieldname": "import_venn_format",
					"fieldtype": "Check",
					"label": "Import Venn Format",
					"insert_after": "import_mt940_fromat",
					"description": "Enable this to automatically convert Venn bank statement CSV files to ERPNext format",
				},
			]
		}
	)


def before_uninstall():
	frappe.db.delete(
		"Custom Field",
		{
			"dt": "Bank Statement Import",
			"fieldname": "import_venn_format",
		},
	)
