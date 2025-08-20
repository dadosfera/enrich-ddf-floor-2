export interface Product {
  id: number;
  name: string;
  description?: string;
  price?: number;
  category?: string;
  sku?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProductRequest {
  name: string;
  description?: string;
  price?: number;
  category?: string;
  sku?: string;
}

export interface UpdateProductRequest extends Partial<CreateProductRequest> {
  id: number;
}

export interface ProductListResponse {
  data: Product[];
  total: number;
  page: number;
  size: number;
}

export interface ProductResponse {
  data: Product;
} 