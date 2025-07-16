# 🪺 Nesting Settings

Nested settings are groups of settings inside another setting. It's like creating a "tree" of settings.

Nesting settings is so useful to order our settings and to don't have collissions with two or more settings with the same name.

## 🪺 How to Nest a Setting

To create a nested setting, we use the [`SettingsManager.nest()`](../api/SettingsManager.md#nest) method, which is available in [`Settings`] and [`NestedSettings`] objects.

This method will return a [`NestedSettings`] object, in that we can add more settings or even more [`NestedSettings`].

This is an example:

```python
from settingslib import Settings

# First, we create an instance of the Settings class.
settings: Settings = Settings(
        path="example/settings.toml",
        version="1.0.0"
    )

# Then, we use the nest() method to create a nested settings instance.
gui_s = settings.nest("gui", comment="GUI SETTINGS")

# Finally, we add new settings to the nested setting.
gui_s.new("theme", "system", 
          comment="The default theme for the graphic interface.")
gui_s.new("minimized", False, 
          comment="Whether the interface must init minimized.")
gui_s.new("type", "simplified",
          comment="The type of the interface.")

# Also we can nest settings in another nested settings, like this:
gui_colors_s = gui_s.nest("colors", comment="THE COLORS TO USE")
gui_colors_s.new("blue", "#365DA5", 
                 comment="The HEX code for the color to use as blue.")

s.save()
```

Also, you can use [context managers](./context_manager.md) to make your code more readable and to avoid creating a lot of variables, like in this example:

```python
from settingslib import Settings

settings: Settings = Settings(
        path="example/settings.toml",
        version="1.0.0"
    )

with settings.nest("gui", comment="GUI SETTINGS") as gui_s:
    gui_s.new("theme", "system", 
            comment="The default theme for the graphic interface.")
    gui_s.new("minimized", False, 
            comment="Whether the interface must init minimized.")
    gui_s.new("type", "simplified",
            comment="The type of the interface.")

    with gui_s.nest("colors", comment="THE COLORS TO USE") as colors:
        colors.new("blue", "#365DA5", 
                 comment="The HEX code for the color to use as blue.")

s.save()
```

When saving the settings, this will be the output:

In [TOML]:
```toml
[attributes]
version = "1.0.0"

[settings]

# *--- GUI SETTINGS ---*

[settings.gui]
# The default theme for the graphic interface.
theme = "system"
# Whether the interface must init minimized.
minimized = false
# The type of the interface.
type = "simplified"

# *--- THE COLORS TO USE ---*

[settings.gui.colors]
# The HEX code for the color to use as blue.
blue = "#365DA5"
```

In [JSON]:

```json
{
    "attributes": {
        "version": "1.0.0"
    },
    "settings": {
        "gui": {
            "theme": "system",
            "minimized": false,
            "type": "simplified",
            "colors": {
                "blue": "#365DA5"
            }
        }
    }
}
```

Don't forget that [JSON] doesn't support comments, so they will be omited.

## 🔑 Nested Keys

To access to our nested settings we can use string keys separated by dots, like this:

```
gui.colors.blue
```

This is supported by all the [`SettingsManager`] methods that works with keys, so you can access to a setting using this example:

```python
settings["gui.colors.blue"]
```

Of course, this is more readable than this:

```python
settings["gui"].value["colors"].value["blue"]
```

[`Settings`]: ../api/Settings.md
[`NestedSettings`]: ../api/NestedSettings.md
[`SettingsManager`]: ../api/SettingsManager.md
[TOML]: https://www.toml.io
[JSON]: https://www.json.org