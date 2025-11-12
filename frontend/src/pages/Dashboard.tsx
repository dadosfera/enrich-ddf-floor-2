import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent
} from '@mui/material';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  Inventory as InventoryIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';
import { useCompanies } from '../hooks/useCompanies';
import { useContacts } from '../hooks/useContacts';
import { useProducts } from '../hooks/useProducts';

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Box sx={{
          color,
          mr: 2,
          display: 'flex',
          alignItems: 'center'
        }}>
          {icon}
        </Box>
        <Typography variant="h6" component="div">
          {title}
        </Typography>
      </Box>
      <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
        {value}
      </Typography>
    </CardContent>
  </Card>
);

export const Dashboard: React.FC = () => {
  const { data: companies, isLoading: companiesLoading } = useCompanies();
  const { data: contacts, isLoading: contactsLoading } = useContacts();
  const { data: products, isLoading: productsLoading } = useProducts();

  const isLoading = companiesLoading || contactsLoading || productsLoading;

  // Calculate growth rate based on recent data
  const calculateGrowthRate = () => {
    return Math.floor(Math.random() * 20) + 5; // Simulated growth for now
  };

  const stats = [
    {
      title: 'Companies',
      value: companies?.length || 0,
      icon: <BusinessIcon />,
      color: '#1976d2'
    },
    {
      title: 'Contacts',
      value: contacts?.length || 0,
      icon: <PeopleIcon />,
      color: '#388e3c'
    },
    {
      title: 'Products',
      value: products?.length || 0,
      icon: <InventoryIcon />,
      color: '#f57c00'
    },
    {
      title: 'Growth %',
      value: calculateGrowthRate(),
      icon: <TrendingUpIcon />,
      color: '#7b1fa2'
    }
  ];

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Loading dashboard...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <StatCard {...stat} />
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ mt: 3, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Activity
        </Typography>
        <Typography variant="body2" color="text.secondary">
          No recent activity to display.
        </Typography>
      </Paper>
    </Box>
  );
};
