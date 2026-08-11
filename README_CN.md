# ComfyUI-MiniMaxH3-MediaPrompt

[English README](README.md)

这是一个专为 `MiniMaxH3ReferenceToVideo` 创建的 ComfyUI 插件，用于更快速地添加和管理 MiniMax 提示词中的图片、视频、音频及台词引用。

## 主要功能

- 动态添加引用图片、引用视频和引用音频，无需手动管理编号输入端口；
- 快速添加视频时可选择“加载视频”（同时接入视频和音频）或“仅加载视频”（不接入音轨）；
- 在提示词编辑器中输入 `@`，即可选择任意已连接的素材；
- 自动将素材引用转换为 MiniMax 所需的 `<Picture N>`、`<Video N>` 和 `<Audio N>` 格式；
- 输入 `#` 创建可编辑的台词块，并自动转换为 MiniMax 所需的 `<d>...</d>` 格式；
- 工作流执行后，可预览完成转换的最终提示词。

## 使用方法

1. 将图片、视频和音频加载节点添加或连接到 `Media` 输入端；
2. 在提示词编辑器中输入 `@`，选择需要引用的素材；
3. 需要台词时输入 `#` 创建台词块，然后在其中输入台词；
4. 将 `MiniMax H3 Media Prompt Output` 连接到 `MiniMaxH3ReferenceToVideo`；
5. 执行工作流，插件会将所有素材引用和台词块转换为 MiniMax 所需的格式。

![连接到 MiniMaxH3ReferenceToVideo 的 MiniMax H3 媒体提示词工作流](images/minimax-h3-media-prompt-workflow.png)

## 视频设置节点

`MiniMax H3 视频设置` 节点集中管理两阶段视频生成参数：

- 视频时长（秒）：默认 `10`；
- 帧率：整数输入，默认 `24`；
- 画幅：支持 `1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`9:16`、`16:9` 和 `21:9`，默认 `16:9`；
- 一采分辨率：支持下表全部 14 档，默认 `480P`；
- 二采分辨率：支持下表全部 14 档，默认 `720P`；
- 一采/二采步数：默认分别为 `6` 和 `2`；
- LoRA 强度：默认 `0.75`。

节点输出视频帧数、两阶段的宽高、两阶段步数、LoRA 强度和 `FLOAT` 类型的帧率。视频帧数按 `max(5, round(a * fps)) + (5 - (max(5, round(a * fps)) % 17)) % 17` 计算，其中 `a` 为输入秒数，`fps` 为整数帧率输入；默认输入 `10` 秒和 `24 FPS` 时输出 `243` 帧，帧率端口输出 `24.0`。宽高会根据画幅按目标像素量计算并对齐到 `32` 的倍数；默认 `16:9` 下，一采为 `864 x 480`，二采为 `1280 x 736`。

| 分辨率档位 | 16:9 基准输出 |
|---|---|
| 360P | 608 x 352 |
| 416P | 736 x 416 |
| 480P | 864 x 480 |
| 540P | 960 x 544 |
| 608P | 1056 x 608 |
| 640P | 1152 x 640 |
| 672P | 1216 x 672 |
| 720P | 1280 x 736 |
| 768P (1344x768) | 1344 x 768 |
| 768P (1376x768) | 1376 x 768 |
| 832P | 1504 x 832 |
| 928P | 1664 x 928 |
| 1024P | 1824 x 1024 |
| 1080P | 1920 x 1088 |

## 安装

将仓库克隆到 `ComfyUI/custom_nodes`，然后重启 ComfyUI：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt.git
```

## 视频依赖

快速添加引用视频需要 [ComfyUI-VideoHelperSuite](https://github.com/kosinkadink/ComfyUI-VideoHelperSuite) 提供的 `Load Video (Upload)` 节点。使用视频引用前，请先安装该插件。

请勿连接 `Load Video (Upload)` 的可选 `VAE` 输入。MiniMax 引用视频需要 `IMAGE` 视频帧批次，而不是 `LATENT` 数据。

