import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Grid, 
  Button, 
  TextField,
  CircularProgress,
  Alert,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip
} from '@mui/material';
import { 
  Add as AddIcon, 
  Search as SearchIcon, 
  Edit as EditIcon,
  Delete as DeleteIcon,
  Category as CategoryIcon,
  AttachMoney as PriceIcon,
  Inventory as InventoryIcon
} from '@mui/icons-material';
import { useProducts, useCreateProduct, useUpdateProduct, useDeleteProduct } from '../hooks/useProducts';
import type { Product, CreateProductRequest } from '../types/product';

const ProductCard: React.FC<{ product: Product; onEdit: (product: Product) => void; onDelete: (id: number) => void }> = ({ 
  product, 
  onEdit, 
  onDelete 
}) => (
  <Card sx={{ height: '100%', position: 'relative' }}>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
        <Typography variant="h6" component="div">
          {product.name}
        </Typography>
        <Box>
          <Tooltip title="Edit">
            <IconButton size="small" onClick={() => onEdit(product)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton size="small" onClick={() => onDelete(product.id)} color="error">
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      {product.description && (
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {product.description}
        </Typography>
      )}
      
      {product.price && (
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <PriceIcon sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
          <Typography variant="body2" color="text.secondary">
            ${product.price.toFixed(2)}
          </Typography>
        </Box>
      )}
      
      {product.sku && (
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <InventoryIcon sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
          <Typography variant="body2" color="text.secondary">
            SKU: {product.sku}
          </Typography>
        </Box>
      )}
      
      {product.category && (
        <Box sx={{ mt: 2 }}>
          <Chip 
            icon={<CategoryIcon />} 
            label={product.category} 
            size="small" 
            variant="outlined"
            color="primary"
          />
        </Box>
      )}
    </CardContent>
  </Card>
);

const ProductFormDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  product?: Product;
}> = ({ open, onClose, product }) => {
  const [formData, setFormData] = useState<CreateProductRequest>({
    name: product?.name || '',
    description: product?.description || '',
    price: product?.price || undefined,
    category: product?.category || '',
    sku: product?.sku || '',
  });

  const createMutation = useCreateProduct();
  const updateMutation = useUpdateProduct();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (product) {
        await updateMutation.mutateAsync({ id: product.id, data: formData });
      } else {
        await createMutation.mutateAsync(formData);
      }
      onClose();
    } catch (error) {
      console.error('Error saving product:', error);
    }
  };

  const handleChange = (field: keyof CreateProductRequest) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = field === 'price' ? (e.target.value ? parseFloat(e.target.value) : undefined) : e.target.value;
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>{product ? 'Edit Product' : 'Add New Product'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Product Name"
                value={formData.name}
                onChange={handleChange('name')}
                required
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Description"
                multiline
                rows={3}
                value={formData.description}
                onChange={handleChange('description')}
              />
            </Grid>
            <Grid size={6}>
              <TextField
                fullWidth
                label="Price"
                type="number"
                slotProps={{
                  htmlInput: { step: "0.01" }
                }}
                value={formData.price || ''}
                onChange={handleChange('price')}
                InputProps={{
                  startAdornment: '$',
                }}
              />
            </Grid>
            <Grid size={6}>
              <TextField
                fullWidth
                label="SKU"
                value={formData.sku}
                onChange={handleChange('sku')}
                helperText="Stock Keeping Unit"
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Category"
                value={formData.category}
                onChange={handleChange('category')}
                helperText="Product category"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button 
            type="submit" 
            variant="contained"
            disabled={createMutation.isPending || updateMutation.isPending}
          >
            {product ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export const Products: React.FC = () => {
  const { data: products, isLoading, error } = useProducts();
  const deleteMutation = useDeleteProduct();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | undefined>();

  const filteredProducts = products?.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.category?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.sku?.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setDialogOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await deleteMutation.mutateAsync(id);
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingProduct(undefined);
  };

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Error loading products: {error.message}
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Products
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />}
          onClick={() => setDialogOpen(true)}
        >
          Add Product
        </Button>
      </Box>

      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search products..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
        />
      </Box>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredProducts.map((product) => (
            <Grid size={12} sm={6} md={4} lg={3} key={product.id}>
              <ProductCard 
                product={product} 
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            </Grid>
          ))}
        </Grid>
      )}

      {!isLoading && filteredProducts.length === 0 && (
        <Box sx={{ textAlign: 'center', p: 3 }}>
          <Typography variant="body1" color="text.secondary">
            {searchTerm ? 'No products found matching your search.' : 'No products found.'}
          </Typography>
        </Box>
      )}

      <ProductFormDialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        product={editingProduct}
      />
    </Box>
  );
}; 