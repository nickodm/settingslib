# `Setting` Class Documentation

```python
class Setting(Generic[_T])
```

The `Setting` class is the basic class of this library to manage settings.

All the settings added to [`SettingsManager`] objects (like [`Settings`] and [`NestedSettings`]) are instances of this class.

## Properties

### value

```python
# Defined in the __init__() method.
```

The value of the setting. It can be any JSON and TOML serializable object.

### default

```python
# Defined in the __init__() method.
```

The default value of the setting. It can be any JSON and TOML serializable object.

### comment

```python
# Defined in the __init__() method.
```

The comment of the setting, defaults to an empty string. If given, this will be displayed above the setting in [TOML] settings file, like this:

```toml
[settings]
# An example setting.
foo = "bar"
```

## Instance Methods

### is_nested()

```python
def is_nested(self) -> bool
```

Whether the setting is a nested setting. In this case, the method will always return `False`.

### is_default()

```python
def is_default(self) -> bool
```

Whether the setting is in its default value.

### update()

```python
def update(self, other: _T) -> Self
```

Change the value of the setting to `other`. This is an alias to `self.value = other`.

#### Arguments
|Argument | Type | Optional? | Description | Default |
| - | - | - | - | - |
| other | Any | No | The new value of the setting. | *No Default* |

### reset()

```python
def reset(self) -> Self
```

Set the value of the setting to the default one. This is an alias to `self.value = self.default`.

### as_dict()

```python
def as_dict(self) -> dict
```

Returns a `dict` representation of the `Setting` object.

## Dunder Methods

### \_\_eq\_\_()

```python
def __eq__(self, other: Self) -> bool
```

Compares the setting's value and default value with the other's value and default.

### \_\_dict\_\_()

```python
def __dict__(self) -> dict
```

Returns `self.as_dict()`.

### \_\_bool\_\_()

```python
def __bool__(self) -> bool
```

Returns `bool(self.value)`.

<!-- LINKS -->
[`Settings`]: ./Settings.md
[`SettingsManager`]: ./SettingsManager.md
[`NestedSettings`]: ./NestedSettings.md
[TOML]: https://www.toml.io