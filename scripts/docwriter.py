import re


class DocWriter:

    def __init__(self, docs, output='docs'):
        self.docs = docs
        self.output = output

    def write_docs(self):
        for category in self.docs:
            for book in category['books']:
                for page in book['pages']:
                    self.__page(category['rid'], book['rid'], page)
                self.__overview(category['rid'], book)

    def write_page(self, page_slug):
        for category in self.docs:
            for book in category['books']:
                if book['slug'] == page_slug:
                    self.__overview(category['rid'], book)

                for page in book['pages']:
                    if page['slug'] == page_slug:
                        self.__page(category['rid'], book['rid'], page)

    def __markdown(self, blocks=None):
        markdown = []
        prev_block_type = None
        for block in blocks:
            if prev_block_type == 'quote' and block['type'] != 'quote':
                markdown.append('\n')
            if prev_block_type == 'bulleted_list_item' and block['type'] != 'bulleted_list_item':
                markdown.append('\n')
            if prev_block_type == 'numbered_list_item' and block['type'] != 'numbered_list_item':
                markdown.append('\n')
            if block['type'].startswith('heading'):
                markdown.append(self.__header(block))
                prev_block_type = block['type']
            elif block['type'] == 'paragraph':
                markdown.append(self.__paragraph(block))
                prev_block_type = block['type']
            elif block['type'] == 'quote':
                markdown.append(self.__quote(block))
                prev_block_type = block['type']
            elif block['type'] == 'bulleted_list_item':
                markdown.append(self.__bullet_list_item(block))
            elif block['type'] == 'numbered_list_item':
                markdown.append(self.__numbered_list_item(block))
                prev_block_type = block['type']
            elif block['type'] == 'link_preview':
                markdown.append(self.__link_preview(block))
                prev_block_type = block['type']
            elif block['type'] == 'link_to_page':
                markdown.append(self.__link_to_page(block))
                prev_block_type = block['type']
            elif block['type'] == 'table':
                markdown.append(self.__table(block))
                prev_block_type = block['type']
            elif block['type'] == 'code':
                markdown.append(self.__code(block))
                prev_block_type = block['type']
            elif block['type'] == 'synced_block':
                markdown.append(self.__synced_block(block))
                prev_block_type = block['type']
            elif block['type'] == 'image':
                if 'file' in block['image']:
                    markdown.append(self.__image_file(block))
                    prev_block_type = block['type']
                if 'external' in block['image']:
                    markdown.append(self.__image_external(block))
                    prev_block_type = block['type']
            elif block['type'] == 'video':
                if block['video']['type'] == 'external':
                    markdown.append(self.__video_external(block))
                    prev_block_type = block['type']
            elif block['type'] == 'equation':
                markdown.append(self.__equation(block))
            else:
                print(block['type'])

        return ''.join(markdown)

    def __paragraph(self, block=None, **kwargs):
        if 'segments' in kwargs:
            segments = kwargs['segments']
        else:
            segments = block['paragraph']['rich_text']

        segments = map(self.__parse_text, segments)

        return ''.join(segments) + "\n\n"
    
    def __parse_text(self, segment):
        if segment['type'] == 'text':
            if segment['text']['link']:
                url = segment['text']['link']['url']
                if re.match('/[a-z0-9]', url):
                    url = self.__retrieve_page(page_id=url[1:])
                    url = url['properties']['Title']['title'][0]['text']['content']
                    url = f"docs:{self.__page_slug(url)}"
                return f"[{segment['plain_text']}]({url})"
            elif segment['annotations']['bold']:
                return f"**{segment['plain_text']}**"
            elif segment['annotations']['italic']:
                return f"*{segment['plain_text']}*"
            elif segment['annotations']['strikethrough']:
                return f"~~{segment['plain_text']}~~"
            elif segment['annotations']['underline']:
                return f"<u>{segment['plain_text']}</u>"
            else:
                return segment['plain_text']
        else:
            return ''
        
    def __header(self, block):
        if block['type'] == 'heading_1' or block['type'] == 'heading_2':
            type = block['type']
            segments = block[type]['rich_text']
            segments = ''.join([ x['plain_text'] for x in segments])
            return f"## {segments}\n\n"
        if block['type'] == 'heading_3':
            type = block['type']
            segments = block[type]['rich_text']
            segments = ''.join([ x['plain_text'] for x in segments])
            return f"### {segments}\n\n"
        
    def __code(self, block, tabSize=4):
        caption = block['code']['caption']

        if len(caption):
            caption = f" {caption[0]['plain_text']}"
        else:
            caption = ''
        
        code = block['code']['rich_text']

        if len(code):
            code = code[0]['plain_text'].replace('\t', ' ' * tabSize)
        else:
            code = ''

        lang = block['code']['language']

        return f"```{lang}{caption}\n{code}\n```\n\n" 
    
    def __synced_block(self, block):
        blocks = block['synced_block']['children']
        return self.__markdown(blocks)
    
    def __quote(self, block):
        plain_text = block['quote']['rich_text'][0]['plain_text']
        if plain_text.endswith('Notes') or plain_text.endswith('Warning'):
            return f"> {block['quote']['rich_text'][0]['plain_text']}\n>\n"
        else:
            segments = block['quote']['rich_text']
            return f"> {self.__paragraph(segments=segments)[:-2]}\n"    

    def __bullet_list_item(self, block):
        segments = block['bulleted_list_item']['rich_text']
        return f"* {self.__paragraph(segments=segments)}"

    def __numbered_list_item(self, block):
        segments = block['numbered_list_item']['rich_text']
        return f"1. {self.__paragraph(segments=segments)}"      

    def __link_preview(self, block):
        title = block['link_preview']['title']
        url = block['link_preview']['url']
        
        return f"![{title}]({url})\n\n"  
    
    def __image_file(self, block):
        url = block['image']['file']['url']
        title = block['image']['file']['title']

        return f"![{title}]({url})\n\n"
    
    def __image_external(self, block):
        url = block['image']['external']['url']
        if block['image']['caption']:
            title = block['image']['caption'][0]['plain_text']
        else:
            title = block['id']

        return f"![{title}]({url})\n\n"
    
    def __video_external(self, block):
        url = block['video']['external']['url']
        title = block['video']['external']['meta']['title']
        html = block['video']['external']['meta']['html']
        image = block['video']['external']['meta']['thumbnail_url']

        return f"""[block:embed]
{
    "html": "{html}",
    "url": "{url}",
    "title": "{title}",
    "favicon": "https://www.google.com/favicon.ico",
    "image": "{image}",
    "provider": "https://www.youtube.com/",
    "href": "{url}",
    "typeOfEmbed": "youtube"
}
[/block]                
"""
    
    def __equation(self, block):
        expression = block['equation']['expression']
        return f"$${expression}$$\n\n"
    
    def __link_to_page(self, block):
        title = block['link_to_page']['title']
        slug = block['link_to_page']['slug']

        return f"[{title}](doc:{slug})\n\n"
    
    def __table(self, block):
        rows = block['table']['children']
        rows_length_matrix = map(self.__table_row_cell_lengths, rows)
        rows_template = list(map(max, zip(*rows_length_matrix)))
        table_header_divider = list(map(lambda x: '-' * x, rows_template))
        rows = list(map(self.__table_row_cells, rows))
        rows.insert(1, table_header_divider)
        rows = '\n'.join([ self.__format_table_row(x, rows_template) for x in rows ])

        return f"{rows}\n\n"

    def __table_row_cells(self, block):
        cells = block['table_row']['cells']
        cells = map(lambda x:  self.__paragraph(segments=x)[:-2] if len(x) > 0 else '   ', cells)
        
        return list(cells)
    
    def __format_table_row(self, row, temp):
        for i in range(len(temp)):
            if len(row[i]) < temp[i]:
                row[i] = row[i] + (temp[i] - len(row[i])) * ' '

        return '| ' + ' | '.join(row) + ' |'
    
    def __table_row_cell_lengths(self, block):
        cells = block['table_row']['cells']
        cells = map(lambda x: len(self.__paragraph(segments=x)[:-2]) if len(x) > 0 else 3, cells)
        
        return list(cells)    

    def __overview(self, category, book):
        title = book['title'][3:]
        slug = book['slug']
        description = book['description']
        if description:
            description = description[0]['plain_text']
        else:
            description = ''

        paragraphs = []
        for page in book['pages']:
            page_slug = page['slug']
            page_title = page['title']
            page_excerpt = self.__markdown(blocks=[page['blocks'][0]])

            paragraphs.append(f"""## [{page_title}](doc:{page_slug})

{page_excerpt}
""")

        paragraphs = '\n'.join(paragraphs)

        with open(f"{self.output}/{slug}.md", 'w') as f:
            f.write(f"""---
title: {title}
excerpt: {description}
category: {category}
slug: {slug}
---

{paragraphs}

""")

    def __page(self, category, book, page):
        title = page['title']
        slug = page['slug']
        blocks = page['blocks']

        with open(f"{self.output}/{slug}.md", 'w') as f:
            f.write(f"""---
title: {title}
category: {category}
slug: {slug}
parentDoc: {book}
---

{self.__markdown(blocks=blocks)}

""")
