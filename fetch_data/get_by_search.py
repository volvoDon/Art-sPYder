import aiohttp
import asyncio
from pyppeteer import launch
import config    

class LabelListPair():
    def __init__(
        self,
        search_terms: str,
        baseurl: str = config.base_url,
        sample_size: str = "Med",
        ):
            if search_terms is None : raise ValueError(f'search term cannot both be blank')
            self.search_terms = search_terms.replace(' ','%20')
            if type(sample_size) == str:
                  if sample_size == "Small": self.sample_size = 30
                  elif sample_size == "Large": self.sample_size = 60
                  elif sample_size == "Med": self.sample_size = 60
                  else: raise ValueError(f'sample_size must be "Small, Med, Large" you entered: {sample_size}')

            else: raise ValueError(f'sample_size must be "Small, Med, Large" you entered: {sample_size}')
            self.baseurl = self.form_url(baseurl)
            self.data = {"label":self.search_terms,"links":self.get_image_urls()}

    def form_url(self,url) -> str:
          url = f'{config.base_url}title={self.search_terms}&artobj_imagesonly=Images_online&pageSize={self.sample_size}'
          return url

    def get_image_urls(self)->list:
        async def extract_img_src_from_thumbnail_class(url):
            browser = await launch()
            page = await browser.newPage()
    
            await page.goto(url, {'waitUntil': 'networkidle0'})
            await page.waitForSelector('img.thumbnail')

            # Extract img src attributes for images with class "thumbnail"
            imgSrcs = await page.querySelectorAllEval('img.thumbnail', 'images => images.map(img => img.src)')

            await browser.close()
            return imgSrcs

        url = self.baseurl
        img_sources = asyncio.get_event_loop().run_until_complete(extract_img_src_from_thumbnail_class(url))
        return img_sources

def data_cleaner(labellistpair: LabelListPair):
    assert len(labellistpair.data['links']) > 0
    print("Cleaning Image Links")
    async def check_status(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return url, response.status

    async def main(url_list):
        tasks = [check_status(url) for url in url_list]
        results = await asyncio.gather(*tasks)
        return [url for url, status in results if status != 404]
    
    filtered_urls = asyncio.run(main(labellistpair.data['links']))
    if len(filtered_urls) < 0: raise ValueError("No Valid Urls left in List")
    print(f'Removed {len(labellistpair.data["links"])-len(filtered_urls)} of {len(labellistpair.data["links"])}')
    labellistpair.data["links"] = filtered_urls 
     
        
if __name__ == '__main__':
     Lemur = LabelListPair('tree')
     print(Lemur.data)
     data_cleaner(Lemur)
     for item in Lemur.data['links']: print(item)
         