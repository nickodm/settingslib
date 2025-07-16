<!-- TODO: Link ./Settings.md to this -->
# `NestedSettings` Class Documentation

```python
class NestedSettings(SettingsManager, Setting[dict[str, Any]])
```

`NestedSettings` are objects that manages settings and are a setting at the same time.

Internally, this class wraps a Python's dictionary with the settings.

`NestedSettings` inherits its **settings managing** methods from [`SettingsManager`](./SettingsManager.md) and its **setting behavior** methods from [`Setting`].

You shouldn't create instances of this class directly. Prefer [`SettingsManager.nest()`](./SettingsManager.md#nest) instead.

To read more about nested settings, see [this guide](../guides/nestingSettings.md).

## Properties

### value

(Override of `Setting.value`)

```python
@property
    def value(self) -> dict[str, Any]
```

Returns all the values of the nested settings in a dictionary.

### default

(Override of `Setting.default`)

```python
@property
def default(self) -> dict[str, Any]
```

Returns all the default values of the nested settings in a dictionary.

## Instance Methods

### is_nested()

(Override of `Setting.is_nested()`)

```python
def is_nested(self) -> bool
```

Whether the setting is a nested setting. In this case, the method will always return `True`.

### copy()

(Override of `SettingsManager.copy()`)

```python
def copy(self) -> Self
```

Returns a **shallow copy** of the nested settings.

### is_default()

(Override of `Setting.is_default()`)

```python
def is_default(self) -> bool
```

Whether the nested settings are in their default values.

Unlike [`Setting.is_default()`](./Setting.md$is_default), it iterates over the nested settings searching for a setting that is not setted to their default value.

<!-- Links -->
[`Setting`]: ./Setting.md