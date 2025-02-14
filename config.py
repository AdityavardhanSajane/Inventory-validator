import os
from typing import Dict, Literal

# Flag to enable demo mode for local testing
DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true'

# SSL Configuration
SSL_VERIFY = os.getenv('SSL_CERT_FILE', True)  # Use custom cert if provided, else verify
SSL_WARNINGS = os.getenv('PYTHONWARNINGS', None)  # For SSL warning suppression if needed

# Base URLs for different Ansible Tower environments
TOWER_BASE_URLS: Dict[Literal['NON_PROD', 'PROD'], Dict[str, str]] = {
    'NON_PROD': {
        'DEV': os.getenv('ANSIBLE_TOWER_DEV_URL', 'https://tower.dev.ansible.apps.baml.com/api/v2'),
        'LLE': os.getenv('ANSIBLE_TOWER_LLE_URL', 'https://tower.dev.ansible.apps.baml.com/api/v2')
    },
    'PROD': {
        'PROD': os.getenv('ANSIBLE_TOWER_PROD_URL', 'https://tower.prod.ansible.apps.baml.com/api/v2')
    }
}

# Demo URLs for local testing (using httpbin.org as a test endpoint)
DEMO_URLS = {
    'NON_PROD': {
        'DEV': 'https://httpbin.org/anything',
        'LLE': 'https://httpbin.org/anything'
    },
    'PROD': {
        'PROD': 'https://httpbin.org/anything'
    }
}

# XLR Configuration
XLR_CONFIG = {
    'BASE_URL': os.getenv('XLR_BASE_URL', 'https://release.horizon.bankofamerica.com'),
    'API_VERSION': 'v1',
    'BASE_URLS': {
        'DEV': os.getenv('XLR_DEV_URL', 'https://release.horizon.bankofamerica.com'),
        'PROD': os.getenv('XLR_PROD_URL', 'https://release.horizon.bankofamerica.com')
    },
    'DEMO_URLS': {  # Demo endpoints for local testing
        'DEV': 'https://httpbin.org/anything',
        'PROD': 'https://httpbin.org/anything'
    }
}

# Environment variable names for authentication
AUTH_CONFIG = {
    'NBK_ID_ENV_VAR': 'ANSIBLE_NBK_ID',
    'PASSWORD_ENV_VAR': 'ANSIBLE_PASSWORD',
    'DEFAULT_INSTANCE': 'NON_PROD'
}

# Logging configuration
LOG_CONFIG = {
    'filename': 'ansible_inventory_reporter.log',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'level': os.getenv('LOG_LEVEL', 'INFO')
}