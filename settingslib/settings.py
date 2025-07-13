from typing import Self, Any, TypeVar, overload, Iterator, Generic, TypedDict
from pathlib import Path
from copy import copy
import json
import abc
import tomlkit as toml

__all__ = ["Settings"]

_T = TypeVar("_T")

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
    
    @overload
    def set(self, key: str, *, value: _T) -> Setting[_T]:
        """Set the value of the setting `key`."""
        ...
        
    @overload
    def set(self, key: str, *, default: _T) -> Setting[_T]:
        """Set the default value of the setting `key`."""
        ...
        
    @overload
    def set(self, key: str, *, value: _T, default: _T) -> Setting[_T]:
        """Set the value and the default value of the setting `key`."""
        ...

    # TODO
    def set(self, key: str, *, value: _T | None = ..., default: _T | None = ...) -> Setting[_T]:
        if not self.has(key):
            raise KeyError(f"There is not a setting with the key '{key}'.")
        
        if value is Ellipsis and default is Ellipsis:
            raise TypeError(f"Either value or default must be filled.")
        
        if value is Ellipsis:
            self[key].default = default
        elif default is Ellipsis:
            self[key].value = value
        else:
            self[key].value = value
            self[key].default = default
        
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
        self._settings[key] = Setting(
            value=value,
            default=default,
            comment=comment
        )
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
                    self._settings[key].value = value
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
        return self._settings.get(key, default)

    def has(self, key: str) -> bool:
        """Check if setting `key` is in the settings."""
        return key in self._settings.keys()
    
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
        ...
        
    def unwrap(self) -> dict[str, Setting]:
        """
        Returns the dict of settings.

        Returns:
            dict[str, Setting]: The dict of settings. **It is not a copy**, so
                                be careful at doing changes.
        """
        return self._settings
        
    def iter(self) -> Iterator[tuple[str, Setting]]:
        return self._settings.items()
    
    def reset(self) -> Self:
        """Sets all the settings to their default value."""
        for setting in self._settings.values():
            setting.reset()
            
        return self
    
    def __in__(self, key: str) -> bool:
        return self.has(key)
    
    def __eq__(self, other: Self | dict) -> bool:
        if isinstance(SettingsManager):
            return self._settings == other._settings
        else:
            return self._settings == other
    
    def __getitem__(self, key: str) -> Setting:
        return self._settings[key]
        
    def __setitem__(self, key: str, value: Setting | Any) -> None:
        self.update({key: value})
                
    def __dict__(self):
        return self.as_dict()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._settings!r})"


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
                 default_values: dict[str, Any] = {},
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
    
    def as_toml(self, *, include_comments: bool = True) -> toml.TOMLDocument:
        """
        Generates a TOML object representing the settings.

        Args:
            include_comments (bool, optional): Whether to include the comments of the settings. Defaults to True.

        Returns:
            tomlkit.TOMLDocument: A `TOMLDocument` object from the library [`tomlkit`](https://github.com/sdispater/tomlkit).
        """
        doc: toml.TOMLDocument = toml.document()
        
        attributes = toml.table()
        
        for key, attribute in self._attributes.items():
            attributes.add(key, attribute)
        
        doc.append("attributes", attributes)
        
        settings = toml.table()
        
        for key, setting in self.iter():
            if setting.comment and include_comments:
                settings.add(toml.comment(setting.comment))
            
            settings.add(key, setting.value)

            # if setting.comment and include_comments:
            #     settings.add(toml.nl())

        doc.append("settings", settings)
        
        return doc
    
    def save_toml(self, path: str | Path, *, include_comments: bool = True) -> Self:
        """
        Save the settings in a TOML file at `path`.

        Args:
            path (str | Path): The destiny path for the TOML file.
            include_comments (bool, optional): Whether to include setting's comments. Defaults to True.
            
        Returns:
            Self: 
        """
        path = Path(path)
        
        with open(path, "w") as fp:
            fp.write(self.as_toml(include_comments=include_comments).as_string())
        
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
        
        return self.as_dict(loaded)
    
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
        
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type: type, exc: BaseException, exc_tb) -> bool:
        self.save()
        return False # To re-raise the exception
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(attributes={self._attributes}, settings={self._settings})"