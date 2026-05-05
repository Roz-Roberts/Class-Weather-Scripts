from __future__ import annotations

import importlib.metadata
import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = PROJECT_ROOT / "pyproject.toml"


def dependency_name(dependency: str) -> str:
    name = dependency.split("[", 1)[0]
    for marker in ("<=", ">=", "==", "~=", "!=", "<", ">"):
        name = name.split(marker, 1)[0]
    return name.strip()


def project_dependencies() -> list[str]:
    with PYPROJECT.open("rb") as file:
        pyproject = tomllib.load(file)

    dependencies = pyproject.get("project", {}).get("dependencies", [])
    return [dependency_name(dependency) for dependency in dependencies]


def installed_version(package_name: str) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def main() -> int:
    dependencies = project_dependencies()

    if not dependencies:
        print("No dependencies found in pyproject.toml.")
        return 0

    print("Project packages listed in pyproject.toml:")
    for package_name in dependencies:
        print(f"- {package_name}: {installed_version(package_name)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
