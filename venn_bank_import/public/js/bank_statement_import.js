frappe.ui.form.on("Bank Statement Import", {
	refresh(frm) {
		frm.trigger("venn_toggle_fields");
	},

	import_venn_format(frm) {
		frm.trigger("venn_toggle_fields");
		frm.dirty();
	},

	venn_toggle_fields(frm) {
		if (frm.doc.import_venn_format) {
			frm.set_value("import_mt940_fromat", 0);
			frm.set_df_property("import_mt940_fromat", "hidden", 1);
			frm.set_df_property("custom_delimiters", "hidden", 1);
			frm.set_df_property("google_sheets_url", "hidden", 1);

			if (frm.is_new()) {
				frm.set_df_property(
					"import_venn_format",
					"description",
					__("Save the document first in order to attach a file")
				);
			} else {
				frm.set_df_property(
					"import_venn_format",
					"description",
					__("Venn bank statement CSV will be automatically converted to ERPNext format")
				);
			}
		} else {
			frm.set_df_property("import_mt940_fromat", "hidden", 0);
			frm.set_df_property("custom_delimiters", "hidden", 0);
			frm.set_df_property("google_sheets_url", "hidden", 0);
			frm.set_df_property("import_venn_format", "description", "");
		}
	},

	import_file(frm) {
		if (
			frm.doc.import_venn_format &&
			frm.doc.import_file &&
			!frm._venn_converting &&
			!frm.doc.import_file.includes("_venn_converted")
		) {
			frm.trigger("venn_convert_file");
		}
	},

	venn_convert_file(frm) {
		if (!frm.doc.import_file || frm._venn_converting) return;

		const file = frm.doc.import_file.toLowerCase();
		if (!file.endsWith(".csv")) {
			frappe.msgprint(__("Venn import expects a CSV file. Please upload a .csv file."));
			return;
		}

		frm._venn_converting = true;

		frappe.show_alert({
			message: __("Converting Venn CSV to ERPNext format..."),
			indicator: "blue",
		});

		frappe
			.call({
				method: "venn_bank_import.venn_converter.convert_venn_csv",
				args: {
					data_import: frm.doc.name,
					file_path: frm.doc.import_file,
				},
			})
			.then((r) => {
				frm._venn_converting = false;
				if (r.message) {
					frappe.show_alert({
						message: __("Venn CSV converted successfully!"),
						indicator: "green",
					});
					// Apply the converted file and auto-mapped template options
					frm.set_value("import_file", r.message.file_url);
					frm.set_value("template_options", r.message.template_options);
					frm.save();
				}
			})
			.catch(() => {
				frm._venn_converting = false;
			});
	},
});
