import { apiClient, API_ENDPOINTS } from './api';
import type { 
  Product, 
  CreateProductRequest, 
  ProductListResponse, 
  ProductResponse 
} from '../types/product';

export const productsService = {
  // Get all products
  getAll: async (): Promise<Product[]> => {
    const response = await apiClient.get<ProductListResponse>(API_ENDPOINTS.PRODUCTS);
    return response.data.data;
  },

  // Get product by ID
  getById: async (id: number): Promise<Product> => {
    const response = await apiClient.get<ProductResponse>(`${API_ENDPOINTS.PRODUCTS}/${id}`);
    return response.data.data;
  },

  // Create new product
  create: async (data: CreateProductRequest): Promise<Product> => {
    const response = await apiClient.post<ProductResponse>(API_ENDPOINTS.PRODUCTS, data);
    return response.data.data;
  },

  // Update product
  update: async (id: number, data: Partial<CreateProductRequest>): Promise<Product> => {
    const response = await apiClient.put<ProductResponse>(`${API_ENDPOINTS.PRODUCTS}/${id}`, data);
    return response.data.data;
  },

  // Delete product
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`${API_ENDPOINTS.PRODUCTS}/${id}`);
  },

  // Search products
  search: async (query: string): Promise<Product[]> => {
    const response = await apiClient.get<ProductListResponse>(`${API_ENDPOINTS.PRODUCTS}?search=${encodeURIComponent(query)}`);
    return response.data.data;
  },

  // Get products by category
  getByCategory: async (category: string): Promise<Product[]> => {
    const response = await apiClient.get<ProductListResponse>(`${API_ENDPOINTS.PRODUCTS}?category=${encodeURIComponent(category)}`);
    return response.data.data;
  },
}; 