"""
Patch SSL verification globally at Python startup time.
This runs before any other imports, ensuring litellm/httpx see the patched SSL.
"""
import ssl
import os

# Patch ssl.create_default_context to skip verification
_original_create_default_context = ssl.create_default_context

def _patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None):
    """Patched version that ignores cert verification."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

ssl.create_default_context = _patched_create_default_context

# Also patch ssl._create_default_https_context
ssl._create_default_https_context = _patched_create_default_context
