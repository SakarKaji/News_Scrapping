def article_data(self, response):
    try:
        url = response.url or response.meta['link']
        category = response.meta['category']
        title = response.xpath(self.title_xpath).extract_first().strip()
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = desc
        news = {
            'title': title,
            'content_description': content,
            'published_date': self.formattedDate,
            'image_url': img_src,
            'url': url,
            'category_name': category,
            'is_recent': True,
            'source_name': self.article_source,
        }
        return news

    except Exception as e:
        print(f"error received in {e}")
        return
        # PostNews.postnews(error=e,source_name=self.name,category=category)
