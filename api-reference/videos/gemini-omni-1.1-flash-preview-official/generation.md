> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini Omni 1.1 视频生成与编辑

> 使用官方 Gemini Omni 1.1 Flash Preview 生成 3-10 秒视频, 支持四种分辨率

通过 `model` 指定 `gemini-omni-1.1-flash-preview-official`. 这是预览模型, 支持文生视频, 图生视频, 参考图生成和视频编辑.

> 💡 **提示**
>
> 中国大陆用户可将示例域名替换为 `https://toapis.cn`.
## 参数

`Authorization: Bearer YOUR_API_KEY`

| 字段              | 说明                                                                              |
| --------------- | ------------------------------------------------------------------------------- |
| `model`         | `gemini-omni-1.1-flash-preview-official`                                        |
| `prompt`        | 必填. 描述需要生成或编辑的内容.                                                               |
| `duration`      | 整数 3-10 秒, 默认 6 秒.                                                              |
| `resolution`    | 360p / 720p / 1080p / 4K, 默认 720p.                                              |
| `aspect_ratio`  | 16:9 / 9:16, 默认 16:9. 视频编辑时不发送此字段.                                              |
| `image_urls`    | 最多 10 张参考图 URL. 与输入视频互斥.                                                        |
| `video_list`    | 最多 3 项, 每项包含 video\_url. 输入视频支持 MP4/MOV, 每项最大 50 MiB.                           |
| `metadata.task` | 可选: text\_to\_video / image\_to\_video / reference\_to\_video / edit. 省略时由模型判断. |

先使用上传接口取得媒体 URL. 不接受 Veo 专属参数, 例如 generateAudio, negativePrompt 和 seed. 视频输入请使用 video\_list.

## 计费

USD, 输出按请求秒数计费. 输入视频按服务端探测时长逐个向上取整为秒后另计 \$0.006950/秒. 以下为基础售价, 分组或账户折扣以报价为准.

| 输出分辨率 |       每秒价格 |
| ----- | ---------: |
| 360p  | \$0.027034 |
| 720p  | \$0.081088 |
| 1080p | \$0.121632 |
| 4K    | \$0.243264 |

## 请求示例

```bash 
curl https://toapis.com/v1/videos/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-omni-1.1-flash-preview-official",
    "prompt": "A red paper boat floating on a calm lake at sunrise",
    "duration": 3,
    "resolution": "360p",
    "aspect_ratio": "16:9"
  }'
```

```json 
{
  "model": "gemini-omni-1.1-flash-preview-official",
  "prompt": "Change the sky to a warm sunset",
  "duration": 6,
  "resolution": "1080p",
  "video_list": [{"video_url": "https://example.com/uploaded-video.mp4"}],
  "metadata": {"task": "edit"}
}
```

## 查询结果

提交后读取返回的任务 id, 使用统一任务查询接口获取状态及结果. 失败和完成状态以查询结果为准.

```bash 
curl https://toapis.com/v1/videos/generations/TASK_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```
