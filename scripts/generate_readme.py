import json
from pathlib import Path


JSON_FILE = Path("data/apps.json")
README_FILE = Path("README.md")

START_MARKER = "<!-- APP_LIST_START -->"
END_MARKER = "<!-- APP_LIST_END -->"


def generate_app_list(data):
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

            for link_name, url in app.get("links", {}).items():
                line += f" [{link_name}]({url})"

            lines.append(line)
            lines.append("")

    return "\n".join(lines).rstrip()


def main():
    # 读取 JSON
    with JSON_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 生成动态内容
    app_list = generate_app_list(data)

    # 读取原 README
    readme = README_FILE.read_text(encoding="utf-8")

    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)

    if start == -1 or end == -1:
        raise RuntimeError(
            f"README.md 中找不到 {START_MARKER} 或 {END_MARKER}"
        )

    if start >= end:
        raise RuntimeError("README.md 中标记顺序错误")

    # 保留固定内容，只替换动态区域
    new_readme = (
        readme[:start + len(START_MARKER)]
        + "\n\n"
        + app_list
        + "\n\n"
        + readme[end:]
    )

    README_FILE.write_text(
        new_readme,
        encoding="utf-8"
    )

    print("README.md generated successfully.")


if __name__ == "__main__":
    main()
