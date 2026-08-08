"""Media and prompt transport nodes for ComfyUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


MAX_IMAGES = 9
MAX_VIDEOS = 3
MAX_AUDIOS = 3
MAX_VIDEO_AUDIOS = MAX_VIDEOS
MAX_MEDIA = MAX_IMAGES + MAX_VIDEOS + MAX_VIDEO_AUDIOS + MAX_AUDIOS
MEDIA_TYPES = ("image", "video", "video_audio", "audio")
CUSTOM_TYPE = "MINIMAX_H3_MEDIA_PROMPT"


@dataclass(frozen=True)
class MiniMaxH3MediaPromptBundle:
    images: tuple[Any, ...]
    videos: tuple[Any, ...]
    video_audios: tuple[Any, ...]
    audios: tuple[Any, ...]
    text: str


def _video_audio(video: Any) -> Any:
    if hasattr(video, "get_components"):
        return video.get_components().audio
    if isinstance(video, dict):
        return video.get("audio")
    return None


class MiniMaxH3MediaPrompt:
    CATEGORY = "MiniMax H3/Media Prompt"
    FUNCTION = "pack"
    RETURN_TYPES = (CUSTOM_TYPE,)
    RETURN_NAMES = ("media_prompt",)
    DESCRIPTION = "Collect ordered MiniMax H3 reference media with @ references and # dialogue text."

    @classmethod
    def INPUT_TYPES(cls):
        optional = {"media": ("*",)}
        for index in range(1, MAX_MEDIA + 1):
            optional[f"media_{index}"] = ("*",)
            optional[f"media_type_{index}"] = ("STRING", {"default": ""})
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True, "default": ""}),
            },
            "optional": optional,
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    @staticmethod
    def pack(text: str, **kwargs):
        media = []
        direct = kwargs.get("media")
        if direct is not None:
            media.append((str(kwargs.get("media_type") or "image").lower(), direct))
        for index in range(1, MAX_MEDIA + 1):
            value = kwargs.get(f"media_{index}")
            if value is None:
                continue
            media_type = str(kwargs.get(f"media_type_{index}") or "image").lower()
            media.append((media_type if media_type in MEDIA_TYPES else "image", value))
        if len(media) > MAX_MEDIA:
            raise ValueError(f"MiniMax H3 Media Prompt accepts at most {MAX_MEDIA} transported values")

        images = tuple(value for media_type, value in media if media_type == "image")
        videos = tuple(value for media_type, value in media if media_type == "video")
        video_audios = tuple(value for media_type, value in media if media_type == "video_audio")
        audios = tuple(value for media_type, value in media if media_type == "audio")
        if (
            len(images) > MAX_IMAGES
            or len(videos) > MAX_VIDEOS
            or len(video_audios) > MAX_VIDEO_AUDIOS
            or len(audios) > MAX_AUDIOS
        ):
            raise ValueError("Media limits are 9 images, 3 videos with soundtracks and 3 standalone audio clips")
        for video in videos:
            shape = getattr(video, "shape", ())
            if len(shape) != 4:
                raise ValueError(
                    "Reference videos must be IMAGE frame batches. Disable the optional VAE input on VHS Load Video."
                )

        paired_video_audios = tuple(
            video_audios[index] if index < len(video_audios) else _video_audio(video)
            for index, video in enumerate(videos)
        )

        return (MiniMaxH3MediaPromptBundle(
            images=images,
            videos=videos,
            video_audios=paired_video_audios,
            audios=audios,
            text=str(text),
        ),)


class MiniMaxH3MediaPromptOutput:
    CATEGORY = "MiniMax H3/Media Prompt"
    FUNCTION = "unpack"
    RETURN_TYPES = (
        *("IMAGE",) * MAX_IMAGES,
        *("IMAGE",) * MAX_VIDEOS,
        *("AUDIO",) * MAX_VIDEOS,
        *("AUDIO",) * MAX_AUDIOS,
        "STRING",
    )
    RETURN_NAMES = (
        *(f"ref_image_{index}" for index in range(MAX_IMAGES)),
        *(f"ref_video_{index}" for index in range(MAX_VIDEOS)),
        *(f"ref_video_audio_{index}" for index in range(MAX_VIDEOS)),
        *(f"ref_audio_{index}" for index in range(MAX_AUDIOS)),
        "text",
    )
    DESCRIPTION = "Expand a media prompt bundle into fixed image, video, audio and text outputs."

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"media_prompt": (CUSTOM_TYPE,)}}

    @staticmethod
    def unpack(media_prompt):
        if not isinstance(media_prompt, MiniMaxH3MediaPromptBundle):
            raise ValueError("Connect the MiniMax H3 Media Prompt output")

        def padded(values, size):
            return (*values[:size], *(None for _ in range(size - len(values))))

        result = (
            *padded(media_prompt.images, MAX_IMAGES),
            *padded(media_prompt.videos, MAX_VIDEOS),
            *padded(media_prompt.video_audios, MAX_VIDEOS),
            *padded(media_prompt.audios, MAX_AUDIOS),
            media_prompt.text,
        )
        return {"ui": {"text": (media_prompt.text,)}, "result": result}


NODE_CLASS_MAPPINGS = {
    "MiniMaxH3MediaPrompt": MiniMaxH3MediaPrompt,
    "MiniMaxH3MediaPromptOutput": MiniMaxH3MediaPromptOutput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiniMaxH3MediaPrompt": "MiniMax H3 Media Prompt",
    "MiniMaxH3MediaPromptOutput": "MiniMax H3 Media Prompt Output",
}