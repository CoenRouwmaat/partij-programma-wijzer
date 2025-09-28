from enum import StrEnum


class Party(StrEnum):
    VVD = "VVD"
    CDA = "CDA"
    PVDA = "PvdA"
    VIJFTIG_PLUS = "50PLUS"


class DocumentStructure(StrEnum):
    CHAPTER = "Hoofdstuk"
    SECTION = "Sectie"
    SUBSECTION = "Subsectie"
