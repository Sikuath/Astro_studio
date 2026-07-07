from pathlib import Path


def parse_colors_conversion(file_path: Path):
    """
    Lit le fichier colors_conversion.txt
    et retourne un mapping stable :
    r_colors_xxx.fit -> HA/OIII/SII
    """

    mapping = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if "->" not in line:
                continue

            left, right = line.split("->")
            left = Path(left.strip()).name
            right = Path(right.strip()).name

            mapping[right] = left  # colors_00001.fit -> HA_astrom.fit

    # inversion logique pour registration
    reverse = {
        "HA": None,
        "OIII": None,
        "SII": None
    }

    for colors_file, source_file in mapping.items():

        if "HA" in source_file:
            reverse["HA"] = colors_file
        elif "OIII" in source_file:
            reverse["OIII"] = colors_file
        elif "SII" in source_file:
            reverse["SII"] = colors_file

    return reverse