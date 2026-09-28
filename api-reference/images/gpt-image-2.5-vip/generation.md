> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# GPT-Image-2.5 VIP 图像生成与编辑

> gpt-image-2.5-flare-vip 和 gpt-image-2.5-sunburst-vip 异步图片任务接入指南, 支持六档质量, 像素尺寸, 透明背景和按实际 token 后付费

VIP 版通过 `POST /v1/images/generations` 创建图片任务, 返回任务 ID. 任务完成后通过查询接口获取图片 URL. VIP 版与普通版的共同点是都使用异步任务; 区别在模型名, size 格式和计价方式.

| 模型           | 请求中的 model                   |
| ------------ | ---------------------------- |
| Flare VIP    | `gpt-image-2.5-flare-vip`    |
| Sunburst VIP | `gpt-image-2.5-sunburst-vip` |

`gpt-image-2.5-vip` 是文档中的系列名称. 调用时请使用表中的完整模型名.

> 💡 **提示**
>
> 普通版同样使用异步任务, 但按分辨率计价并使用比例形式的 size, 请查看独立的 [GPT-Image-2.5 文档](../gpt-image-2.5/generation). VIP 版使用像素尺寸, 并按实际 token 结算.


中国大陆用户可将示例中的 `https://api.toapis.com` 替换为 `https://api.toapis.cn`. API Key 可在 [控制台](https://toapis.com/dashboard) 创建.

## 快速开始

将自己的 API Key 设置为环境变量 `TOAPIS_API_KEY`, 提交任务:

```bash 
curl --fail-with-body --request POST \
  --url https://api.toapis.com/v1/images/generations \
  --header "Authorization: Bearer $TOAPIS_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2.5-flare-vip",
    "prompt": "儿童绘本风格, 一位兽医用听诊器给小水獭检查心跳",
    "quality": "low",
    "size": "1024x1024",
    "n": 1
  }'
```

提交响应示例:

```json 
{
  "id": "tsk_img_example",
  "object": "generation.task",
  "model": "gpt-image-2.5-flare-vip",
  "status": "pending",
  "progress": 0,
  "created_at": 1788951900,
  "metadata": {}
}
```

保存返回的 `id`, 将下方的 `TASK_ID` 替换为该值后查询:

```bash 
curl --fail-with-body \
  --url https://api.toapis.com/v1/images/generations/TASK_ID \
  --header "Authorization: Bearer $TOAPIS_API_KEY"
```

任务可能经过 `pending`, `queued`, `in_progress`, 最终进入 `completed` 或 `failed`. `completed` 时从 `result.data` 读取图片 URL, `failed` 时读取 `error`. 建议每隔数秒查询一次. 完整字段见 [图片任务状态接口](../../tasks/image-status).

提交成功表示任务已创建. 请等到 `completed` 后再下载图片; 等待期间继续查询同一个任务 ID. 高质量请求耗时较长, 请保持轮询, 不要重复提交.

## 生成请求参数

### `Authorization`

`string` · 必填

使用 `Bearer YOUR_TOAPIS_API_KEY` 认证.


### `model`

`string` · 必填

`gpt-image-2.5-flare-vip` 或 `gpt-image-2.5-sunburst-vip`.


### `prompt`

`string` · 必填

图片描述. 编辑时描述需要保留和修改的内容.


### `quality`

`string` · 默认值：`high`

支持 `auto`, `low`, `medium`, `high`, `xhigh`, `max` 六档, 默认 `high`. 使用小写值. `auto` 表示由上游模型为每个请求自动选择质量档位.

quality 影响生成质量和实际输出 token. 相同 quality 的图片也可能因尺寸和内容不同而产生不同费用.


### `size`

`string` · 默认值：`1024x1024`

输出像素尺寸, 使用 `宽x高` 格式. 例如 `1024x1024`, `1536x1024`, `1024x1536`, `1280x1024`.

支持上游允许的自定义像素尺寸, 不限于上述示例. 合法尺寸范围以接口校验为准. VIP 示例不使用 `1:1` 这样的比例值, 也不需要额外传入 resolution.


### `background`

`string`

可选的背景参数. 传入 `"transparent"` 生成透明背景图片, 不传此参数时正常生图.

文生图和参考图编辑均可使用. 普通生图请直接省略此字段.


### `n`

`integer` · 默认值：`1`

每次请求使用 `1`, 生成一张图片.


### `reference_images`

`string[]`

可选的参考图 URL 列表, 用于图生图. 图片地址需要能被服务端访问. 本接口只支持图片 URL, 不支持本地文件上传或 base64; 本地图片请先通过 [上传图片接口](../../uploads/images) 获取 URL.

也兼容 `image_urls`. 选择其中一个字段即可. 生成接口传入参考图 URL 时按图生图处理.


## 透明背景

生成请求中加入 `"background": "transparent"` 即可得到透明背景的图片. 不传该字段时正常生图.

```bash 
curl --fail-with-body --request POST \
  --url https://api.toapis.com/v1/images/generations \
  --header "Authorization: Bearer $TOAPIS_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2.5-flare-vip",
    "prompt": "一个红色圆形贴纸, 背景透明",
    "quality": "low",
    "size": "1024x1024",
    "background": "transparent",
    "n": 1
  }'
```

提交后同样通过任务 ID 查询, 从 `result.data` 读取图片 URL.

## 参考图编辑

编辑使用 `POST /v1/images/edits`, 请求为 `multipart/form-data`. 异步编辑只支持图片 URL, 将 URL 放在 `image` 字段中, 同时传入 `model`, `prompt`, `quality`, `size` 和 `n`. 不支持本地文件上传或 base64. 编辑同样是异步任务, 提交后返回任务 ID, 查询方式与生成相同.

下例使用 Sunburst VIP, 给参考图中的小水獭增加黄色围巾. 请将示例 URL 替换为自己的图片 URL:

```bash 
curl --fail-with-body --request POST \
  --url https://api.toapis.com/v1/images/edits \
  --header "Authorization: Bearer $TOAPIS_API_KEY" \
  --form 'model=gpt-image-2.5-sunburst-vip' \
  --form 'prompt=保留原图中的小水獭和兽医, 给小水獭增加一条黄色围巾' \
  --form 'image=https://example.com/otter.png' \
  --form 'quality=low' \
  --form 'size=1024x1024' \
  --form 'n=1'
```

让 curl 自动设置 multipart 的 Content-Type 和 boundary. 使用响应中的任务 ID 轮询查询接口, 从 `result.data` 读取编辑后的图片 URL.

Flare VIP 也支持同样的编辑方式, 将 model 改为 `gpt-image-2.5-flare-vip` 即可. 参考图输入会产生图片输入 token 费用.

## token 价格

以下为 2026-09-09 核对的标准价格, 两个 VIP 模型相同, 按官方 token 单价的 8 折计费:

| 类型     | USD/百万 token |
| ------ | -----------: |
| 文本输入   |         4.00 |
| 缓存文本输入 |         1.00 |
| 图片输入   |         6.40 |
| 缓存图片输入 |         1.60 |
| 图片输出   |        24.00 |

六档 quality 共用上述 token 单价. VIP 没有按 quality 固定的每张价格, 任务完成后按实际用量结算. 提交任务时会先预扣, 完成后按实际文本和图片 token 结算, 多退少补. 调用前仍需有足够的账户余额和 API Key 额度.

费用公式, 单位为 USD:

```text 
费用 = (
  未缓存文本输入 token * 4
  + 缓存文本输入 token * 1
  + 未缓存图片输入 token * 6.4
  + 缓存图片输入 token * 1.6
  + 图片输出 token * 24
) / 1,000,000
```

例如一次 `low` 质量的 1024x1024 文生图包含 27 个文本输入 token 和 196 个图片输出 token, 费用为:

```text 
(27 * 4 + 196 * 24) / 1,000,000 = $0.004812
```

一次参考图编辑实测包含 21 个文本输入 token, 1024 个图片输入 token 和 196 个图片输出 token. 公式金额为 $0.0113416, 按平台额度最小单位舍入后实扣 $0.011342. 这些是具体请求的示例, 不代表同一质量下每张图的固定费用.

账户专属定价或折扣可能不同, 最新价格以 [模型定价页](https://toapis.com/pricing) 和账户实际配置为准. 最终扣费可在使用日志中核对.

## 从普通版切换

1. 将完整模型名改为对应的 `-vip` 模型名.
2. 将 size 从比例改为像素尺寸, 并省略 resolution.
3. 文生图和参考图编辑都通过任务 ID 轮询结果, 从 `result.data` 读取图片 URL.
4. 参考图编辑改用 `/v1/images/edits` 并传入图片 URL.
5. 按实际 token 预估费用.

普通版的任务提交和查询示例见 [GPT-Image-2.5 文档](../gpt-image-2.5/generation).
