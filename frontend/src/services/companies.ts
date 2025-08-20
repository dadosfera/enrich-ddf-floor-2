import { apiClient, API_ENDPOINTS } from './api';
import type { 
  Company, 
  CreateCompanyRequest, 
  UpdateCompanyRequest, 
  CompanyListResponse, 
  CompanyResponse 
} from '../types/company';

export const companiesService = {
  // Get all companies
  getAll: async (): Promise<Company[]> => {
    const response = await apiClient.get<CompanyListResponse>(API_ENDPOINTS.COMPANIES);
    return response.data.data;
  },

  // Get company by ID
  getById: async (id: number): Promise<Company> => {
    const response = await apiClient.get<CompanyResponse>(`${API_ENDPOINTS.COMPANIES}/${id}`);
    return response.data.data;
  },

  // Create new company
  create: async (data: CreateCompanyRequest): Promise<Company> => {
    const response = await apiClient.post<CompanyResponse>(API_ENDPOINTS.COMPANIES, data);
    return response.data.data;
  },

  // Update company
  update: async (id: number, data: Partial<CreateCompanyRequest>): Promise<Company> => {
    const response = await apiClient.put<CompanyResponse>(`${API_ENDPOINTS.COMPANIES}/${id}`, data);
    return response.data.data;
  },

  // Delete company
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`${API_ENDPOINTS.COMPANIES}/${id}`);
  },

  // Search companies
  search: async (query: string): Promise<Company[]> => {
    const response = await apiClient.get<CompanyListResponse>(`${API_ENDPOINTS.COMPANIES}?search=${encodeURIComponent(query)}`);
    return response.data.data;
  },
}; 