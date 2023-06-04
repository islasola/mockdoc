---
title: {{group_title}}
slug: {{group_slug}}
category: {{category_id}}
---
{%- for page in pages %}

## [{{page['title']}}](doc:{{page['slug']}})

{{page['description']}}
{%- endfor %}
