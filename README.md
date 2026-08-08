# ComfyUI-MiniMaxH3-MediaPrompt

[中文说明](README_CN.md)

This plugin provides media prompt inputs for `MiniMaxH3ReferenceToVideo`.

This plugin now registers two nodes only. The legacy MiniMax H3 loading and generation nodes are disabled.

## Workflow Example

![MiniMax H3 Media Prompt workflow connected to MiniMaxH3ReferenceToVideo](images/minimax-h3-media-prompt-workflow.png)

## Installation

Clone the [YingsenP/ComfyUI-MiniMaxH3-MediaPrompt](https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt) repository into `ComfyUI/custom_nodes`, then restart ComfyUI:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt.git
```

## Required Dependency

Video quick-create relies on the `Load Video (Upload)` node. Install [ComfyUI-VideoHelperSuite](https://github.com/kosinkadink/ComfyUI-VideoHelperSuite) before using this feature.

## MiniMax H3 Media Prompt

- One `Media` input accepts images, videos, and audio clips.
- Supports up to 9 images, 3 videos, and 3 standalone audio clips.
- Video quick-create uses ComfyUI-VideoHelperSuite's `Load Video (Upload)` node.
- The VHS `IMAGE` frames and `AUDIO` outputs are paired as the same-numbered video and soundtrack.
- Do not connect the optional `VAE` input on the VHS loader; MiniMax reference videos require `IMAGE` frame batches, not `LATENT` values.
- The text editor retains `@` media mentions and `#` dialogue blocks.
- Mentions become `<Picture N>`, `<Video N>`, or `<Audio N>` at execution time.
- Dialogue blocks become `<d>...</d>` at execution time.
- Returns one custom `MINIMAX_H3_MEDIA_PROMPT` value.

## MiniMax H3 Media Prompt Output

Accepts `MINIMAX_H3_MEDIA_PROMPT` and returns these fixed outputs:

- `ref_image_0` through `ref_image_8`;
- `ref_video_0` through `ref_video_2` (`IMAGE` frame batches, compatible with VHS loaders);
- `ref_video_audio_0` through `ref_video_audio_2`;
- `ref_audio_0` through `ref_audio_2`;
- `text`.

After execution, the node displays the converted final prompt in a read-only preview.

Unconnected media outputs are `None`. Video audio is extracted from each video object's embedded audio track.

