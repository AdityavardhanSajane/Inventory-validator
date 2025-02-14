import re
import os
import logging
from typing import Optional

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def validate_spk_name(spk_name: str) -> bool:
    """
    Validate SPK name format
    Returns True if valid, False otherwise
    """
    if not spk_name or not isinstance(spk_name, str):
        return False
    # SPK names should only contain alphanumeric characters, underscores, and hyphens
    # and should be between 3 and 50 characters long
    return bool(re.match(r'^[A-Za-z0-9_-]{3,50}$', spk_name))

def ensure_output_directory() -> Optional[str]:
    """
    Ensure the output directory exists and is writable
    Returns the directory path if successful, None if there are permission issues
    """
    output_dir = 'reports'
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Test write permissions
        test_file = os.path.join(output_dir, '.write_test')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return output_dir
        except (IOError, OSError) as e:
            logging.error(f"Directory {output_dir} is not writable: {str(e)}")
            return None
    except Exception as e:
        logging.error(f"Error creating output directory: {str(e)}")
        return None