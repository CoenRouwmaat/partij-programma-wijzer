import argparse
from pathlib import Path

from src.enums import Party


def find_project_root(marker_file: str = "pyproject.toml") -> Path:
    """Finds the project root by searching for a marker file."""
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / marker_file).exists():
            return parent
    raise FileNotFoundError(f"Could not find project root with marker file: '{marker_file}'")


def get_party_from_string(party_str: str) -> Party:
    """
    Custom type function for argparse to convert a string to a Party enum.
    """
    try:
        if party_str.upper() == "50PLUS":
            party_str = "VIJFTIG_PLUS"  # Name incompatible as attribute
        return Party[party_str.upper()]
    except KeyError:
        valid_parties = [party.name for party in Party]
        raise argparse.ArgumentTypeError(
            f"Invalid party '{party_str}'. Please choose from: {', '.join(valid_parties)}"
        )
