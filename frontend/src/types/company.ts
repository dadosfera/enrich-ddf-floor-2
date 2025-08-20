export interface Company {
  id: number;
  name: string;
  industry?: string;
  website?: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateCompanyRequest {
  name: string;
  industry?: string;
  website?: string;
  description?: string;
}

export interface UpdateCompanyRequest extends Partial<CreateCompanyRequest> {
  id: number;
}

export interface CompanyListResponse {
  data: Company[];
  total: number;
  page: number;
  size: number;
}

export interface CompanyResponse {
  data: Company;
} 