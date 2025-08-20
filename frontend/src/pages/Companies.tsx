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
  Language as WebsiteIcon,
  Business as IndustryIcon
} from '@mui/icons-material';
import { useCompanies, useCreateCompany, useUpdateCompany, useDeleteCompany } from '../hooks/useCompanies';
import type { Company, CreateCompanyRequest } from '../types/company';

const CompanyCard: React.FC<{ company: Company; onEdit: (company: Company) => void; onDelete: (id: number) => void }> = ({ 
  company, 
  onEdit, 
  onDelete 
}) => (
  <Card sx={{ height: '100%', position: 'relative' }}>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
        <Typography variant="h6" component="div">
          {company.name}
        </Typography>
        <Box>
          <Tooltip title="Edit">
            <IconButton size="small" onClick={() => onEdit(company)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton size="small" onClick={() => onDelete(company.id)} color="error">
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      {company.industry && (
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <IndustryIcon sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
          <Typography variant="body2" color="text.secondary">
            {company.industry}
          </Typography>
        </Box>
      )}
      
      {company.website && (
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <WebsiteIcon sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
          <Typography variant="body2" color="text.secondary">
            {company.website}
          </Typography>
        </Box>
      )}
      
      {company.description && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          {company.description}
        </Typography>
      )}
    </CardContent>
  </Card>
);

const CompanyFormDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  company?: Company;
}> = ({ open, onClose, company }) => {
  const [formData, setFormData] = useState<CreateCompanyRequest>({
    name: company?.name || '',
    industry: company?.industry || '',
    website: company?.website || '',
    description: company?.description || '',
  });

  const createMutation = useCreateCompany();
  const updateMutation = useUpdateCompany();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (company) {
        await updateMutation.mutateAsync({ id: company.id, data: formData });
      } else {
        await createMutation.mutateAsync(formData);
      }
      onClose();
    } catch (error) {
      console.error('Error saving company:', error);
    }
  };

  const handleChange = (field: keyof CreateCompanyRequest) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }));
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>{company ? 'Edit Company' : 'Add New Company'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Company Name"
                value={formData.name}
                onChange={handleChange('name')}
                required
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Industry"
                value={formData.industry}
                onChange={handleChange('industry')}
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Website"
                value={formData.website}
                onChange={handleChange('website')}
                placeholder="https://example.com"
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
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button 
            type="submit" 
            variant="contained"
            disabled={createMutation.isPending || updateMutation.isPending}
          >
            {company ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export const Companies: React.FC = () => {
  const { data: companies, isLoading, error } = useCompanies();
  const deleteMutation = useDeleteCompany();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCompany, setEditingCompany] = useState<Company | undefined>();

  const filteredCompanies = companies?.filter(company =>
    company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    company.industry?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    company.description?.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const handleEdit = (company: Company) => {
    setEditingCompany(company);
    setDialogOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this company?')) {
      try {
        await deleteMutation.mutateAsync(id);
      } catch (error) {
        console.error('Error deleting company:', error);
      }
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingCompany(undefined);
  };

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Error loading companies: {error.message}
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Companies
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />}
          onClick={() => setDialogOpen(true)}
        >
          Add Company
        </Button>
      </Box>

      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search companies..."
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
          {filteredCompanies.map((company) => (
            <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={company.id}>
              <CompanyCard 
                company={company} 
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            </Grid>
          ))}
        </Grid>
      )}

      {!isLoading && filteredCompanies.length === 0 && (
        <Box sx={{ textAlign: 'center', p: 3 }}>
          <Typography variant="body1" color="text.secondary">
            {searchTerm ? 'No companies found matching your search.' : 'No companies found.'}
          </Typography>
        </Box>
      )}

      <CompanyFormDialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        company={editingCompany}
      />
    </Box>
  );
}; 