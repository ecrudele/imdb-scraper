import requests
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, Mock, patch

from scraper.imdb_scraper import IMDbScraper


class TestIMDbScraper:
    @patch.object(requests, "get")
    def test_get_rows_returns_correct_number_of_rows(self, mock_get):
        response_mock = Mock()
        response_mock.text = """
            <tbody>
                <tr>Row 1</tr>
                <tr>Row 2</tr>
                <tr>Row 3</tr>
            </tbody>
        """
        mock_get.return_value = response_mock

        scraper = IMDbScraper()
        soup = BeautifulSoup(response_mock.text, "html.parser")

        rows = scraper.get_rows(3, soup)

        assert len(rows) == 3

    @patch.object(requests, "get")
    def test_get_rows_returns_correct_row_content(self, mock_get):
        response_mock = Mock()
        response_mock.text = """
            <tbody>
                <tr><td class="titleColumn"><a href="/movie1">Movie 1</a></td></tr>
                <tr><td class="titleColumn"><a href="/movie2">Movie 2</a></td></tr>
                <tr><td class="titleColumn"><a href="/movie3">Movie 3</a></td></tr>
            </tbody>
        """
        mock_get.return_value = response_mock

        scraper = IMDbScraper()
        soup = BeautifulSoup(response_mock.text, "html.parser")

        rows = scraper.get_rows(3, soup)

        expected_content = [
            '<tr><td class="titleColumn"><a href="/movie1">Movie 1</a></td></tr>',
            '<tr><td class="titleColumn"><a href="/movie2">Movie 2</a></td></tr>',
            '<tr><td class="titleColumn"><a href="/movie3">Movie 3</a></td></tr>',
        ]
        for i, row in enumerate(rows):
            assert str(row) == expected_content[i]

    def test_process_row_returns_correct_data(self):
        scraper = IMDbScraper()
        row_html = """
            <tr>
                <td class="titleColumn">
                    <a href="/movie1">Movie Title</a>
                </td>
                <td class="ratingColumn imdbRating">
                    <strong>8.5</strong>
                </td>
            </tr>
        """
        row_mock = BeautifulSoup(row_html, "html.parser")
        scraper.get_summary = MagicMock(return_value="Movie summary")

        result = scraper.process_row(row_mock)

        assert result == ["Movie Title", "8.5", "Movie summary"]

    @patch.object(requests, "get")
    def test_get_summary_returns_correct_summary(self, mock_get):
        response_mock = Mock()
        response_mock.text = """
            <span data-testid="plot-xs_to_m">Movie summary</span>
        """
        mock_get.return_value = response_mock

        scraper = IMDbScraper()
        summary = scraper.get_summary("https://www.imdb.com/movie1")

        assert summary == "Movie summary"
