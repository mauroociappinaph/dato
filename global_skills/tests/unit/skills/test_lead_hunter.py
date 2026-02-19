"""
Tests for apify-lead-hunter (sovereign edition).
Tests DuckDuckGo parsing, dedup logic, scorer JSON extraction, and output formats.
No network or Ollama required.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / "apify-lead-hunter" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


# Sample DuckDuckGo LITE HTML for testing
SAMPLE_DDG_HTML = """
<html><body>
<table>
  <tr>
    <td><a href="https://example-agency.com" class="result-link">Example Agency</a></td>
    <td class="result-snippet">A digital marketing agency in Bilbao</td>
  </tr>
  <tr>
    <td><a href="https://bilbao-realty.es" class="result-link">Bilbao Realty</a></td>
    <td class="result-snippet">Real estate services in Bilbao</td>
  </tr>
  <tr>
    <td><a href="https://example-agency.com" class="result-link">Example Agency (dup)</a></td>
    <td class="result-snippet">Duplicate entry</td>
  </tr>
</table>
</body></html>
"""


class TestHunterParsing:
    """Test DuckDuckGo HTML parsing."""

    def test_deduplicates_by_url(self):
        from hunter import search_duckduckgo

        with patch("hunter.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = SAMPLE_DDG_HTML
            mock_post.return_value = mock_response

            results = search_duckduckgo("test query", max_results=20)

            # Should deduplicate example-agency.com
            urls = [r["url"] for r in results]
            assert len(urls) == len(set(urls)), "URLs should be unique"

    def test_respects_max_results(self):
        from hunter import search_duckduckgo

        with patch("hunter.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = SAMPLE_DDG_HTML
            mock_post.return_value = mock_response

            results = search_duckduckgo("test", max_results=1)
            assert len(results) <= 1

    def test_handles_http_error(self):
        from hunter import search_duckduckgo

        with patch("hunter.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 503
            mock_post.return_value = mock_response

            results = search_duckduckgo("test")
            assert results == []

    def test_handles_network_error(self):
        from hunter import search_duckduckgo

        with patch("hunter.requests.post", side_effect=Exception("Network error")):
            results = search_duckduckgo("test")
            assert results == []


class TestHuntLeads:
    """Test the hunt_leads wrapper."""

    def test_output_format(self):
        from hunter import hunt_leads

        with patch("hunter.search_duckduckgo", return_value=[
            {"name": "Test Co", "url": "https://test.com", "snippet": "Testing"}
        ]):
            result = hunt_leads("test query", max_results=5)

            assert "query" in result
            assert "leads_found" in result
            assert "leads" in result
            assert result["leads_found"] == 1
            assert result["query"] == "test query"


class TestScorer:
    """Test lead scoring JSON extraction."""

    def test_score_lead_parses_json(self):
        from scorer import score_lead

        mock_response = '{"score": 82, "reasoning": "Good B2B prospect"}'

        with patch("scorer.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"response": mock_response}
            mock_post.return_value = mock_resp

            lead = {"name": "Test Agency", "url": "https://test.com", "snippet": ""}
            result = score_lead(lead)

            assert result["score"] == 82
            assert "Good B2B" in result["reasoning"]

    def test_score_lead_handles_markdown_wrapped_json(self):
        from scorer import score_lead

        mock_response = '```json\n{"score": 75, "reasoning": "Medium potential"}\n```'

        with patch("scorer.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"response": mock_response}
            mock_post.return_value = mock_resp

            lead = {"name": "Test", "url": "https://test.com", "snippet": ""}
            result = score_lead(lead)

            assert result["score"] == 75

    def test_score_lead_fallback_on_parse_error(self):
        from scorer import score_lead

        with patch("scorer.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"response": "unparseable garbage"}
            mock_post.return_value = mock_resp

            lead = {"name": "Test", "url": "https://test.com", "snippet": ""}
            result = score_lead(lead)

            assert result["score"] == 50  # Default fallback
            assert "default" in result["reasoning"].lower() or "failed" in result["reasoning"].lower()

    def test_score_leads_sorts_descending(self):
        from scorer import score_leads

        def mock_score(lead, model=""):
            scores = {"A": 90, "B": 30, "C": 70}
            lead["score"] = scores.get(lead["name"], 50)
            lead["reasoning"] = "test"
            return lead

        with patch("scorer.score_lead", side_effect=mock_score):
            result = score_leads([
                {"name": "B"}, {"name": "A"}, {"name": "C"}
            ])

            scores = [l["score"] for l in result["leads"]]
            assert scores == [90, 70, 30], "Should be sorted descending"


class TestPersistDedup:
    """Test deduplication logic."""

    def test_persist_dry_run(self):
        from persist import persist_leads

        leads = [
            {"name": "Test", "url": "https://test.com", "score": 80, "reasoning": "good"},
        ]
        result = persist_leads(leads, dry_run=True)

        assert result["dry_run"] is True
        assert result["would_persist"] == 1
