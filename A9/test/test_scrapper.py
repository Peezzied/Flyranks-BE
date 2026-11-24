import unittest

class TestScraper(unittest.TestCase):
    def test_invalid_record(self):
        from scrapper.discover import discover
        from scrapper.extract import extract
        from scrapper.reports import ReportManager
        
        urls = discover(3)
        urls[next(reversed(urls))].extend(["https://books.toscrape.com/catalogue/nigga/index.html"])
        extract(urls)
        
        self.assertEqual(ReportManager._raw_record["failed_pages"], 1)

if __name__ == "__main__":
    unittest.main()