import { apiClient, API_ENDPOINTS } from './api';
import type {
  Contact,
  CreateContactRequest,
  ContactListResponse,
  ContactResponse
} from '../types/contact';

export const contactsService = {
  // Get all contacts
  getAll: async (): Promise<Contact[]> => {
    const response = await apiClient.get<ContactListResponse>(API_ENDPOINTS.CONTACTS);
    return response.data.data;
  },

  // Get contact by ID
  getById: async (id: number): Promise<Contact> => {
    const response = await apiClient.get<ContactResponse>(`${API_ENDPOINTS.CONTACTS}/${id}`);
    return response.data.data;
  },

  // Create new contact
  create: async (data: CreateContactRequest): Promise<Contact> => {
    const response = await apiClient.post<ContactResponse>(API_ENDPOINTS.CONTACTS, data);
    return response.data.data;
  },

  // Update contact
  update: async (id: number, data: Partial<CreateContactRequest>): Promise<Contact> => {
    const response = await apiClient.put<ContactResponse>(`${API_ENDPOINTS.CONTACTS}/${id}`, data);
    return response.data.data;
  },

  // Delete contact
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`${API_ENDPOINTS.CONTACTS}/${id}`);
  },

  // Search contacts
  search: async (query: string): Promise<Contact[]> => {
    const response = await apiClient.get<ContactListResponse>(`${API_ENDPOINTS.CONTACTS}?search=${encodeURIComponent(query)}`);
    return response.data.data;
  },

  // Get contacts by company
  getByCompany: async (companyId: number): Promise<Contact[]> => {
    const response = await apiClient.get<ContactListResponse>(`${API_ENDPOINTS.CONTACTS}?company_id=${companyId}`);
    return response.data.data;
  },
};
