import os
import scrapy
import html2text
import re

class MySpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["hubspot.com"]
    start_urls = ["https://www.businessnewsdaily.com/11348-mobile-pos-benefits.html",]

    def parse(self, response):
        # Extract the title and entire HTML content of the page
        title = response.css('h1::text').get()
        html_content = response.body
        if not title:
            title = "Blog"
        # Convert HTML to Markdown
        converter = html2text.HTML2Text()
        markdown_content = converter.handle(html_content.decode("utf-8"))

        # Remove links from the Markdown content
        markdown_content = re.sub(r'\[([^\]]+)\]\(([^)]+?)\)', r'\1', markdown_content)
        markdown_content = re.sub(r'\(([^)]+?)\)', r'\1', markdown_content)
        markdown_content = re.sub(r'https?://[^\s]+', '', markdown_content)

        # Create a new folder
        output_folder = "output_files"
        os.makedirs(output_folder, exist_ok=True)

        # Use the title as the filename within the output folder
        filename = f"{output_folder}/{title.replace(' ', '_')}_without_links.md"

        # Save the Markdown content without links to the file with the title as the filename
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        self.log(f"Saved Markdown content without links to {filename}")
