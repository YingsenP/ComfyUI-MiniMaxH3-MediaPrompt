# ComfyUI-MiniMaxH3-MediaPrompt

[English README](README.md)

本插件为 `MiniMaxH3ReferenceToVideo` 提供媒体提示词输入。

本插件现在只注册两个节点，旧版 MiniMax H3 加载与生成节点已停用。

## 工作流示例

![连接到 MiniMaxH3ReferenceToVideo 的 MiniMax H3 媒体提示词工作流](images/minimax-h3-media-prompt-workflow.png)

## 安装

将 [YingsenP/ComfyUI-MiniMaxH3-MediaPrompt](https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt) 仓库克隆到 `ComfyUI/custom_nodes`，然后重启 ComfyUI：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt.git
```

## 必需依赖

快速创建视频功能依赖 `Load Video (Upload)` 节点。使用此功能前，请先安装 [ComfyUI-VideoHelperSuite](https://github.com/kosinkadink/ComfyUI-VideoHelperSuite)。

## MiniMax H3 Media Prompt

- 一个可接入图片、视频和音频的 `Media` 输入端；
- 最多接入 9 张图片、3 个视频和 3 个独立音频；
- 从 `Media` 端口快速创建视频时使用 VideoHelperSuite 的 `Load Video (Upload)`；
- VHS 的 `IMAGE` 帧输出和 `AUDIO` 输出会自动作为同编号的视频与视频音轨配对；
- 不要给 VHS 加载节点连接可选 `VAE`，MiniMax 参考视频需要 `IMAGE` 帧批次而不是 `LATENT`；
- 文本编辑器保留 `@` 素材引用和 `#` 台词块功能；
- `@` 引用在执行时转换为 `<Picture N>`、`<Video N>` 或 `<Audio N>`；
- `#` 台词块在执行时转换为 `<d>...</d>`；
- 输出一个 `MINIMAX_H3_MEDIA_PROMPT` 自定义类型。

## MiniMax H3 Media Prompt Output

接收 `MINIMAX_H3_MEDIA_PROMPT`，并按固定顺序输出：

- `ref_image_0` 至 `ref_image_8`；
- `ref_video_0` 至 `ref_video_2`（`IMAGE` 视频帧批次，与 VHS 加载器兼容）；
- `ref_video_audio_0` 至 `ref_video_audio_2`；
- `ref_audio_0` 至 `ref_audio_2`；
- `text`。

节点执行后会在只读预览区显示已经转换完成的最终提示词。

没有连接的媒体输出为 `None`。视频音频从视频对象自带的音轨中提取。

