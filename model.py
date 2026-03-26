import base64
import io
from typing import List
from PIL import Image
from agentscope.model import OpenAIChatModel
from agentscope.token import TokenCounterBase

class VLTokenCounter(TokenCounterBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def count(self, messages: List[dict], **kwargs) -> int:
        total_tokens = 0
        
        for message in messages:
            content = message.get("content", "")
            if isinstance(content, str):
                total_tokens += int(len(content) / 1.5)
            elif isinstance(content, list):
                for item in content:
                    item_type = item['type']
                    if item_type == "text":
                        text = item['text']
                        total_tokens += int(len(text) / 1.5)
                    elif item_type == "image_url":
                        url = item['image_url']['url']
                        if url.startswith("data:image"):
                            base64_data = url.split(",")[1]
                            image_bytes = base64.b64decode(base64_data)
                            image = Image.open(io.BytesIO(image_bytes))
                            width, height = image.size
                            total_tokens += int((width * height) / (32 * 32))
        return total_tokens

class OpenAIChatModelCached(OpenAIChatModel): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __call__(self, messages, *args, **kwargs):
        target_msg = messages[-2] if len(messages) >= 2 else messages[-1]
        self._add_cache_control(target_msg)
        return await super().__call__(messages, *args, **kwargs)

    @staticmethod
    def _add_cache_control(msg):
        ephemeral = {"type": "ephemeral"}
        if isinstance(msg['content'], str):
            msg['content'] = [{'type': 'text', 'text': msg['content'], "cache_control": ephemeral}]
        elif isinstance(msg['content'], list):
            for block in reversed(msg['content']):
                if isinstance(block, dict) and block.get('type') == 'text':
                    block['cache_control'] = ephemeral
                    return
            if msg['content']:
                msg['content'][-1]['cache_control'] = ephemeral
