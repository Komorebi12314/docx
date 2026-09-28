> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# GPT-Image-2.5 官方渠道 图像生成

> Sunburst 和 Flare 官方渠道的异步图片任务, R2 结果和官方 8 折 token 计费

通过 Azure 官方渠道调用两个 GPT-Image-2.5 型号. 提交后立即返回异步任务 ID, 后台生成图片并将结果转存到 R2.

| 型号                | model                             |
| ----------------- | --------------------------------- |
| Sunburst Official | `gpt-image-2.5-sunburst-official` |
| Flare Official    | `gpt-image-2.5-flare-official`    |

调用时必须使用表中的完整模型名. `gpt-image-2.5-official` 只是系列名称, 不能作为请求的 model.

中国大陆用户可将示例中的 `https://api.toapis.com` 替换为 `https://api.toapis.cn`. 在 [控制台](https://toapis.com/console/token) 创建 API Key, 并设置环境变量 `TOAPIS_API_KEY`.

## 提交和查询

提交一张 Flare 图片. 调用 Sunburst 时替换 model 即可:

```bash 
curl --fail-with-body --request POST \
  --url https://api.toapis.com/v1/images/generations \
  --header "Authorization: Bearer $TOAPIS_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2.5-flare-official",
    "prompt": "A small blue circle on a plain white background",
    "quality": "low",
    "size": "1024x1024",
    "n": 1
  }'
```

```json 
{
  "id": "tsk_img_example",
  "object": "generation.task",
  "model": "gpt-image-2.5-flare-official",
  "status": "pending",
  "progress": 0,
  "created_at": 1789099098,
  "metadata": {}
}
```

保存提交响应的 `id`, 将下方 `TASK_ID` 替换为该值:

```bash 
curl --fail-with-body \
  --url https://api.toapis.com/v1/images/generations/TASK_ID \
  --header "Authorization: Bearer $TOAPIS_API_KEY"
```

提交响应为 `pending`. 查询时可能看到 `queued` 或 `in_progress`, 最终为 `completed` 或 `failed`. `completed` 时从 `result.data[].url` 获取已转存 R2 的图片 URL, `failed` 时读取 `error`. 建议每隔数秒查询同一个任务 ID; 高质量生成可能需要数分钟, 等待期间不要重复提交. 完整字段见 [图片任务状态接口](../../tasks/image-status).

## 请求参数

### `Authorization`

`string` · 必填

使用 ToAPIs API Key, 格式为 `Bearer YOUR_API_KEY`. 无需提供 Azure 凭据.


### `model`

`string` · 必填

`gpt-image-2.5-sunburst-official` / `gpt-image-2.5-flare-official`.


### `prompt`

`string` · 必填

图片描述. 使用参考图时描述希望保留和修改的内容.


### `quality`

`string` · 默认值：`high`

支持 `auto`, `low`, `medium`, `high`, `xhigh`, `max` 六档. `auto` 表示由上游模型为每个请求自动选择质量档位. 质量和尺寸会影响实际 token 用量与耗时.


### `size`

`string` · 默认值：`1024x1024`

使用像素尺寸, 例如 `1024x1024`, `1536x1024` 或 `1024x1536`. 自定义尺寸须满足上游校验. 以下示例不需要额外传入 resolution.


### `background`

`string`

可选. 传入 `transparent` 请求透明背景, 省略时使用上游默认背景. 默认 PNG 输出可保留透明通道.


### `n`

`integer` · 默认值：`1`

当前 official 渠道每次请求固定生成一张图片, 使用 `1`.


## 参考图 URL

需要图生图时, 在同一个 JSON 生成请求中添加 `image_urls`. URL 必须可由服务端访问. 可先使用 [图片上传接口](../../uploads/images) 获取 URL. 参考图产生图片输入 token 费用, 提交和查询仍使用同一套异步流程.

```bash 
curl --fail-with-body --request POST \
  --url https://api.toapis.com/v1/images/generations \
  --header "Authorization: Bearer $TOAPIS_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2.5-sunburst-official",
    "prompt": "Keep the subject and replace the background with a snowy forest",
    "image_urls": ["https://example.com/reference.png"],
    "quality": "high",
    "size": "1024x1024",
    "n": 1
  }'
```

## token 价格

2026-09-11 核对的标准售价如下. 两个 official 型号均按官方 token 价格的 80% 计费, 即官方 8 折:

| 类型     | USD / 1,000,000 tokens |
| ------ | ---------------------: |
| 文本输入   |                   4.00 |
| 缓存文本输入 |                   1.00 |
| 图片输入   |                   6.40 |
| 缓存图片输入 |                   1.60 |
| 图片输出   |                  24.00 |

提交时先预扣额度, 成功后按上游实际文本和图片 token 用量多退少补. 六档质量共用上述单价, 没有按质量固定的每张价格. 调用前需要足够的账户余额和 API Key 额度.

费用公式, 单位为 USD:

```text 
USD = (
  uncached_text_input_tokens * 4
  + cached_text_input_tokens * 1
  + uncached_image_input_tokens * 6.4
  + cached_image_input_tokens * 1.6
  + image_output_tokens * 24
) / 1,000,000
```

例如一次请求使用 17 个未缓存文本输入 tokens 和 196 个图片输出 tokens, 费用为 `(17 * 4 + 196 * 24) / 1,000,000 = $0.004772`. 这不是每张图片的固定价格.

账户专属定价或折扣继续适用. 最终扣费可在使用日志中核对, 最新售价以 [定价页](https://toapis.com/pricing) 和账户配置为准.

## 相关型号

[普通版](../gpt-image-2.5/generation) 和 [VIP 版](../gpt-image-2.5-vip/generation) 使用各自的完整模型名. 调用本页官方渠道时请使用 `-official` 后缀.
