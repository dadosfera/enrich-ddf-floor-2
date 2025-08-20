export interface Contact {
  id: number;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  company_id?: number;
  position?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateContactRequest {
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  company_id?: number;
  position?: string;
}

export interface UpdateContactRequest extends Partial<CreateContactRequest> {
  id: number;
}

export interface ContactListResponse {
  data: Contact[];
  total: number;
  page: number;
  size: number;
}

export interface ContactResponse {
  data: Contact;
} 