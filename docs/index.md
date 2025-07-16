# SettingsLib Documentation

This is the official documentation of settingslib. 

Although the library exports only one class (`Settings`), a lot of its methods returns instances of another own classes like `Setting` or `NestedSettings`.

Furthermore, `Settings` and `NestedSettings` inherit the majority of their methods from `SettingsManager`.

# Contents
* 📥 [Installation](./guides/installation.md)
* 🚀 [Quick start](./guides/quickstart.md)
* [API reference](./api)
  * ⚙️ [Settings](./api/Settings.md)
  * ⚙️ [Setting](./api/Setting.md)
  * ⚙️ [SettingsManager](./api/SettingsManager.md)
  * ⚙️ [NestedSettings](./api/NestedSettings.md)
* [Guides](./guides/)
  * [Using Context Managers with Settings](./guides/context_manager.md)