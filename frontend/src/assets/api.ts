import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = axios.create({
  baseURL,
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error),
);

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface Snippet {
  id: number;
  title: string;
  language: string;
  code: string;
  author_id: number;
  created_at: string;
}

export interface Comment {
  id: number;
  snippet_id: number;
  author_id: number;
  line_number: number;
  body: string;
  created_at: string;
}

export async function register(
  email: string,
  username: string,
  password: string,
): Promise<void> {
  await api.post("/api/auth/register", { email, username, password });
}

export async function login(email: string, password: string) {
  const body = new URLSearchParams({ username: email, password: password });
  const response = await api.post("/api/auth/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  const token = response.data.access_token;
  localStorage.setItem("token", token);
  return token;
}

export async function fetchMe() {
  const response = await api.get<User>("/api/auth/me");
  return response.data;
}

export async function createSnippet(payload: {
  title: string;
  language: string;
  code: string;
}): Promise<Snippet> {
  const response = await api.post<Snippet>("/api/snippets", payload);
  return response.data;
}

export async function fetchSnippets(): Promise<Snippet[]> {
  const response = await api.get<Snippet[]>("/api/snippets");
  return response.data;
}

export async function fetchSnippet(id: number): Promise<Snippet> {
  const response = await api.get<Snippet>(`/api/snippets/${id}`);
  return response.data;
}

export async function fetchComments(snippetId: number): Promise<Comment[]> {
  const response = await api.get<Comment[]>(
    `/api/snippets/${snippetId}/comments`,
  );
  return response.data;
}

export async function createComment(
  snippetId: number,
  line_number: number,
  body: string,
): Promise<Comment> {
  const response = await api.post<Comment>(
    `/api/snippets/${snippetId}/comments`,
    { line_number, body },
  );
  return response.data;
}
