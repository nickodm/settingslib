# `Settings` class

## Properties

### path

```python
@property
def path(self) -> str
```

The path where the config file is located.

### file_type

```python
@property
def file_type(self) -> str
```

"""The type of the config file."""

### attributes

```python
@property
def attributes(self) -> dict[str, Any]
```

Special attributes of the settings. You can use it as you want.

### version

```python
@property
def version(self) -> str
```

The version of the software's settings. It's the same as `self.attributes["version"]`

## Methods

`Settings` objects also has a lot of methods related to the settings management (similar to a Python's dictionary) and to the reading and writting [TOML] and [JSON] files.

### __init__

```python
def __init__(self, *, path: str | Path, version: str = "")
```

<!-- TODO -->

### is_json()

```python
def is_json(self) -> bool
```

Whether `self.path.suffix` equals to ".json". Does not verifies if the file exists.

### is_toml ()

```python
def is_toml(self) -> bool
```

Whether `self.path.suffix` equals to ".toml". Does not verifies if the file exists.

### as_dict()

```python
def as_dict(self, *, include_defaults: bool = False) -> dict[str, Any]
```

Generates a dictionary with the keys and the values of the attributes and the settings.

Does not includes setting's comments or default values.

Example:
```python
{
    "attributes": {
        "version": "1.0.0",
        "custom_attribute": True
    },
    "settings": {
        "example_setting": True
    }
}
```

#### Arguments

|Argument | Type | Optional? | Description | Default |
| -     | - | - | - | - |
| include_defaults | bool | Yes | Whether the dict should include the default values. | False  |


### as_json()

```
def as_json(self) -> str
```

Generates a [JSON] string with the keys and the values of the settings.

Does not includes comments or default values.

### as_toml()

```
def as_toml(self) -> str
```

Generates a [TOML] object with the keys and the values of the settings.

Includes comments , but not default values.

### save_toml()

```python
def save_toml(self, p: str | Path) -> Self
```


### save_json

### save

### load_dict

### load_toml

### load_json

### load

### try_load

### copy

### \_\_exit\_\_

### \_\_repr\_\_

<!-- Links -->
[TOML]: https://www.toml.io
[JSON]: https://www.json.org