export interface QueryRequest {
  question: string;
}

export interface QueryResponse {
  answer: string;
  content?: string;
  thread_id?: string;
}

export interface ApiError {
  message: string;
  status?: number;
}