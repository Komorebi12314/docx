> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# seedance-2.5 视频生成

> 使用 seedance-2-5 模型生成视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


Seedance 2.5 的公共模型名为 `seedance-2-5`，火山引擎上游模型 ID 为 `doubao-seedance-2-5-260628`。

* 支持文生视频、首帧/首尾帧图生视频、视频编辑、视频延长和多模态参考生视频。
* 支持图片、视频、音频参考，也支持纯音频参考。
* 接口为异步任务：提交后返回 `generation.task`，完成后通过任务状态接口获取视频。

## Authorizations

### `Authorization`

`string` · 必填

所有请求都需要 Bearer Token。请在 [API Key 管理页面](https://toapis.com/console/token) 获取密钥，并在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填 · 默认值：`seedance-2-5`

ToAPIs 公共模型名，固定使用 `seedance-2-5`。


### `private_asset_review`

`boolean` · 默认值：`false`

可选, 默认 `false`. 设为 `true` 时按所选渠道能力准备并审核素材; 不支持私有素材库的渠道跳过提审, 沿用原有生成流程.

仅用于包含以下媒体字段的异步生成请求: `image_urls`, `image_with_roles`, `video_with_roles`, `audio_with_roles`.

纯文本或仅在 metadata 中提供素材的请求请省略或设为 `false`. 不适用于独立的 remix 或 extend 接口. 设为 `true` 时拒绝 `asset://`, 模型原有的媒体格式和数量限制不变. 详见[按需素材审核](../private-assets).

本接口的 `video_operation=edit` 或 `video_operation=extend` 可以使用此开关, 仍需满足对应的素材和时长要求.


### `prompt`

`string`

描述场景、镜头运动、主体动作、风格和声音氛围。引用素材时使用“图片1”“视频1”“音频1”等标签。


### `video_operation`

`string` · 默认值：`generate`

视频业务类型，可选 `generate`、`edit` 或 `extend`。编辑和延长至少需要一个 `video_with_roles`；编辑使用 `duration=-1`，延长使用 `4`–`30` 或 `-1`。三种操作共用本接口。


### `client_business_id`

`string`

客户侧订单号或业务任务 ID。提交后会随任务保存，也可用 `GET /v1/videos/generations/{client_business_id}` 查询。


### `duration`

`integer`

输出视频时长（秒），范围为 `4`–`30`；`-1` 表示由模型自动选择时长。编辑任务只能使用 `-1`，输出时长与输入视频基本一致；延长任务可使用 `4`–`30` 或 `-1`，此时按延长后的输出总时长计算。


### `aspect_ratio`

`string`

可选：`21:9`、`16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`adaptive`。

编辑、视频延长和首尾帧任务按上游要求使用 `adaptive`；也可让输入素材决定比例。


### `image_urls`

`string[]`

兼容模式的图片 URL 数组。新接入建议使用 `image_with_roles` 明确每张图的用途；两个字段不能同时传。


### `image_with_roles`

`array`

带角色的图片数组，每项包含必填 `url` 和 `role`。角色可为 `first_frame`、`last_frame` 或 `reference_image`。最多 30 张图片；首尾帧模式与参考图模式不能混用。


### `video_with_roles`

`array`

参考视频数组，每项包含必填 `url`，角色固定为 `reference_video`。最多 10 段视频。


### `audio_with_roles`

`array`

参考音频数组，每项包含必填 `url`，角色固定为 `reference_audio`。最多 10 段音频，也支持纯音频参考。


### `resolution`

`string`

分辨率：`480p`、`720p` 或 `1080p`。


### `output_format`

`string` · 默认值：`mp4`

支持 `mp4` 和 `mov`。


### `generate_audio`

`boolean` · 默认值：`true`

是否生成同步音频。


### `return_last_frame`

`boolean` · 默认值：`false`

是否在完成结果中返回生成视频的尾帧图片。


### `tools`

`array`

可选工具：`[{ "type": "web_search" }]`。仅适用于纯文生视频，不能与图片、视频或音频输入同时使用。


### `callback_url`

`string`

ToAPIs 任务完成回调地址，详见[任务 Webhook](/docs/cn/api-reference/webhooks/task-webhooks)。


### `trace_id`

`string`

调用方自定义的链路追踪 ID。


## 参考素材限制

总计最多 50 个参考素材：图片 30 张、视频 10 段、音频 10 段。请使用显式角色，避免首帧/尾帧与参考素材被错误推断。

> ⚠️ **注意**
>
> 非法任务组合可能失败。编辑和延长任务会显式指定上游任务类型，特殊限制不符合时在提交阶段立即返回错误；其余任务类型由模型按素材和提示词判断，不符合时在异步阶段失败并返回 `InvalidParameter.TaskTypeConstraint`。编辑、延长和首尾帧任务按上游要求将 `aspect_ratio` 设为 `adaptive`。


## Response
- **`id`**（`string`） — 任务 ID，用于查询状态。
- **`client_business_id`**（`string`） — 请求传入该字段时返回。
- **`object`**（`string`） — 固定为 `generation.task`。
- **`model`**（`string`） — 本次请求的模型名。
- **`status`**（`string`） — `queued`、`in_progress`、`completed` 或 `failed`。
- **`progress`**（`integer`） — `0`–`100` 的任务进度。
- **`created_at`**（`integer`） — 创建时间戳。
### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "seedance-2-5",
    "prompt": "电影感产品特写，镜头缓慢推进，保留自然室内声音。",
    "duration": 10,
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "generate_audio": true
  }'
```

```json 多模态参考请求 
{
  "model": "seedance-2-5",
  "prompt": "使用图片1中的人物、视频1的运镜和音频1的节奏。",
  "duration": 12,
  "aspect_ratio": "16:9",
  "image_with_roles": [{"url": "https://example.com/ref.png", "role": "reference_image"}],
  "video_with_roles": [{"url": "https://example.com/motion.mp4", "role": "reference_video"}],
  "audio_with_roles": [{"url": "https://example.com/rhythm.mp3", "role": "reference_audio"}]
}
```

```json 视频延长请求 
{
  "model": "seedance-2-5",
  "prompt": "向后延长视频1，镜头继续推进并展示窗外的城市。",
  "video_operation": "extend",
  "duration": 11,
  "aspect_ratio": "adaptive",
  "output_format": "mov",
  "video_with_roles": [{"url": "https://example.com/source.mov", "role": "reference_video"}]
}
```


### 响应示例

```json 200 
{
  "id": "tsk_vid_xxx",
  "object": "generation.task",
  "model": "seedance-2-5",
  "status": "in_progress",
  "progress": 10,
  "created_at": 1781577600
}
```

