# `SettingsManager` Class Documentation

```python
class SettingsManager
```

Abstract class that wraps a Python's `dict` with `Setting` objects.

This class includes all the methods for managing settings. It doesn't reads or writes in any kind of file.

[`Settings`](./Settings.md) and [`NestedSettings`](./NestedSettings.md) inherit the majority of their methods from this class.

## Instance Methods

### set()

```python
    def set(self,
        key: str, *, 
        value: _T | None = ..., 
        default: _T | None = ...,
        comment: _T | None = ...) -> Setting[_T]
```

Set the properties of a setting. 

It doesn't creates a new setting. For that, use [`self.new()`](./SettingsManager.md#new).

At least one of the arguments in addition to `key` must be filled. Otherwise, the method will raise `TypeError`.

Returns the modified setting.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| key | str | No | The key to find the setting. | *No Default* |
| value | Any | Yes | The new value for the setting. | ... |
| default | Any | Yes | The new default for the setting. | ... |
| comment | str | Yes | The new comment for the setting. | "" |

#### Raises
| Exception | When |
| - | - |
| KeyError | When the `key` setting doesn't exists. |
| TypeError | When all the arguments except `key` are empty. |

### new()

```python
def new(self, key: str, value: _T, default: _T | None = ..., comment: str = "") -> Setting[_T]
```

Creates a new setting or overrides the existing one.

It supports [nested keys][nestingSettings].

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| key | str | No | The key of the setting to create or override. | *No Default* |
| value | Any | No | The value for the new setting. | *No Default* |
| default | Any | Yes | The default value for the new setting. | The `value` argument. |
| comment | str | Yes | The comment for the new setting. | "" |

### nest()

```python
def nest(self, key: str, *, comment: str = "") -> NestedSettings
```

Nests settings into another settings, creating a hierarchy of them.

#### Example of nested settings

In JSON:

```json
"api": {
    "enabled": true,
    "connection": {
        "base_url": "https://www.api.cl",
        "custom_key": ""
    }
}
```

In TOML:

```toml

# *--- API SETTINGS ---*

[settings.api]
enabled = true

[settings.api.connection]
# The base URL for the API.
base_url = "https://www.api.cl"
# The custom user's API key.
custom_key = ""
```

In this example, "api" is a nested setting, which has a normal setting ("normal") and another nested setting ("connection").

For more information about nested settings, see the [documentation about this][nestingSettings].

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| key | str | No | The key to get the nested setting. | *No Default* |
| comment | str | Yes | The comment to display above the nested setting in TOML files. | "" |

### update()

```python
def update(self, other: dict[str, Setting | Any] | SettingsManager) -> Self
```

Update the settings from the given object `other`.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| other | dict[str, Setting \| Any ] \| SettingsManager | No | The other dictionary or SettingsManager object to update the settings. | *No Default* |

### get()

```python
def get(self, key: str, default: _T | None = None) -> Setting | _T
```

Gets the `Setting` object with the key `key`, if exists. Otherwise, returns `default`.

It supports [nested keys][nestingSettings].

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| key | str | No | The key to get the setting. | *No Default* |
| default | Any | Yes | The value to return if the setting is not found. | None |

### items()

```python
def items(self, *, deep: bool = False) -> Iterator[tuple[str, Setting]]
```

Iterates over the settings, similar to the Python's native `dict.items()`.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| deep | bool | Yes | Whether to include nested settings items also. | False |

### keys()

```python
def keys(self, *, deep: bool = False) -> Iterator[str]
```

Iterates over the settings keys, similar to the Python's native `dict.keys()`.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| deep | bool | Yes | Whether to include nested settings keys also. | False |

### items()

```python
def values(self, *, deep: bool = False) -> Iterator[Setting]
```

Iterates over the settings objects, similar to the Python's native `dict.values()`.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| deep | bool | Yes | Whether to include nested settings also. | False |

### setdefault()

```python
def setdefault(self, key: str, default: _T, comment: str = "") -> Setting[_T]
```

Returns the setting with the key, if exists. If not, creates a new setting with the given key and returns it. Similar to Python's native `dict.setdefault()`.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| key | str | No | The setting key. | *No Default* |
| default | Any | No | The default value to set to the setting if doesn't exists. | *No Default* |
| comment | str | Yes | The comment for the setting if doesn't exists. | "" |

### has()

```
def has(self, key: str) -> bool
```

Check if the setting `key` is in the settings. It supports [nested keys][nestingSettings].

[nestingSettings]: ../guides/nestingSettings.md

### as_dict()
```python
def as_dict(self) -> dict[str, Any]
```

Generates a dictionary with the keys and the values of the settings. Does not includes the default values or the comments.

### *abstractmethod* copy()

```python
@abc.abstractmethod
def copy(self) -> Self
```

Creates a shallow copy of `self`.

### unwrap()

```python
def unwrap(self) -> dict[str, Setting]
```

Returns the wrapped dict of settings.

It is not a copy, so be careful when doing changes.

### reset()

```python
def reset(self) -> Self
```

Set all the settings to ther default value.

## Dunder Methods

### \_\_in\_\_()

```python
def __in__(self, key: str) -> bool
```

Checks if the key is in the settings, by calling [`self.has(key)`](./SettingsManager.md#has).

It supports [nested keys][nestingSettings].

### \_\_eq\_\_()

```python
def __eq__(self, other: SettingsManager | dict) -> bool
```

Compares another `SettingsManager` or a Python's `dict` with `self`.

### \_\_getitem\_\_()

```python
def __getitem__(self, key: str) -> bool
```

Support for `self[key]` operations.

It supports [nested keys][nestingSettings].

### \_\_setitem\_\_()

```python
def __setitem__(self, key: str, value: Setting | Any) -> bool
```

Support for `self[key] = value` operations.

It supports [nested keys][nestingSettings].


### \_\_dict\_\_()

```python
def __dict__(self)
```

Support for ``dict(self)` operations, by returning [`self.as_dict()`](./SettingsManager.md#as_dict).

### \_\_enter\_\_()

```python
def __enter__(self) -> Self
```

Support for context managers. Only returns `self`.

To get more information about using context managers in this library, see [its guide](../guides/context_manager.md).

### \_\_exit\_\_()

```python
def __exit__(self, *args, **kw) -> Self
```

Support for context managers. Does nothing to the settings.

To get more information about using context managers in this library, see [its guide](../guides/context_manager.md).