export interface Product {
  id: number;
  name: string;
  price: number;
  description: string;
  image_url: string;
  category: string;
  stock: number;
}

export interface ProductListResponse {
  products: Product[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface CartItem {
  id: number;
  product_id: number;
  name: string;
  price: number;
  quantity: number;
  image_url: string;
  category: string;
  stock: number;
}

export interface CartResponse {
  items: CartItem[];
  total_price: number;
  count: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  created_at?: string;
}

export interface LoginResponse {
  message: string;
  token: string;
  user: User;
}

export interface ApiError {
  error: string;
  code?: string;
}
