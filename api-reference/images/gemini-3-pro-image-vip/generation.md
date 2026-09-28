> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini 3 Pro Image VIP 图像生成

> Gemini 3 Pro Image VIP 支持文生图和图生图, 最多 14 张参考图.

> 💡 **提示**
>
> 中国大陆用户请使用 `https://toapis.cn` 作为 Base URL, 替换示例中的 `https://toapis.com`.


## 版本选择

| 版本                                                    | 参考图上限 | 适用场景          |
| ----------------------------------------------------- | ----- | ------------- |
| [普通版](../gemini-3-pro-image/generation)               | 6 张   | 文生图和少量参考图编辑   |
| [VIP](../gemini-3-pro-image-vip/generation)           | 14 张  | 需要更多参考图的编辑和组合 |
| [Official](../gemini-3-pro-image-official/generation) | 14 张  | 需要原生生成参数控制    |

参考图数量指输入图片总数, 不代表输出图片数量. 三个版本使用不同的模型 ID, 请按对应页面的参数和示例调用.

## 当前版本

使用 `model: "gemini-3-pro-image-preview-vip"` 选择 VIP, 支持文生图和最多 14 张参考图的图生图或图像编辑.
适合需要 7 到 14 张参考图的编辑或多图组合. 多图请求可按列表顺序说明各张图片的用途.
请求异步执行, 提交成功后通过任务 ID 查询结果.

> ⚠️ **注意**
>
> `image_urls` 仅支持图片 URL, 不直接接收 base64. 请先使用 [上传图片接口](../../uploads/images) 获取可访问的 URL.


## 认证

### `Authorization`

`string` · 必填

使用 `Bearer YOUR_API_KEY` 认证. API Key 可在 [控制台](https://toapis.com/dashboard/tokens) 创建.


## 请求参数

### `model`

`string` · 必填 · 默认值：`gemini-3-pro-image-preview-vip`

固定使用 `gemini-3-pro-image-preview-vip`. 普通模型名和其他别名不会自动切换到本 VIP 路由.


### `prompt`

`string` · 必填

描述需要生成或编辑的图像. 传入多张参考图时, 可按列表顺序说明各图的用途.


### `size`

`string`

图像宽高比, 例如 `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.


### `n`

`integer` · 默认值：`1`

每次请求生成 1 张图片. 使用数字 `1`, 不要使用字符串 `"1"`.


### `image_urls`

`object[]`

可选参考图列表, 最多 14 张. 文生图时省略本字段.
先用 [上传图片接口](../../uploads/images) 获取可访问的图片 URL, 不直接传入 base64.

<details>
<summary>参考图字段</summary>

**`url`** — `string` · 必填

可公开访问的 HTTP 或 HTTPS 图片 URL.


示例: `[{"url": "https://example.com/reference-1.png"}, {"url": "https://example.com/reference-2.png"}]`.
14 张是输入参考图上限, 不是一次请求的输出图片数量.


### `metadata`

`object`

<details>
<summary>输出分辨率</summary>

**`resolution`** — `string` · 默认值：`2K`

支持 `1K`, `2K`, `4K`. 省略时使用 `2K`.


## 请求示例

```bash 
curl --request POST 'https://toapis.com/v1/images/generations' \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gemini-3-pro-image-preview-vip",
    "prompt": "保留第一张图的人物, 采用第二张图的背景和配色, 生成一张自然光肖像.",
    "size": "1:1",
    "n": 1,
    "image_urls": [
      {"url": "https://example.com/reference-1.png"},
      {"url": "https://example.com/reference-2.png"}
    ],
    "metadata": {"resolution": "2K"}
  }'
```

将示例 URL 替换为实际可访问的参考图地址. 可继续添加参考图, 但列表总数不得超过 14.
文生图请求只需移除 `image_urls`, 并修改提示词.

## 查询结果

提交响应中的 `id` 是任务 ID. 使用 [图片任务查询接口](../../tasks/image-status) 获取状态和最终图片.
任务查询和 [Webhook 回调](../../webhooks/task-webhooks) 沿用通用异步图片接口约定.
