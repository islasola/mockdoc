---
title: {{page_title}}
excerpt: {{page_excerpt}}
slug: {{page_slug}}
category: {{category_id}}
parentDoc: {{parent_id}}
---

<div>
    {%- if page_method == 'get' %}
    <div style="display: inline-block; background: #0d8d67; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.4em 1em;">
        <span>GET</span>
    </div>
    {%- endif %}
    {%- if page_method == 'post' %}
    <div style="display: inline-block; background: #026aca; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.4em 1em;">
        <span>POST</span>
    </div>
    {%- endif %}
    {%- if page_method == 'put' %}
    <div style="display: inline-block; background: #604aa2; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.4em 1em;">
        <span>PUT</span>
    </div>
    {%- endif %}
    {%- if page_method == 'delete' %}
    <div style="display: inline-block; background: #b91926; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.4em 1em;">
        <span>DELETE</span>
    </div>
    {%- endif %}
    <span style="font-weight: bold;">{{  page_url}}</span>
</div>


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
{%- if v['type'] not in ['array', 'object'] %}
| `{{k}}`  | **{{v['type']}}** {%- if k in req_body['required'] -%}(required){%- endif -%}<br>{{v['description']}} |
{%- elif v['type'] == 'object' %}
| `{{k}}`  | **{{v['type']}}** {%- if k in req_body['required'] -%}(required){%- endif -%}<br>{{v['description']}} |
{%- for ko, vo in v['properties'].items() %}
| `{{k}}.{{ko}}`  | **{{vo['type']}}**<br>{{vo['description']}} |
{%- endfor %}
{%- elif v['type'] == 'array' %}
| `{{k}}`  | **{{v['type']}}** {%- if k in req_body['required'] -%}(required){%- endif -%}<br>{{v['description']}} |
{%- if v['items'] == 'object' %}
{%- for ka, va in v['items']['properties'].items() %}
| `{{k}}[].{{ka}}`  | **{{va['type']}}**<br>{{va['description']}} |
{%- endfor %}
{%- endif %}
{%- endif %}
{%- endfor %}


{%- endfor %}
{%- else %}

No request body required

{%- endif %}

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
{%- if v['type'] not in ['array', 'object'] or 'properties' not in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- elif v['type'] == 'array' and 'properties' in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- for ka, va in v['items']['properties'].items() %}
| `data.{{k}}[].{{ka}}`   | **{{va['type']}}**<br>{{va['description']}} |
{%- endfor %}
{%- elif v['type'] == 'object' %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- for ko, vo in v['properties'].items() %}
| `data.{{k}}.{{ko}}`   | **{{vo['type']}}**<br>{{vo['description']}} |
{%- endfor %}
{%- endif %}
{%- endfor %}
{%- elif 'items' in res_body['properties']['data'] %}
| `data`  | **array**<br>A data array of {{res_body['properties']['data']['items']['type']}}s. |
{%- if res_body['properties']['data']['items']['type'] == 'object' %}
{%- for k, v in res_body['properties']['data']['items']['properties'].items() %}
{%- if v['type'] not in ['array', 'object'] or 'properties' not in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- elif v['type'] == 'array' and 'properties' in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- for ka, va in v['items']['properties'].items() %}
| `data.{{k}}[].{{ka}}`   | **{{va['type']}}**<br>{{va['description']}} |
{%- endfor %}
{%- elif v['type'] == 'object' %}
| `data.{{k}}`   | **{{v['type']}}**<br>{{v['description']}} |
{%- for ko, vo in v['properties'].items() %}
| `data.{{k}}.{{ko}}`   | **{{vo['type']}}**<br>{{vo['description']}} |
{%- endfor %}
{%- endif %}
{%- endfor %}
{%- endif%}
{%- endif %}
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Possible Errors

| Code | Error Message |
| ---- | ------------- |
{{ page_title | list_error }}

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.
