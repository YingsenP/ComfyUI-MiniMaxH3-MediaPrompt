"""Media and prompt transport nodes for ComfyUI."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any


MAX_IMAGES = 9
MAX_VIDEOS = 3
MAX_AUDIOS = 3
MAX_VIDEO_AUDIOS = MAX_VIDEOS
MAX_MEDIA = MAX_IMAGES + MAX_VIDEOS + MAX_VIDEO_AUDIOS + MAX_AUDIOS
MEDIA_TYPES = ("image", "video", "video_audio", "audio")
CUSTOM_TYPE = "MINIMAX_H3_MEDIA_PROMPT"
DEFAULT_VIDEO_FRAME_RATE = 24
ASPECT_RATIOS = {
    "1:1 (Square)": (1, 1),
    "2:3 (Portrait Photo)": (2, 3),
    "3:2 (Photo)": (3, 2),
    "3:4 (Portrait Standard)": (3, 4),
    "4:3 (Standard)": (4, 3),
    "9:16 (Portrait Widescreen)": (9, 16),
    "16:9 (Widescreen)": (16, 9),
    "21:9 (Ultrawide)": (21, 9),
}
RESOLUTIONS = {
    "0.2 (360P)": (608, 352),
    "0.3 (416P)": (736, 416),
    "0.4 (480P)": (864, 480),
    "0.5 (540P)": (960, 544),
    "0.6 (608P)": (1056, 608),
    "0.7 (640P)": (1152, 640),
    "0.8 (672P)": (1216, 672),
    "0.9 (720P)": (1280, 736),
}


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


def _dimensions(aspect_ratio: str, resolution: str) -> tuple[int, int]:
    base_width, base_height = RESOLUTIONS[resolution]
    aspect_width, aspect_height = ASPECT_RATIOS[aspect_ratio]
    if (aspect_width, aspect_height) == (16, 9):
        return base_width, base_height

    target_pixels = base_width * base_height
    ratio = aspect_width / aspect_height
    width = round(sqrt(target_pixels * ratio) / 32) * 32
    height = round(sqrt(target_pixels / ratio) / 32) * 32
    return width, height


def _video_frame_length(video_length: int, frame_rate: int) -> int:
    frame_length = max(5, round(video_length * frame_rate))
    return frame_length + (5 - (frame_length % 17)) % 17


class MiniMaxH3VideoSettings:
    CATEGORY = "MiniMax H3/Video"
    FUNCTION = "build"
    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = (
        "video_length",
        "first_width",
        "first_height",
        "total_steps",
        "separate_steps",
        "upscale_factor",
        "lora_strength",
        "frame_rate",
    )
    DESCRIPTION = "Build two-stage video dimensions and sampling settings."

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_length": ("INT", {"default": 10, "min": 1, "max": 10000, "step": 1}),
                "aspect_ratio": (tuple(ASPECT_RATIOS), {"default": "16:9 (Widescreen)"}),
                "first_resolution": (tuple(RESOLUTIONS), {"default": "0.5 (540P)"}),
                "total_steps": ("INT", {"default": 8, "min": 1, "max": 10000, "step": 1}),
                "separate_steps": ("INT", {"default": 2, "min": 1, "max": 10000, "step": 1}),
                "upscale_factor": ("FLOAT", {"default": 1.4, "min": 0.01, "max": 100.0, "step": 0.01}),
                "lora_strength": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "frame_rate": ("INT", {"default": DEFAULT_VIDEO_FRAME_RATE, "min": 1, "max": 240, "step": 1}),
            }
        }

    @staticmethod
    def build(
        video_length: int,
        aspect_ratio: str,
        first_resolution: str,
        total_steps: int,
        separate_steps: int,
        upscale_factor: float,
        lora_strength: float,
        frame_rate: int,
    ):
        output_video_length = _video_frame_length(video_length, frame_rate)
        first_width, first_height = _dimensions(aspect_ratio, first_resolution)
        return (
            output_video_length,
            first_width,
            first_height,
            total_steps,
            separate_steps,
            upscale_factor,
            lora_strength,
            float(frame_rate),
        )


NODE_CLASS_MAPPINGS = {
    "MiniMaxH3MediaPrompt": MiniMaxH3MediaPrompt,
    "MiniMaxH3MediaPromptOutput": MiniMaxH3MediaPromptOutput,
    "MiniMaxH3VideoSettings": MiniMaxH3VideoSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiniMaxH3MediaPrompt": "MiniMax H3 Media Prompt",
    "MiniMaxH3MediaPromptOutput": "MiniMax H3 Media Prompt Output",
    "MiniMaxH3VideoSettings": "MiniMax H3 Video Settings",
}