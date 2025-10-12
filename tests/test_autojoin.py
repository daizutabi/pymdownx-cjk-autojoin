import textwrap

import pytest
from markdown import Markdown

from pymdownx_cjk_autojoin.autojoin import CjkAutojoinExtension


@pytest.fixture(params=[CjkAutojoinExtension(), "pymdownx_cjk_autojoin"])
def extension(request: pytest.FixtureRequest) -> CjkAutojoinExtension | str:
    return request.param


@pytest.fixture
def md(extension: CjkAutojoinExtension | str) -> Markdown:
    return Markdown(extensions=[extension])


def test_join(md: Markdown) -> None:
    text = "これは\nテストです。"
    expected = "<p>これはテストです。</p>"
    assert md.convert(text) == expected


def test_paragraph(md: Markdown) -> None:
    text = "これは\n\nテストです。"
    expected = "<p>これは</p>\n<p>テストです。</p>"
    assert md.convert(text) == expected


def test_list(md: Markdown) -> None:
    text = "- あ\n- い\n  う\n- え"
    html = md.convert(text)

    expected = """\
        <ul>
        <li>あ</li>
        <li>いう</li>
        <li>え</li>
        </ul>"""

    assert html == textwrap.dedent(expected)


def test_fenced_code() -> None:
    md = Markdown()
    text = "```\nあ\nい\n```"
    html = md.convert(text)

    expected = """\
    <p><code>あ
    い</code></p>"""

    assert html == textwrap.dedent(expected)


@pytest.mark.parametrize(
    "extensions",
    [
        ["pymdownx.superfences", "pymdownx_cjk_autojoin"],
        ["pymdownx_cjk_autojoin", "pymdownx.superfences"],
    ],
)
def test_super_fences(extensions: list[str]) -> None:
    md = Markdown(extensions=extensions)
    text = "```\nあ\nい\n```"
    html = md.convert(text)

    expected = """\
    <div class="highlight"><pre><span></span><code>あ
    い
    </code></pre></div>"""

    assert html == textwrap.dedent(expected)
