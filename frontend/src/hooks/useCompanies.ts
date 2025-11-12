import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { companiesService } from '../services/companies';
import type { CreateCompanyRequest } from '../types/company';

// Query keys
export const companyKeys = {
  all: ['companies'] as const,
  lists: () => [...companyKeys.all, 'list'] as const,
  list: (filters: string) => [...companyKeys.lists(), { filters }] as const,
  details: () => [...companyKeys.all, 'detail'] as const,
  detail: (id: number) => [...companyKeys.details(), id] as const,
};

// Get all companies
export const useCompanies = () => {
  return useQuery({
    queryKey: companyKeys.lists(),
    queryFn: companiesService.getAll,
  });
};

// Get company by ID
export const useCompany = (id: number) => {
  return useQuery({
    queryKey: companyKeys.detail(id),
    queryFn: () => companiesService.getById(id),
    enabled: !!id,
  });
};

// Search companies
export const useSearchCompanies = (query: string) => {
  return useQuery({
    queryKey: companyKeys.list(query),
    queryFn: () => companiesService.search(query),
    enabled: !!query && query.length > 0,
  });
};

// Create company mutation
export const useCreateCompany = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: companiesService.create,
    onSuccess: () => {
      // Invalidate and refetch companies list
      queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
    },
  });
};

// Update company mutation
export const useUpdateCompany = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<CreateCompanyRequest> }) =>
      companiesService.update(id, data),
    onSuccess: (_, { id }) => {
      // Invalidate specific company and list
      queryClient.invalidateQueries({ queryKey: companyKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
    },
  });
};

// Delete company mutation
export const useDeleteCompany = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: companiesService.delete,
    onSuccess: () => {
      // Invalidate companies list
      queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
    },
  });
};
