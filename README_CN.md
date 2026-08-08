# ComfyUI-MiniMaxH3-MediaPrompt

[English README](README.md)

这是一个专为 `MiniMaxH3ReferenceToVideo` 创建的 ComfyUI 插件，用于更快速地添加和管理 MiniMax 提示词中的图片、视频、音频及台词引用。

## 主要功能

- 动态添加引用图片、引用视频和引用音频，无需手动管理编号输入端口；
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

## 安装

将仓库克隆到 `ComfyUI/custom_nodes`，然后重启 ComfyUI：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt.git
```

## 视频依赖

快速添加引用视频需要 [ComfyUI-VideoHelperSuite](https://github.com/kosinkadink/ComfyUI-VideoHelperSuite) 提供的 `Load Video (Upload)` 节点。使用视频引用前，请先安装该插件。

请勿连接 `Load Video (Upload)` 的可选 `VAE` 输入。MiniMax 引用视频需要 `IMAGE` 视频帧批次，而不是 `LATENT` 数据。

