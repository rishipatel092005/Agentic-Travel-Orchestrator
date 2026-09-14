import yaml
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> dict:
    path = Path(config_path)
    if not path.is_absolute():
        project_root = Path(__file__).resolve().parents[1]
        path = project_root / path

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config
