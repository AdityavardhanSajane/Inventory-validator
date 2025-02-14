from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Optional, Dict, Any
import logging
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from config import XLR_CONFIG
import os
import ssl
import certifi

logger = logging.getLogger('AnsibleInventoryReporter')

class XLRClient:
    def __init__(self, environment: str, nbk_id: str, password: str):
        """Initialize XLR client with NBK credentials"""
        self.base_url = XLR_CONFIG['BASE_URL']
        self.username = nbk_id
        self.password = password
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(nbk_id, password)

        # SSL Certificate handling
        ssl_cert_file = os.getenv('SSL_CERT_FILE')
        if ssl_cert_file and os.path.exists(ssl_cert_file):
            self.session.verify = ssl_cert_file
            logger.info(f"Using custom SSL certificate: {ssl_cert_file}")
        else:
            # Use default verification
            self.session.verify = True
            logger.info("Using default SSL certificate verification")

    def _validate_url(self, xlr_train_url: str) -> bool:
        """Validate XLR train URL format"""
        try:
            result = urlparse(xlr_train_url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False

    def _check_ssl_configuration(self):
        """Verify SSL configuration and provide helpful error messages"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.SSLError as e:
            logger.error("SSL Certificate Verification Failed!")
            logger.error("Please check the following:")
            logger.error("1. You are connected to the office VPN")
            logger.error("2. You have the correct corporate SSL certificates")
            logger.error("3. SSL_CERT_FILE environment variable is set correctly")
            logger.error(f"Detailed error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            raise

    def get_components_from_train(self, xlr_train_url: str) -> List[str]:
        """
        Fetch component names from XLR train's Relationship view using web scraping
        since we're working with the web interface
        """
        try:
            if not self._validate_url(xlr_train_url):
                logger.error(f"Invalid XLR train URL: {xlr_train_url}")
                raise ValueError("Invalid XLR train URL format")

            # Verify SSL configuration first
            self._check_ssl_configuration()

            # First authenticate with XLR
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=Console()
            ) as progress:
                task = progress.add_task("[cyan]Authenticating with XLR train...[/cyan]", total=None)
                response = self.session.get(xlr_train_url, timeout=30)

                if response.status_code == 401:
                    logger.error("Invalid NBK credentials for XLR")
                    raise ValueError("Invalid NBK credentials for XLR access")

                response.raise_for_status()

                # Parse the HTML response
                progress.update(task, description="[cyan]Parsing XLR train components...[/cyan]")
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract components from the Relationship view
                components = []
                relationship_view = soup.find('div', {'class': 'relationship-view'})
                if relationship_view:
                    component_elements = relationship_view.find_all('div', {'class': 'component'})
                    for element in component_elements:
                        name_element = element.find('span', {'class': 'component-name'})
                        if name_element:
                            components.append(name_element.text.strip())

                if not components:
                    progress.update(task, description="[yellow]No components found in XLR train[/yellow]")
                    logger.warning(f"No components found in XLR train URL: {xlr_train_url}")
                    return []

                progress.update(task, description=f"[green]Successfully retrieved {len(components)} components![green]")
                logger.info(f"Successfully retrieved {len(components)} components from XLR train")
                return components

        except requests.exceptions.Timeout:
            logger.error("XLR request timed out")
            raise TimeoutError("Connection to XLR timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching XLR components: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in XLR request: {str(e)}")
            raise

    def _extract_train_id(self, xlr_train_url: str) -> str:
        """Extract train ID from XLR URL"""
        try:
            # Example: https://xlr.company.com/trains/12345 -> 12345
            return xlr_train_url.split('/')[-1]
        except Exception as e:
            logger.error(f"Failed to extract train ID from URL: {xlr_train_url}")
            raise ValueError(f"Invalid XLR train URL format: {str(e)}")

    def _parse_components(self, response_data: Dict[str, Any]) -> List[str]:
        """Parse XLR API response to extract component names"""
        try:
            components = []
            if 'relationships' in response_data:
                for rel in response_data['relationships']:
                    if 'component' in rel:
                        components.append(rel['component']['name'])
            return list(set(components))  # Remove duplicates
        except Exception as e:
            logger.error(f"Error parsing XLR API response: {str(e)}")
            raise ValueError(f"Invalid XLR API response format: {str(e)}")