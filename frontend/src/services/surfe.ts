import { apiClient } from './api';

// Surfe API Configuration
const SURFE_API_BASE = 'https://api.surfe.com/v2';

export interface SurfeCredentials {
  apiKey: string;
}

export interface PersonSearchRequest {
  filters: {
    industries?: string[];
    companies?: string[];
    locations?: string[];
    jobTitles?: string[];
    seniorities?: string[];
    companySize?: string[];
    technologies?: string[];
  };
  limit?: number;
  offset?: number;
}

export interface PersonEnrichRequest {
  include: {
    email?: boolean;
    mobile?: boolean;
    linkedin?: boolean;
  };
  people: Array<{
    firstName: string;
    lastName: string;
    companyName?: string;
    companyDomain?: string;
    linkedinUrl?: string;
    externalID?: string;
  }>;
}

export interface CompanySearchRequest {
  filters: {
    industries?: string[];
    locations?: string[];
    companySize?: string[];
    technologies?: string[];
    revenue?: string[];
    founded?: string[];
  };
  limit?: number;
  offset?: number;
}

export interface CompanyEnrichRequest {
  companies: Array<{
    domain?: string;
    name?: string;
    linkedinUrl?: string;
    externalID?: string;
  }>;
}

export interface SurfeResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  errors?: string[];
  credits_used?: {
    email?: number;
    mobile?: number;
  };
  credits_remaining?: {
    email?: number;
    mobile?: number;
  };
}

export interface PersonSearchData {
  id: string;
  firstName: string;
  lastName: string;
  fullName: string;
  headline?: string;
  location?: string;
  linkedinUrl?: string;
  company?: {
    name: string;
    domain?: string;
    industry?: string;
    size?: string;
    linkedinUrl?: string;
  };
  jobTitle?: string;
  seniority?: string;
  confidence: number;
}

export interface PersonEnrichData {
  externalID?: string;
  firstName: string;
  lastName: string;
  fullName: string;
  linkedinUrl?: string;
  email?: {
    address: string;
    confidence: number;
    type: 'work' | 'personal';
    source: string;
  };
  mobile?: {
    number: string;
    confidence: number;
    type: string;
    source: string;
  };
  company?: {
    name: string;
    domain?: string;
    industry?: string;
    size?: string;
    linkedinUrl?: string;
  };
  jobTitle?: string;
  location?: string;
  profileData?: {
    headline?: string;
    summary?: string;
    skills?: string[];
    experience?: Array<{
      title: string;
      company: string;
      duration?: string;
    }>;
    education?: Array<{
      school: string;
      degree?: string;
      field?: string;
    }>;
  };
}

export interface CompanySearchData {
  id: string;
  name: string;
  domain?: string;
  industry?: string;
  description?: string;
  website?: string;
  linkedinUrl?: string;
  location?: {
    city?: string;
    state?: string;
    country?: string;
    address?: string;
  };
  size?: {
    employees?: number;
    range?: string;
  };
  revenue?: {
    amount?: number;
    range?: string;
  };
  founded?: number;
  technologies?: string[];
  confidence: number;
}

export interface CompanyEnrichData {
  externalID?: string;
  name: string;
  domain?: string;
  website?: string;
  industry?: string;
  description?: string;
  linkedinUrl?: string;
  location?: {
    city?: string;
    state?: string;
    country?: string;
    address?: string;
    zipCode?: string;
  };
  size?: {
    employees?: number;
    range?: string;
  };
  revenue?: {
    amount?: number;
    range?: string;
    currency?: string;
  };
  founded?: number;
  technologies?: string[];
  socialProfiles?: {
    twitter?: string;
    facebook?: string;
    instagram?: string;
  };
  keyPeople?: Array<{
    name: string;
    title: string;
    linkedinUrl?: string;
  }>;
}

export interface SurfeCreditsData {
  email: {
    remaining: number;
    total: number;
    daily_quota: number;
    daily_used: number;
  };
  mobile: {
    remaining: number;
    total: number;
    daily_quota: number;
    daily_used: number;
  };
}

export interface SurfeFiltersData {
  industries: string[];
  locations: string[];
  companySize: string[];
  technologies: string[];
  jobTitles: string[];
  seniorities: string[];
  revenue: string[];
  founded: string[];
}

class SurfeService {
  private credentials: SurfeCredentials | null = null;

  setCredentials(credentials: SurfeCredentials) {
    this.credentials = credentials;
  }

  private getHeaders() {
    if (!this.credentials) {
      throw new Error('Surfe API credentials not set');
    }

    return {
      'Authorization': `Bearer ${this.credentials.apiKey}`,
      'Content-Type': 'application/json',
      'User-Agent': 'Enrich-DDF-Floor-2/1.0',
    };
  }

  // Test API connection
  async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(`${SURFE_API_BASE}/credits`, {
        method: 'GET',
        headers: this.getHeaders(),
      });
      return response.ok;
    } catch (error) {
      console.error('❌ Surfe API connection test failed:', error);
      return false;
    }
  }

  // Get account credits
  async getCredits(): Promise<SurfeResponse<SurfeCreditsData>> {
    try {
      const response = await fetch(`${SURFE_API_BASE}/credits`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      return {
        success: true,
        data: this.transformCreditsResponse(data),
        message: 'Credits retrieved successfully'
      };
    } catch (error) {
      console.error('❌ Failed to get Surfe credits:', error);
      return {
        success: false,
        data: {
          email: { remaining: 0, total: 0, daily_quota: 0, daily_used: 0 },
          mobile: { remaining: 0, total: 0, daily_quota: 0, daily_used: 0 }
        },
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Get available filters
  async getFilters(): Promise<SurfeResponse<SurfeFiltersData>> {
    try {
      const response = await fetch(`${SURFE_API_BASE}/filters`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      return {
        success: true,
        data: data,
        message: 'Filters retrieved successfully'
      };
    } catch (error) {
      console.error('❌ Failed to get Surfe filters:', error);
      return {
        success: false,
        data: {
          industries: [],
          locations: [],
          companySize: [],
          technologies: [],
          jobTitles: [],
          seniorities: [],
          revenue: [],
          founded: []
        },
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Search for people
  async searchPeople(request: PersonSearchRequest): Promise<SurfeResponse<PersonSearchData[]>> {
    try {
      console.log('🔍 Searching for people with filters:', request.filters);

      const response = await fetch(`${SURFE_API_BASE}/people/search`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      console.log('✅ People search successful');
      return {
        success: true,
        data: data.people?.map((person: any) => this.transformPersonSearchResponse(person)) || [],
        message: `Found ${data.people?.length || 0} people`
      };
    } catch (error) {
      console.error('❌ People search failed:', error);
      return {
        success: false,
        data: [],
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Enrich people data
  async enrichPeople(request: PersonEnrichRequest): Promise<SurfeResponse<PersonEnrichData[]>> {
    try {
      console.log('🔍 Enriching people data for:', request.people.length, 'people');

      const response = await fetch(`${SURFE_API_BASE}/people/enrich`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      console.log('✅ People enrichment successful');
      return {
        success: true,
        data: data.people?.map((person: any) => this.transformPersonEnrichResponse(person)) || [],
        message: 'People enriched successfully',
        credits_used: data.credits_used,
        credits_remaining: data.credits_remaining
      };
    } catch (error) {
      console.error('❌ People enrichment failed:', error);
      return {
        success: false,
        data: [],
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Search for companies
  async searchCompanies(request: CompanySearchRequest): Promise<SurfeResponse<CompanySearchData[]>> {
    try {
      console.log('🏢 Searching for companies with filters:', request.filters);

      const response = await fetch(`${SURFE_API_BASE}/companies/search`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      console.log('✅ Company search successful');
      return {
        success: true,
        data: data.companies?.map((company: any) => this.transformCompanySearchResponse(company)) || [],
        message: `Found ${data.companies?.length || 0} companies`
      };
    } catch (error) {
      console.error('❌ Company search failed:', error);
      return {
        success: false,
        data: [],
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Enrich company data
  async enrichCompanies(request: CompanyEnrichRequest): Promise<SurfeResponse<CompanyEnrichData[]>> {
    try {
      console.log('🏢 Enriching company data for:', request.companies.length, 'companies');

      const response = await fetch(`${SURFE_API_BASE}/companies/enrich`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      console.log('✅ Company enrichment successful');
      return {
        success: true,
        data: data.companies?.map((company: any) => this.transformCompanyEnrichResponse(company)) || [],
        message: 'Companies enriched successfully'
      };
    } catch (error) {
      console.error('❌ Company enrichment failed:', error);
      return {
        success: false,
        data: [],
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Transform credits response
  private transformCreditsResponse(rawData: any): SurfeCreditsData {
    return {
      email: {
        remaining: rawData.email?.remaining || 0,
        total: rawData.email?.total || 0,
        daily_quota: rawData.email?.daily_quota || 0,
        daily_used: rawData.email?.daily_used || 0
      },
      mobile: {
        remaining: rawData.mobile?.remaining || 0,
        total: rawData.mobile?.total || 0,
        daily_quota: rawData.mobile?.daily_quota || 0,
        daily_used: rawData.mobile?.daily_used || 0
      }
    };
  }

  // Transform person search response
  private transformPersonSearchResponse(rawData: any): PersonSearchData {
    return {
      id: rawData.id || '',
      firstName: rawData.firstName || '',
      lastName: rawData.lastName || '',
      fullName: rawData.fullName || `${rawData.firstName} ${rawData.lastName}`,
      headline: rawData.headline,
      location: rawData.location,
      linkedinUrl: rawData.linkedinUrl,
      company: rawData.company ? {
        name: rawData.company.name || '',
        domain: rawData.company.domain,
        industry: rawData.company.industry,
        size: rawData.company.size,
        linkedinUrl: rawData.company.linkedinUrl
      } : undefined,
      jobTitle: rawData.jobTitle,
      seniority: rawData.seniority,
      confidence: rawData.confidence || 0
    };
  }

  // Transform person enrich response
  private transformPersonEnrichResponse(rawData: any): PersonEnrichData {
    return {
      externalID: rawData.externalID,
      firstName: rawData.firstName || '',
      lastName: rawData.lastName || '',
      fullName: rawData.fullName || `${rawData.firstName} ${rawData.lastName}`,
      linkedinUrl: rawData.linkedinUrl,
      email: rawData.email ? {
        address: rawData.email.address || '',
        confidence: rawData.email.confidence || 0,
        type: rawData.email.type || 'work',
        source: rawData.email.source || 'surfe'
      } : undefined,
      mobile: rawData.mobile ? {
        number: rawData.mobile.number || '',
        confidence: rawData.mobile.confidence || 0,
        type: rawData.mobile.type || 'mobile',
        source: rawData.mobile.source || 'surfe'
      } : undefined,
      company: rawData.company ? {
        name: rawData.company.name || '',
        domain: rawData.company.domain,
        industry: rawData.company.industry,
        size: rawData.company.size,
        linkedinUrl: rawData.company.linkedinUrl
      } : undefined,
      jobTitle: rawData.jobTitle,
      location: rawData.location,
      profileData: rawData.profileData ? {
        headline: rawData.profileData.headline,
        summary: rawData.profileData.summary,
        skills: rawData.profileData.skills || [],
        experience: rawData.profileData.experience || [],
        education: rawData.profileData.education || []
      } : undefined
    };
  }

  // Transform company search response
  private transformCompanySearchResponse(rawData: any): CompanySearchData {
    return {
      id: rawData.id || '',
      name: rawData.name || '',
      domain: rawData.domain,
      industry: rawData.industry,
      description: rawData.description,
      website: rawData.website,
      linkedinUrl: rawData.linkedinUrl,
      location: rawData.location ? {
        city: rawData.location.city,
        state: rawData.location.state,
        country: rawData.location.country,
        address: rawData.location.address
      } : undefined,
      size: rawData.size ? {
        employees: rawData.size.employees,
        range: rawData.size.range
      } : undefined,
      revenue: rawData.revenue ? {
        amount: rawData.revenue.amount,
        range: rawData.revenue.range
      } : undefined,
      founded: rawData.founded,
      technologies: rawData.technologies || [],
      confidence: rawData.confidence || 0
    };
  }

  // Transform company enrich response
  private transformCompanyEnrichResponse(rawData: any): CompanyEnrichData {
    return {
      externalID: rawData.externalID,
      name: rawData.name || '',
      domain: rawData.domain,
      website: rawData.website,
      industry: rawData.industry,
      description: rawData.description,
      linkedinUrl: rawData.linkedinUrl,
      location: rawData.location ? {
        city: rawData.location.city,
        state: rawData.location.state,
        country: rawData.location.country,
        address: rawData.location.address,
        zipCode: rawData.location.zipCode
      } : undefined,
      size: rawData.size ? {
        employees: rawData.size.employees,
        range: rawData.size.range
      } : undefined,
      revenue: rawData.revenue ? {
        amount: rawData.revenue.amount,
        range: rawData.revenue.range,
        currency: rawData.revenue.currency
      } : undefined,
      founded: rawData.founded,
      technologies: rawData.technologies || [],
      socialProfiles: rawData.socialProfiles || {},
      keyPeople: rawData.keyPeople?.map((person: any) => ({
        name: person.name || '',
        title: person.title || '',
        linkedinUrl: person.linkedinUrl
      })) || []
    };
  }

  // Proxy enrichment through backend
  async enrichPeopleViaBackend(request: PersonEnrichRequest): Promise<SurfeResponse<PersonEnrichData[]>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/surfe/enrich-people', request);

      return {
        success: true,
        data: response.data.data,
        message: response.data.message,
        credits_used: response.data.credits_used,
        credits_remaining: response.data.credits_remaining
      };
    } catch (error: any) {
      return {
        success: false,
        data: [],
        errors: [error.response?.data?.detail || error.message || 'Backend enrichment failed']
      };
    }
  }

  async searchPeopleViaBackend(request: PersonSearchRequest): Promise<SurfeResponse<PersonSearchData[]>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/surfe/search-people', request);

      return {
        success: true,
        data: response.data.data,
        message: response.data.message
      };
    } catch (error: any) {
      return {
        success: false,
        data: [],
        errors: [error.response?.data?.detail || error.message || 'Backend search failed']
      };
    }
  }
}

// Create singleton instance
export const surfeService = new SurfeService();

// Utility functions for validation
export const validatePersonData = (person: Partial<PersonEnrichRequest['people'][0]>): boolean => {
  return !!(person.firstName && person.lastName);
};

export const validateCompanyData = (company: Partial<CompanyEnrichRequest['companies'][0]>): boolean => {
  return !!(company.domain || company.name);
};

export const validateEmailAddress = (email: string): boolean => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
};

export const validatePhoneNumber = (phone: string): boolean => {
  const phonePattern = /^\+?[\d\s\-\(\)]+$/;
  return phonePattern.test(phone.replace(/\s/g, '')) && phone.replace(/\D/g, '').length >= 10;
};
