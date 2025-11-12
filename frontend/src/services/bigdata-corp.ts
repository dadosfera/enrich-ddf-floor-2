import { apiClient } from './api';

// BigData Corp API Configuration
const BIGDATA_API_BASE = 'https://plataforma.bigdatacorp.com.br/api/v1';

export interface BigDataCorpCredentials {
  apiKey: string;
  apiSecret: string;
}

export interface CPFQueryRequest {
  document: string; // CPF number
  datasets?: string[];
}

export interface CNPJQueryRequest {
  document: string; // CNPJ number
  datasets?: string[];
}

export interface BigDataCorpResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  errors?: string[];
}

export interface CPFPersonData {
  cpf: string;
  name: string;
  birthdate?: string;
  emails?: Array<{
    email: string;
    type: string;
    confidence: number;
  }>;
  phones?: Array<{
    number: string;
    type: string;
    confidence: number;
  }>;
  addresses?: Array<{
    street: string;
    city: string;
    state: string;
    zipcode: string;
    type: string;
  }>;
  professional_data?: {
    company?: string;
    position?: string;
    income_range?: string;
  };
}

export interface CNPJCompanyData {
  cnpj: string;
  company_name: string;
  trade_name?: string;
  legal_form?: string;
  industry?: string;
  registration_date?: string;
  status: string;
  emails?: Array<{
    email: string;
    type: string;
  }>;
  phones?: Array<{
    number: string;
    type: string;
  }>;
  addresses?: Array<{
    street: string;
    city: string;
    state: string;
    zipcode: string;
    type: string;
  }>;
  shareholders?: Array<{
    name: string;
    document: string;
    participation: number;
  }>;
  website?: string;
}

class BigDataCorpService {
  private credentials: BigDataCorpCredentials | null = null;

  setCredentials(credentials: BigDataCorpCredentials) {
    this.credentials = credentials;
  }

  private getHeaders() {
    if (!this.credentials) {
      throw new Error('BigData Corp credentials not set');
    }

    return {
      'Authorization': `Bearer ${this.credentials.apiKey}`,
      'X-API-Secret': this.credentials.apiSecret,
      'Content-Type': 'application/json',
    };
  }

  // Test API connection
  async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(`${BIGDATA_API_BASE}/health`, {
        method: 'GET',
        headers: this.getHeaders(),
      });
      return response.ok;
    } catch (error) {
      console.error('❌ BigData Corp connection test failed:', error);
      return false;
    }
  }

  // Enrich contact with CPF data
  async enrichContactByCPF(request: CPFQueryRequest): Promise<BigDataCorpResponse<CPFPersonData>> {
    try {
      console.log('🔍 Enriching contact with CPF:', request.document);

      const response = await fetch(`${BIGDATA_API_BASE}/pessoas`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          q: `doc{${request.document}}`,
          datasets: request.datasets || [
            'basic_data{name,birthdate}',
            'emails.filter(type=WORK).limit(3)',
            'phones.filter(type=MOBILE).limit(3)',
            'addresses.limit(1)',
            'professional_data'
          ].join(',')
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      console.log('✅ CPF enrichment successful');
      return {
        success: true,
        data: this.transformCPFResponse(data),
        message: 'Contact enriched successfully'
      };
    } catch (error) {
      console.error('❌ CPF enrichment failed:', error);
      return {
        success: false,
        data: {} as any,
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Enrich company with CNPJ data
  async enrichCompanyByCNPJ(request: CNPJQueryRequest): Promise<BigDataCorpResponse<CNPJCompanyData>> {
    try {
      console.log('🏢 Enriching company with CNPJ:', request.document);

      const response = await fetch(`${BIGDATA_API_BASE}/empresas`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          q: `doc{${request.document}}`,
          datasets: request.datasets || [
            'basic_data{company_name,trade_name,legal_form,industry,registration_date,status}',
            'emails.filter(type=WORK).limit(3)',
            'phones.limit(3)',
            'addresses.limit(1)',
            'shareholders.limit(5)',
            'websites.limit(1)'
          ].join(',')
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      console.log('✅ CNPJ enrichment successful');
      return {
        success: true,
        data: this.transformCNPJResponse(data),
        message: 'Company enriched successfully'
      };
    } catch (error) {
      console.error('❌ CNPJ enrichment failed:', error);
      return {
        success: false,
        data: {} as any,
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Transform CPF response to standardized format
  private transformCPFResponse(rawData: any): CPFPersonData {
    return {
      cpf: rawData.basic_data?.cpf || '',
      name: rawData.basic_data?.name || '',
      birthdate: rawData.basic_data?.birthdate || undefined,
      emails: rawData.emails?.map((email: any) => ({
        email: email.email,
        type: email.type || 'UNKNOWN',
        confidence: email.confidence || 0
      })) || [],
      phones: rawData.phones?.map((phone: any) => ({
        number: phone.number,
        type: phone.type || 'UNKNOWN',
        confidence: phone.confidence || 0
      })) || [],
      addresses: rawData.addresses?.map((address: any) => ({
        street: address.street || '',
        city: address.city || '',
        state: address.state || '',
        zipcode: address.zipcode || '',
        type: address.type || 'UNKNOWN'
      })) || [],
      professional_data: rawData.professional_data ? {
        company: rawData.professional_data.company,
        position: rawData.professional_data.position,
        income_range: rawData.professional_data.income_range
      } : undefined
    };
  }

  // Transform CNPJ response to standardized format
  private transformCNPJResponse(rawData: any): CNPJCompanyData {
    return {
      cnpj: rawData.basic_data?.cnpj || '',
      company_name: rawData.basic_data?.company_name || '',
      trade_name: rawData.basic_data?.trade_name || undefined,
      legal_form: rawData.basic_data?.legal_form || undefined,
      industry: rawData.basic_data?.industry || undefined,
      registration_date: rawData.basic_data?.registration_date || undefined,
      status: rawData.basic_data?.status || 'UNKNOWN',
      emails: rawData.emails?.map((email: any) => ({
        email: email.email,
        type: email.type || 'UNKNOWN'
      })) || [],
      phones: rawData.phones?.map((phone: any) => ({
        number: phone.number,
        type: phone.type || 'UNKNOWN'
      })) || [],
      addresses: rawData.addresses?.map((address: any) => ({
        street: address.street || '',
        city: address.city || '',
        state: address.state || '',
        zipcode: address.zipcode || '',
        type: address.type || 'UNKNOWN'
      })) || [],
      shareholders: rawData.shareholders?.map((shareholder: any) => ({
        name: shareholder.name || '',
        document: shareholder.document || '',
        participation: shareholder.participation || 0
      })) || [],
      website: rawData.websites?.[0]?.url || undefined
    };
  }

  // Proxy enrichment through backend
  async enrichContactViaBackend(cpf: string): Promise<BigDataCorpResponse<CPFPersonData>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/bigdata/enrich-contact', {
        cpf: cpf
      });

      return {
        success: true,
        data: response.data.data,
        message: response.data.message
      };
    } catch (error: any) {
      return {
        success: false,
        data: {} as any,
        errors: [error.response?.data?.detail || error.message || 'Backend enrichment failed']
      };
    }
  }

  async enrichCompanyViaBackend(cnpj: string): Promise<BigDataCorpResponse<CNPJCompanyData>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/bigdata/enrich-company', {
        cnpj: cnpj
      });

      return {
        success: true,
        data: response.data.data,
        message: response.data.message
      };
    } catch (error: any) {
      return {
        success: false,
        data: {} as any,
        errors: [error.response?.data?.detail || error.message || 'Backend enrichment failed']
      };
    }
  }
}

// Create singleton instance
export const bigDataCorpService = new BigDataCorpService();

// Utility functions for document validation
export const validateCPF = (cpf: string): boolean => {
  const cleanCPF = cpf.replace(/\D/g, '');
  return cleanCPF.length === 11 && !/^(\d)\1{10}$/.test(cleanCPF);
};

export const validateCNPJ = (cnpj: string): boolean => {
  const cleanCNPJ = cnpj.replace(/\D/g, '');
  return cleanCNPJ.length === 14 && !/^(\d)\1{13}$/.test(cleanCNPJ);
};

export const formatCPF = (cpf: string): string => {
  const clean = cpf.replace(/\D/g, '');
  return clean.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
};

export const formatCNPJ = (cnpj: string): string => {
  const clean = cnpj.replace(/\D/g, '');
  return clean.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};
