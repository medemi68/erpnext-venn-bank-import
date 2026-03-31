app_name = "venn_bank_import"
app_title = "Venn Bank Import"
app_publisher = "Miguel Medeiros"
app_description = "Frappe plugin to import Venn bank statements into ERPNext"
app_email = "miguel@medeirosconsulting.ca"
app_license = "mit"

required_apps = ["erpnext"]

after_install = "venn_bank_import.install.after_install"
before_uninstall = "venn_bank_import.install.before_uninstall"

# Include JS in Bank Statement Import form
doctype_js = {"Bank Statement Import": "public/js/bank_statement_import.js"}
