import scrapy
import html2text

class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
        "https://hi.wikipedia.org/wiki/बुद्धि",
        "https://hi.wikipedia.org/wiki/कार्बन_चक्र",
        "https://hi.wikipedia.org/wiki/वीडियो_खेल",
        "https://hi.wikipedia.org/wiki/आँवला",
        "https://hi.wikipedia.org/wiki/पाइथागोरस",
        "https://hi.wikipedia.org/wiki/निंजा_हतोड़ी",
        "https://hi.wikipedia.org/wiki/महाभारत",
        "https://hi.wikipedia.org/wiki/कंप्यूटर",
        "https://hi.wikipedia.org/wiki/आयुर्विज्ञान",
        "https://hi.wikipedia.org/wiki/चन्द्रयान",
        "https://hi.wikipedia.org/wiki/ग्लेशियर_नेशनल_पार्क",
        "https://hi.wikipedia.org/wiki/गुरुत्वाकर्षण",
        "https://hi.wikipedia.org/wiki/धर्म_(पंथ)",
        "https://hi.wikipedia.org/wiki/कृत्रिम_बुद्धि",
        "https://hi.wikipedia.org/wiki/महाकाव्य",
    ]

    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = True
        self.count = 0

    def parse(self, response):
        # Extracting the last part of the URL (the Hindi title)
        #page_title = response.url.split("/")[-1]
        page_title = response.css(".mw-page-title-main::text").get()
        if page_title != None:
            filename = f"{page_title}.md"
        
        elif page_title == None:
            filename = f"{'Nonefile'}-{self.count}.md"
            self.count += 1


        sections = response.css('.mw-parser-output > *')
        current_heading = ''
        content = []

        for section in sections:
            if section.xpath('name()').get() == 'h2':
                current_heading = self.html_to_markdown(section.get())
            elif section.xpath('name()').get() == 'p':
                paragraph = self.html_to_markdown(section.get())
                if paragraph.strip():
                    content.append((current_heading, paragraph))

        # Write the contents to the file with the title as the filename
        with open(filename, 'w', encoding='utf-8') as f:
            for heading, paragraph in content:
                f.write(f"{heading}\n{paragraph}\n\n")

        self.log(f'Saved file {filename}')

    def html_to_markdown(self, html):
        return self.converter.handle(html).strip()
