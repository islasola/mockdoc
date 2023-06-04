---
title: {{group_title}}
slug: {{group_slug}}
category: {{category_id}}
---
{%- for page in pages %}

## [{{page['title']}}](ref:{{page['slug']}})

{{page['description']}}
{%- endfor %}
