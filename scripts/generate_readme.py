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

# 表格中显示的平台顺序
PLATFORM_ORDER = [
    "android",
    "ios",
    "windows",
    "macos",
    "linux",
    "source",
]


def escape_markdown(text):
    """转义 Markdown 表格中的特殊字符。"""
    return str(text).replace("|", r"\|").replace("\n", "<br>")


def generate_app_list(data):
    lines = []

    for category, apps in data.items():
        lines.append(f"## {category}")
        lines.append("")

        # 表头
        headers = [
            "序号",
            "应用名称",
            "预览图",
            *[LINK_NAMES[key] for key in PLATFORM_ORDER],
            "描述",
        ]

        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        for index, app in enumerate(apps, 1):
            name = escape_markdown(app.get("name", ""))
            description = escape_markdown(
                app.get("description", "")
            )

            # 预览图：支持 preview 字段
            preview = app.get("preview", "")
            if preview:
                preview = f"![预览图]({preview})"
            else:
                preview = "-"

            # 平台链接
            links = app.get("links", {})
            platform_links = []

            for link_type in PLATFORM_ORDER:
                url = links.get(link_type)

                if url:
                    link_name = LINK_NAMES[link_type]
                    platform_links.append(
                        f"[{link_name}]({url})"
                    )
                else:
                    platform_links.append("-")

            row = [
                str(index),
                name,
                preview,
                *platform_links,
                description or "-",
            ]

            # 避免单元格中的 | 破坏表格结构
            row = [
                escape_markdown(value)
                if value != preview
                else value
                for value in row
            ]

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
