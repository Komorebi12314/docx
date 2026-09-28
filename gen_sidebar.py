# -*- coding: utf-8 -*-
"""Generate docsify _sidebar.md from directory structure, extracting H1 titles."""
import os
import io
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 目录顺序与中文分组名
GROUPS = [
    ("", None),                                    # 顶层文件
    ("integrations", "集成指南"),
    ("api-reference/account", "账户管理"),
    ("api-reference/chat", "文本对话"),
    ("api-reference/images", "图像生成"),
    ("api-reference/videos", "视频生成"),
    ("api-reference/tasks", "任务管理"),
    ("api-reference/uploads", "文件上传"),
    ("api-reference/rate-limits", "速率限制"),
    ("api-reference/webhooks", "Webhooks 回调"),
]

# 顶层文件固定顺序
TOP_FILES = ["quickstart.md", "faqs.md"]


def get_title(path):
    """Extract first H1 heading from a markdown file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if line.startswith("# "):
                    return line[2:].strip()
    except OSError:
        pass
    return None


lines = ["- **ToAPIs 文档**", ""]
emitted_top = False

for dirname, label in GROUPS:
    full = os.path.join(ROOT, dirname) if dirname else ROOT
    if not os.path.isdir(full):
        continue
    if dirname:
        if emitted_top:
            lines.append("")
        lines.append(f"- **{label}**")
        # 直接位于分类目录下的 md 文件
        entries = sorted(
            f for f in os.listdir(full)
            if f.endswith(".md") and os.path.isfile(os.path.join(full, f))
        )
    else:
        entries = [f for f in TOP_FILES if os.path.exists(os.path.join(full, f))]
    for fname in entries:
        title = get_title(os.path.join(full, fname)) or fname[:-3]
        link = f"{dirname}/{fname}" if dirname else fname
        lines.append(f"  - [{title}](/{link})")
        emitted_top = True

    # 递归处理一级子目录（如 images/flux-2/generation.md）
    if dirname:
        subdirs = sorted(
            d for d in os.listdir(full)
            if os.path.isdir(os.path.join(full, d)) and not d.startswith("assets")
        )
        for sub in subdirs:
            subfull = os.path.join(full, sub)
            for fname in sorted(
                f for f in os.listdir(subfull)
                if f.endswith(".md") and os.path.isfile(os.path.join(subfull, f))
            ):
                title = get_title(os.path.join(subfull, fname))
                if not title:
                    title = f"{sub} {fname[:-3]}"
                lines.append(f"  - [{title}](/{dirname}/{sub}/{fname})")
                emitted_top = True

with open(os.path.join(ROOT, "_sidebar.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"生成完成: _sidebar.md, 共 {sum(len(l) for l in lines)} 条相关行")
