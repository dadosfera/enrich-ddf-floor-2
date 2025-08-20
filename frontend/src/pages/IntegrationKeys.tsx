import React, { useEffect, useState } from 'react';
import { Box, Typography, Card, CardContent, Grid, TextField, Button, IconButton, Tooltip } from '@mui/material';
import { credentialsService, StoredCredentials, IntegrationName } from '../services/credentials';
import { VisibilityOff as HideIcon, Save as SaveIcon, Delete as DeleteIcon } from '@mui/icons-material';

const integrationLabels: Record<IntegrationName, string> = {
  bigdata: 'BigData Corp',
  wiza: 'Wiza',
  surfe: 'Surfe',
  pdl: 'People Data Labs'
};

const IntegrationKeys: React.FC = () => {
  const [credentials, setCredentials] = useState<StoredCredentials>({});
  const [editing, setEditing] = useState<IntegrationName | null>(null);
  const [tempValue, setTempValue] = useState('');

  useEffect(() => {
    setCredentials(credentialsService.getAll());
  }, []);

  const handleEdit = (name: IntegrationName) => {
    setEditing(name);
    setTempValue(credentials[name] || '');
  };

  const handleSave = (name: IntegrationName) => {
    credentialsService.save(name, tempValue.trim());
    setCredentials(credentialsService.getAll());
    setEditing(null);
  };

  const handleDelete = (name: IntegrationName) => {
    credentialsService.remove(name);
    setCredentials(credentialsService.getAll());
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>API Keys</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Manage and securely store your integration API keys locally in your browser. Keys are saved in localStorage.
      </Typography>
      <Grid container spacing={2}>
        {(Object.keys(integrationLabels) as IntegrationName[]).map((name) => (
          <Grid item xs={12} sm={6} md={4} key={name}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>{integrationLabels[name]}</Typography>
                {editing === name ? (
                  <TextField
                    fullWidth
                    label="API Key"
                    type="password"
                    value={tempValue}
                    onChange={(e) => setTempValue(e.target.value)}
                    sx={{ mb: 2 }}
                  />
                ) : (
                  <TextField
                    fullWidth
                    label="API Key"
                    type="password"
                    value={credentials[name] || ''}
                    InputProps={{ readOnly: true }}
                    sx={{ mb: 2 }}
                  />
                )}
                {editing === name ? (
                  <Button
                    variant="contained"
                    startIcon={<SaveIcon />}
                    onClick={() => handleSave(name)}
                    disabled={!tempValue.trim()}
                  >
                    Save
                  </Button>
                ) : (
                  <Box>
                    <Button variant="outlined" onClick={() => handleEdit(name)} sx={{ mr: 1 }}>Edit</Button>
                    {credentials[name] && (
                      <Tooltip title="Remove key">
                        <IconButton color="error" onClick={() => handleDelete(name)}>
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default IntegrationKeys; 