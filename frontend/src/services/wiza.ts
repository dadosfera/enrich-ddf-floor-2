import { apiClient } from './api';

// Wiza API Configuration
const WIZA_API_BASE = 'https://api.wiza.co/api/v1';

export interface WizaCredentials {
  apiKey: string;
}

export interface LinkedInProfileRequest {
  linkedin_url: string;
  include_emails?: boolean;
  include_phone?: boolean;
}

export interface EmailFinderRequest {
  first_name: string;
  last_name: string;
  company_domain: string;
  linkedin_url?: string;
}

export interface CompanyEnrichmentRequest {
  company_domain?: string;
  company_name?: string;
  linkedin_url?: string;
}

export interface WizaResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  errors?: string[];
  credits_used?: number;
  credits_remaining?: number;
}

export interface LinkedInProfileData {
  linkedin_url: string;
  first_name: string;
  last_name: string;
  full_name: string;
  headline?: string;
  summary?: string;
  location?: string;
  industry?: string;
  current_company?: {
    name: string;
    title: string;
    duration?: string;
    linkedin_url?: string;
  };
  previous_companies?: Array<{
    name: string;
    title: string;
    duration?: string;
    linkedin_url?: string;
  }>;
  education?: Array<{
    school: string;
    degree?: string;
    field_of_study?: string;
    duration?: string;
  }>;
  skills?: string[];
  emails?: Array<{
    email: string;
    type: 'work' | 'personal';
    confidence: number;
    source: string;
  }>;
  phones?: Array<{
    number: string;
    type: 'work' | 'mobile' | 'home';
    confidence: number;
  }>;
  social_profiles?: {
    twitter?: string;
    facebook?: string;
    instagram?: string;
    github?: string;
  };
  profile_image_url?: string;
  connections_count?: number;
  followers_count?: number;
}

export interface EmailFinderData {
  email: string;
  confidence: number;
  type: 'work' | 'personal';
  source: string;
  verification_status: 'valid' | 'invalid' | 'unknown' | 'risky';
  first_name: string;
  last_name: string;
  company_name?: string;
  title?: string;
  linkedin_url?: string;
}

export interface CompanyEnrichmentData {
  company_name: string;
  domain: string;
  linkedin_url?: string;
  website?: string;
  industry?: string;
  company_size?: string;
  founded_year?: number;
  headquarters?: {
    city: string;
    state?: string;
    country: string;
    address?: string;
  };
  description?: string;
  specialties?: string[];
  employee_count?: number;
  revenue_range?: string;
  social_profiles?: {
    linkedin?: string;
    twitter?: string;
    facebook?: string;
    instagram?: string;
  };
  employees?: Array<{
    name: string;
    title: string;
    linkedin_url?: string;
    email?: string;
  }>;
  technologies?: string[];
  company_type?: string;
  stock_symbol?: string;
}

class WizaService {
  private credentials: WizaCredentials | null = null;

  setCredentials(credentials: WizaCredentials) {
    this.credentials = credentials;
  }

  private getHeaders() {
    if (!this.credentials) {
      throw new Error('Wiza API credentials not set');
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
      const response = await fetch(`${WIZA_API_BASE}/credits`, {
        method: 'GET',
        headers: this.getHeaders(),
      });
      return response.ok;
    } catch (error) {
      console.error('❌ Wiza API connection test failed:', error);
      return false;
    }
  }

  // Get account credits
  async getCredits(): Promise<WizaResponse<{ credits: number }>> {
    try {
      const response = await fetch(`${WIZA_API_BASE}/credits`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      return {
        success: true,
        data: { credits: data.credits || 0 },
        message: 'Credits retrieved successfully'
      };
    } catch (error) {
      console.error('❌ Failed to get Wiza credits:', error);
      return {
        success: false,
        data: { credits: 0 },
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Enrich LinkedIn profile
  async enrichLinkedInProfile(request: LinkedInProfileRequest): Promise<WizaResponse<LinkedInProfileData>> {
    try {
      console.log('🔍 Enriching LinkedIn profile:', request.linkedin_url);
      
      const response = await fetch(`${WIZA_API_BASE}/enrich/profile`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          linkedin_url: request.linkedin_url,
          include_emails: request.include_emails ?? true,
          include_phone: request.include_phone ?? true,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      console.log('✅ LinkedIn profile enrichment successful');
      return {
        success: true,
        data: this.transformLinkedInProfileResponse(data),
        message: 'LinkedIn profile enriched successfully',
        credits_used: data.credits_used,
        credits_remaining: data.credits_remaining
      };
    } catch (error) {
      console.error('❌ LinkedIn profile enrichment failed:', error);
      return {
        success: false,
        data: {} as LinkedInProfileData,
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Find email for a person
  async findEmail(request: EmailFinderRequest): Promise<WizaResponse<EmailFinderData[]>> {
    try {
      console.log('📧 Finding email for:', `${request.first_name} ${request.last_name} @ ${request.company_domain}`);
      
      const response = await fetch(`${WIZA_API_BASE}/enrich/email`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      console.log('✅ Email finding successful');
      return {
        success: true,
        data: Array.isArray(data.emails) ? data.emails : [data],
        message: 'Email(s) found successfully',
        credits_used: data.credits_used,
        credits_remaining: data.credits_remaining
      };
    } catch (error) {
      console.error('❌ Email finding failed:', error);
      return {
        success: false,
        data: [],
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Enrich company data
  async enrichCompany(request: CompanyEnrichmentRequest): Promise<WizaResponse<CompanyEnrichmentData>> {
    try {
      console.log('🏢 Enriching company:', request.company_domain || request.company_name);
      
      const response = await fetch(`${WIZA_API_BASE}/enrich/company`, {
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
        data: this.transformCompanyResponse(data),
        message: 'Company enriched successfully',
        credits_used: data.credits_used,
        credits_remaining: data.credits_remaining
      };
    } catch (error) {
      console.error('❌ Company enrichment failed:', error);
      return {
        success: false,
        data: {} as CompanyEnrichmentData,
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  // Transform LinkedIn profile response to standardized format
  private transformLinkedInProfileResponse(rawData: any): LinkedInProfileData {
    return {
      linkedin_url: rawData.linkedin_url || '',
      first_name: rawData.first_name || '',
      last_name: rawData.last_name || '',
      full_name: rawData.full_name || `${rawData.first_name} ${rawData.last_name}`,
      headline: rawData.headline,
      summary: rawData.summary,
      location: rawData.location,
      industry: rawData.industry,
      current_company: rawData.current_company ? {
        name: rawData.current_company.name,
        title: rawData.current_company.title,
        duration: rawData.current_company.duration,
        linkedin_url: rawData.current_company.linkedin_url
      } : undefined,
      previous_companies: rawData.previous_companies?.map((company: any) => ({
        name: company.name,
        title: company.title,
        duration: company.duration,
        linkedin_url: company.linkedin_url
      })) || [],
      education: rawData.education?.map((edu: any) => ({
        school: edu.school,
        degree: edu.degree,
        field_of_study: edu.field_of_study,
        duration: edu.duration
      })) || [],
      skills: rawData.skills || [],
      emails: rawData.emails?.map((email: any) => ({
        email: email.email,
        type: email.type || 'work',
        confidence: email.confidence || 0,
        source: email.source || 'wiza'
      })) || [],
      phones: rawData.phones?.map((phone: any) => ({
        number: phone.number,
        type: phone.type || 'work',
        confidence: phone.confidence || 0
      })) || [],
      social_profiles: rawData.social_profiles || {},
      profile_image_url: rawData.profile_image_url,
      connections_count: rawData.connections_count,
      followers_count: rawData.followers_count
    };
  }

  // Transform company response to standardized format
  private transformCompanyResponse(rawData: any): CompanyEnrichmentData {
    return {
      company_name: rawData.company_name || rawData.name || '',
      domain: rawData.domain || rawData.website?.replace(/^https?:\/\//, '') || '',
      linkedin_url: rawData.linkedin_url,
      website: rawData.website,
      industry: rawData.industry,
      company_size: rawData.company_size,
      founded_year: rawData.founded_year,
      headquarters: rawData.headquarters ? {
        city: rawData.headquarters.city || '',
        state: rawData.headquarters.state,
        country: rawData.headquarters.country || '',
        address: rawData.headquarters.address
      } : undefined,
      description: rawData.description,
      specialties: rawData.specialties || [],
      employee_count: rawData.employee_count,
      revenue_range: rawData.revenue_range,
      social_profiles: rawData.social_profiles || {},
      employees: rawData.employees?.map((emp: any) => ({
        name: emp.name,
        title: emp.title,
        linkedin_url: emp.linkedin_url,
        email: emp.email
      })) || [],
      technologies: rawData.technologies || [],
      company_type: rawData.company_type,
      stock_symbol: rawData.stock_symbol
    };
  }

  // Proxy enrichment through backend
  async enrichProfileViaBackend(linkedinUrl: string): Promise<WizaResponse<LinkedInProfileData>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/wiza/enrich-profile', {
        linkedin_url: linkedinUrl
      });
      
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
        data: {} as LinkedInProfileData,
        errors: [error.response?.data?.detail || error.message || 'Backend enrichment failed']
      };
    }
  }

  async findEmailViaBackend(request: EmailFinderRequest): Promise<WizaResponse<EmailFinderData[]>> {
    try {
      const response = await apiClient.post('/api/v1/integrations/wiza/find-email', request);
      
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
        errors: [error.response?.data?.detail || error.message || 'Backend email finding failed']
      };
    }
  }
}

// Create singleton instance
export const wizaService = new WizaService();

// Utility functions for LinkedIn URL validation
export const validateLinkedInUrl = (url: string): boolean => {
  const linkedinPattern = /^https?:\/\/(www\.)?linkedin\.com\/(in|company)\/[a-zA-Z0-9-]+\/?$/;
  return linkedinPattern.test(url);
};

export const validateEmailDomain = (domain: string): boolean => {
  const domainPattern = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/;
  return domainPattern.test(domain);
};

export const extractLinkedInId = (url: string): string | null => {
  const match = url.match(/linkedin\.com\/(in|company)\/([a-zA-Z0-9-]+)/);
  return match ? match[2] : null;
}; 