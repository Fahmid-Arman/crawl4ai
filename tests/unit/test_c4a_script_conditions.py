"""C4A-Script IF conditions must compile to valid JavaScript for any selector."""

from crawl4ai.script.c4ai_script import compile_string


def test_exists_escapes_quotes_in_selector():
    js = compile_string("IF (EXISTS `input[name='q']`) THEN CLICK `button`")[0]

    assert "document.querySelector('input[name=\\'q\\']')" in js


def test_not_exists_escapes_quotes_in_selector():
    js = compile_string("IF (NOT EXISTS `a[href='/login']`) THEN CLICK `button`")[0]

    assert "!(!!document.querySelector('a[href=\\'/login\\']'))" in js


def test_exists_escapes_backslashes_in_selector():
    js = compile_string("IF (EXISTS `#a\\:b`) THEN CLICK `button`")[0]

    assert "document.querySelector('#a\\\\:b')" in js
