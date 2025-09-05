"""
Utility functions.
"""

import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Returns the full, absolute resource path given the relative path.

    Arguments:
        relative_path (str): Relative path.
    
    Returns:
        str
    """
    
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
