import os

# 阿里云 DashScope API 配置（敏感信息，勿提交到公开仓库）
AI_CHAT_CONFIG = {
    "api_endpoint": os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ).rstrip("/") + "/chat/completions",
    "api_key": os.getenv(
        "DASHSCOPE_API_KEY",
        "sk-8b2c0bd5d1214cffb84976ed048c346c",
    ),
    "model": os.getenv("DASHSCOPE_MODEL", "qwen3.5-plus"),
    "stream": True,
    "timeout": 120,
}
