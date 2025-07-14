# Using Context Managers with `Settings`

You can use a `Settings` object with a context manager, to guarantee that the changes applied to the program's settings.

When the context manager exits, the settings are saved to `self.path`.

# Example

```python
from settingslib import Settings
from pathlib import Path

s = Settings(path=Path.home() / "settingslib/settings.toml")

with s:
    s.new("api.key", value="<api-key>", comment="The key of the API.")

# When the with block finishes, the settings are saved.
# THIS WILL OVERRIDE THE SETTINGS FILE IF EXISTS.
```

```python
from settingslib import Settings
from pathlib import Path

s = Settings(path=Path.home() / "settingslib/settings.toml")

s.new("api.key", value="<api-key>", comment="The key of the API")

s.save()

# THIS WILL OVERRIDE THE SETTINGS FILE IF EXISTS.
```