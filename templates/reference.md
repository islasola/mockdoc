---
title: {{page_title}}
excerpt: {{page_excerpt}}
category: {{category_id}}
slug: {{title_slug}}
---

## Request

### Parameters

{% if query_params -%}

- Query parameters

    | Parameter        | Description                                                                               |
    |------------------|-------------------------------------------------------------------------------------------|
    {%- for param in query_params %}
    | `{{param['name']}}`  | **{{param['schema']['type']}}** {%- if param['required'] -%}(required){%- endif -%}<br>{{param['description']}} |
    {%- endfor %}

{%- else -%}

- No query parameters required

{%- endif %}

{% if path_params -%}

- Path parameters

    | Parameter        | Description                                                                               |
    |------------------|-------------------------------------------------------------------------------------------|
    {%- for param in path_params %}
    | `{{param['name']}}`  | **{{param['schema']['type']}}** {%- if param['required'] -%}(required){%- endif -%}<br>{{param['description']}} |
    {%- endfor %}

{%- else -%}

- No path parameters required

{%- endif %}

### Request Body

{%- if req_bodies -%}
{%- for req_body in req_bodies %}

```json
{{req_body | req_format }}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
{%- for k, v in req_body['properties'].items() %}
| `{{k}}`  | **{{v['type']}}** {%- if k in req_body['required'] -%}(required){%- endif -%}<br>{{v['description']}} |

{%- endfor %}


{%- endfor %}
{%- endif -%}

## Response

{{ res_des }}

### Response Bodies

- Response body if we process your request successfully

```json
{{res_body | res_format }}
```

- Response body if we failed to process your request

```json
{
    "code": string,
    "message": string
}
```

### Properties

The properties in the returned response are listed in the following table.

| Property | Description                                                                                                                                 |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `code`   | **integer**<br>Indicates whether the request succeeds.<br><ul><li>`200`: The request succeeds.</li><li>Others: Some error occurs.</li></ul> |
{%- if 'properties' in res_body['properties']['data'] %}
| `data`    | **object**<br>A data object. |
{%- for k, v in res_body['properties']['data']['properties'].items() %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- endfor %}
{%- elif 'items' in res_body['properties']['data'] %}
| `data`  | **array**<br>A data array |
{%- for k, v in res_body['properties']['data']['items']['properties'].items() %}
| `data[].{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- endfor %}
{%- endif %}
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.
