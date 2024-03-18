import { REQUEST_TIMEOUT_MS } from "@/app/constant";

import { fetchEventSource } from "@fortaine/fetch-event-source";
import { Embedding } from "../fetch/url";

export const MESSAGE_ROLES = [
  "system",
  "user",
  "assistant",
  "URL",
  "memory",
] as const;
export type MessageRole = (typeof MESSAGE_ROLES)[number];

export interface MessageContentDetail {
  type: "text" | "image_url";
  text: string;
  image_url: { url: string };
}

export type MessageContent = string | MessageContentDetail[];

export interface RequestMessage {
  role: MessageRole;
  content: MessageContent;
}

export interface ResponseMessage {
  role: MessageRole;
  content: string;
}

export const ALL_MODELS = [
  'chatglm-6b',
  "gpt-4",
  "gpt-4-1106-preview",
  "gpt-4-vision-preview",
  "gpt-3.5-turbo",
  "gpt-3.5-turbo-16k",
] as const;

export type ModelType = (typeof ALL_MODELS)[number];

export interface LLMConfig {
  model: ModelType;
  temperature?: number;
  topP?: number;
  sendMemory?: boolean;
  maxTokens?: number;
}

export interface ChatOptions {
  message: MessageContent;
  chatHistory: RequestMessage[];
  config: LLMConfig;
  datasource?: string;
  embeddings?: Embedding[];
  controller: AbortController;
  onUpdate: (message: string) => void;
  onFinish: (memoryMessage?: ResponseMessage) => void;
  onError?: (err: Error) => void;
}

// const CHAT_PATH = "/api/llm";
const CHAT_PATH = "http://192.168.125.128:8000/api/chat/api/chat";

export function isVisionModel(model: ModelType) {
  return model === "gpt-4-vision-preview";
}

export class LLMApi {
  async chat(options: ChatOptions) {
    const requestPayload = {
      message: options.message,
      chatHistory: options.chatHistory.map((m) => ({
        role: m.role,
        content: m.content,
      })),
      config: options.config,
      datasource: options.datasource,
      embeddings: options.embeddings,
    };

    console.log("[Request] payload: ", requestPayload);

    const controller = new AbortController();
    const signal = controller.signal;
    options.controller = controller;

    const fetchOptions = {
      method: 'POST',
      body: JSON.stringify(requestPayload),
      signal: signal,
      headers: {
        "Content-Type": "application/json",
      },
    };

    console.log("[Request] making chat request to: ", CHAT_PATH);

    try {
      const response = await fetch(CHAT_PATH, fetchOptions);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("[Response] data: ", data);

      const answerArray = data;
      const responseMessage: ResponseMessage = {
        role: "assistant", 
        content: answerArray[0],
      };
      options.onFinish(responseMessage);
      console.log('----------',responseMessage)
    } catch (e) {
      console.error("[Request] failed to make a chat request", e);
    }
  }
}