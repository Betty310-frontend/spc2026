import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5001";

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// 요청 인터셉터: JWT 자동 첨부
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// ── Auth ──────────────────────────────────
export const authApi = {
  register: (data: { username: string; password: string; email: string }) =>
    apiClient.post("/api/auth/register", data),
  login: (data: { username: string; password: string }) => apiClient.post("/api/auth/login", data),
  me: () => apiClient.get("/api/auth/me"),
};

// ── Products ──────────────────────────────
export const productsApi = {
  list: (params?: { category?: string; keyword?: string; page?: number; per_page?: number }) =>
    apiClient.get("/api/products", { params }),
  detail: (id: number) => apiClient.get(`/api/products/${id}`),
  categories: () => apiClient.get("/api/products/categories"),
};

// ── Cart ──────────────────────────────────
export const cartApi = {
  get: () => apiClient.get("/api/cart"),
  add: (product_id: number, quantity: number = 1) =>
    apiClient.post("/api/cart", { product_id, quantity }),
  update: (cart_id: number, quantity: number) =>
    apiClient.put(`/api/cart/${cart_id}`, { quantity }),
  remove: (cart_id: number) => apiClient.delete(`/api/cart/${cart_id}`),
  clear: () => apiClient.delete("/api/cart"),
};
