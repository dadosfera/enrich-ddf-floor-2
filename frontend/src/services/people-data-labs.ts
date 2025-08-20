import { apiClient } from './api';

// People Data Labs API Configuration
const PDL_API_BASE = 'https://api.peopledatalabs.com/v5';

export interface PDLCredentials {
  apiKey: string;
}

export interface PersonEnrichRequest {
  params: {
    name?: string;
    first_name?: string;
    last_name?: string;
    middle_name?: string;
    email?: string;
    phone?: string;
    linkedin_url?: string;
    linkedin_username?: string;
    linkedin_id?: string;
    facebook_url?: string;
    facebook_username?: string;
    facebook_id?: string;
    twitter_url?: string;
    twitter_username?: string;
    github_url?: string;
    github_username?: string;
    company?: string;
    school?: string;
    location?: string;
    country?: string;
    region?: string;
    locality?: string;
    street_address?: string;
    postal_code?: string;
    birth_date?: string;
    min_likelihood?: number;
    required?: string;
    pretty?: boolean;
  };
}

export interface PersonSearchRequest {
  query: {
    name?: string[];
    first_name?: string[];
    last_name?: string[];
    email?: string[];
    phone?: string[];
    birth_date?: string[];
    linkedin_url?: string[];
    linkedin_username?: string[];
    linkedin_id?: string[];
    facebook_url?: string[];
    facebook_username?: string[];
    facebook_id?: string[];
    twitter_url?: string[];
    twitter_username?: string[];
    github_url?: string[];
    github_username?: string[];
    job_title?: string[];
    job_title_role?: string[];
    job_title_sub_role?: string[];
    job_title_levels?: string[];
    job_company_name?: string[];
    job_company_website?: string[];
    job_company_size?: string[];
    job_company_industry?: string[];
    job_company_linkedin_url?: string[];
    job_company_linkedin_id?: string[];
    job_company_facebook_url?: string[];
    job_company_twitter_url?: string[];
    job_company_location_name?: string[];
    job_company_location_locality?: string[];
    job_company_location_region?: string[];
    job_company_location_country?: string[];
    job_start_date?: string[];
    job_end_date?: string[];
    location_name?: string[];
    location_locality?: string[];
    location_region?: string[];
    location_country?: string[];
    location_continent?: string[];
    education_school?: string[];
    education_school_name?: string[];
    education_school_type?: string[];
    education_degree_name?: string[];
    skills?: string[];
    interests?: string[];
    industry?: string[];
    years_experience?: string[];
    languages?: string[];
  };
  size?: number;
  from?: number;
  scroll_token?: string;
  include_if_matched?: boolean;
  pretty?: boolean;
}

export interface CompanyEnrichRequest {
  params: {
    name?: string;
    profile?: string;
    ticker?: string;
    website?: string;
    location?: string;
    locality?: string;
    region?: string;
    country?: string;
    linkedin_url?: string;
    linkedin_id?: string;
    facebook_url?: string;
    twitter_url?: string;
    min_likelihood?: number;
    required?: string;
    pretty?: boolean;
  };
}

export interface CompanySearchRequest {
  query: {
    name?: string[];
    website?: string[];
    ticker?: string[];
    type?: string[];
    tags?: string[];
    industry?: string[];
    naics?: string[];
    sic?: string[];
    size?: string[];
    employee_count?: string[];
    revenue?: string[];
    location_name?: string[];
    location_locality?: string[];
    location_region?: string[];
    location_country?: string[];
    location_continent?: string[];
    linkedin_url?: string[];
    linkedin_id?: string[];
    facebook_url?: string[];
    twitter_url?: string[];
    founded?: string[];
  };
  size?: number;
  from?: number;
  scroll_token?: string;
  pretty?: boolean;
}

export interface PDLResponse<T = any> {
  status: number;
  data?: T;
  error?: {
    type: string;
    message: string;
  };
  likelihood?: number;
  credits_remaining?: number;
}

export interface PersonData {
  id: string;
  full_name: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  gender?: string;
  birth_year?: number;
  birth_date?: string;
  linkedin_url?: string;
  linkedin_username?: string;
  linkedin_id?: string;
  facebook_url?: string;
  facebook_username?: string;
  facebook_id?: string;
  twitter_url?: string;
  twitter_username?: string;
  github_url?: string;
  github_username?: string;
  work_email?: string;
  personal_emails?: string[];
  // phone_numbers?: string[]; // Replaced by detailed version below
  mobile_phone?: string;
  industry?: string;
  job_title?: string;
  job_title_role?: string;
  job_title_sub_role?: string;
  job_title_levels?: string[];
  job_company_name?: string;
  job_company_website?: string;
  job_company_size?: string;
  job_company_industry?: string;
  job_company_linkedin_url?: string;
  job_company_linkedin_id?: string;
  job_company_facebook_url?: string;
  job_company_twitter_url?: string;
  job_company_founded?: number;
  job_company_type?: string;
  job_last_updated?: string;
  job_start_date?: string;
  job_summary?: string;
  location_name?: string;
  location_locality?: string;
  location_region?: string;
  location_country?: string;
  location_continent?: string;
  location_street_address?: string;
  location_address_line_2?: string;
  location_postal_code?: string;
  location_geo?: string;
  education?: Array<{
    school?: {
      name?: string;
      type?: string;
      id?: string;
      location?: string;
      linkedin_url?: string;
      facebook_url?: string;
      twitter_url?: string;
      linkedin_id?: string;
      facebook_id?: string;
      twitter_id?: string;
      website?: string;
    };
    degrees?: string[];
    start_date?: string;
    end_date?: string;
    gpa?: number;
    summary?: string;
  }>;
  experience?: Array<{
    company?: {
      name?: string;
      size?: string;
      id?: string;
      founded?: number;
      industry?: string;
      location?: string;
      linkedin_url?: string;
      linkedin_id?: string;
      facebook_url?: string;
      twitter_url?: string;
      website?: string;
    };
    location_names?: string[];
    end_date?: string;
    start_date?: string;
    title?: {
      name?: string;
      role?: string;
      sub_role?: string;
      levels?: string[];
    };
    summary?: string;
  }>;
  skills?: string[];
  interests?: string[];
  languages?: Array<{
    name: string;
    proficiency?: number;
  }>;
  emails?: Array<{
    address: string;
    type?: string;
  }>;
  phone_numbers?: Array<{
    number: string;
    type?: string;
  }>;
  profiles?: Array<{
    network: string;
    id?: string;
    url?: string;
    username?: string;
  }>;
}

export interface CompanyData {
  id: string;
  name: string;
  size?: string;
  employee_count?: number;
  id_source?: string;
  founded?: number;
  industry?: string;
  naics?: Array<{
    naics_code: string;
    sector: string;
    sub_sector: string;
    industry_group: string;
    naics_industry: string;
    national_industry: string;
  }>;
  sic?: Array<{
    sic_code: string;
    major_group: string;
    industry_group: string;
    industry: string;
  }>;
  location?: {
    name?: string;
    locality?: string;
    region?: string;
    metro?: string;
    country?: string;
    continent?: string;
    street_address?: string;
    address_line_2?: string;
    postal_code?: string;
    geo?: string;
  };
  linkedin_url?: string;
  linkedin_id?: string;
  facebook_url?: string;
  twitter_url?: string;
  profiles?: Array<{
    network: string;
    id?: string;
    url?: string;
    username?: string;
  }>;
  website?: string;
  ticker?: string;
  type?: string;
  summary?: string;
  tags?: string[];
  headline?: string;
  alternative_names?: string[];
  affiliated_profiles?: Array<{
    network: string;
    id?: string;
    url?: string;
    username?: string;
  }>;
}

export interface PDLCreditsData {
  credits_remaining: number;
  credits_used_today: number;
  daily_credit_limit: number;
  monthly_credits_remaining: number;
  monthly_credit_limit: number;
}

class PeopleDataLabsService {
  private credentials: PDLCredentials | null = null;

  setCredentials(credentials: PDLCredentials) {
    this.credentials = credentials;
  }

  private getHeaders() {
    if (!this.credentials) {
      throw new Error('People Data Labs API credentials not set');
    }
    
    return {
      'X-Api-Key': this.credentials.apiKey,
      'Content-Type': 'application/json',
      'User-Agent': 'Enrich-DDF-Floor-2/1.0',
    };
  }

  // Test API connection
  async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(`${PDL_API_BASE}/person/enrich?min_likelihood=0&name=test`, {
        method: 'GET',
        headers: this.getHeaders(),
      });
      return response.status === 200 || response.status === 404; // 404 is valid (no person found)
    } catch (error) {
      console.error('❌ People Data Labs API connection test failed:', error);
      return false;
    }
  }

  // Get account credits (this is a mock since PDL doesn't have a dedicated credits endpoint)
  async getCredits(): Promise<PDLResponse<PDLCreditsData>> {
    try {
      // Perform a minimal request to check credits in headers
      const response = await fetch(`${PDL_API_BASE}/person/enrich?min_likelihood=0&name=test`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      // PDL returns credits info in headers
      const creditsRemaining = response.headers.get('x-credits-remaining');
      const creditsUsed = response.headers.get('x-credits-used');
      
      return {
        status: 200,
        data: {
          credits_remaining: creditsRemaining ? parseInt(creditsRemaining) : 0,
          credits_used_today: creditsUsed ? parseInt(creditsUsed) : 0,
          daily_credit_limit: 10000, // Default estimate
          monthly_credits_remaining: creditsRemaining ? parseInt(creditsRemaining) : 0,
          monthly_credit_limit: 100000 // Default estimate
        }
      };
    } catch (error) {
      console.error('❌ Failed to get People Data Labs credits:', error);
      return {
        status: 500,
        error: {
          type: 'credits_error',
          message: error instanceof Error ? error.message : 'Unknown error'
        }
      };
    }
  }

  // Enrich person data
  async enrichPerson(request: PersonEnrichRequest): Promise<PDLResponse<PersonData>> {
    try {
      console.log('🔍 Enriching person data with params:', request.params);
      
      const queryParams = new URLSearchParams();
      Object.entries(request.params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });

      const response = await fetch(`${PDL_API_BASE}/person/enrich?${queryParams}`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error?.message || `API request failed: ${response.status}`);
      }

      console.log('✅ Person enrichment successful');
      return {
        status: response.status,
        data: this.transformPersonResponse(data),
        likelihood: data.likelihood,
        credits_remaining: response.headers.get('x-credits-remaining') ? 
          parseInt(response.headers.get('x-credits-remaining')!) : undefined
      };
    } catch (error) {
      console.error('❌ Person enrichment failed:', error);
      return {
        status: 500,
        error: {
          type: 'enrichment_error',
          message: error instanceof Error ? error.message : 'Unknown error'
        }
      };
    }
  }

  // Search for people
  async searchPeople(request: PersonSearchRequest): Promise<PDLResponse<PersonData[]>> {
    try {
      console.log('🔍 Searching for people with query:', request.query);
      
      const response = await fetch(`${PDL_API_BASE}/person/search`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error?.message || `API request failed: ${response.status}`);
      }

      console.log('✅ People search successful');
      return {
        status: response.status,
        data: data.data?.map((person: any) => this.transformPersonResponse(person)) || [],
        credits_remaining: response.headers.get('x-credits-remaining') ? 
          parseInt(response.headers.get('x-credits-remaining')!) : undefined
      };
    } catch (error) {
      console.error('❌ People search failed:', error);
      return {
        status: 500,
        error: {
          type: 'search_error',
          message: error instanceof Error ? error.message : 'Unknown error'
        }
      };
    }
  }

  // Enrich company data
  async enrichCompany(request: CompanyEnrichRequest): Promise<PDLResponse<CompanyData>> {
    try {
      console.log('🏢 Enriching company data with params:', request.params);
      
      const queryParams = new URLSearchParams();
      Object.entries(request.params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });

      const response = await fetch(`${PDL_API_BASE}/company/enrich?${queryParams}`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error?.message || `API request failed: ${response.status}`);
      }

      console.log('✅ Company enrichment successful');
      return {
        status: response.status,
        data: this.transformCompanyResponse(data),
        likelihood: data.likelihood,
        credits_remaining: response.headers.get('x-credits-remaining') ? 
          parseInt(response.headers.get('x-credits-remaining')!) : undefined
      };
    } catch (error) {
      console.error('❌ Company enrichment failed:', error);
      return {
        status: 500,
        error: {
          type: 'enrichment_error',
          message: error instanceof Error ? error.message : 'Unknown error'
        }
      };
    }
  }

  // Search for companies
  async searchCompanies(request: CompanySearchRequest): Promise<PDLResponse<CompanyData[]>> {
    try {
      console.log('🏢 Searching for companies with query:', request.query);
      
      const response = await fetch(`${PDL_API_BASE}/company/search`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error?.message || `API request failed: ${response.status}`);
      }

      console.log('✅ Company search successful');
      return {
        status: response.status,
        data: data.data?.map((company: any) => this.transformCompanyResponse(company)) || [],
        credits_remaining: response.headers.get('x-credits-remaining') ? 
          parseInt(response.headers.get('x-credits-remaining')!) : undefined
      };
    } catch (error) {
      console.error('❌ Company search failed:', error);
      return {
        status: 500,
        error: {
          type: 'search_error',
          message: error instanceof Error ? error.message : 'Unknown error'
        }
      };
    }
  }

  // Transform person response
  private transformPersonResponse(rawData: any): PersonData {
    return {
      id: rawData.id || '',
      full_name: rawData.full_name || `${rawData.first_name || ''} ${rawData.last_name || ''}`.trim(),
      first_name: rawData.first_name || '',
      middle_name: rawData.middle_name,
      last_name: rawData.last_name || '',
      gender: rawData.gender,
      birth_year: rawData.birth_year,
      birth_date: rawData.birth_date,
      linkedin_url: rawData.linkedin_url,
      linkedin_username: rawData.linkedin_username,
      linkedin_id: rawData.linkedin_id,
      facebook_url: rawData.facebook_url,
      facebook_username: rawData.facebook_username,
      facebook_id: rawData.facebook_id,
      twitter_url: rawData.twitter_url,
      twitter_username: rawData.twitter_username,
      github_url: rawData.github_url,
      github_username: rawData.github_username,
      work_email: rawData.work_email,
      personal_emails: rawData.personal_emails || [],
      phone_numbers: rawData.phone_numbers || [],
      mobile_phone: rawData.mobile_phone,
      industry: rawData.industry,
      job_title: rawData.job_title,
      job_title_role: rawData.job_title_role,
      job_title_sub_role: rawData.job_title_sub_role,
      job_title_levels: rawData.job_title_levels || [],
      job_company_name: rawData.job_company_name,
      job_company_website: rawData.job_company_website,
      job_company_size: rawData.job_company_size,
      job_company_industry: rawData.job_company_industry,
      job_company_linkedin_url: rawData.job_company_linkedin_url,
      job_company_linkedin_id: rawData.job_company_linkedin_id,
      job_company_facebook_url: rawData.job_company_facebook_url,
      job_company_twitter_url: rawData.job_company_twitter_url,
      job_company_founded: rawData.job_company_founded,
      job_company_type: rawData.job_company_type,
      job_last_updated: rawData.job_last_updated,
      job_start_date: rawData.job_start_date,
      job_summary: rawData.job_summary,
      location_name: rawData.location_name,
      location_locality: rawData.location_locality,
      location_region: rawData.location_region,
      location_country: rawData.location_country,
      location_continent: rawData.location_continent,
      location_street_address: rawData.location_street_address,
      location_address_line_2: rawData.location_address_line_2,
      location_postal_code: rawData.location_postal_code,
      location_geo: rawData.location_geo,
      education: rawData.education || [],
      experience: rawData.experience || [],
      skills: rawData.skills || [],
      interests: rawData.interests || [],
      languages: rawData.languages || [],
      emails: rawData.emails || [],
      profiles: rawData.profiles || []
    };
  }

  // Transform company response
  private transformCompanyResponse(rawData: any): CompanyData {
    return {
      id: rawData.id || '',
      name: rawData.name || '',
      size: rawData.size,
      employee_count: rawData.employee_count,
      id_source: rawData.id_source,
      founded: rawData.founded,
      industry: rawData.industry,
      naics: rawData.naics || [],
      sic: rawData.sic || [],
      location: rawData.location || {},
      linkedin_url: rawData.linkedin_url,
      linkedin_id: rawData.linkedin_id,
      facebook_url: rawData.facebook_url,
      twitter_url: rawData.twitter_url,
      profiles: rawData.profiles || [],
      website: rawData.website,
      ticker: rawData.ticker,
      type: rawData.type,
      summary: rawData.summary,
      tags: rawData.tags || [],
      headline: rawData.headline,
      alternative_names: rawData.alternative_names || [],
      affiliated_profiles: rawData.affiliated_profiles || []
    };
  }

  // Proxy enrichment through backend
  async enrichPersonViaBackend(request: PersonEnrichRequest): Promise<PDLResponse<PersonData>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/pdl/enrich-person', request);
      
      return {
        status: 200,
        data: response.data.data,
        likelihood: response.data.likelihood,
        credits_remaining: response.data.credits_remaining
      };
    } catch (error: any) {
      return {
        status: 500,
        error: {
          type: 'backend_error',
          message: error.response?.data?.detail || error.message || 'Backend enrichment failed'
        }
      };
    }
  }

  async searchPeopleViaBackend(request: PersonSearchRequest): Promise<PDLResponse<PersonData[]>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/pdl/search-people', request);
      
      return {
        status: 200,
        data: response.data.data,
        credits_remaining: response.data.credits_remaining
      };
    } catch (error: any) {
      return {
        status: 500,
        error: {
          type: 'backend_error',
          message: error.response?.data?.detail || error.message || 'Backend search failed'
        }
      };
    }
  }

  async enrichCompanyViaBackend(request: CompanyEnrichRequest): Promise<PDLResponse<CompanyData>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/pdl/enrich-company', request);
      
      return {
        status: 200,
        data: response.data.data,
        likelihood: response.data.likelihood,
        credits_remaining: response.data.credits_remaining
      };
    } catch (error: any) {
      return {
        status: 500,
        error: {
          type: 'backend_error',
          message: error.response?.data?.detail || error.message || 'Backend enrichment failed'
        }
      };
    }
  }

  async searchCompaniesViaBackend(request: CompanySearchRequest): Promise<PDLResponse<CompanyData[]>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/pdl/search-companies', request);
      
      return {
        status: 200,
        data: response.data.data,
        credits_remaining: response.data.credits_remaining
      };
    } catch (error: any) {
      return {
        status: 500,
        error: {
          type: 'backend_error',
          message: error.response?.data?.detail || error.message || 'Backend search failed'
        }
      };
    }
  }
}

// Create singleton instance
export const peopleDataLabsService = new PeopleDataLabsService();

// Utility functions for validation
export const validatePersonEnrichParams = (params: Partial<PersonEnrichRequest['params']>): boolean => {
  const hasIdentifier = !!(
    params.name || 
    params.email || 
    params.phone || 
    params.linkedin_url || 
    params.linkedin_username ||
    (params.first_name && params.last_name)
  );
  return hasIdentifier;
};

export const validateCompanyEnrichParams = (params: Partial<CompanyEnrichRequest['params']>): boolean => {
  const hasIdentifier = !!(
    params.name || 
    params.website || 
    params.linkedin_url || 
    params.ticker
  );
  return hasIdentifier;
};

export const validateEmail = (email: string): boolean => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
};

export const validateLinkedInUrl = (url: string): boolean => {
  const linkedinPattern = /^https?:\/\/(www\.)?linkedin\.com\/(in|company)\/[a-zA-Z0-9-]+\/?$/;
  return linkedinPattern.test(url);
};

export const validatePhoneNumber = (phone: string): boolean => {
  const phonePattern = /^\+?[\d\s\-\(\)]+$/;
  return phonePattern.test(phone.replace(/\s/g, '')) && phone.replace(/\D/g, '').length >= 10;
}; 