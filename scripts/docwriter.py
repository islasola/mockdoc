import re
import json


class DocWriter:

    def __init__(self, docs, output='docs', indent=0):
        self.docs = docs
        self.output = output
        self.indent = indent
        self.vault = []
        self.pages = [ dict(
            id=''.join(p['id'].split('-')),
            title=p['title'],
            slug=p['slug'],
        ) for c in docs for b in c['books'] for p in b['pages'] ]
        self.__replace_links()

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

    def __replace_links(self):
        for category in self.docs:
            for book in category['books']:
                for page in book['pages']:
                    for block in page['blocks']:
                        if 'rich_text' in block[block['type']]:
                            for segment in block[block['type']]['rich_text']:
                                if segment['type'] == 'text':
                                    if segment['text']['link']:
                                        url = segment['text']['link']['url']
                                        if url.startswith('https://www.notion.so/') or url.startswith('/'):
                                            page_id = url.split('/')[-1]
                                            page = self.__get_page_slug_by_id(page_id)
                                            if page:
                                                segment['text']['link']['url'] = f"doc:{page['slug']}"
                                            else:
                                                self.vault.append(f"[WARNING] {page_id} not found, link to it will be broken\n\n")

    def __get_page_slug_by_id(self, page_id):
        page = list(filter(lambda x: x['id'] == page_id, self.pages))
        if page:
            return page[0]
        else:
            self.vault.append(f"[WARNING] {page_id} not found, link to it will be broken\n\n")

    def __markdown(self, blocks=None, indent=0):
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
                markdown.append(indent * ' ' + self.__header(block))
                prev_block_type = block['type']
            elif block['type'] == 'paragraph':
                markdown.append(indent * ' ' + self.__paragraph(block))
                prev_block_type = block['type']
            elif block['type'] == 'quote':
                markdown.append(indent * ' ' + self.__quote(block))
                prev_block_type = block['type']
            elif block['type'] == 'bulleted_list_item':
                markdown.append(indent * ' ' + self.__bullet_list_item(block, indent=indent))
            elif block['type'] == 'numbered_list_item':
                markdown.append(indent * ' ' + self.__numbered_list_item(block, indent=indent))
                prev_block_type = block['type']
            elif block['type'] == 'link_preview':
                markdown.append(indent * ' ' + self.__link_preview(block))
                prev_block_type = block['type']
            elif block['type'] == 'link_to_page':
                markdown.append(indent * ' ' + self.__link_to_page(block))
                prev_block_type = block['type']
            elif block['type'] == 'table':
                markdown.append(self.__table(block, indent=indent))
                prev_block_type = block['type']
            elif block['type'] == 'code':
                markdown.append(self.__code(block, indent=indent))
                prev_block_type = block['type']
            elif block['type'] == 'synced_block':
                markdown.append(indent * ' ' + self.__synced_block(block))
                prev_block_type = block['type']
            elif block['type'] == 'image':
                if 'file' in block['image']:
                    markdown.append(indent * ' ' + self.__image_file(block))
                    prev_block_type = block['type']
                if 'external' in block['image']:
                    markdown.append(indent * ' ' + self.__image_external(block))
                    prev_block_type = block['type']
            elif block['type'] == 'video':
                if block['video']['type'] == 'external':
                    markdown.append(indent * ' ' + self.__video_external(block))
                    prev_block_type = block['type']
            elif block['type'] == 'equation':
                markdown.append(indent * ' ' + self.__equation(block))
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

    def __place_indent_in_code(self, code_lines, indent, tabSize):
        code_lines = [ x['plain_text'] for x in code_lines ]
        code_lines = ''.join(code_lines)
        code_lines = code_lines.split('\n')
        code_lines = [ indent * ' ' + x.replace('\t', tabSize * ' ') for x in code_lines ]
        
        return '\n'.join(code_lines)

    def __code(self, block, indent, tabSize=4):
        caption = block['code']['caption']

        if len(caption):
            caption = f" {caption[0]['plain_text']}"
        else:
            caption = ''
        
        code = block['code']['rich_text']

        if len(code):
            code = self.__place_indent_in_code(code, indent, tabSize)
        else:
            code = ''

        lang = block['code']['language']

        return f"{indent*' '}```{lang}{caption}\n{code}\n{indent*' '}```\n\n" 
    
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

    def __bullet_list_item(self, block, indent):
        segments = block['bulleted_list_item']['rich_text']
        if block['has_children']:
            children = self.__markdown(indent=indent+4, blocks=block['bulleted_list_item']['children'])
            return f"* {self.__paragraph(segments=segments)}\n\n{children}"
        return f"* {self.__paragraph(segments=segments)}"

    def __numbered_list_item(self, block, indent):
        segments = block['numbered_list_item']['rich_text']
        if block['has_children']:
            children = self.__markdown(indent=indent+4, blocks=block['numbered_list_item']['children'])
            return f"* {self.__paragraph(segments=segments)}\n\n{children}"
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
        block = {
            "html": re.sub('height="[0-9]{3}"', 'height="450"', html),
            "url": url,
            "title": title,
            "favicon": "https://www.google.com/favicon.ico",
            "image": image,
            "provider": "https://www.youtube.com/",
            "href": url,
            "typeOfEmbed": "youtube"
        }

        return f"""[block:embed]
{json.dumps(block, indent=4)}
[/block]                
"""
    
    def __equation(self, block):
        expression = block['equation']['expression']
        return f"$${expression}$$\n\n"
    
    def __link_to_page(self, block):
        page_id = block['link_to_page']['page_id']
        page = self.__get_page_slug_by_id(page_id)
        if page:
            return f"[{page['title']}](doc:{page['slug']})\n\n"
        else:
            self.vault.append(f"[WARNING] {page_id} not found, link to it will be broken\n\n")
    
    def __table(self, block, indent):
        rows = block['table']['children']
        rows_length_matrix = map(self.__table_row_cell_lengths, rows)
        rows_template = list(map(max, zip(*rows_length_matrix)))
        table_header_divider = list(map(lambda x: '-' * x, rows_template))
        rows = list(map(self.__table_row_cells, rows))
        rows.insert(1, table_header_divider)
        rows = '\n'.join([ self.__format_table_row(x, rows_template, indent=indent) for x in rows ])

        return f"{rows}\n\n"
    
    def __table_row_cells(self, block):
        cells = block['table_row']['cells']
        cells = map(lambda x:  self.__paragraph(segments=x)[:-2].replace('\n', '<br>') if len(x) > 0 else '   ', cells)
        
        return list(cells)
    
    def __format_table_row(self, row, temp, indent):
        for i in range(len(temp)):
            if len(row[i]) < temp[i]:
                row[i] = row[i] + (temp[i] - len(row[i])) * ' '

        return indent * ' ' + '| ' + ' | '.join(row) + ' |'
    
    def __table_row_cell_lengths(self, block):
        cells = block['table_row']['cells']
        cells = map(lambda x: len(self.__paragraph(segments=x)[:-2]) if len(x) > 0 else 3, cells)
        
        return list(cells)    

    def __overview(self, category, book):
        title = book['title']
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