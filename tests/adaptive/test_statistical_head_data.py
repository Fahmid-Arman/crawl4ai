"""
StatisticalStrategy must read link preview data in the shape link preview
produces: the page title at the top level, description and keywords under "meta".
"""

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.append(str(Path(__file__).parent.parent.parent))

from crawl4ai.adaptive_crawler import CrawlState, StatisticalStrategy
from crawl4ai.models import Link


def test_relevance_uses_head_data_title():
    strategy = StatisticalStrategy()
    state = CrawlState(query="python asyncio")
    link = Link(
        href="https://example.com/a",
        text="Read more",
        head_data={"title": "Python asyncio tutorial", "meta": {}},
    )

    assert strategy._calculate_relevance(link, state) == 1.0


def test_novelty_uses_head_data_meta_description_and_keywords():
    strategy = StatisticalStrategy()
    state = CrawlState(query="python")
    state.knowledge_base.append(
        SimpleNamespace(url="https://example.com/", markdown=None)
    )
    state.term_frequencies.update({"read": 1, "more": 1})
    link = Link(
        href="https://example.com/b",
        text="Read more",
        head_data={
            "title": "",
            "meta": {"description": "quantum entanglement", "keywords": "qubits"},
        },
    )

    # "read" and "more" are known, the 3 terms from the preview are new
    assert strategy._calculate_novelty(link, state) == 0.6
