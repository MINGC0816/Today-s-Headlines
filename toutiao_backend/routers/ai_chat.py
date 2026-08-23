import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from config.ai_conf import AI_CHAT_CONFIG
from utils.response import fail_response, success_response

router = APIRouter(prefix="/api/ai", tags=["AI问答"])


class ChatRequest(BaseModel):
    message: str
    history: list = []
    stream: bool = False


@router.post("/chat", summary="AI 智能问答")
async def ai_chat(request: ChatRequest):
    if not AI_CHAT_CONFIG.get("api_key"):
        return fail_response(code=500, msg="API Key 未配置")

    if not request.message.strip():
        return fail_response(code=400, msg="消息内容不能为空")

    try:
        messages = request.history + [{"role": "user", "content": request.message}]
        payload = {
            "model": AI_CHAT_CONFIG["model"],
            "messages": messages,
            "stream": request.stream,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_CHAT_CONFIG['api_key']}",
        }

        if request.stream:
            async def event_generator():
                async with httpx.AsyncClient() as gen_client:
                    async with gen_client.stream(
                        "POST",
                        AI_CHAT_CONFIG["api_endpoint"],
                        headers=headers,
                        json=payload,
                        timeout=AI_CHAT_CONFIG.get("timeout", 60.0),
                    ) as gen_response:
                        if gen_response.status_code != 200:
                            error_data = await gen_response.aread()
                            yield f"data: AI 服务调用失败: {error_data.decode()}\n\n"
                            return

                        async for chunk in gen_response.aiter_text():
                            if chunk:
                                yield chunk

            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                AI_CHAT_CONFIG["api_endpoint"],
                headers=headers,
                json=payload,
                timeout=AI_CHAT_CONFIG.get("timeout", 60.0),
            )

            if response.status_code != 200:
                return fail_response(code=500, msg=f"AI 服务调用失败: {response.text}")

            resp_data = response.json()
            reply_text = ""
            if resp_data.get("choices"):
                reply_text = resp_data["choices"][0].get("message", {}).get("content", "")

            return success_response(data={
                "reply": reply_text,
                "usage": resp_data.get("usage", {}),
            })

    except Exception as e:
        return fail_response(code=500, msg=f"AI 服务异常: {str(e)}")
