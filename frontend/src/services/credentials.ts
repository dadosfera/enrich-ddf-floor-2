export type IntegrationName = 'bigdata' | 'wiza' | 'surfe' | 'pdl';

export interface StoredCredentials {
  bigdata?: string;
  wiza?: string;
  surfe?: string;
  pdl?: string;
}

const STORAGE_KEY = 'enrich-ddf-integrations-credentials';

export const credentialsService = {
  getAll(): StoredCredentials {
    if (typeof window === 'undefined') return {};
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    try {
      return JSON.parse(raw) as StoredCredentials;
    } catch {
      return {};
    }
  },
  get(key: IntegrationName): string | undefined {
    return this.getAll()[key];
  },
  save(key: IntegrationName, value: string) {
    const current = this.getAll();
    current[key] = value;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  },
  remove(key: IntegrationName) {
    const current = this.getAll();
    delete current[key];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  }
};
