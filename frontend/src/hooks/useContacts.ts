import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { contactsService } from '../services/contacts';
import type { CreateContactRequest } from '../types/contact';

// Query keys
export const contactKeys = {
  all: ['contacts'] as const,
  lists: () => [...contactKeys.all, 'list'] as const,
  list: (filters: string) => [...contactKeys.lists(), { filters }] as const,
  details: () => [...contactKeys.all, 'detail'] as const,
  detail: (id: number) => [...contactKeys.details(), id] as const,
  byCompany: (companyId: number) => [...contactKeys.all, 'company', companyId] as const,
};

// Get all contacts
export const useContacts = () => {
  return useQuery({
    queryKey: contactKeys.lists(),
    queryFn: contactsService.getAll,
  });
};

// Get contact by ID
export const useContact = (id: number) => {
  return useQuery({
    queryKey: contactKeys.detail(id),
    queryFn: () => contactsService.getById(id),
    enabled: !!id,
  });
};

// Search contacts
export const useSearchContacts = (query: string) => {
  return useQuery({
    queryKey: contactKeys.list(query),
    queryFn: () => contactsService.search(query),
    enabled: !!query && query.length > 0,
  });
};

// Get contacts by company
export const useContactsByCompany = (companyId: number) => {
  return useQuery({
    queryKey: contactKeys.byCompany(companyId),
    queryFn: () => contactsService.getByCompany(companyId),
    enabled: !!companyId,
  });
};

// Create contact mutation
export const useCreateContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: contactsService.create,
    onSuccess: () => {
      // Invalidate and refetch contacts list
      queryClient.invalidateQueries({ queryKey: contactKeys.lists() });
    },
  });
};

// Update contact mutation
export const useUpdateContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<CreateContactRequest> }) =>
      contactsService.update(id, data),
    onSuccess: (_, { id }) => {
      // Invalidate specific contact and list
      queryClient.invalidateQueries({ queryKey: contactKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: contactKeys.lists() });
    },
  });
};

// Delete contact mutation
export const useDeleteContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: contactsService.delete,
    onSuccess: () => {
      // Invalidate contacts list
      queryClient.invalidateQueries({ queryKey: contactKeys.lists() });
    },
  });
}; 