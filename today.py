import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dateutil import relativedelta
from lxml import etree


BIRTHDAY = datetime.date(2003, 3, 3)
PROFILE_TIMEZONE = ZoneInfo("Europe/Istanbul")
SVG_FILES = (Path("dark_mode.svg"), Path("light_mode.svg"))


def profile_today() -> datetime.date:
    return datetime.datetime.now(PROFILE_TIMEZONE).date()


def format_age(birthday: datetime.date, today: datetime.date | None = None) -> str:
    """Return a human-readable age for the profile's uptime field."""
    difference = relativedelta.relativedelta(today or profile_today(), birthday)
    units = (
        (difference.years, "year"),
        (difference.months, "month"),
        (difference.days, "day"),
    )
    return ", ".join(
        f"{value} {label}{'' if value == 1 else 's'}" for value, label in units
    )


def update_svg(path: Path, age: str) -> None:
    """Update the single dynamic uptime value in an SVG file."""
    tree = etree.parse(path)
    elements = tree.xpath(".//*[@id='age_data']")
    if len(elements) != 1:
        raise ValueError(f"Expected one age_data element in {path}, found {len(elements)}")

    elements[0].text = age
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    age = format_age(BIRTHDAY)
    for svg_file in SVG_FILES:
        update_svg(svg_file, age)
    print(f"Updated profile uptime: {age}")


if __name__ == "__main__":
    main()
