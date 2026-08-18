/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

// AI 问答功能配置（已迁移到后端，仅保留接口路径）
export const aiChatConfig = {
  // 后端 AI 问答接口地址（流式）
  chatEndpoint: `${apiConfig.baseURL}/api/ai/chat`,
  
  // 非流式接口地址（备用）
  nonStreamEndpoint: `${apiConfig.baseURL}/api/ai/chat/non-stream`,
  
  // 是否使用流式输出
  useStream: true,
}
