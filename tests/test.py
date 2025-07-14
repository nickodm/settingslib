from settingslib.settings import Settings
from pathlib import Path
import tomlkit as toml
import json

def _read_toml(p: Path) -> str:
    with open(p, "r") as fp:
        return toml.load(fp).unwrap()
    
def _read_json(p: Path) -> str:
    with open(p, "r") as fp:
        return json.dumps(json.load(fp), indent=4)

EXPECTED_TOML: dict = _read_toml("tests/expected/expected.toml")
EXPECTED_JSON: str = _read_json("tests/expected/expected.json")

def get_test_settings(tmp_path: Path) -> Settings:
    s: Settings = Settings(
        path=tmp_path / "settings.toml",
        version="1.0.0"
    )
    
    s.attributes["user"] = "nickodm"
    
    s.new("prefer_cli", True, comment="Whether to prefer the command line interface instead of GUI")
    
    with s.nest("gui", comment="GUI SETTINGS") as gui_s:
        gui_s.new("theme", "system", comment="The default theme for the graphic interface.")
        gui_s.new("minimized", False, comment="Whether the interface must init minimized.")
        gui_s.new("type", "simplified", comment="The type of the interface.")
    
    with s.nest("api", comment="API SETTINGS") as api_s:
        api_s.new("enabled", True) # No comment
        
        with api_s.nest("connection") as c: # No comment
            c.new("base_url", "https://www.api.cl", comment="The base URL for the API.")
            c.new("custom_key", "", comment="The custom user's API key.")
    
    with s.nest("editor", comment="EDITOR SETTINGS") as ed_s:
        ed_s.new("bg_color", "black", comment="Background color")
        ed_s.new("fg_color", "white", comment="Font color")
        ed_s.new("indent", 4, comment="Amount of spaces to use for indentation")
        ed_s.new("suggestions", True, comment="Whether to allow suggestions in the program")

    with s.nest("colors", comment="COLOR CODES") as colors:
        colors.new("blue", "blue")
        colors.new("green", "green")
        colors.new("black", "black")
        colors.new("red", "red")
    
    return s

def test(tmp_path: Path):
    s: Settings = get_test_settings(tmp_path)
    
    assert s.as_toml().unwrap() == EXPECTED_TOML
    assert s.as_json() == EXPECTED_JSON
    
    s.set("api.connection.custom_key", value="key")
    
    assert s.get("api.connection.custom_key").value == "key"
    assert s.get("api.connection.custom_key").value == s["api.connection.custom_key"].value
    assert s.get("api.connection.custom_key").value == s["api.connection.custom_key"].value

    s["api.connection.custom_key"].reset()
    
    assert s.get("api.connection.custom_key").value != "key"
    assert s["api.connection.custom_key"].value != "key"
    assert s["api.connection.custom_key"].value == ""
    assert s.has("api.connection.custom_key")
    
    s.save_json(tmp_path / "settings.json")
    s.save_toml(tmp_path / "settings.toml")
    
    assert s == Settings.from_load(tmp_path / "settings.json")
    assert s == Settings.from_load(tmp_path / "settings.toml")
    
    s.save(tmp_path / "settings.json")
    
    with open(tmp_path / "settings.json", "r") as fp:
        print(fp.read())
    
    s.save(tmp_path / "settings.toml")

    assert s == Settings.from_load(tmp_path / "settings.json")
    assert s == Settings.from_load(tmp_path / "settings.toml")
    
# To test:
# Settings.__init__()
# *--- Managing Methods ---*
# new()
# set()
# nest()
# update()
# get()
# has()
# setdefault()
# items()
# keys()
# values()
# as_dict()
# copy()
# reset()

# Settings.load()
# Settings.as_toml()
# Settings.as_json()
# Settings.as_dict()
# Settings.unwrap()
# Settings.save()