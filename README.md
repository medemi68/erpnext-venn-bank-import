# Venn Bank Import

A Frappe plugin that adds support for importing [Venn](https://www.venn.ca/) bank statement CSV files into ERPNext's Bank Statement Import.

Venn does not export bank statements in the standard MT940 format. This plugin preprocesses Venn's proprietary CSV format and converts it into the format ERPNext expects, with automatic column mapping.

## How It Works

1. Open **Bank Statement Import** in ERPNext
2. Fill in **Company** and **Bank Account**, then save
3. Check **Import Venn Format**
4. Upload your Venn CSV file
5. The plugin automatically converts it and maps all columns
6. Click **Start Import**

### Field Mapping

| Venn CSV Column | ERPNext Bank Transaction Field |
|---|---|
| Date | Date |
| Amount (positive) | Deposit |
| Amount (negative) | Withdrawal |
| Description + Merchant + Category + Transaction Type | Description |
| Description + Date + Time | Reference Number |
| Currency | Currency |

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch main
bench install-app venn_bank_import
```

Or, for local development with a symlink:

```bash
ln -s /path/to/this/repo $PATH_TO_YOUR_BENCH/apps/venn_bank_import
cd $PATH_TO_YOUR_BENCH
bench install-app venn_bank_import
bench build --app venn_bank_import
```

## Disclaimer

This plugin is built against the Venn CSV export format as of early 2026. **Venn may change their CSV format at any time without notice**, which could break this plugin. There is no affiliation with or endorsement by Venn. If the import stops working, the CSV format has likely changed and the plugin will need to be updated accordingly.

The expected Venn CSV headers are:

```
Date, Time, Description, Transaction Type, Status, Currency, Amount, Balance, Name, Receipt Attached, Card last 4 numbers, Card Name, Merchant, Category, Memo
```

If your exported CSV has different headers, the plugin will not recognize it as a Venn file and will show an error.

## Requirements

- Frappe v16+
- ERPNext v16+

## License

MIT
