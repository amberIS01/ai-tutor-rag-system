"""
Environment Configuration Validator
Validates that all required environment variables are set
"""

import os
from typing import Dict, List, Tuple
from logger import logger


REQUIRED_ENV_VARS = {
    "OPENROUTER_API_KEY": "OpenRouter API key for LLM access",
    "MODEL_NAME": "Name of the LLM model to use"
}

OPTIONAL_ENV_VARS = {
    "LOG_LEVEL": "Logging level (default: INFO)",
    "MAX_FILE_SIZE_MB": "Maximum file upload size in MB (default: 50)",
    "CHUNK_SIZE": "PDF chunk size for processing (default: 1000)",
    "DATABASE_PATH": "Path to database file (default: ./data/app.db)"
}


def validate_environment() -> Tuple[bool, List[str]]:
    """
    Validate that all required environment variables are set
    
    Returns:
        Tuple of (is_valid, missing_vars)
    """
    missing = []
    
    for var_name in REQUIRED_ENV_VARS:
        if not os.getenv(var_name):
            missing.append(var_name)
            logger.warning(f"Missing required environment variable: {var_name}")
    
    return len(missing) == 0, missing


def get_environment_status() -> Dict[str, any]:
    """Get environment configuration status"""
    status = {
        "required_vars": {},
        "optional_vars": {},
        "all_valid": True
    }
    
    for var_name, description in REQUIRED_ENV_VARS.items():
        value = os.getenv(var_name)
        status["required_vars"][var_name] = {
            "description": description,
            "is_set": value is not None,
            "value": "***" if value else None
        }
        if not value:
            status["all_valid"] = False
    
    for var_name, description in OPTIONAL_ENV_VARS.items():
        value = os.getenv(var_name)
        status["optional_vars"][var_name] = {
            "description": description,
            "is_set": value is not None,
            "value": value
        }
    
    return status


def load_environment():
    """Load and validate environment configuration"""
    is_valid, missing = validate_environment()
    
    if not is_valid:
        logger.error(f"Environment validation failed. Missing: {', '.join(missing)}")
        raise RuntimeError(f"Missing required environment variables: {missing}")
    
    logger.info("Environment configuration validated successfully")
