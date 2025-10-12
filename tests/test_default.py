import textwrap

from markdown import Markdown


def test_default() -> None:
    md = Markdown()
    text = "これは\nテストです。"
    html = md.convert(text)
    assert html == f"<p>{text}</p>"


def test_list() -> None:
    md = Markdown()
    text = "- a\n- b\n  c\n- d"
    html = md.convert(text)

    expected = """\
    <ul>
    <li>a</li>
    <li>b
      c</li>
    <li>d</li>
    </ul>"""

    assert html == textwrap.dedent(expected)


def test_fenced_code() -> None:
    md = Markdown()
    text = "```\na\nb\n```"
    html = md.convert(text)

    expected = """\
    <p><code>a
    b</code></p>"""

    assert html == textwrap.dedent(expected)


def test_super_fences() -> None:
    md = Markdown(extensions=["pymdownx.superfences"])
    text = "```\na\nb\n```"
    html = md.convert(text)

    expected = """\
    <div class="highlight"><pre><span></span><code>a
    b
    </code></pre></div>"""

    assert html == textwrap.dedent(expected)
