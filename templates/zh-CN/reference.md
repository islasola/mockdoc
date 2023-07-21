---
title: {{page_title}}
excerpt: {{page_excerpt}}
slug: {{page_slug}}
category: {{category_id}}
parentDoc: {{parent_id}}
---

<div>
    {%- if page_method == 'get' %}
    <div style="display: inline-block; background: #0d8d67; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.3em 1em;">
        <span>GET</span>
    </div>
    {%- endif %}
    {%- if page_method == 'post' %}
    <div style="display: inline-block; background: #026aca; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.3em 1em;">
        <span>POST</span>
    </div>
    {%- endif %}
    {%- if page_method == 'put' %}
    <div style="display: inline-block; background: #604aa2; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.3em 1em;">
        <span>PUT</span>
    </div>
    {%- endif %}
    {%- if page_method == 'delete' %}
    <div style="display: inline-block; background: #b91926; font-size: 0.6em; border-radius: 10px; color: #ffffff; padding: 0.3em 1em;">
        <span>DELETE</span>
    </div>
    {%- endif %}
    <span style="font-weight: bold;">  {{server}}{{page_url}}</span>
</div>

---

## 示例

{{ page_title | get_example }}

## 请求

### 参数

{% if query_params -%}

- 查询参数

    | 参数名称          | 参数说明                                                                               |
    |------------------|-------------------------------------------------------------------------------------------|
    {%- for param in query_params %}
    | `{{param['name']}}`  | **{{param['schema']['type']}}** {%- if param['required'] -%}（必选）{%- endif -%}<br>{{param['description']}}{%- if param['default'] -%}<br>默认值为 **{{param['default']}}**.{%- endif -%}{%- if param['minimum'] and param['maximum'] -%}<br>参数取值范围在 **{{param['minimum']}}** 到 **{{param['maximum']}}** 之间.{%- endif -%}{%- if param['minimum'] and not param['maximum'] -%}<br>最小值为 **{{param['minimum']}}**.{%- endif -%}{%- if param['maximum'] and not param['minimum'] -%}<br>最大值为 **{{param['maximum']}}**.{%- endif -%} |
    {%- endfor %}

{%- else -%}

- 无查询参数。

{%- endif %}

{% if path_params -%}

- 路径参数

    | Parameter        | Description                                                                               |
    |------------------|-------------------------------------------------------------------------------------------|
    {%- for param in path_params %}
    | `{{param['name']}}`  | **{{param['schema']['type']}}** {%- if param['required'] -%}（必选）{%- endif -%}<br>{{param['description']}}{%- if param['default'] -%}<br>默认值为 **{{param['default']}}**.{%- endif -%}{%- if param['minimum'] and param['maximum'] -%}<br>参数取值范围在 **{{param['minimum']}}** 到 **{{param['maximum']}}** 之间.{%- endif -%}{%- if param['minimum'] and not param['maximum'] -%}<br>最小值为 **{{param['minimum']}}**.{%- endif -%}{%- if param['maximum'] and not param['minimum'] -%}<br>最大值为 **{{param['maximum']}}**.{%- endif -%} |
    {%- endfor %}

{%- else -%}

- 无路径参数。

{%- endif %}

### 请求体

{%- if req_bodies -%}
{%- for req_body in req_bodies %}

```json
{{req_body | req_format }}
```

| 参数名称        | 参数描述                                                                               |
|------------------|-------------------------------------------------------------------------------------------|
{%- for k, v in req_body['properties'].items() %}
{%- if v['type'] not in ['array', 'object'] %}
| `{{k}}`  | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}** {%- if k in req_body['required'] -%}（必选）{%- endif -%}<br>{{v['description']}}{%- if v['default'] -%}<br>默认值为 **{{v['default']}}**.{%- endif -%}{%- if v['minimum'] and v['maximum'] -%}<br>参数取值在 **{{v['minimum']}}** 和 **{{v['maximum']}}** 之间.{%- endif -%}{%- if v['minimum'] and not v['maximum'] -%}<br>最小值为 **{{v['minimum']}}**.{%- endif -%}{%- if v['maximum'] and not v['minimum'] -%}<br>最大值为 **{{v['maximum']}}**.{%- endif -%} |
{%- elif v['type'] == 'object' %}
| `{{k}}`  | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}** {%- if k in req_body['required'] -%}（必选）{%- endif -%}<br>{{v['description']}}{%- if v['default'] -%}<br>默认值为 **{{v['default']}}**.{%- endif -%}{%- if v['minimum'] and v['maximum'] -%}<br>参数取值在 **{{v['minimum']}}** 和 **{{v['maximum']}}** 之间.{%- endif -%}{%- if v['minimum'] and not v['maximum'] -%}<br>最小值为 **{{v['minimum']}}**.{%- endif -%}{%- if v['maximum'] and not v['minimum'] -%}<br>最大值为 **{{v['maximum']}}**.{%- endif -%} |
{%- for ko, vo in v['properties'].items() %}
| `{{k}}.{{ko}}`  | **{{vo['type']}}{%if 'format' in vo %}({{vo['format']}}){%- endif %}**<br>{{vo['description']}}{%- if vo['default'] -%}<br>默认值为 **{{vo['default']}}**.{%- endif -%}{%- if vo['minimum'] and vo['maximum'] -%}<br>参数取值在 **{{vo['minimum']}}** 和 **{{vo['maximum']}}** 之间.{%- endif -%}{%- if vo['minimum'] and not vo['maximum'] -%}<br>最小值为 **{{vo['minimum']}}**.{%- endif -%}{%- if vo['maximum'] and not vo['minimum'] -%}<br>最大值为 **{{vo['maximum']}}**.{%- endif -%} |
{%- endfor %}
{%- elif v['type'] == 'array' %}
| `{{k}}`  | **{{v['type']}}{%if 'format' in v['items'] %} ({{v['items']['type']}} \[{{v['items']['format']}}\]){%- endif %}** {%- if k in req_body['required'] -%}（必选）{%- endif -%}<br>{{v['description']}}{%- if v['default'] -%}<br>默认值为 **{{v['default']}}**.{%- endif -%}{%- if v['minimum'] and v['maximum'] -%}<br>参数取值在 **{{v['minimum']}}** 和 **{{v['maximum']}}** 之间.{%- endif -%}{%- if v['minimum'] and not v['maximum'] -%}<br>最小值为 **{{v['minimum']}}**.{%- endif -%}{%- if v['maximum'] and not v['minimum'] -%}<br>最大值为 **{{v['maximum']}}**.{%- endif -%} |
{%- if v['items'] == 'object' %}
{%- for ka, va in v['items']['properties'].items() %}
| `{{k}}[].{{ka}}`  | **{{va['type']}}{%if 'format' in va %}({{va['format']}}){%- endif %}**<br>{{va['description']}}{%- if va['default'] -%}<br>默认值为 **{{va['default']}}**.{%- endif -%}{%- if va['minimum'] and va['maximum'] -%}<br>参数取值在 **{{va['minimum']}}** 和 **{{va['maximum']}}** 之间.{%- endif -%}{%- if va['minimum'] and not va['maximum'] -%}<br>最小值为 **{{va['minimum']}}**.{%- endif -%}{%- if va['maximum'] and not va['minimum'] -%}<br>最大值为 **{{va['maximum']}}**.{%- endif -%} |
{%- endfor %}
{%- endif %}
{%- endif %}
{%- endfor %}


{%- endfor %}
{%- else %}

无请求体。

{%- endif %}

## 响应

{{ res_des }}

### 响应体

- 处理请求成功后返回

```json
{{res_body | res_format }}
```

- 处理请求失败后返回

```json
{
    "code": integer,
    "message": string
}
```

### 属性

下表罗列了响应包含的所有属性。

| 属性名称  | 属性描述                                                                                                                               |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `code`   | **integer**<br>表示请求是否成功。<br><ul><li>`200`：请求成功。</li><li>其它：存在错误。</li></ul> |
{%- if 'properties' in res_body['properties']['data'] %}
| `data`    | **object**<br>表示响应中携带的数据对象。 |
{%- for k, v in res_body['properties']['data']['properties'].items() %}
{%- if v['type'] not in ['array', 'object'] or 'properties' not in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}**<br>{{v['description']}} |
{%- elif v['type'] == 'array' and 'properties' in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}**<br>{{v['description']}} |
{%- for ka, va in v['items']['properties'].items() %}
| `data.{{k}}[].{{ka}}`   | **{{va['type']}}{%if 'format' in va %}({{va['format']}}){%- endif %}**<br>{{va['description']}} |
{%- endfor %}
{%- elif v['type'] == 'object' %}
| `data.{{k}}`   | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}**<br>{{v['description']}} |
{%- for ko, vo in v['properties'].items() %}
| `data.{{k}}.{{ko}}`   | **{{vo['type']}}{%if 'format' in vo %}({{vo['format']}}){%- endif %}**<br>{{vo['description']}} |
{%- endfor %}
{%- endif %}
{%- endfor %}
{%- elif 'items' in res_body['properties']['data'] %}
| `data`  | **array**<br>表示响应中携带的 {{res_body['properties']['data']['items']['type']}} 数组. |
{%- if res_body['properties']['data']['items']['type'] == 'object' %}
{%- for k, v in res_body['properties']['data']['items']['properties'].items() %}
{%- if v['type'] not in ['array', 'object'] or 'properties' not in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}**<br>{{v['description']}} |
{%- elif v['type'] == 'array' and 'properties' in v['items'] %}
| `data.{{k}}`   | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}**<br>{{v['description']}} |
{%- for ka, va in v['items']['properties'].items() %}
| `data.{{k}}[].{{ka}}`   | **{{va['type']}}{%if 'format' in va %}({{va['format']}}){%- endif %}**<br>{{va['description']}} |
{%- endfor %}
{%- elif v['type'] == 'object' %}
| `data.{{k}}`   | **{{v['type']}}{%if 'format' in v %}({{v['format']}}){%- endif %}**<br>{{v['description']}} |
{%- for ko, vo in v['properties'].items() %}
| `data.{{k}}.{{ko}}`   | **{{vo['type']}}{%if 'format' in vo %}({{vo['format']}}){%- endif %}**<br>{{vo['description']}} |
{%- endfor %}
{%- endif %}
{%- endfor %}
{%- endif%}
{%- endif %}
| `message`  | **string**<br>具体描述请示错误的原因。 |

## 错误码清单

| 错误码 | 错误消息 |
| ---- | ------------- |
{{ page_title | list_error }}
