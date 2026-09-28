> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 生成视频时按需审核素材

> 通过 private_asset_review 按所选渠道自动处理素材审核, 并在同一个任务中生成视频

在视频生成请求中设置 `private_asset_review: true`, 平台会按正常规则选择渠道. 支持私有素材库的渠道会先准备并审核素材, 不支持的渠道跳过这一环节, 继续按原有方式处理媒体并生成视频. 不需要自行判断渠道能力, 重复列出素材, 单独查询审核接口.

> 💡 **提示**
>
> 本方式用于带媒体输入的异步视频生成请求, 不限于 Seedance. 平台需启用此功能; 纯文本请求, 同步接口以及独立的视频 remix 和 extend 接口不适用. 模型的媒体要求和渠道可用性规则不变. 跳过私有素材提审不代表跳过供应商自身的内容审核. 中国大陆用户可将示例中的 `https://toapis.com` 替换为 `https://toapis.cn`.


## 请求方式

继续调用 `POST /v1/videos/generations`. 图片, 视频和音频仍放在原有输入字段中, 只需增加布尔开关.

下面以 Seedance 2 为例. 使用其他模型时, 请按对应模型文档选择媒体字段和生成参数, 再添加 `private_asset_review: true`.

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "seedance-2",
    "client_business_id": "avatar-demo-001",
    "prompt": "Animate the character in image 1 using the movement in video 1.",
    "duration": 5,
    "aspect_ratio": "16:9",
    "image_with_roles": [
      {"url": "https://files.example.com/avatar.jpg", "role": "reference_image"}
    ],
    "video_with_roles": [
      {"url": "https://files.example.com/motion.mp4", "role": "reference_video"}
    ],
    "private_asset_review": true
  }'
```

将示例中的地址换成自己的公网 URL. 需要提审时, 下列提审字段中实际选用的素材必须全部通过, 不能只选择其中一部分. 原有模型数量限制和角色校验不变.

| 字段                     | 类型      | 说明                                                     |
| ---------------------- | ------- | ------------------------------------------------------ |
| `private_asset_review` | boolean | 可选, 默认 `false`. 设为 `true` 启用按需审核; 不传或设为 `false` 保留原有行为 |

私有素材提审使用以下字段. 不需要提审的渠道继续使用模型原有的媒体字段和限制:

图片按 `image_with_roles[].url` > `reference_images` > `image_urls` > `images` > `image` 选择第一个非空字段, 不合并这些字段. 原来禁止字段混用的模型仍会报错. 不扫描提示词或 metadata, 也不让原本忽略的输入字段生效.

| 素材类型    | 视频输入字段                   | 角色                                              |
| ------- | ------------------------ | ----------------------------------------------- |
| `image` | `image_with_roles[].url` | `first_frame`, `last_frame` 或 `reference_image` |
| `video` | `video_with_roles[].url` | `reference_video`                               |
| `audio` | `audio_with_roles[].url` | `reference_audio`                               |

原模型支持的 `video_list` 可以继续使用, 也可以作为唯一媒体输入, 例如 Kling Omni 和 Gemini Omni 1.1 的参考视频请求. 此字段不纳入上述私有素材提审范围, 仍按对应模型规则处理. 开关不会让模型原本不支持的字段或格式生效.

上述提审字段中的 HTTP(S) URL 去除首尾空格后用于匹配, 最多 2048 个 UTF-8 字节, 不得内嵌用户名或密码. 同一 URL 同类型重复输入会复用, 类型冲突则报错. 图片也支持纯 Base64 或 `data:image/...;base64,...`; 需要提审时, 平台校验解码内容后转存再审核. 跳过提审的渠道按原模型规则处理 URL 或 Base64, 不会因此获得新的格式支持. 上述视频和音频字段只接受 HTTP(S). 不接受本地路径; 也可先[上传图片](../uploads/images)获取 URL.

按需转存要求文件非空, 图片不超过 20 MiB, 视频和音频不超过 100 MiB; 模型或审核服务还可能有更严格的格式, 时长和大小限制. 上面的上传入口适用于图片, 本地视频和音频分别使用[上传视频](../uploads/videos)和[上传音频](../uploads/audios).

## 等待和查询结果

1. 请求受理后返回视频任务, 不会保持 HTTP 连接等待整个审核过程. 返回任务不代表素材已通过或视频已经开始生成.
2. 支持素材库的渠道会检查可复用记录. 没有可用记录时, 平台自动准备并审核素材. 同一用户, 素材来源和渠道的并发请求共用准备过程, 避免重复准备和提审.
3. 本轮需要提审的素材全部通过后才提交视频生成. 首次准备可能持续数分钟; 命中可用记录会跳过重复审核. 不支持素材库的渠道直接走原有媒体处理和生成流程. 视频仍然异步生成.

使用返回的任务 ID, 或请求中的 `client_business_id`, 查询同一个视频任务:

```bash 
curl --request GET \
  --url https://toapis.com/v1/videos/generations/avatar-demo-001 \
  --header 'Authorization: Bearer YOUR_API_KEY'
```

沿用[视频任务状态](../tasks/video-status)和[任务 Webhook](../webhooks/task-webhooks). 审核等待期间可以保持 `queued`, 不需要调用旧素材状态接口. `completed` 才表示视频完成, `failed` 时查看 `error.message`.

当前默认每轮素材准备期限为 20 分钟, 从该轮开始准备计时, 不是每份素材各有 20 分钟, 也不包含后续视频生成耗时. 多份素材共用本轮期限; 平台配置可能调整, 切换渠道时会重新开始一轮准备. 素材被拒绝或准备超时会结束该视频任务, 不会继续提交视频.

首次审核未通过不会扣视频生成费用. 素材准备完成后按正常视频流程预占和结算; 复用记录或跳过私有素材提审都不改变模型的计价方式和默认参数.

## 复用, 重试和保留时间

* 后续请求仍传入素材并设置 `private_asset_review: true`, 无需保存素材 ID. 对于需要提审的渠道, 同用户同渠道下 URL 按完整地址匹配, Base64 图片按解码内容摘要匹配, 纯编码与 data URI 可复用同一记录. 不跨用户或渠道共享.
* 改了 URL 就按新的来源处理. 同一 URL 的内容发生变化时, 平台不会按文件内容重新识别, 请使用新的版本 URL.
* 需要提审时, 平台为各渠道保存独立副本. 当前默认清理策略以 60 天未使用为阈值, 实际保留期以平台配置为准. 通过旧素材接口管理的素材不受此清理策略影响. 视频提交被接受即算一次使用, 不必等最终生成成功. 清理后再次请求会重新准备, 所以来源 URL 仍应保持有效.
* 同一个业务请求的网络重试使用相同 `client_business_id`, 已存在的任务会回放, 不会因此新建一条视频任务. 要生成另一条视频或失败后重新尝试, 使用新的业务 ID. 不要因审核等待而连续创建新任务.
* 如果视频是否提交成功尚未确认, 保留原任务并继续查询或联系支持, 不要立即用新业务 ID 重发.

## 与旧素材接口并行使用

省略开关或设为 `false` 时, 旧的[虚拟人像素材接口](./seedance-2/private-avatar)及已有 `asset://` 引用保持原有行为. 设为 `true` 时, 媒体字段中出现任何 `asset://` 都返回 HTTP 400, 不查旧记录, 不复制或迁移历史素材.

此开关不改变模型能力或素材内容要求, 也不替代单独的[真人人像认证](./seedance-2/real-avatar). 此前方案中的 `private_assets` 字段不再接受, 请改用布尔字段 `private_asset_review`.

参数错误先检查开关类型, asset:// 引用, URL 或 Base64 格式. 来源下载失败检查访问权限和有效期. 功能未启用, 没有可用生成渠道或审核配置异常时, 联系平台处理; 已配置审核的渠道不会因配置错误而自动跳过审核.
