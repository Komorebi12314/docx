> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini 3 Pro Image Official 图像生成

> Gemini 3 Pro Image Official 支持文生图和图生图, 最多 14 张参考图.

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 版本选择

| 版本                                                    | 参考图上限 | 适用场景          |
| ----------------------------------------------------- | ----- | ------------- |
| [普通版](../gemini-3-pro-image/generation)               | 6 张   | 文生图和少量参考图编辑   |
| [VIP](../gemini-3-pro-image-vip/generation)           | 14 张  | 需要更多参考图的编辑和组合 |
| [Official](../gemini-3-pro-image-official/generation) | 14 张  | 需要原生生成参数控制    |

参考图数量指输入图片总数, 不代表输出图片数量. 三个版本使用不同的模型 ID, 请按对应页面的参数和示例调用.

## 当前版本

使用 `model: "gemini-3-pro-image-official"` 选择 Official, 支持文生图和最多 14 张参考图的图生图或图像编辑.
通过 Google Vertex AI 调用, 支持 `temperature`, `topP`, `thinkingConfig`, `safetySettings` 等原生扩展参数, 具体字段见下方说明.
请求异步执行, 提交成功后通过任务 ID 查询结果.

> ⚠️ **注意**
>
> `image_urls` 仅支持图片 URL, 不直接接收 base64. 请先使用 [上传图片接口](../../uploads/images) 获取可访问的 URL.


## 认证

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## 请求参数

### `model`

`string` · 必填 · 默认值：`gemini-3-pro-image-official`

图像生成模型名称

示例: `"gemini-3-pro-image-official"`


### `prompt`

`string` · 必填

图像生成的文本描述


### `size`

`string`

图像宽高比

支持的格式：

* `1:1` - 正方形
* `3:2` / `2:3`
* `3:4` / `4:3`
* `4:5` / `5:4`
* `9:16` / `16:9`
* `21:9`


### `n`

`integer` · 默认值：`1`

生成图像的数量

固定为 1


### `image_urls`

`string[]`

参考图像 URL 数组，用于图生图或图像编辑

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图片 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 最多 14 张图片
* 单张图片不得超过 10MB
* 支持格式：.jpeg, .jpg, .png, .webp


### `metadata`

`object`

Vertex AI 原生扩展参数

<details>
<summary>显示 metadata 字段</summary>

**`temperature`** — `number`

生成温度，控制输出的随机性

取值范围：`0.0` - `2.0`


**`topP`** — `number`

Top-P 采样参数

取值范围：`0.0` - `1.0`，默认 `0.95`


**`maxOutputTokens`** — `integer`

最大输出 token 数

默认 `32768`


**`resolution`** — `string`

输出图像分辨率，后端自动映射为 Vertex AI 原生 imageSize

可选值：`1K`、`2K`、`4K`，默认 `1K`


**`personGeneration`** — `string`

人物生成控制

可选值：

* `ALLOW_ALL` - 允许生成所有人物（包括成人和儿童）
* `ALLOW_ADULT` - 仅允许生成成人
* `ALLOW_NONE` - 禁止生成人物


**`imageOutputOptions`** — `object`

图像输出格式配置

<details>
<summary>imageOutputOptions 字段</summary>

**`mimeType`** — `string`

输出图像格式

可选值：`image/png`、`image/jpeg`、`image/webp`


**`compressionQuality`** — `integer`

压缩质量（仅 JPEG 有效）


**`thinkingConfig`** — `object`

思考模式配置，启用后模型会先进行推理再生成图像，适合复杂场景

<details>
<summary>thinkingConfig 字段</summary>

**`thinkingBudget`** — `integer`

思考 token 预算，控制模型思考的深度

取值范围：`0` - `24576`，默认由模型自动决定


**`thinkingLevel`** — `string`

思考级别

可选值：`LOW`、`MEDIUM`、`HIGH`、`MINIMAL`


**`safetySettings`** — `array`

安全设置数组，控制内容安全过滤级别

<details>
<summary>safetySettings 元素</summary>

**`category`** — `string`

安全类别

可选值：`HARM_CATEGORY_HATE_SPEECH`、`HARM_CATEGORY_DANGEROUS_CONTENT`、`HARM_CATEGORY_SEXUALLY_EXPLICIT`、`HARM_CATEGORY_HARASSMENT`


**`threshold`** — `string`

过滤阈值

可选值：`OFF`、`BLOCK_LOW_AND_ABOVE`、`BLOCK_MEDIUM_AND_ABOVE`、`BLOCK_ONLY_HIGH`


## 响应字段

### `id`

`string`

任务唯一标识符，用于查询任务状态


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的模型名称


### `status`

`string`

任务状态

* `queued` - 排队等待处理
* `in_progress` - 处理中
* `completed` - 成功完成
* `failed` - 失败


### `progress`

`integer`

任务进度百分比（0-100）


### `created_at`

`integer`

任务创建时间戳（Unix 时间戳）


### `metadata`

`object`

任务元数据


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gemini-3-pro-image-official",
    "prompt": "未来城市的天际线，霓虹灯光，赛博朋克风格",
    "size": "16:9",
    "n": 1,
    "metadata": {
      "temperature": 1.0,
      "topP": 0.95,
      "resolution": "2K",
      "personGeneration": "ALLOW_ALL",
      "thinkingConfig": {
        "thinkingLevel": "HIGH"
      }
    }
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "gemini-3-pro-image-official",
        "prompt": "未来城市的天际线，霓虹灯光，赛博朋克风格",
        "size": "16:9",
        "n": 1,
        "metadata": {
            "temperature": 1.0,
            "topP": 0.95,
            "resolution": "2K",
            "personGeneration": "ALLOW_ALL",
            "thinkingConfig": {
                "thinkingLevel": "HIGH"
            }
        }
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gemini-3-pro-image-official',
    prompt: '未来城市的天际线，霓虹灯光，赛博朋克风格',
    size: '16:9',
    n: 1,
    metadata: {
      temperature: 1.0,
      topP: 0.95,
      resolution: '2K',
      personGeneration: 'ALLOW_ALL',
      thinkingConfig: {
        thinkingLevel: 'HIGH'
      }
    }
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "task_img_abc123def456",
  "object": "generation.task",
  "model": "gemini-3-pro-image-official",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```


## 查询结果

提交响应中的 `id` 是任务 ID. 使用 [图片任务查询接口](../../tasks/image-status) 获取状态和最终图片.
任务查询和 [Webhook 回调](../../webhooks/task-webhooks) 沿用通用异步图片接口约定.
