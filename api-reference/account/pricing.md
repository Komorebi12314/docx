> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 价格与实际费用

> 查询 API Key 可用价格，并从生成响应中读取已确认费用

> 💡 **提示**
>
> 中国大陆用户请使用 `https://toapis.cn` 作为 Base URL，并将下方示例中的 `https://toapis.com` 替换为 `https://toapis.cn`。


使用 `GET /v1/pricing` 查询当前 API Key 可用的图片和视频费率。响应已包含客户固定价或折扣，以及生效的分组价格。

该接口返回价格目录，不是某次生成请求的报价。它不会预留或锁定价格，也不会根据生成参数估算总费用。

## 身份验证

### `Authorization`

`string` · 必填

使用生成 API Key，格式为 `Bearer YOUR_API_KEY`。


## 查询参数

### `model`

`string`

精确模型 ID。不传时返回所有可用的图片和视频模型。


### `type`

`string`

按 `image` 或 `video` 筛选。


### `limit`

`integer` · 默认值：`100`

返回的模型数量，取值范围为 `1` 到 `100`。


### `after`

`string`

使用上一次响应中的 `next_after` 继续分页。


Seedance 地区版本使用不同的模型 ID。例如，通过 `model` 查询 `seedance-2-5`、`seedance-2-5-cn` 或 `seedance-2-5-global`。接口没有单独的地区参数。

### 请求示例

```bash cURL 
curl --request GET \
  --url 'https://toapis.com/v1/pricing?model=seedance-2-5' \
  --header 'Authorization: Bearer <token>'
```


### 响应示例

```json 200 
{
  "object": "list",
  "currency": "USD",
  "data": [
    {
      "id": "seedance-2-5",
      "type": "video",
      "prices": [
        {
          "group": "default",
          "conditions": {
            "resolution": "720p",
            "has_video_input": false
          },
          "charge_type": "per_token",
          "price_basis": "total_tokens",
          "unit": "1m_tokens",
          "unit_price": "4"
        }
      ]
    }
  ],
  "has_more": false,
  "next_after": ""
}
```


以上数值仅用于说明响应结构，请以当前 API Key 实际返回的价格目录为准。

## 价格字段

### `currency`

`string`

价格币种，当前为 `USD`。


### `object`

`string`

对象类型，固定为 `list`。


### `data`

`array`

可用模型列表。每个元素包含精确模型 `id`、模型 `type` 和零个或多个 `prices`。


### `has_more`

`boolean`

是否还有下一页。


### `next_after`

`string`

下一次请求使用的游标。`has_more` 为 `false` 时返回空字符串。


### `prices[].group`

`string`

该价格适用的路由分组。使用自动分组的 API Key 可能收到多个分组。


### `prices[].conditions`

`object`

价格成立的条件，包含影响计价的模型默认值。生成请求应与这些值匹配。


### `prices[].charge_type`

`string`

计费类型：`per_request`、`per_second` 或 `per_token`。


### `prices[].price_basis`

`string`

计费依据：`request`、`output_seconds`、`total_tokens` 或 `text_input_tokens`。


### `prices[].unit`

`string`

价格单位：`request`、`second` 或 `1m_tokens`。


### `prices[].unit_price`

`string`

以十进制字符串返回的 USD 生效单价。该价格已包含客户价格和分组倍率，不要再次乘以分组倍率。


价格还可能包含 `input_unit_price`、`input_image_unit_price`、`free_input_image_count`、`minimum_charge_usd` 或 `image_token_prices`。分时价格还可能包含 `pricing_period`、`pricing_timezone`、`pricing_schedule_version` 和 `pricing_peak_windows`。

图片 token 计价中的 `image_token_prices` 可包含 `text_input`、`cached_text_input`、`image_input`、`cached_image_input` 和 `image_output`。每项金额单位均为 USD/100 万 tokens。

目录只返回至少有一个已启用候选渠道与所列条件兼容的价格。该检查不会预留路由，也不会探测渠道实时健康状态。服务无法安全确认完整费率时，模型仍可能返回，但 `prices` 为空。空数组或缺少某项价格不代表模型免费。

## 实际费用字段

费用可以确认时，生成响应使用以下对象：

```json 
{
  "billing": {
    "status": "settled",
    "credits": "100",
    "cost_usd": "0.5"
  }
}
```

| 字段         | 含义                               |
| ---------- | -------------------------------- |
| `status`   | `pending`、`settled` 或 `refunded` |
| `credits`  | 已确认消耗的 ToAPIs Credits，以十进制字符串返回  |
| `cost_usd` | 同一笔已确认费用的 USD 金额，以十进制字符串返回       |

`pending` 表示最终金额尚未确认，因此不返回金额字段。`refunded` 表示已确认净费用为零。缺少整个 `billing` 对象表示平台无法确认安全的公开值，不代表本次请求免费。

该对象可能出现在：

* 异步图片任务查询 `GET /v1/images/generations/{task_id}`
* 异步视频任务查询 `GET /v1/videos/generations/{task_id}`
* 任务 Webhook 的 `data.billing`
* 兼容的非流式同步图片生成或编辑响应顶层 `billing`

对于异步任务，任务完成后可将任务查询接口作为获取最终费用的兜底方式。流式图片响应、不支持的供应商响应格式、Playground 请求和延迟批量计费可能不返回该对象。

## 错误

| 状态码           | 错误码                     | 含义                            |
| ------------- | ----------------------- | ----------------------------- |
| `400`         | `invalid_request_error` | 查询参数不受支持，或 `type`、`limit` 无效  |
| `401` / `403` | 视情况而定                   | API Key 无效、过期、受限，或无权使用对应账户或分组 |
| `404`         | `model_not_found`       | 当前 API Key 无法使用该精确模型 ID       |
| `503`         | `pricing_unavailable`   | 无法安全加载客户价格，不会降级返回公开价          |

响应使用 `Cache-Control: private, no-store`。
