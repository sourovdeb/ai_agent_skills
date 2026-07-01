---
name: "invoice-file-organizer"
description: "Load this skill when you need to organize financial data, receipts, accounting logs, or miscellaneous attachments. Applies smart categorical heuristics for structural tabular sorting."
---
# Invoice & File Organizer

Applies smart categorical heuristics to unorganized financial data, directories of receipts, accounting logs, and miscellaneous attachments to establish structural tabular sorting.

## Natural Triggers
- "organize my receipts"
- "sort financial documents"
- "categorize invoices"
- "clean up accounting files"
- "structure financial data"
- "file organization"
- "expense categorization"
- "document sorting"
- "financial cleanup"
- "tax document organization"

## Core Capabilities

### File Analysis
- Scan directory structures
- Identify file types
- Extract metadata
- Read file contents (when appropriate)
- Detect patterns

### Categorization
- Automatic category assignment
- Learn from user corrections
- Handle edge cases
- Custom category definitions
- Multi-level categorization

### Data Extraction
- Extract dates
- Identify amounts
- Parse vendor information
- Extract invoice numbers
- Identify tax information

### Structural Organization
- Create folder hierarchies
- Generate naming conventions
- Organize by date ranges
- Group by categories
- Create tabular representations

## Supported File Types

### Financial Documents
- Invoices (PDF, Word, Excel)
- Receipts (PDF, images, text)
- Purchase orders
- Quotes/Estimates
- Statements
- Tax forms

### Accounting Files
- Spreadsheets (CSV, Excel)
- QuickBooks files
- Bank statements
- Credit card statements
- Expense reports

### Miscellaneous
- Emails with financial data
- Scanned documents
- Screenshots
- Text files
- JSON data

## Categorization Schema

### Default Categories

#### Income
- Sales invoices
- Client payments
- Refunds
- Interest income
- Other income

#### Expenses
- **Office Supplies**
  - Stationery
  - Printer supplies
  - Software licenses
- **Travel**
  - Flights
  - Accommodation
  - Meals
  - Transportation
  - Car rental
- **Utilities**
  - Electricity
  - Internet
  - Phone
  - Water
- **Professional Services**
  - Legal fees
  - Accounting fees
  - Consulting fees
- **Marketing**
  - Advertising
  - Promotional materials
  - Events
- **Technology**
  - Hardware
  - Software
  - Hosting
  - Domains
- **Facilities**
  - Rent
  - Maintenance
  - Cleaning
- **Insurance**
  - Business insurance
  - Health insurance
  - Liability insurance
- **Taxes**
  - Income tax
  - Sales tax
  - Payroll tax

#### Assets
- Equipment purchases
- Vehicle purchases
- Property purchases
- Investments

#### Liabilities
- Loans
- Credit cards
- Lines of credit
- Accounts payable

#### Tax Documents
- W-9 forms
- 1099 forms
- W-2 forms
- Tax returns
- Deduction receipts

### Custom Categories
Users can define their own categories based on:
- Business-specific needs
- Industry standards
- Personal preferences
- Accounting system requirements

## Workflow

### Step 1: Discovery
- Scan specified directory
- Identify all files
- Extract basic metadata (size, type, dates)
- Sample file contents for categorization clues

### Step 2: Analysis
- Detect file types
- Extract text from PDFs and images (OCR)
- Parse structured data (CSV, Excel)
- Identify patterns and similarities
- Group similar files

### Step 3: Categorization
- Apply categorization rules
- Use machine learning for pattern matching
- Handle ambiguous cases
- Request user input for uncertain items
- Learn from user corrections

### Step 4: Organization
- Create directory structure
- Move files to appropriate locations
- Rename files for consistency
- Generate index files
- Create tabular summaries

### Step 5: Validation
- Verify all files are categorized
- Check for duplicates
- Validate extracted data
- Confirm user satisfaction
- Generate reports

## Organization Strategies

### By Date
```
/Financials/
  /2026/
    /01-January/
      /Invoices/
      /Receipts/
      /Statements/
    /02-February/
      ...
```

### By Category
```
/Financials/
  /Income/
    /Invoices/
    /Payments/
  /Expenses/
    /Office_Supplies/
    /Travel/
    /Utilities/
  /Assets/
  /Liabilities/
```

### By Vendor
```
/Financials/
  /Vendors/
    /Amazon/
    /Google/
    /Microsoft/
    /Local_Suppliers/
```

### Hybrid Approach
```
/Financials/
  /2026/
    /Income/
      /Invoices/
        /Client_A/
        /Client_B/
    /Expenses/
      /Office_Supplies/
      /Travel/
```

## Data Extraction

### From Invoices
- Invoice number
- Date issued
- Due date
- Vendor name
- Vendor contact
- Line items
- Amounts
- Tax amounts
- Total amount
- Payment terms
- Payment status

### From Receipts
- Date of purchase
- Vendor
- Items purchased
- Amount
- Payment method
- Transaction ID
- Tax information

### From Bank Statements
- Transaction date
- Description
- Amount
- Balance
- Transaction type
- Reference number

## Output Formats

### Directory Structure
Physical organization of files on disk with meaningful folder names and consistent naming conventions.

### Tabular Data
CSV or Excel files with structured data:
```csv
Filename,Category,Subcategory,Date,Amount,Vendor,Status,Notes
invoice_001.pdf,Income,Client Payments,2026-01-15,1500.00,Acme Corp,Paid,
receipt_042.jpg,Expenses,Office Supplies,2026-01-20,125.50,Staples,Unreimbursed,
```

### Database
Structured database with:
- Files table
- Categories table
- Vendors table
- Transactions table
- Relationships between entities

### Reports
- Summary by category
- Monthly spending
- Vendor analysis
- Tax-deductible expenses
- Outstanding invoices

## Smart Heuristics

### File Naming Patterns
- `invoice_*.pdf` → Invoices
- `receipt_*.jpg` → Receipts
- `statement_*.pdf` → Bank statements
- `PO_*.pdf` → Purchase orders

### Content Patterns
- "Invoice No:" → Invoice number
- "Total:" → Amount
- "Due Date:" → Due date
- "Vendor:" → Vendor name
- "Thank you for your purchase" → Receipt

### Date Detection
- File creation date
- File modification date
- Dates in filenames
- Dates in content
- Standard date formats

### Amount Detection
- Currency symbols ($, €, £, etc.)
- Number patterns (1,000.00)
- "Total:", "Amount:", "Subtotal:"
- Tax calculations

## Quality Standards

### Accuracy
- Correct categorization
- Accurate data extraction
- Proper date handling
- Correct amount parsing

### Completeness
- All files processed
- All relevant data extracted
- No files left uncategorized
- All edge cases handled

### Consistency
- Uniform naming conventions
- Consistent categorization
- Standardized date formats
- Uniform currency handling

### Usability
- Intuitive organization
- Easy to navigate
- Clear naming
- Helpful reports

## Best Practices

### For Users
- Provide clear directory paths
- Specify categorization preferences
- Define custom categories upfront
- Review and validate results
- Provide feedback for improvement

### For Implementation
- Handle large directories efficiently
- Process files in batches
- Provide progress updates
- Handle errors gracefully
- Preserve original files

### For Maintenance
- Regularly update categorization rules
- Learn from user corrections
- Adapt to new file types
- Improve accuracy over time

## Security & Privacy

### Sensitive Data
- Handle financial data carefully
- Don't store sensitive information unnecessarily
- Comply with data protection regulations
- Secure file storage

### Access Control
- Respect file permissions
- Don't access unauthorized directories
- Request explicit permission
- Document data access

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills

## Integration with Other Skills
- **Tapestry Knowledge Graphs**: For creating knowledge graphs of financial data
- **Content Research Writer**: For generating financial reports
- **Superpowers**: For complex financial organization workflows
