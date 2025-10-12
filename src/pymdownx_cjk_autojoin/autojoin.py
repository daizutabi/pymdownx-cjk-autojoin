from __future__ import annotations

import re
from typing import Any

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor

# Regex to match CJK characters
# (Hiragana, Katakana, CJK Unified Ideographs, and some punctuation)
# This pattern covers a good range of CJK characters.
# \u3000-\u303f: CJK Symbols and Punctuation
# \u3040-\u309f: Hiragana
# \u30a0-\u30ff: Katakana
# \u4e00-\u9fff: CJK Unified Ideographs
CJK_CHAR_PATTERN = r"[\u3000-\u30ff\u4e00-\u9fff]"


class CjkAutojoinPreprocessor(Preprocessor):
    def run(self, lines: list[str]) -> list[str]:
        text = "\n".join(lines)

        # Use re.sub to find CJK_CHAR + newline + CJK_CHAR and remove the newline
        # The ( ) create capturing groups, and \1\2 refers to the captured groups.
        # This effectively removes the newline between two CJK characters.
        processed_text = re.sub(
            f"({CJK_CHAR_PATTERN})\\n *({CJK_CHAR_PATTERN})",
            r"\1\2",
            text,
        )

        # Split the processed text back into lines
        return processed_text.split("\n")


class CjkAutojoinExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        """Add CjkAutojoinPreprocessor to the Markdown instance."""
        # Priority 27 is before 'fenced_code_blocks' (30) and after 'header' (20)
        # cjk_autojoin runs before block-level parsing but after basic line processing.
        md.preprocessors.register(CjkAutojoinPreprocessor(md), "cjk_autojoin", 27)


def makeExtension(**kwargs: Any) -> CjkAutojoinExtension:
    return CjkAutojoinExtension(**kwargs)
