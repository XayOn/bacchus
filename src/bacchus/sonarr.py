from .arr import Arr


class Sonarr(Arr):
    def settings(self, base_url, api_key):
        cats = [
            5010, 5030, 5040, 2000, 2010, 2020, 2030, 2035, 2040, 2045,
            2050, 2060
        ]
        return {
            "minimumSeeders": 1,
            "requiredFlags": [],
            "baseUrl": base_url,
            "multiLanguages": [],
            "apiKey": api_key,
            "categories": cats,
            "animeCategories": [],
            "removeYear": False,
            "searchByTitle": False,
        }
