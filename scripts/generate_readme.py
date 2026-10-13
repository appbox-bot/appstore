import json
from pathlib import Path


JSON_FILE = Path("data/apps.json")
README_FILE = Path("README.md")

START_MARKER = "<!-- APP_LIST_START -->"
END_MARKER = "<!-- APP_LIST_END -->"

LINK_NAMES = {
    "android": "Android",
    "ios": "iOS",
    "windows": "Windows",
    "macos": "macOS",
    "linux": "Linux",
    "source": "Source",
}


def escape_markdown(text):
    """转义 Markdown 表格中的特殊字符。"""
    return str(text).replace("|", r"\|").replace("\n", "<br>")


def generate_app_list(data):
    lines = []

    for category, apps in data.items():
        lines.append(f"## {category}")
        lines.append("")

        # 表头
        lines.append("| 序号 | 应用名称 | 预览图 | 下载地址 | 描述 |")
        lines.append("| --- | --- | --- | --- | --- |")

        for index, app in enumerate(apps, 1):
            name = escape_markdown(app.get("name", ""))
            description = escape_markdown(app.get("description", ""))

            # 预览图：允许为空
            preview = app.get("preview")
            if preview:
                preview = f"![预览图]({preview})"
            else:
                preview = "-"

            # 合并所有下载地址
            links = app.get("links", {})
            link_items = []

            for link_type, url in links.items():
                if not url:
                    continue

                link_name = LINK_NAMES.get(link_type, link_type)
                link_items.append(f"[{link_name}]({url})")

            download_links = "<br>".join(link_items) if link_items else "-"

            row = [
                str(index),
                name,
                preview,
                download_links,
                description or "-",
            ]

            # 转义普通文本列，保留 Markdown 图片和链接语法
            row[1] = escape_markdown(row[1])
            row[4] = escape_markdown(row[4])

            lines.append("| " + " | ".join(row) + " |")

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
        encoding="utf-8",
    )

    print("README.md generated successfully.")


if __name__ == "__main__":
    main()
