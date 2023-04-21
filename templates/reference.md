---
title: {{page_title}}
excerpt: {{page_excerpt}}
category: 64368bb63b18090510bad283
---

## Request

### Parameters

{%- if query_params %}

- Query parameters

    | Parameter        | Description                                                                               |
    |------------------|-------------------------------------------------------------------------------------------|
    {% for param in query_params -%}
    | {{param['name']}}  | **{{param['schema']['type']}}** {%- if param['required'] -%}(required){%- endif -%}<br>{{param['description']}} |
    {%- endfor %}

{% else %}

- No query parameters required

{%- endif %}

{% if path_params -%}

- Path parameters

    | Parameter        | Description                                                                               |
    |------------------|-------------------------------------------------------------------------------------------|
    {% for param in query_params -%}
    | {{param['name']}}  | **{{param['schema']['type']}}** {%- if param['required'] -%}(required){%- endif -%}<br>{{param['description']}} |
    {%- endfor %}

{%- else %}

- No path parameters required

{%- endif %}

### Body

{% for req_body in req_bodies -%}
```json
{{req_body['body']}}
```

| Parameter        | Description                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
{% for prop in req_body['properties'] -%}
| {{prop}}  | **{{req_body['properties'][prop]['type']}}** {%- if req_body['properties'][prop]['required'] -%}(required){%- endif -%}<br>{{req_body['properties'][prop]['description']}} |
{%- endfor %}

{% endfor %}

## Response

{{ response_description }}

### Body

- Response body if we process your request successfully

```json
{{res_body['body']}}
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

| Property | Description                                                                                                                                  |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `code`     | **integer**<br>Indicates whether the request succeeds.<br><ul><li>`200`: The request succeeds.</li><li>Others: Some error occurs.</li></ul> |
{% for prop in res_body['properties'] -%}
| `{{prop}}` | **{{res_body['properties'][prop]['type']}}**<br>{{res_body['properties'][prop]['description']}} |
{%- endfor %}
| `message`  | **string**<br>Indicates the possible reason for the reported error. |

## Errors

The following table lists the errors that the request possibly returns.

| Code            | Message        | Possible Reasons |
|-----------------|----------------|------------------|
<% for err in errors -%>
| {{err['code']}} | {{err['msg']}} | {{err['desc']}}  |
<%- endfor %>

## Have a try!

Use our API explorer on the side pane to call this API and check the request and responses. Remember to fill in the necessary body parameters below, if applicable.
