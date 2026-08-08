# ComfyUI-MiniMaxH3-MediaPrompt

[中文说明](README_CN.md)

A ComfyUI plugin created for `MiniMaxH3ReferenceToVideo`. It makes MiniMax image, video, audio, and dialogue references faster to add and easier to manage in a prompt.

## Features

- Dynamically add reference images, videos, and audio without manually managing numbered inputs.
- Type `@` in the prompt editor to select any connected media.
- Automatically convert media mentions into the MiniMax prompt syntax: `<Picture N>`, `<Video N>`, and `<Audio N>`.
- Type `#` to create an editable dialogue block, which is converted into `<d>...</d>` for MiniMax.
- Preview the final converted prompt after running the workflow.

## Workflow

1. Add or connect image, video, and audio loader nodes to the `Media` input.
2. Type `@` in the prompt editor and select the media you want to reference.
3. Type `#` when you need a dialogue block, then enter the dialogue inside it.
4. Connect `MiniMax H3 Media Prompt Output` to `MiniMaxH3ReferenceToVideo`.
5. Run the workflow. The plugin converts all media mentions and dialogue blocks into the syntax required by MiniMax.

![MiniMax H3 Media Prompt workflow connected to MiniMaxH3ReferenceToVideo](images/minimax-h3-media-prompt-workflow.png)

## Installation

Clone the repository into `ComfyUI/custom_nodes`, then restart ComfyUI:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YingsenP/ComfyUI-MiniMaxH3-MediaPrompt.git
```

## Video Dependency

Quickly adding a reference video uses the `Load Video (Upload)` node from [ComfyUI-VideoHelperSuite](https://github.com/kosinkadink/ComfyUI-VideoHelperSuite). Install it before using video references.

Do not connect the optional `VAE` input on `Load Video (Upload)`. MiniMax reference videos require `IMAGE` frame batches rather than `LATENT` values.

