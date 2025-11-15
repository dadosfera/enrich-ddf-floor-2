"""Configuration package for Enrich DDF Floor 2."""

# Export ports module
# Import settings from parent config.py for backward compatibility
# Note: config.py is in the parent directory, not in this package
# We use importlib to avoid circular import issues
import importlib.util
from pathlib import Path

from config import ports


parent_dir = Path(__file__).parent.parent
config_path = parent_dir / "config.py"
spec = importlib.util.spec_from_file_location("_config_module", config_path)
_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_config_module)

# Export settings
settings = _config_module.settings

__all__ = ["ports", "settings"]
