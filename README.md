# SettingsLib - Manage Settings Easily & Quickly

SettingsLib is a Python library to manage settings quickly.

It supports reading and writting in TOML and JSON files.

Read the documentation [here](./docs/index.md)!

# Usage
The library works exporting the class `Settings`.

## Code
```python
s = Settings(
    path="project_dir/settings.toml",
    version="1.0.0"
)

# Defining the settings.
s.new("type", value="sql", comment="The type of the database.")
s.new("host", value="localhost", comment="The host of the database.")
s.new("foo", value="bar", comment="Bla, bla, bla, bla.")

# Save them in settings.toml
s.save()
```

## Result
### TOML
```toml
[attributes]
version = "1.0.0"

[settings]
# The type of the database.
type = "sql"

# The host of the database.
host = "localhost"

# Bla, bla, bla, bla.
foo = "bar"
```

### JSON
```json
{
    "attributes": {
        "version": "1.0.0"
    },
    "settings": {
        "type": "sql",
        "host": "localhost",
        "foo": "bar"
    }
}
```