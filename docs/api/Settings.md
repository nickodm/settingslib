# Settings Class Documentation

```python
class Settings(SettingsManager)
```

`Settings` is the main class of this library. It behaves similar to a Python's common dictionary (because it's a wrapper of one), supporting reading and writting settings from [TOML] and [JSON] files.

`Settings` and `NestedSettings` classes inherit from `SettingsManager`, the class that manages the settings internally.

**The related to creating and editing settings are in [SettingsManager](./SettingsManager.md).**

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

The type of the config file.

### attributes

```python
@property
def attributes(self) -> dict[str, Any]
```

Special attributes of the settings. You can use it as you want.

For default, the attributes dict always includes a `version` key.

### version

```python
@property
def version(self) -> str
```

The version of the software's settings. It's the same as `self.attributes["version"]`.

## Instance Methods

`Settings` objects also has a lot of methods related to the settings management (similar to a Python's dictionary) and to the reading and writting [TOML] and [JSON] files.

**The methods related to creating and editing settings are in [SettingsManager](./SettingsManager.md).**

### \_\_init\_\_()

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

```python
def as_json(self, *, 
            indent: int = 4, 
            include_defaults: bool = False) -> str
```

Generates a [JSON] string with the keys and the values of the attributes and the settings.

As [JSON] doesn't support comments, they will be omited.

The returned string does not include comments or default values.

#### Arguments

|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| indent | int | Yes | The amount of spaces used as indentation in the JSON file. | 4 |
| include_defaults | bool | Yes | Whether the JSON should include the default values. | False |

You can see an example of a JSON file generated with this library by [clicking here](../tests/expected/expected.json).

### as_toml()

```python
def as_toml(self) -> tomlkit.TOMLDocument
```

Generates a [TOMLDocument](https://tomlkit.readthedocs.io/en/latest/api/#module-tomlkit.toml_document) object from the [tomlkit](https://github.com/sdispater/tomlkit) library with the keys and the values of the attributes and the settings.

Includes comments, but not default values.

You can see an example of a [TOML] file generated with this library by [clicking here](../tests/expected/expected.toml).

### save_toml()

```python
def save_toml(self, p: str | Path) -> Self
```

Saves the settings in a [TOML] file at `path`.

#### Arguments

|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| path | str \| [pathlib.Path] | No | The destiny path for the TOML file. | *No Default* |

### save_json()

```python
def save_json(self, path: str | Path, *, indent: int = 4) -> Self
```

Saves the settings in a JSON file at `path`.

#### Arguments

|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| path | str \| [pathlib.Path] | No | The destiny path for the JSON file. | *No Default* |
| indent | int | Yes | The amount of spaces used as indentation in the JSON file. | 4 |

### save()

```python
def save(self,
         path: str | Path = ...,
         *,
         json_indent: int = 4,
         create_dirs: bool = False) -> Self
```

Saves the settings in `self.path` or `path` if given, using the [TOML] or [JSON] according to the format.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| path | str \| [pathlib.Path] | Yes | The destiny path for the settings file. | `self.path` |
| json_indent | int | Yes | The amount of spaces used as indentation if the file is a [JSON]. | 4 |
| create_dirs | bool | Yes | Whether to create the parent directories that doesn't exists. | False |

### load_dict()
```python
def load_dict(self, d: _SettingsDict) -> Self
```

Loads settings from a dictionary.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| d | dict[str, dict[str, Any]] | No | The dictionary with the **attributes and settings** to load. | *No Default* |

### load_toml()

```python
def load_toml(self, s: str) -> Self
```

Loads settings from a TOML document.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| s | str | No | The TOML document as a string. | *No Default* |

### load_json()

```python
def load_json(self, s: str) -> Self
```

Loads settings from a JSON document.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| s | str | No | The JSON document as a string. | *No Default* |

### load()

```python
def load(self, path: str | Path = ...) -> Self
```

Loads the settings in `self.path` or in `path` (if provided) and updates the settings with the loaded ones.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| path | str \| [pathlib.Path] | Yes | The path of the settings file. It must be in TOML or JSON format. | `self.path` |

### try_load()

```python
def try_load(self, path: str | Path = ...) -> Self
```

Tries to load settings from `path` (or `self.path` if not given).

Instead of [`Settings.load()`](./Settings.md#load), this method doesn't raises `FileNotFoundError` when the `path` doesn't exists.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| path | str \| [pathlib.Path] | Yes | The path of the settings file. It must be in TOML or JSON format. | `self.path` |

### copy()

```python
def copy(self) -> Self
```

Returns a shallow copy of the settings.

### \_\_exit\_\_()

```python
def __exit__(self, *args, **kw) -> bool
```

Calls [`self.save()`](./Settings.md#save) when the context manager ends.

<!-- TODO-->
<!-- Read more about using context managers with this library in  -->

## Class Methods

### from_load()

```python
@classmethod
def from_load(cls, path: str | Path) -> Self:
```

Generates a `Settings` object from a loaded [TOML] or [JSON] file at `path`.

|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| path | str \| [pathlib.Path] | No | The path of the settings file to load. | *No Default* |

<!-- Links -->
[TOML]: https://www.toml.io
[JSON]: https://www.json.org
[pathlib.Path]: https://docs.python.org/3/library/pathlib.html#pathlib.Path