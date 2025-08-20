import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { productsService } from '../services/products';
import type { CreateProductRequest } from '../types/product';

// Query keys
export const productKeys = {
  all: ['products'] as const,
  lists: () => [...productKeys.all, 'list'] as const,
  list: (filters: string) => [...productKeys.lists(), { filters }] as const,
  details: () => [...productKeys.all, 'detail'] as const,
  detail: (id: number) => [...productKeys.details(), id] as const,
  byCategory: (category: string) => [...productKeys.all, 'category', category] as const,
};

// Get all products
export const useProducts = () => {
  return useQuery({
    queryKey: productKeys.lists(),
    queryFn: productsService.getAll,
  });
};

// Get product by ID
export const useProduct = (id: number) => {
  return useQuery({
    queryKey: productKeys.detail(id),
    queryFn: () => productsService.getById(id),
    enabled: !!id,
  });
};

// Search products
export const useSearchProducts = (query: string) => {
  return useQuery({
    queryKey: productKeys.list(query),
    queryFn: () => productsService.search(query),
    enabled: !!query && query.length > 0,
  });
};

// Get products by category
export const useProductsByCategory = (category: string) => {
  return useQuery({
    queryKey: productKeys.byCategory(category),
    queryFn: () => productsService.getByCategory(category),
    enabled: !!category,
  });
};

// Create product mutation
export const useCreateProduct = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: productsService.create,
    onSuccess: () => {
      // Invalidate and refetch products list
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
    },
  });
};

// Update product mutation
export const useUpdateProduct = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<CreateProductRequest> }) =>
      productsService.update(id, data),
    onSuccess: (_, { id }) => {
      // Invalidate specific product and list
      queryClient.invalidateQueries({ queryKey: productKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
    },
  });
};

// Delete product mutation
export const useDeleteProduct = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: productsService.delete,
    onSuccess: () => {
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
    },
  });
}; 