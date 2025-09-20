import argparse

from src.enums import Party


def get_party_from_string(party_str: str) -> Party:
    """
    Custom type function for argparse to convert a string to a Party enum.
    """
    try:
        return Party[party_str.upper()]
    except KeyError:
        valid_parties = [party.name for party in Party]
        raise argparse.ArgumentTypeError(
            f"Invalid party '{party_str}'. Please choose from: {', '.join(valid_parties)}"
        )
