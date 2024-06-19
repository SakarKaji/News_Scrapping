from Utils import Utils
from Utils import PostNews
from news.date_time_convertor import date_time_object


def article_data(self, response, source):
    try: 
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).extract_first().strip() 
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = desc
        formattedDate = date_time_object()
        news = {
            'title': title,
            'content_description': content,
            'published_date': formattedDate,
            'image_url': img_src,
            'url': url,
            'category_name': category,
            'is_recent': True,
            'source_name': source,
            }
        PostNews.postnews(news,self.name)

    except Exception as e:
        print(f"errror received in {e}")
        PostNews.postnews(error=e,source_name=self.name,category=category)    
       
    
       
       


        