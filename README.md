# Inventory-validator

An automated Python tool for extracting and reporting Ansible Tower inventory data with secure credential management.

## Features

- Interactive authentication with secure credential storage
- Dynamic password expiry handling
- Encrypted credential management for multiple environments
- Robust API integration with Ansible Tower and XLR reporting
- Excel report generation with detailed inventory information

## Prerequisites

- Python 3.11
- Office VPN connection
- Access to internal Ansible Tower instances
- Access to XLR (Release Horizon)
- Read permissions for Ansible Tower inventories and XLR trains

## Required Python Packages

```bash
pip install rich beautifulsoup4 openpyxl requests cryptography typing-extensions
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>/Inventory-validator.git
cd Inventory-validator
```

2. Create required directories:
```bash
mkdir reports
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Optional: Set environment variables for non-interactive mode:
```bash
export ANSIBLE_NBK_ID=your_nbk_id
export ANSIBLE_PASSWORD=your_password
export ANSIBLE_INSTANCE=NON_PROD  # or PROD
```

## Usage

Run the tool:
```bash
python ansible_inventory_reporter.py
```

The tool will:
1. Prompt for authentication (or use environment variables)
2. Verify connectivity to required services
3. Allow you to search for specific SPK inventories
4. Generate Excel reports in the `reports` directory

## Files Created by the Tool

- `.key`: Secure credential storage
- `.credentials`: Encrypted credentials (if saved)
- `ansible_inventory_reporter.log`: Application logs
- Reports are saved in the `reports` directory

## Security Notes

- Credentials are encrypted using Fernet encryption
- The tool supports both interactive and non-interactive authentication
- Failed login attempts are tracked to prevent unauthorized access

## Support

For issues related to:
- Ansible Tower access: Contact your Ansible Tower administrator
- XLR access: Contact your Release Horizon support team
- Tool functionality: Open an issue in this repository
