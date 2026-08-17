#!/usr/bin/env python3
"""从常见文档格式中提取纯文本，供阅读内容分析使用。

用法:
    python3 extract_text.py <文件路径>

支持格式:
    - .txt / .md / .markdown  纯文本，直接读取
    - .pdf                    需要 PyMuPDF (pip install pymupdf)
    - .docx                   需要 python-docx (pip install python-docx)
    - .epub                   需要 ebooklib (pip install ebooklib)

依赖缺失时，脚本会提示安装方式并跳过该格式；纯文本格式始终可用。
"""

import sys
from pathlib import Path


def extract_txt(path: Path) -> str:
    """直接读取纯文本文件（兼容多种编码）。"""
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def extract_pdf(path: Path) -> str:
    """使用 PyMuPDF 提取 PDF 文本。"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError("提取 PDF 需要 PyMuPDF，请运行: pip install pymupdf")
    doc = fitz.open(path)
    parts = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    return "\n".join(parts)


def extract_docx(path: Path) -> str:
    """使用 python-docx 提取 Word 文档文本。"""
    try:
        import docx
    except ImportError:
        raise RuntimeError("提取 DOCX 需要 python-docx，请运行: pip install python-docx")
    document = docx.Document(str(path))
    return "\n".join(p.text for p in document.paragraphs if p.text.strip())


def extract_epub(path: Path) -> str:
    """使用 ebooklib 提取 EPUB 文本。"""
    try:
        from ebooklib import ITEM_DOCUMENT, epub
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError(
            "提取 EPUB 需要 ebooklib 和 beautifulsoup4，请运行: "
            "pip install ebooklib beautifulsoup4"
        )
    book = epub.read_epub(str(path))
    parts = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        parts.append(soup.get_text("\n", strip=True))
    return "\n".join(parts)


EXTRACTORS = {
    ".txt": extract_txt,
    ".md": extract_txt,
    ".markdown": extract_txt,
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".epub": extract_epub,
}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"错误: 文件不存在: {path}", file=sys.stderr)
        return 1

    extractor = EXTRACTORS.get(path.suffix.lower())
    if extractor is None:
        print(
            f"错误: 不支持的文件类型 '{path.suffix}'。"
            f"支持: {', '.join(sorted(EXTRACTORS))}",
            file=sys.stderr,
        )
        return 1

    try:
        text = extractor(path)
    except RuntimeError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    if not text.strip():
        print("警告: 未能从文档中提取到文本（可能是扫描件，需要 OCR）。", file=sys.stderr)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
