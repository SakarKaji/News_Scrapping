class BaseScraper:
    def __init__(self):
        # Define shared variables here
        self.articlelink_xpath = None
        self.description_xpath =None
        self.title_xpath = None
        self.image_xpath = None
        self.date_xpath = None
        self.article_source = None
        self.categories = None

    