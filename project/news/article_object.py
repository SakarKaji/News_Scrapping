from Utils import Utils


def article_data(self, response):
    try:
        url = response.url
        category = response.meta['category']
        title = response.xpath(
            self.title_xpath).extract_first().strip() or None
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        unwanted_chars = ['\xa0', '\x00', '\n', '\u202f','\u200d']
        for char in unwanted_chars:
            title = title.replace(char, '')
            content = content.replace(char, '')
        news = {
            'title': title,
            'content_description': content,
            'published_date': self.formattedDate,
            'url': url,
            'category': category,
            'is_recent': True,
            'source': self.article_source,
        }
        if img_src:
            news['image_url'] = img_src
        return news

    except Exception as e:
        print(f"error received in {e}")
