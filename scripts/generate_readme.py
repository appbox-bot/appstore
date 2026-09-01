import json
from pathlib import Path


JSON_FILE = Path("data/apps.json")
README_FILE = Path("README.md")


def generate_link(name, url):
    return f"[{name}]({url})"


def generate_readme(data):
    lines = []

    for category, apps in data.items():
        lines.append(f"## {category}")
        lines.append("")

        for index, app in enumerate(apps, 1):
            name = app["name"]
            description = app.get("description", "")

            line = f"{index}、{name}"

            if description:
                line += f" 【{description}】"

            links = app.get("links", {})

            for link_name, url in links.items():
                line += f" {generate_link(link_name, url)}"

            lines.append(line)
            lines.append("")

    return "\n".join(lines)


def main():
    with JSON_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    content = generate_readme(data)

    README_FILE.write_text(
        content,
        encoding="utf-8"
    )

    print(f"Generated {README_FILE}")


if __name__ == "__main__":
    main()