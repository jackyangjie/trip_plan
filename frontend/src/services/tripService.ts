import axios from 'axios';
import { API_BASE_URL } from '../constants';

export interface PlanningStep {
  step: number;
  message: string;
  action: string;
  progress: number;
  agent?: string;
  data?: any;
  error?: string;
}

export async function* aiPlanTripGenerator(
  tripData: any,
  token: string,
): AsyncGenerator<PlanningStep, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/trips/ai-plan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(tripData),
  });

  if (!response.ok) {
    throw new Error(`AI 规划请求失败: ${response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('无法读取响应流');
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      // 解码并追加到缓冲区
      buffer += decoder.decode(value, { stream: true });

      // 按行分割
      const lines = buffer.split('\n');
      // 保留最后可能不完整的行
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const jsonData = line.slice(6);
          try {
            const step: PlanningStep = JSON.parse(jsonData);
            yield step;
          } catch (error) {
            console.error('解析步骤失败:', error, jsonData);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

export async function createSimpleTrip(tripData: any, token?: string): Promise<any> {
  try {
    const response = await axios.post(`${API_BASE_URL}/trips`, tripData, {
      headers: token ? {
        'Authorization': `Bearer ${token}`,
      } : {},
    });

    return response.data;
  } catch (error: any) {
    console.error('创建行程失败:', error);
    throw error;
  }
}
