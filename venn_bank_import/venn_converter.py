import csv
import io
import json

import frappe
from frappe import _
from frappe.utils.file_manager import get_file, save_file


ERPNEXT_HEADERS = [
	"Date",
	"Deposit",
	"Withdrawal",
	"Description",
	"Reference Number",
	"Bank Account",
	"Currency",
]

COLUMN_TO_FIELD_MAP = {
	"Date": "date",
	"Deposit": "deposit",
	"Withdrawal": "withdrawal",
	"Description": "description",
	"Reference Number": "reference_number",
	"Bank Account": "bank_account",
	"Currency": "currency",
}


def is_venn_format(content: str) -> bool:
	"""Check if CSV content matches the Venn bank statement format."""
	try:
		reader = csv.reader(io.StringIO(content))
		headers = next(reader)
		headers = [h.strip() for h in headers]
		required = {"Date", "Time", "Transaction Type", "Amount", "Balance", "Merchant", "Category"}
		return required.issubset(set(headers))
	except Exception:
		return False


def convert_venn_to_erpnext_csv(rows: list[dict], bank_account: str) -> str:
	"""Convert parsed Venn CSV rows to ERPNext Bank Transaction CSV format."""
	csv_buffer = io.StringIO()
	writer = csv.writer(csv_buffer)
	writer.writerow(ERPNEXT_HEADERS)

	for row in rows:
		amount_str = row.get("Amount", "0").strip()
		try:
			amount = float(amount_str)
		except ValueError:
			continue

		deposit = amount if amount > 0 else ""
		withdrawal = abs(amount) if amount < 0 else ""

		# Build a rich description from available fields
		parts = []
		desc = row.get("Description", "").strip()
		merchant = row.get("Merchant", "").strip()
		category = row.get("Category", "").strip()
		txn_type = row.get("Transaction Type", "").strip()
		memo = row.get("Memo", "").strip()

		if desc:
			parts.append(desc)
		if merchant and merchant != desc:
			parts.append(merchant)
		if category:
			parts.append(f"[{category}]")
		if txn_type:
			parts.append(f"({txn_type})")

		description = " | ".join(parts)
		if memo:
			description += f" | {memo}"

		# Use Description + Date + Time as reference
		date_str = row.get("Date", "").strip()
		time_str = row.get("Time", "").strip()
		reference = f"{desc} {date_str} {time_str}".strip()

		currency = row.get("Currency", "").strip()

		writer.writerow([date_str, deposit, withdrawal, description, reference, bank_account, currency])

	result = csv_buffer.getvalue()
	csv_buffer.close()
	return result


@frappe.whitelist()
def convert_venn_csv(data_import: str, file_path: str) -> dict:
	"""Convert an uploaded Venn CSV to ERPNext Bank Transaction format.

	Returns dict with file_url and template_options for the client to apply.
	"""
	doc = frappe.get_doc("Bank Statement Import", data_import)

	_file_doc, content = get_file(file_path)

	if isinstance(content, bytes):
		content = content.decode("utf-8-sig")

	if not is_venn_format(content):
		frappe.throw(_("The uploaded file does not appear to be in Venn bank statement CSV format."))

	reader = csv.DictReader(io.StringIO(content))
	rows = list(reader)

	if not rows:
		frappe.throw(_("The uploaded CSV file contains no transaction rows."))

	converted_csv = convert_venn_to_erpnext_csv(rows, doc.bank_account)

	filename = f"{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}_venn_converted.csv"
	saved_file = save_file(
		filename,
		converted_csv.encode("utf-8"),
		doc.doctype,
		doc.name,
		is_private=True,
		df="import_file",
	)

	return {
		"file_url": saved_file.file_url,
		"template_options": json.dumps({"column_to_field_map": COLUMN_TO_FIELD_MAP}),
	}
