from typing import Self, Any, TypeVar, overload, Iterator, Generic, TypedDict
from pathlib import Path
from copy import copy
import json
import abc
import tomlkit as toml

__all__ = ["Settings"]

_T = TypeVar("_T")

def _is_nested_key(key: str) -> bool:
    """Whether the `key` has "." characters in its body."""
    return "." in key

class _SettingsDict(TypedDict):
    """
    A dictionary structrured like a `Settings` object.
    """
    attributes: dict[str, Any]
    settings: dict[str, Any]

    
class _SettingDict(TypedDict, Generic[_T]):
    """
    A dictionary structrured like a `Setting` object.
    """
    value: _T
    default: _T


class Setting(Generic[_T]):
    def __init__(self, value: _T, default: _T | None = ..., comment: str = ""):
        self.value: _T = value
        self.comment: str = comment
        
        if default is Ellipsis:
            self.default: _T = copy(value)
        else:
            self.default: _T = default

    def is_default(self) -> bool:
        """Whether the value of the setting is equal to the default value."""
        return self.value == self.default
    
    def is_nested(self) -> bool:
        """Whether the setting are nested settings."""
        return False
    
    def update(self, other: _T) -> Self:
        """
        Changes the value of the setting to `other`.
        Alias for `Setting.value = other`.
        
        Args:
            other (Any): The new value of the setting.

        Returns:
            Self: 
        """
        self.value = other
        return self

    def reset(self) -> Self:
        """Set the value to the default."""
        self.value = self.default
        return self
    
    def as_dict(self) -> _SettingDict:
        """Returns a `dict` representation of the `Setting` object."""
        return {
            "value": self.value,
            "default": self.default
        }
        
    def __eq__(self, other: Self) -> bool:
        return self.value == other.value and self.default == other.default
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r}, default={self.default!r})"
    
    def __dict__(self):
        return self.as_dict()
    
    def __bool__(self) -> bool:
        return bool(self.value)


class SettingsManager(abc.ABC):
    """
    Abstract class for objects that wraps a dict with `Setting` objects.
    """
    
    def __init__(self):
        self._settings: dict[str, Setting] = {}

    def set(self,
            key: str, *, 
            value: _T | None = ..., 
            default: _T | None = ...,
            comment: _T | None = ...) -> Setting[_T]:
        """
        Set the properties of a setting.

        Args:
            key (str): The key to find the setting.
            value (_T | None, optional): The new value for the setting. Defaults to ....
            default (_T | None, optional): The new default value for the setting. Defaults to ....

        Raises:
            KeyError: When the setting doesn't exists.
            TypeError: When both of value and default are not filled.

        Returns:
            Setting[_T]: The setting with the changed applied.
        """
        if not self.has(key):
            raise KeyError(f"There is not a setting with the key '{key}'.")
        
        if Ellipsis in (value, default, comment):
            raise TypeError(f"Either value or default must be filled.")
        
        if value is not Ellipsis:
            self[key].value = value

        if default is not Ellipsis:
            self[key].default = default

        if comment is not Ellipsis:
            self[key].comment = comment
            
        return self._settings[key]

    def new(self, key: str, value: _T, default: _T | None = ..., comment: str = "") -> Setting[_T]:
        """
        Creates a new setting or overrides the existing one.

        Args:
            key (str): The name of the setting to create or override.
            value (Any): The value for the new setting.
            default (Any, optional): The default value for the new setting.. Defaults to ....
            comment (str, optional): The comment to write in the TOML document adove the setting. Defaults to "".

        Returns:
            Setting[_T]: An object representing the setting.
        """
        if isinstance(value, (dict, NestedSettings)):
            self._settings[key] = NestedSettings(
                value=value,
                comment=comment
            )
        else:
            self._settings[key] = Setting(
                value=value,
                default=default,
                comment=comment
            )
        
        return self._settings[key]
    
    def nest(self, key: str, *, comment: str = "") -> 'NestedSettings':
        """
        Nests a settings object into another one, creating hierarchy.

        Args:
            key (str): The key to get the nested setting.
            comment (str, optional): The comment to display above the nested setting section in TOML. Defaults to "".

        Returns:
            NestedSettings: The nested setting object.
        """
        self._settings[key] = NestedSettings(comment=comment)
        return self._settings[key]

    @overload
    def update(self, other: Self) -> Self:
        ...
    @overload
    def update(self, other: dict[str, Setting | Any]) -> Self:
        ...
    
    def update(self, other: dict[str, Setting | Any] | Self) -> Self:
        """
        Update the settings from the given object.

        Args:
            d (dict[str, Setting | Any] | SettingsManager): 

        Returns:
            Self: 
        """
        
        if isinstance(other, dict):
            if other == {}:
                return self
            
            for key, value in other.items():
                if isinstance(value, Setting):
                    self._settings[key] = value
                elif self.has(key):
                    self._settings[key].update(value)
                elif isinstance(value, (dict, NestedSettings)):
                    self._settings[key] = NestedSettings(value)
                else:
                    self._settings[key] = Setting(value)
        else:
            self._settings.update(other._settings)
        
        return self
    
    def get(self, key: str, default: _T | None = None) -> Setting | _T:
        """
        Gets the `Setting` with the key `key`.

        Args:
            key (str): The key to get the setting.
            default (_T, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            Setting | _T: The found setting or the default value.
        """
        try:
            # See SettingsManager.__getitem__() to understand the code.
            return self[key]
        except KeyError:
            return default
    
    def items(self, *, deep: bool = False) -> Iterator[tuple[str, Setting]]:
        """
        Iterates over the settings.

        Args:
            deep (bool, optional): Whether to include nested keys. Defaults to False.

        Yields:
            tuple[str, Setting]: A tuple with the key of the setting and the `Setting` object.
        """
        for key, setting in self._settings.items():
            yield (key, setting)
            
            if deep and isinstance(setting, NestedSettings):
                for k, s in setting.items(deep=True):
                    yield ((key + "." + k), s)

    def keys(self, *, deep: bool = False) -> Iterator[str]:
        """
        Iterates over the settings keys.

        Args:
            deep (bool, optional): Whether to include nested keys. Defaults to False.

        Yields:
            str: A setting key.
        """
        for k, _ in self.items(deep=deep):
            yield k
            
    def values(self, *, deep: bool = False) -> Iterator[Setting]:
        """
        Iterates over the settings values.

        Args:
            deep (bool, optional): Whether to include nested keys. Defaults to False.

        Yields:
            Setting: A Setting object.
        """
        for _, s in self.items(deep=deep):
            yield s
            
    def setdefault(self, key: str, default: _T, comment: str = "") -> Setting[_T]:
        """
        Returns the setting with the key, if exists. If not, creates a new setting
        with the given key and returns it.

        Args:
            key (str): The setting key.
            default (_T): The default value if the key doesn't exists.
            comment (str, optional): The comment for the setting if doesn't exists. Defaults to "".

        Returns:
            Setting[_T]: The new setting.
        """
        if self.has(key):
            return self[key]
        return self.new(key, default, comment=comment)
    
    def has(self, key: str) -> bool:
        """Check if setting `key` is in the settings."""
        if not _is_nested_key(key):
            return key in self._settings.keys()
        
        keys: list[str] = key.split(".")
        
        if not self.has(keys[0]):
            return False
        
        nested = self[keys[0]]
        
        if not isinstance(nested, NestedSettings):
            return False
        
        return nested.has(".".join(keys[1:]))
    
    def as_dict(self) -> dict[str, Any]:
        """
        Generates a dictionary with the keys and the values of the settings. Does not includes the
        default values or the comments.

        Returns:
            dict[str, Any]: The dictionary with the keys and values of the settings.
        """
        return {k: s.value for k, s in self._settings.items()}

    @abc.abstractmethod
    def copy(self) -> Self:
        """Creates a shallow copy of self."""
        raise NotImplementedError(f"SettingsManager.copy() was not implemented in {self.__class__.__name__}.")
        
    def unwrap(self) -> dict[str, Setting]:
        """
        Returns the dict of settings.

        Returns:
            dict[str, Setting]: The dict of settings. **It is not a copy**, so
                                be careful at doing changes.
        """
        return self._settings
    
    def reset(self) -> Self:
        """Sets all the settings to their default value."""
        for setting in self._settings.values():
            setting.reset()
            
        return self
    
    def __in__(self, key: str) -> bool:
        return self.has(key)
    
    def __eq__(self, other: Self | dict) -> bool:
        if isinstance(other, SettingsManager):
            return self._settings == other._settings
        else:
            return self._settings == other
    
    def __getitem__(self, key: str) -> Setting:
        if not _is_nested_key(key):
            return self._settings[key]

        keys: list[str] = key.split(".")
        
        # If the key doesn't exists or if the last key is empty
        # like "key."
        if not self.has(keys[0]) \
           or (len(keys) > 2 and keys[-1] == ""):
            raise KeyError(key)
        
        nested = self.get(keys[0])
        
        if not isinstance(nested, NestedSettings):
            raise KeyError(key)
        
        return nested[".".join(keys[1:])]
        
    def __setitem__(self, key: str, value: Setting | Any) -> None:
        if _is_nested_key(key):
            self[key].update(value)
        else:
            self.update({key: value})
                
    def __dict__(self):
        return self.as_dict()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._settings!r})"
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type: type, exc_val: BaseException, exc_tb) -> bool:
        return False # To re-raise the exception


class NestedSettings(SettingsManager, Setting[dict[str, Any]]):
    """
    A class representing a nested setting.
    
    A nested setting is a settings manager and a setting at the same time.
    
    # Example
    
    In JSON:
    ```
    {
        "attributes": {
            "version": "1.0.0
        },
        "settings": {
            "prefer_cli": true,

            # This is a nested setting.
            "api": {
                "base_url": "https://www.api.cl",
                "key": ""
            }
        }
        ""
    }
    ```
    
    In a TOML:
    ```
    [attributes]
    version = "1.0.0"
    
    [settings]
    prefer_cli = true
    
    # This is a nested setting.
    [settings.api]
    base_url = "https://www.api.cl"
    key = ""
    ```
    """
    def __init__(self, value: dict[str, Any] = None, *, comment = ""):
        SettingsManager.__init__(self)
        
        # Setting.value and Setting.default are overwritten by this class.

        self.comment = comment

        if value is not None:
            self.update(value)
        
    @property
    def value(self) -> dict[str, Any]:
        return super().as_dict()
    
    # TODO
    @value.setter
    def value(self, other: dict[str, Any]) -> None:
        self.update(other)
        
    @property
    def default(self) -> dict[str, Any]:
        buffer: dict[str, Any] = {}

        for key, setting in self._settings.items():
            buffer[key] = setting.default
        
        return buffer
    
    @default.setter
    def default(self, other: dict[str, Any]) -> None:
        if other == {}:
            return self
        
        for key, default in other.items():
            if isinstance(default, Setting):
                self._settings[key] = default
            elif self.has(key):
                self._settings[key].default = default
            else:
                self._settings[key] = Setting(
                    value=default,
                    default=default
                )
    
    def is_nested(self) -> bool:
        return True
    
    def copy(self) -> Self:
        new = NestedSettings.__new__(NestedSettings)
        
        new._settings = self._settings.copy()
        new.comment = self.comment
        
        return new
    
    def is_default(self) -> bool:
        # I override Setting.is_default() because it will get all the values
        # and defaults first and then check if they are default.
        # With this, the function will return False as soon as it finds a setting
        # that is not default.
        for setting in self._settings.values():
            if not setting.is_default():
                return False
        
        return True


class Settings(SettingsManager):
    """
    A class representing the software's settings, similar to a dict.
    
    Supports native reading and writting [TOML](https://toml.io/) and [JSON](https://www.json.org/) files.
    
    # Use Example
    
    ```
    s = Settings(
        path="project/settings.toml",
        version="1.0.0"
    )
    
    s.new("database", "")
    
    s.try_load()
    
    # <Very important code>
    
    s.save()
    ```
    """

    def __init__(self,
                 *,
                 path: str | Path,
                 version: str = ""
                 ):
        super().__init__()
        # self._settings: dict[str, Setting] = {k: Setting(v) for k, v in default_values.items()}
        self._attributes: dict[str, Any] = {
            "version": version
        }
        self._path: Path = Path(path)
    
    @property
    def path(self) -> Path:
        """The path where the config file is located."""
        return self._path
    
    @path.setter
    def path(self, new_path: Path) -> None:
        self._path = new_path
    
    @property
    def file_type(self) -> str:
        """The type of the config file."""
        return self.path.suffix
    
    @property
    def version(self) -> str:
        """The version of the software's settings."""
        return self._attributes.get("version", "")
    
    @version.setter
    def version(self, new: str) -> None:
        self._attributes["version"] = new
        
    @property
    def attributes(self) -> dict[str, Any]:
        """Special attributes of the settings."""
        return self._attributes
    
    @attributes.setter
    def attributes(self, new: dict[str, Any]) -> None:
        self._attributes = new
        
    def is_json(self) -> bool:
        """Whether the settings file is `.json`."""
        return self.file_type == ".json"
    
    def is_toml(self) -> bool:
        """Wheter the settings file is `.toml`."""
        return self.file_type == ".toml"
        
    def as_dict(self, *, include_defaults: bool = False) -> _SettingsDict:
        """
        Get a dict representation of the `Settings` object.

        Args:
            include_defaults (bool, optional): Whether the dict should include the default values. Defaults to False.

        Returns:
            _SettingsDict: A dict with two keys: "attributes" and "settings".
        """
        buffer: dict = {
            "attributes": self._attributes.copy(),
            "settings": {}
        }
        
        if include_defaults:
            for key, setting in self._settings.items():
                buffer["settings"][key] = setting.as_dict()
        else:
            for key, setting in self._settings.items():
                buffer["settings"][key] = setting.value
        
        return buffer
    
    def as_json(self, *, 
                indent: int = 4, 
                include_defaults: bool = False) -> str:
        """
        Generates a JSON string representation of the settings.

        Args:
            indent (int, optional): The amount of spaces to use as the JSON file indentation. Defaults to 4.
            include_defaults (bool, optional): If True, includes the default values in the JSON. Defaults to False.

        Returns:
            str: The JSON string.
        """
        d: _SettingsDict = self.as_dict(include_defaults=include_defaults)
        return json.dumps(d, indent=indent)
    
    # TODO: Debug
    def as_toml(self) -> toml.TOMLDocument:
        """
        Generates a TOML object representing the settings.

        Returns:
            tomlkit.TOMLDocument: A `TOMLDocument` object from the library [`tomlkit`](https://github.com/sdispater/tomlkit).
        """
        doc: toml.TOMLDocument = toml.document()
        
        attributes = toml.table()
        
        for key, attribute in self._attributes.items():
            attributes.add(key, attribute)
        
        doc.append("attributes", attributes)
        
        settings = toml.table()
        
        def add_comment(toml_object, setting):
            if setting.comment:
                if isinstance(setting, NestedSettings):
                    toml_object.add(toml.nl())
                    toml_object.add(toml.comment(
                        "*--- " + setting.comment + " ---*"
                        ))
                else:
                    toml_object.add(toml.comment(setting.comment))
        
        def parse(s: NestedSettings | Setting):
            if not isinstance(s, NestedSettings):
                return s.value
            
            table = toml.table()
            
            for key, setting in s.items():
                if setting.comment:
                    add_comment(table, setting)

                if isinstance(setting, NestedSettings):                    
                    table.add(key, parse(setting))
                else:
                    table.add(key, setting.value)
            
            return table
        
        for key, setting in self.items():
            add_comment(settings, setting)

            settings.add(key, parse(setting))

        doc.append("settings", settings)
        
        return doc
    
    def save_toml(self, path: str | Path) -> Self:
        """
        Save the settings in a TOML file at `path`.

        Args:
            path (str | Path): The destiny path for the TOML file.
            
        Returns:
            Self: 
        """
        path = Path(path)
        
        with open(path, "w") as fp:
            fp.write(self.as_toml().as_string())
        
        return self
    
    def save_json(self, path: str | Path, *, indent: int = 4) -> Self:
        """
        Save the settings in a JSON file at `path`.

        Args:
            path (str | Path): The destiny path for the JSON file.
            indent (int, optional): The amount of spaces to use as the JSON file indentation. Defaults to 4.

        Returns:
            Self: 
        """
        path = Path(path)
        
        with open(path, "w") as fp:
            fp.write(self.as_json(indent=indent))
        
        return self
    
    def save(self,
             path: str | Path = ...,
             *,
             json_indent: int = 4,
             create_dirs: bool = False) -> Self:
        """
        Saves the settings in `self.path` or `path` if given.

        Args:
            path (str | Path, optional): The path to write the config file. Defaults to `self.path`.
            json_indent (int, optional): The spaces to indent if the file is a JSON. Defaults to 4.
            create_dirs (bool, optional): Whether to create the parent directories that doesn't exists. Defaults to False.

        Raises:
            FileNotFoundError: When `indent` is False and the parent directory doesn't exists.

        Returns:
            Self: 
        """
        if path is Ellipsis:
            path = self._path
        elif type(path) is str:
            path = Path(path)
        
        if not path.parent.exists() and not create_dirs:
            raise FileNotFoundError(f"The directory '{path.parent}' doesn't exists.")

        if not path.parent.exists() and create_dirs:
            path.parent.mkdir(parents=True)
        
        match self.file_type:
            case ".toml":
                self.save_toml(path)

            case ".json" | _:
                self.save_json(path, indent=json_indent)

        return self
    
    def load_dict(self, d: _SettingsDict) -> Self:
        """
        Loads settings from a dictionary.

        Args:
            d (dict[str, dict[str, Any]]): The dictionary with the attributes and settings to load.

        Raises:
            TypeError: When the dictionary doesn't has attributes and settings structure.

        Returns:
            Self: 
        """
        attributes: dict[str, Any] = d.get("attributes")
        settings: dict[str, Any] = d.get("settings")
        
        if attributes is None \
           or not isinstance(attributes, dict) \
           or settings is None \
           or not isinstance(settings, dict):
            raise TypeError(f"The loaded dict is not a valid config object.")
        
        for key, value in settings.items():
            if self.has(key):
                self[key].value = value

            elif isinstance(value, dict):
                self[key] = NestedSettings(value)
            else:
                self[key] = Setting(value)
        return self
    
    def load_toml(self, s: str) -> Self:
        """
        Load settings from a TOML document.

        Args:
            s (str): The TOML document as a string.

        Returns:
            Self: 
        """
        doc: toml.TOMLDocument = toml.loads(s)
        return self.load_dict(doc.unwrap())
        
    def load_json(self, s: str) -> Self:
        """
        Loads settings from a JSON document.

        Args:
            s (str): The JSON document as a string.

        Raises:
            TypeError: When the JSON document is not a dict.

        Returns:
            Self: 
        """
        loaded: dict[str, dict[str, Any]] = json.loads(s)
        
        if not isinstance(loaded, dict):
            raise TypeError(f"The loaded JSON document is not a valid config file.")
        
        return self.load_dict(loaded)
    
    @overload
    def load(self) -> Self: ...
    @overload
    def load(self, path: str | Path) -> Self: ...
    
    def load(self, path: str | Path = ...) -> Self:
        """
        Loads the settings in `self.path` or in `path` (if provided) and updates the settings with the loaded ones.

        Args:
            path (str | Path, optional): The path of the config file. Defaults to `self.path`.

        Raises:
            FileNotFoundError: When the config file or `path` doesn't exists.
            TypeError: When the loaded object is not a `dict`.

        Returns:
            Self:
        """
        if path is Ellipsis:
            path = self._path
        elif type(path) is str:
            path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"'{path}' doesn't exists.")
        
        with open(path, "r") as fp:
            match self.file_type:
                case ".toml":
                    return self.load_toml(fp.read())
                    
                case ".json" | _:
                    return self.load_json(fp.read())
                
    @overload
    def try_load(self) -> Self: ...
    @overload
    def try_load(self, path: str | Path) -> Self: ...
    
    def try_load(self, path: str | Path = ...) -> Self:
        """
        Tries to load the settings from the config file or `path`.\n
        Doesn't raises an exception when the file doesn't exists.
        """
        if not path.exists():
            return self
        
        return self.load(path)

    @classmethod
    def from_load(cls, path: str | Path) -> Self:
        """
        Loads the config file in `path`.

        Args:
            path (str | Path): The path of the config to load.

        Returns:
            Self: A Settings objects.
        """
        self: Self = cls.__new__(cls)
        self.__init__(path=path)
        return self.load()
    
    def copy(self) -> Self:
        """Returns a copy of the settings."""
        new = self.__new__(type(self))
        
        new._settings = self._settings.copy()
        new._attributes = self._attributes.copy()
        new._path = copy(self.path)
        
        return new
    
    def __exit__(self, exc_type: type, exc: BaseException, exc_tb) -> bool:
        self.save()
        return False # To re-raise the exception
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(attributes={self._attributes}, settings={self._settings})"