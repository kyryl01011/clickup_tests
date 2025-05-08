from playwright.sync_api import Page

class PageActions:
    def __init__(self, page: Page):
        self.page = page