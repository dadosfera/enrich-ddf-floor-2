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
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import { 
  Api as ApiIcon,
  Person as PersonIcon,
  Business as BusinessIcon,
  Search as SearchIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  ExpandMore as ExpandMoreIcon,
  Settings as SettingsIcon,
  Security as SecurityIcon,
  LinkedIn as LinkedInIcon,
  Email as EmailIcon,
  AccountBalance as CreditIcon,
  Groups as GroupsIcon,
  Phone as PhoneIcon,
  FilterList as FilterIcon,
  Storage as DatabaseIcon,
  Work as WorkIcon
} from '@mui/icons-material';
import { 
  bigDataCorpService, 
  validateCPF, 
  validateCNPJ, 
  formatCPF, 
  formatCNPJ,
  type CPFPersonData,
  type CNPJCompanyData,
  type BigDataCorpCredentials
} from '../services/bigdata-corp';
import {
  wizaService,
  validateLinkedInUrl,
  validateEmailDomain,
  type LinkedInProfileData,
  type EmailFinderData,
  type CompanyEnrichmentData,
  type WizaCredentials
} from '../services/wiza';
import {
  surfeService,
  validatePersonData,
  validateCompanyData,
  validateEmailAddress,
  validatePhoneNumber,
  type PersonSearchData,
  type PersonEnrichData,
  type CompanySearchData,
  type CompanyEnrichData as SurfeCompanyEnrichData,
  type SurfeCredentials,
  type SurfeCreditsData
} from '../services/surfe';
import {
  peopleDataLabsService,
  validatePersonEnrichParams,
  validateCompanyEnrichParams,
  validateEmail,
  type PersonData as PDLPersonData,
  type CompanyData as PDLCompanyData,
  type PDLCredentials,
  type PDLCreditsData,
  type PersonEnrichRequest,
  type PersonSearchRequest,
  type CompanyEnrichRequest,
  type CompanySearchRequest
} from '../services/people-data-labs';

const IntegrationCard: React.FC<{
  title: string;
  description: string;
  icon: React.ReactNode;
  status: 'connected' | 'disconnected' | 'error';
  onConfigure: () => void;
}> = ({ title, description, icon, status, onConfigure }) => (
  <Card sx={{ height: '100%', position: 'relative' }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        {icon}
        <Typography variant="h6" component="div" sx={{ ml: 1 }}>
          {title}
        </Typography>
        <Box sx={{ ml: 'auto' }}>
          <Chip 
            label={status} 
            color={status === 'connected' ? 'success' : status === 'error' ? 'error' : 'default'}
            size="small"
            icon={status === 'connected' ? <CheckIcon /> : <ErrorIcon />}
          />
        </Box>
      </Box>
      
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        {description}
      </Typography>
      
      <Button 
        variant="outlined" 
        startIcon={<SettingsIcon />}
        onClick={onConfigure}
        fullWidth
      >
        Configure
      </Button>
    </CardContent>
  </Card>
);

const BigDataCorpConfigDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  onSave: (credentials: BigDataCorpCredentials) => void;
}> = ({ open, onClose, onSave }) => {
  const [credentials, setCredentials] = useState<BigDataCorpCredentials>({
    apiKey: '',
    apiSecret: ''
  });

  const handleSave = () => {
    if (credentials.apiKey && credentials.apiSecret) {
      onSave(credentials);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <SecurityIcon sx={{ mr: 1 }} />
          BigData Corp API Configuration
        </Box>
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          Enter your BigData Corp API credentials. These will be stored securely and used for data enrichment.
        </Alert>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={12}>
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={credentials.apiKey}
              onChange={(e) => setCredentials(prev => ({ ...prev, apiKey: e.target.value }))}
              required
            />
          </Grid>
          <Grid size={12}>
            <TextField
              fullWidth
              label="API Secret"
              type="password"
              value={credentials.apiSecret}
              onChange={(e) => setCredentials(prev => ({ ...prev, apiSecret: e.target.value }))}
              required
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button 
          variant="contained" 
          onClick={handleSave}
          disabled={!credentials.apiKey || !credentials.apiSecret}
        >
          Save & Test Connection
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const WizaConfigDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  onSave: (credentials: WizaCredentials) => void;
}> = ({ open, onClose, onSave }) => {
  const [credentials, setCredentials] = useState<WizaCredentials>({
    apiKey: ''
  });
  const [credits, setCredits] = useState<number | null>(null);
  const [testing, setTesting] = useState(false);

  const handleSave = async () => {
    if (credentials.apiKey) {
      setTesting(true);
      try {
        wizaService.setCredentials(credentials);
        const creditsResponse = await wizaService.getCredits();
        if (creditsResponse.success) {
          setCredits(creditsResponse.data.credits);
          onSave(credentials);
          onClose();
        } else {
          throw new Error('Invalid API key');
        }
      } catch (error) {
        console.error('Failed to validate Wiza API key:', error);
      } finally {
        setTesting(false);
      }
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <LinkedInIcon sx={{ mr: 1 }} />
          Wiza API Configuration
        </Box>
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          Enter your Wiza API key. This will be used for LinkedIn profile enrichment and email finding.
          Visit <a href="https://wiza.co/api-docs" target="_blank" rel="noopener noreferrer">Wiza API Docs</a> for more information.
        </Alert>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={12}>
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={credentials.apiKey}
              onChange={(e) => setCredentials(prev => ({ ...prev, apiKey: e.target.value }))}
              required
              helperText="Get your API key from Wiza dashboard"
            />
          </Grid>
          {credits !== null && (
            <Grid size={12}>
              <Alert severity="success">
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <CreditIcon sx={{ mr: 1 }} />
                  Available Credits: {credits}
                </Box>
              </Alert>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button 
          variant="contained" 
          onClick={handleSave}
          disabled={!credentials.apiKey || testing}
          startIcon={testing ? <CircularProgress size={20} /> : null}
        >
          {testing ? 'Testing...' : 'Save & Test Connection'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const EnrichmentDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  type: 'cpf' | 'cnpj';
}> = ({ open, onClose, type }) => {
  const [document, setDocument] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CPFPersonData | CNPJCompanyData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleEnrich = async () => {
    if (!document) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      if (type === 'cpf') {
        if (!validateCPF(document)) {
          throw new Error('Invalid CPF format');
        }
        const response = await bigDataCorpService.enrichContactByCPF({ document });
        if (response.success) {
          setResult(response.data);
        } else {
          throw new Error(response.errors?.[0] || 'Enrichment failed');
        }
      } else {
        if (!validateCNPJ(document)) {
          throw new Error('Invalid CNPJ format');
        }
        const response = await bigDataCorpService.enrichCompanyByCNPJ({ document });
        if (response.success) {
          setResult(response.data);
        } else {
          throw new Error(response.errors?.[0] || 'Enrichment failed');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setDocument('');
    setResult(null);
    setError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        Enrich {type === 'cpf' ? 'Contact (CPF)' : 'Company (CNPJ)'}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={12} sm={8}>
            <TextField
              fullWidth
              label={type === 'cpf' ? 'CPF' : 'CNPJ'}
              value={document}
              onChange={(e) => setDocument(e.target.value)}
              placeholder={type === 'cpf' ? '000.000.000-00' : '00.000.000/0000-00'}
              helperText={`Enter a valid ${type.toUpperCase()} to enrich data`}
            />
          </Grid>
          <Grid size={12} sm={4}>
            <Button
              fullWidth
              variant="contained"
              startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
              onClick={handleEnrich}
              disabled={loading || !document}
              sx={{ height: '56px' }}
            >
              {loading ? 'Enriching...' : 'Enrich'}
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Enrichment Results
            </Typography>
            <Card variant="outlined">
              <CardContent>
                {type === 'cpf' ? (
                  <CPFResultDisplay data={result as CPFPersonData} />
                ) : (
                  <CNPJResultDisplay data={result as CNPJCompanyData} />
                )}
              </CardContent>
            </Card>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
        {result && (
          <Button variant="contained">
            Create {type === 'cpf' ? 'Contact' : 'Company'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

const CPFResultDisplay: React.FC<{ data: CPFPersonData }> = ({ data }) => (
  <Grid container spacing={2}>
    <Grid size={12}>
      <Typography variant="h6">{data.name}</Typography>
      <Typography variant="body2" color="text.secondary">
        CPF: {formatCPF(data.cpf)}
      </Typography>
      {data.birthdate && (
        <Typography variant="body2" color="text.secondary">
          Birth Date: {data.birthdate}
        </Typography>
      )}
    </Grid>

    {data.emails && data.emails.length > 0 && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2" gutterBottom>Emails</Typography>
        <List dense>
          {data.emails.map((email, index) => (
            <ListItem key={index}>
              <ListItemText 
                primary={email.email} 
                secondary={`${email.type} (${email.confidence}% confidence)`}
              />
            </ListItem>
          ))}
        </List>
      </Grid>
    )}

    {data.phones && data.phones.length > 0 && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2" gutterBottom>Phones</Typography>
        <List dense>
          {data.phones.map((phone, index) => (
            <ListItem key={index}>
              <ListItemText 
                primary={phone.number} 
                secondary={`${phone.type} (${phone.confidence}% confidence)`}
              />
            </ListItem>
          ))}
        </List>
      </Grid>
    )}

    {data.professional_data && (
      <Grid size={12}>
        <Typography variant="subtitle2" gutterBottom>Professional Data</Typography>
        <Box>
          {data.professional_data.company && (
            <Typography variant="body2">Company: {data.professional_data.company}</Typography>
          )}
          {data.professional_data.position && (
            <Typography variant="body2">Position: {data.professional_data.position}</Typography>
          )}
          {data.professional_data.income_range && (
            <Typography variant="body2">Income Range: {data.professional_data.income_range}</Typography>
          )}
        </Box>
      </Grid>
    )}
  </Grid>
);

const CNPJResultDisplay: React.FC<{ data: CNPJCompanyData }> = ({ data }) => (
  <Grid container spacing={2}>
    <Grid size={12}>
      <Typography variant="h6">{data.company_name}</Typography>
      {data.trade_name && (
        <Typography variant="body1" color="text.secondary">
          Trade Name: {data.trade_name}
        </Typography>
      )}
      <Typography variant="body2" color="text.secondary">
        CNPJ: {formatCNPJ(data.cnpj)}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Status: {data.status}
      </Typography>
    </Grid>

    {data.industry && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2">Industry</Typography>
        <Typography variant="body2">{data.industry}</Typography>
      </Grid>
    )}

    {data.website && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2">Website</Typography>
        <Typography variant="body2">{data.website}</Typography>
      </Grid>
    )}

    {data.shareholders && data.shareholders.length > 0 && (
      <Grid size={12}>
        <Typography variant="subtitle2" gutterBottom>Shareholders</Typography>
        <List dense>
          {data.shareholders.map((shareholder, index) => (
            <ListItem key={index}>
              <ListItemText 
                primary={shareholder.name} 
                secondary={`${shareholder.participation}% participation`}
              />
            </ListItem>
          ))}
        </List>
      </Grid>
    )}
  </Grid>
);

const WizaEnrichmentDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  type: 'linkedin' | 'email';
}> = ({ open, onClose, type }) => {
  const [linkedInUrl, setLinkedInUrl] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [companyDomain, setCompanyDomain] = useState('');
  const [loading, setLoading] = useState(false);
  const [linkedInResult, setLinkedInResult] = useState<LinkedInProfileData | null>(null);
  const [emailResult, setEmailResult] = useState<EmailFinderData[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creditsUsed, setCreditsUsed] = useState<number | null>(null);

  const handleEnrich = async () => {
    if (type === 'linkedin' && !linkedInUrl) return;
    if (type === 'email' && (!firstName || !lastName || !companyDomain)) return;

    setLoading(true);
    setError(null);
    setLinkedInResult(null);
    setEmailResult(null);

    try {
      if (type === 'linkedin') {
        if (!validateLinkedInUrl(linkedInUrl)) {
          throw new Error('Invalid LinkedIn URL format');
        }
        const response = await wizaService.enrichLinkedInProfile({ 
          linkedin_url: linkedInUrl,
          include_emails: true,
          include_phone: true
        });
        if (response.success) {
          setLinkedInResult(response.data);
          setCreditsUsed(response.credits_used || null);
        } else {
          throw new Error(response.errors?.[0] || 'LinkedIn enrichment failed');
        }
      } else {
        if (!validateEmailDomain(companyDomain)) {
          throw new Error('Invalid company domain format');
        }
        const response = await wizaService.findEmail({
          first_name: firstName,
          last_name: lastName,
          company_domain: companyDomain,
          linkedin_url: linkedInUrl || undefined
        });
        if (response.success) {
          setEmailResult(response.data);
          setCreditsUsed(response.credits_used || null);
        } else {
          throw new Error(response.errors?.[0] || 'Email finding failed');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setLinkedInUrl('');
    setFirstName('');
    setLastName('');
    setCompanyDomain('');
    setLinkedInResult(null);
    setEmailResult(null);
    setError(null);
    setCreditsUsed(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="lg" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {type === 'linkedin' ? <LinkedInIcon sx={{ mr: 1 }} /> : <EmailIcon sx={{ mr: 1 }} />}
          {type === 'linkedin' ? 'Enrich LinkedIn Profile' : 'Find Email Address'}
        </Box>
      </DialogTitle>
      <DialogContent>
        {type === 'linkedin' ? (
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={12} sm={8}>
              <TextField
                fullWidth
                label="LinkedIn Profile URL"
                value={linkedInUrl}
                onChange={(e) => setLinkedInUrl(e.target.value)}
                placeholder="https://linkedin.com/in/profile-name"
                helperText="Enter a valid LinkedIn profile URL"
              />
            </Grid>
            <Grid size={12} sm={4}>
              <Button
                fullWidth
                variant="contained"
                startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                onClick={handleEnrich}
                disabled={loading || !linkedInUrl}
                sx={{ height: '56px' }}
              >
                {loading ? 'Enriching...' : 'Enrich'}
              </Button>
            </Grid>
          </Grid>
        ) : (
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={12} sm={4}>
              <TextField
                fullWidth
                label="First Name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </Grid>
            <Grid size={12} sm={4}>
              <TextField
                fullWidth
                label="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </Grid>
            <Grid size={12} sm={4}>
              <TextField
                fullWidth
                label="Company Domain"
                value={companyDomain}
                onChange={(e) => setCompanyDomain(e.target.value)}
                placeholder="company.com"
                required
              />
            </Grid>
            <Grid size={12} sm={8}>
              <TextField
                fullWidth
                label="LinkedIn URL (Optional)"
                value={linkedInUrl}
                onChange={(e) => setLinkedInUrl(e.target.value)}
                placeholder="https://linkedin.com/in/profile-name"
                helperText="Optional: LinkedIn profile URL for better accuracy"
              />
            </Grid>
            <Grid size={12} sm={4}>
              <Button
                fullWidth
                variant="contained"
                startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                onClick={handleEnrich}
                disabled={loading || !firstName || !lastName || !companyDomain}
                sx={{ height: '56px' }}
              >
                {loading ? 'Finding...' : 'Find Email'}
              </Button>
            </Grid>
          </Grid>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {creditsUsed && (
          <Alert severity="info" sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <CreditIcon sx={{ mr: 1 }} />
              Credits used: {creditsUsed}
            </Box>
          </Alert>
        )}

        {linkedInResult && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              LinkedIn Profile Results
            </Typography>
            <Card variant="outlined">
              <CardContent>
                <LinkedInProfileResultDisplay data={linkedInResult} />
              </CardContent>
            </Card>
          </Box>
        )}

        {emailResult && emailResult.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Email Finding Results
            </Typography>
            <Grid container spacing={2}>
              {emailResult.map((email, index) => (
                <Grid size={12} sm={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <EmailResultDisplay data={email} />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
        {(linkedInResult || (emailResult && emailResult.length > 0)) && (
          <Button variant="contained">
            Create {type === 'linkedin' ? 'Contact' : 'Contact with Email'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

const LinkedInProfileResultDisplay: React.FC<{ data: LinkedInProfileData }> = ({ data }) => (
  <Grid container spacing={2}>
    <Grid size={12}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        {data.profile_image_url && (
          <Box 
            component="img" 
            src={data.profile_image_url} 
            alt={data.full_name}
            sx={{ width: 60, height: 60, borderRadius: '50%', mr: 2 }}
          />
        )}
        <Box>
          <Typography variant="h6">{data.full_name}</Typography>
          {data.headline && (
            <Typography variant="body2" color="text.secondary">
              {data.headline}
            </Typography>
          )}
          {data.location && (
            <Typography variant="body2" color="text.secondary">
              📍 {data.location}
            </Typography>
          )}
        </Box>
      </Box>
    </Grid>

    {data.current_company && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2" gutterBottom>Current Position</Typography>
        <Typography variant="body2">
          <strong>{data.current_company.title}</strong> at {data.current_company.name}
        </Typography>
        {data.current_company.duration && (
          <Typography variant="body2" color="text.secondary">
            {data.current_company.duration}
          </Typography>
        )}
      </Grid>
    )}

    {data.emails && data.emails.length > 0 && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2" gutterBottom>Email Addresses</Typography>
        <List dense>
          {data.emails.map((email, index) => (
            <ListItem key={index} sx={{ pl: 0 }}>
              <ListItemText 
                primary={email.email} 
                secondary={`${email.type} (${email.confidence}% confidence)`}
              />
            </ListItem>
          ))}
        </List>
      </Grid>
    )}

    {data.phones && data.phones.length > 0 && (
      <Grid size={12} sm={6}>
        <Typography variant="subtitle2" gutterBottom>Phone Numbers</Typography>
        <List dense>
          {data.phones.map((phone, index) => (
            <ListItem key={index} sx={{ pl: 0 }}>
              <ListItemText 
                primary={phone.number} 
                secondary={`${phone.type} (${phone.confidence}% confidence)`}
              />
            </ListItem>
          ))}
        </List>
      </Grid>
    )}

    {data.skills && data.skills.length > 0 && (
      <Grid size={12}>
        <Typography variant="subtitle2" gutterBottom>Skills</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {data.skills.slice(0, 10).map((skill, index) => (
            <Chip key={index} label={skill} size="small" />
          ))}
          {data.skills.length > 10 && (
            <Chip label={`+${data.skills.length - 10} more`} size="small" variant="outlined" />
          )}
        </Box>
      </Grid>
    )}
  </Grid>
);

const EmailResultDisplay: React.FC<{ data: EmailFinderData }> = ({ data }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{data.email}</Typography>
    <Box sx={{ mb: 2 }}>
      <Chip 
        label={data.verification_status.toUpperCase()} 
        color={data.verification_status === 'valid' ? 'success' : 
               data.verification_status === 'invalid' ? 'error' : 'warning'}
        size="small"
        sx={{ mr: 1 }}
      />
      <Chip 
        label={`${data.confidence}% confidence`} 
        size="small"
        variant="outlined"
      />
    </Box>
    <Typography variant="body2">
      <strong>Name:</strong> {data.first_name} {data.last_name}
    </Typography>
    <Typography variant="body2">
      <strong>Type:</strong> {data.type}
    </Typography>
    <Typography variant="body2">
      <strong>Source:</strong> {data.source}
    </Typography>
    {data.company_name && (
      <Typography variant="body2">
        <strong>Company:</strong> {data.company_name}
      </Typography>
    )}
    {data.title && (
      <Typography variant="body2">
        <strong>Title:</strong> {data.title}
      </Typography>
    )}
  </Box>
);

const SurfeConfigDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  onSave: (credentials: SurfeCredentials) => void;
}> = ({ open, onClose, onSave }) => {
  const [credentials, setCredentials] = useState<SurfeCredentials>({
    apiKey: ''
  });
  const [credits, setCredits] = useState<SurfeCreditsData | null>(null);
  const [testing, setTesting] = useState(false);

  const handleSave = async () => {
    if (credentials.apiKey) {
      setTesting(true);
      try {
        surfeService.setCredentials(credentials);
        const creditsResponse = await surfeService.getCredits();
        if (creditsResponse.success) {
          setCredits(creditsResponse.data);
          onSave(credentials);
          onClose();
        } else {
          throw new Error('Invalid API key');
        }
      } catch (error) {
        console.error('Failed to validate Surfe API key:', error);
      } finally {
        setTesting(false);
      }
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <GroupsIcon sx={{ mr: 1 }} />
          Surfe API Configuration
        </Box>
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          Enter your Surfe API key. This will be used for people and company search and enrichment.
          Visit <a href="https://developers.surfe.com/" target="_blank" rel="noopener noreferrer">Surfe API Docs</a> for more information.
        </Alert>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={12}>
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={credentials.apiKey}
              onChange={(e) => setCredentials(prev => ({ ...prev, apiKey: e.target.value }))}
              required
              helperText="Get your API key from Surfe dashboard"
            />
          </Grid>
          {credits && (
            <Grid size={12}>
              <Alert severity="success">
                <Typography variant="h6" gutterBottom>Credits Available</Typography>
                <Grid container spacing={2}>
                  <Grid size={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <EmailIcon sx={{ mr: 1, fontSize: 16 }} />
                      <Typography variant="body2">
                        <strong>Email:</strong> {credits.email.remaining}/{credits.email.total}
                      </Typography>
                    </Box>
                    <Typography variant="caption" color="text.secondary">
                      Daily: {credits.email.daily_used}/{credits.email.daily_quota}
                    </Typography>
                  </Grid>
                  <Grid size={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <PhoneIcon sx={{ mr: 1, fontSize: 16 }} />
                      <Typography variant="body2">
                        <strong>Mobile:</strong> {credits.mobile.remaining}/{credits.mobile.total}
                      </Typography>
                    </Box>
                    <Typography variant="caption" color="text.secondary">
                      Daily: {credits.mobile.daily_used}/{credits.mobile.daily_quota}
                    </Typography>
                  </Grid>
                </Grid>
              </Alert>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button 
          variant="contained" 
          onClick={handleSave}
          disabled={!credentials.apiKey || testing}
          startIcon={testing ? <CircularProgress size={20} /> : null}
        >
          {testing ? 'Testing...' : 'Save & Test Connection'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const SurfeEnrichmentDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  type: 'search-people' | 'enrich-people' | 'search-companies' | 'enrich-companies';
}> = ({ open, onClose, type }) => {
  const [searchFilters, setSearchFilters] = useState({
    industries: [] as string[],
    locations: [] as string[],
    jobTitles: [] as string[],
    seniorities: [] as string[],
    companySize: [] as string[]
  });
  const [enrichData, setEnrichData] = useState({
    firstName: '',
    lastName: '',
    companyName: '',
    companyDomain: '',
    linkedinUrl: ''
  });
  const [loading, setLoading] = useState(false);
  const [peopleResults, setPeopleResults] = useState<PersonSearchData[] | PersonEnrichData[] | null>(null);
  const [companyResults, setCompanyResults] = useState<CompanySearchData[] | SurfeCompanyEnrichData[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creditsUsed, setCreditsUsed] = useState<{email?: number; mobile?: number} | null>(null);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setPeopleResults(null);
    setCompanyResults(null);

    try {
      if (type === 'search-people') {
        const response = await surfeService.searchPeople({
          filters: searchFilters,
          limit: 50
        });
        if (response.success) {
          setPeopleResults(response.data);
        } else {
          throw new Error(response.errors?.[0] || 'People search failed');
        }
      } else if (type === 'enrich-people') {
        if (!enrichData.firstName || !enrichData.lastName) {
          throw new Error('First name and last name are required');
        }
        const response = await surfeService.enrichPeople({
          include: { email: true, mobile: true, linkedin: true },
          people: [{
            firstName: enrichData.firstName,
            lastName: enrichData.lastName,
            companyName: enrichData.companyName || undefined,
            companyDomain: enrichData.companyDomain || undefined,
            linkedinUrl: enrichData.linkedinUrl || undefined
          }]
        });
        if (response.success) {
          setPeopleResults(response.data);
          setCreditsUsed(response.credits_used || null);
        } else {
          throw new Error(response.errors?.[0] || 'People enrichment failed');
        }
      } else if (type === 'search-companies') {
        const response = await surfeService.searchCompanies({
          filters: {
            industries: searchFilters.industries,
            locations: searchFilters.locations,
            companySize: searchFilters.companySize
          },
          limit: 50
        });
        if (response.success) {
          setCompanyResults(response.data);
        } else {
          throw new Error(response.errors?.[0] || 'Company search failed');
        }
      } else if (type === 'enrich-companies') {
        if (!enrichData.companyDomain && !enrichData.companyName) {
          throw new Error('Company domain or name is required');
        }
        const response = await surfeService.enrichCompanies({
          companies: [{
            domain: enrichData.companyDomain || undefined,
            name: enrichData.companyName || undefined,
            linkedinUrl: enrichData.linkedinUrl || undefined
          }]
        });
        if (response.success) {
          setCompanyResults(response.data);
        } else {
          throw new Error(response.errors?.[0] || 'Company enrichment failed');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setSearchFilters({ industries: [], locations: [], jobTitles: [], seniorities: [], companySize: [] });
    setEnrichData({ firstName: '', lastName: '', companyName: '', companyDomain: '', linkedinUrl: '' });
    setPeopleResults(null);
    setCompanyResults(null);
    setError(null);
    setCreditsUsed(null);
    onClose();
  };

  const getDialogTitle = () => {
    switch (type) {
      case 'search-people': return 'Search People';
      case 'enrich-people': return 'Enrich People';
      case 'search-companies': return 'Search Companies';
      case 'enrich-companies': return 'Enrich Companies';
    }
  };

  const getDialogIcon = () => {
    switch (type) {
      case 'search-people': return <SearchIcon sx={{ mr: 1 }} />;
      case 'enrich-people': return <PersonIcon sx={{ mr: 1 }} />;
      case 'search-companies': return <FilterIcon sx={{ mr: 1 }} />;
      case 'enrich-companies': return <BusinessIcon sx={{ mr: 1 }} />;
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="lg" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {getDialogIcon()}
          {getDialogTitle()}
        </Box>
      </DialogTitle>
      <DialogContent>
        {(type === 'search-people' || type === 'search-companies') ? (
          <Box sx={{ mt: 1 }}>
            <Typography variant="h6" gutterBottom>Search Filters</Typography>
            <Grid container spacing={2}>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Industries (comma-separated)"
                  value={searchFilters.industries.join(', ')}
                  onChange={(e) => setSearchFilters(prev => ({ 
                    ...prev, 
                    industries: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Technology, Healthcare, Finance"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Locations (comma-separated)"
                  value={searchFilters.locations.join(', ')}
                  onChange={(e) => setSearchFilters(prev => ({ 
                    ...prev, 
                    locations: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="San Francisco, New York, London"
                />
              </Grid>
              {type === 'search-people' && (
                <>
                  <Grid size={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Job Titles (comma-separated)"
                      value={searchFilters.jobTitles.join(', ')}
                      onChange={(e) => setSearchFilters(prev => ({ 
                        ...prev, 
                        jobTitles: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                      }))}
                      placeholder="CEO, CTO, Marketing Manager"
                    />
                  </Grid>
                  <Grid size={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Seniorities (comma-separated)"
                      value={searchFilters.seniorities.join(', ')}
                      onChange={(e) => setSearchFilters(prev => ({ 
                        ...prev, 
                        seniorities: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                      }))}
                      placeholder="Senior, Executive, Manager"
                    />
                  </Grid>
                </>
              )}
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Company Size (comma-separated)"
                  value={searchFilters.companySize.join(', ')}
                  onChange={(e) => setSearchFilters(prev => ({ 
                    ...prev, 
                    companySize: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="1-10, 11-50, 51-200"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  onClick={handleSearch}
                  disabled={loading}
                  sx={{ height: '56px' }}
                >
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </Grid>
            </Grid>
          </Box>
        ) : (
          <Box sx={{ mt: 1 }}>
            <Typography variant="h6" gutterBottom>Enrichment Data</Typography>
            <Grid container spacing={2}>
              {type === 'enrich-people' && (
                <>
                  <Grid size={12} sm={6}>
                    <TextField
                      fullWidth
                      label="First Name"
                      value={enrichData.firstName}
                      onChange={(e) => setEnrichData(prev => ({ ...prev, firstName: e.target.value }))}
                      required
                    />
                  </Grid>
                  <Grid size={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Last Name"
                      value={enrichData.lastName}
                      onChange={(e) => setEnrichData(prev => ({ ...prev, lastName: e.target.value }))}
                      required
                    />
                  </Grid>
                </>
              )}
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Company Name"
                  value={enrichData.companyName}
                  onChange={(e) => setEnrichData(prev => ({ ...prev, companyName: e.target.value }))}
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Company Domain"
                  value={enrichData.companyDomain}
                  onChange={(e) => setEnrichData(prev => ({ ...prev, companyDomain: e.target.value }))}
                  placeholder="company.com"
                />
              </Grid>
              <Grid size={12} sm={8}>
                <TextField
                  fullWidth
                  label="LinkedIn URL (Optional)"
                  value={enrichData.linkedinUrl}
                  onChange={(e) => setEnrichData(prev => ({ ...prev, linkedinUrl: e.target.value }))}
                  placeholder="https://linkedin.com/in/profile-name"
                />
              </Grid>
              <Grid size={12} sm={4}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  onClick={handleSearch}
                  disabled={loading}
                  sx={{ height: '56px' }}
                >
                  {loading ? 'Enriching...' : 'Enrich'}
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {creditsUsed && (
          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="body2">
              Credits used: Email: {creditsUsed.email || 0}, Mobile: {creditsUsed.mobile || 0}
            </Typography>
          </Alert>
        )}

        {peopleResults && peopleResults.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              People Results ({peopleResults.length})
            </Typography>
            <Grid container spacing={2}>
              {peopleResults.slice(0, 10).map((person, index) => (
                <Grid size={12} sm={6} md={4} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <SurfePersonResultDisplay data={person} />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
            {peopleResults.length > 10 && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Showing first 10 of {peopleResults.length} results
              </Typography>
            )}
          </Box>
        )}

        {companyResults && companyResults.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Company Results ({companyResults.length})
            </Typography>
            <Grid container spacing={2}>
              {companyResults.slice(0, 10).map((company, index) => (
                <Grid size={12} sm={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <SurfeCompanyResultDisplay data={company} />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
            {companyResults.length > 10 && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Showing first 10 of {companyResults.length} results
              </Typography>
            )}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
        {(peopleResults?.length || companyResults?.length) && (
          <Button variant="contained">
            Create {type.includes('people') ? 'Contacts' : 'Companies'} ({(peopleResults?.length || companyResults?.length || 0)})
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

const SurfePersonResultDisplay: React.FC<{ data: PersonSearchData | PersonEnrichData }> = ({ data }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{data.fullName}</Typography>
    
    {data.company && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Company:</strong> {data.company.name}
        {data.company.industry && ` (${data.company.industry})`}
      </Typography>
    )}
    
    {'jobTitle' in data && data.jobTitle && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Job Title:</strong> {data.jobTitle}
      </Typography>
    )}
    
    {data.location && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Location:</strong> {data.location}
      </Typography>
    )}
    
    {'email' in data && data.email && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Email:</strong> {data.email.address} ({data.email.confidence}%)
      </Typography>
    )}
    
    {'mobile' in data && data.mobile && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Mobile:</strong> {data.mobile.number} ({data.mobile.confidence}%)
      </Typography>
    )}
    
    {data.linkedinUrl && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>LinkedIn:</strong>{' '}
        <a href={data.linkedinUrl} target="_blank" rel="noopener noreferrer">
          Profile
        </a>
      </Typography>
    )}
    
    {'confidence' in data && (
      <Box sx={{ mt: 2 }}>
        <Chip 
          label={`${data.confidence}% confidence`} 
          size="small"
          color={data.confidence > 80 ? 'success' : data.confidence > 60 ? 'warning' : 'default'}
        />
      </Box>
    )}
  </Box>
);

const SurfeCompanyResultDisplay: React.FC<{ data: CompanySearchData | SurfeCompanyEnrichData }> = ({ data }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{data.name}</Typography>
    
    {data.domain && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Domain:</strong> {data.domain}
      </Typography>
    )}
    
    {data.industry && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Industry:</strong> {data.industry}
      </Typography>
    )}
    
    {data.size && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Size:</strong>{' '}
        {data.size.employees ? `${data.size.employees} employees` : data.size.range}
      </Typography>
    )}
    
    {data.location && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Location:</strong> {[data.location.city, data.location.state, data.location.country].filter(Boolean).join(', ')}
      </Typography>
    )}
    
    {data.revenue && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Revenue:</strong>{' '}
        {data.revenue.amount ? `$${data.revenue.amount}` : data.revenue.range}
      </Typography>
    )}
    
    {data.founded && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Founded:</strong> {data.founded}
      </Typography>
    )}
    
    {data.website && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Website:</strong>{' '}
        <a href={data.website} target="_blank" rel="noopener noreferrer">
          {data.website}
        </a>
      </Typography>
    )}
    
    {data.linkedinUrl && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>LinkedIn:</strong>{' '}
        <a href={data.linkedinUrl} target="_blank" rel="noopener noreferrer">
          Company Page
        </a>
      </Typography>
    )}
    
    {'confidence' in data && (
      <Box sx={{ mt: 2 }}>
        <Chip 
          label={`${data.confidence}% confidence`} 
          size="small"
          color={data.confidence > 80 ? 'success' : data.confidence > 60 ? 'warning' : 'default'}
        />
      </Box>
    )}
  </Box>
);

const PDLConfigDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  onSave: (credentials: PDLCredentials) => void;
}> = ({ open, onClose, onSave }) => {
  const [credentials, setCredentials] = useState<PDLCredentials>({
    apiKey: ''
  });
  const [credits, setCredits] = useState<PDLCreditsData | null>(null);
  const [testing, setTesting] = useState(false);

  const handleSave = async () => {
    if (credentials.apiKey) {
      setTesting(true);
      try {
        peopleDataLabsService.setCredentials(credentials);
        const creditsResponse = await peopleDataLabsService.getCredits();
        if (creditsResponse.status === 200 && creditsResponse.data) {
          setCredits(creditsResponse.data);
          onSave(credentials);
          onClose();
        } else {
          throw new Error('Invalid API key');
        }
      } catch (error) {
        console.error('Failed to validate People Data Labs API key:', error);
      } finally {
        setTesting(false);
      }
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <DatabaseIcon sx={{ mr: 1 }} />
          People Data Labs API Configuration
        </Box>
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          Enter your People Data Labs API key. This will be used for comprehensive person and company data enrichment.
          Visit <a href="https://www.peopledatalabs.com/pricing/person" target="_blank" rel="noopener noreferrer">People Data Labs</a> for more information.
        </Alert>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={12}>
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={credentials.apiKey}
              onChange={(e) => setCredentials(prev => ({ ...prev, apiKey: e.target.value }))}
              required
              helperText="Get your API key from People Data Labs dashboard"
            />
          </Grid>
          {credits && (
            <Grid size={12}>
              <Alert severity="success">
                <Typography variant="h6" gutterBottom>Credits Available</Typography>
                <Grid container spacing={2}>
                  <Grid size={6}>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      <strong>Credits Remaining:</strong> {credits.credits_remaining.toLocaleString()}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Daily: {credits.credits_used_today.toLocaleString()}/{credits.daily_credit_limit.toLocaleString()}
                    </Typography>
                  </Grid>
                  <Grid size={6}>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      <strong>Monthly:</strong> {credits.monthly_credits_remaining.toLocaleString()}/{credits.monthly_credit_limit.toLocaleString()}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      High-quality B2B data
                    </Typography>
                  </Grid>
                </Grid>
              </Alert>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button 
          variant="contained" 
          onClick={handleSave}
          disabled={!credentials.apiKey || testing}
          startIcon={testing ? <CircularProgress size={20} /> : null}
        >
          {testing ? 'Testing...' : 'Save & Test Connection'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const PDLEnrichmentDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  type: 'enrich-person' | 'search-people' | 'enrich-company' | 'search-companies';
}> = ({ open, onClose, type }) => {
  const [personParams, setPersonParams] = useState({
    name: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    linkedin_url: '',
    company: '',
    location: '',
    min_likelihood: 0.7
  });
  
  const [companyParams, setCompanyParams] = useState({
    name: '',
    website: '',
    linkedin_url: '',
    location: '',
    min_likelihood: 0.7
  });

  const [searchQuery, setSearchQuery] = useState({
    job_title: [] as string[],
    job_company_name: [] as string[],
    location_country: [] as string[],
    skills: [] as string[],
    industry: [] as string[],
    education_school: [] as string[]
  });

  const [loading, setLoading] = useState(false);
  const [personResults, setPersonResults] = useState<PDLPersonData[] | null>(null);
  const [companyResults, setCompanyResults] = useState<PDLCompanyData[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creditsUsed, setCreditsUsed] = useState<number | null>(null);
  const [likelihood, setLikelihood] = useState<number | null>(null);

  const handleEnrich = async () => {
    setLoading(true);
    setError(null);
    setPersonResults(null);
    setCompanyResults(null);

    try {
      if (type === 'enrich-person') {
        if (!validatePersonEnrichParams(personParams)) {
          throw new Error('Please provide at least one identifier (name, email, phone, or LinkedIn URL)');
        }
        
        const response = await peopleDataLabsService.enrichPerson({ params: personParams });
        if (response.status === 200 && response.data) {
          setPersonResults([response.data]);
          setLikelihood(response.likelihood || null);
          setCreditsUsed(1);
        } else {
          throw new Error(response.error?.message || 'Person enrichment failed');
        }
      } else if (type === 'search-people') {
        const response = await peopleDataLabsService.searchPeople({
          query: searchQuery,
          size: 50
        });
        if (response.status === 200 && response.data) {
          setPersonResults(response.data);
          setCreditsUsed(response.data.length);
        } else {
          throw new Error(response.error?.message || 'People search failed');
        }
      } else if (type === 'enrich-company') {
        if (!validateCompanyEnrichParams(companyParams)) {
          throw new Error('Please provide at least one identifier (name, website, LinkedIn URL, or ticker)');
        }
        
        const response = await peopleDataLabsService.enrichCompany({ params: companyParams });
        if (response.status === 200 && response.data) {
          setCompanyResults([response.data]);
          setLikelihood(response.likelihood || null);
          setCreditsUsed(1);
        } else {
          throw new Error(response.error?.message || 'Company enrichment failed');
        }
      } else if (type === 'search-companies') {
        const response = await peopleDataLabsService.searchCompanies({
          query: {
            name: searchQuery.job_company_name,
            industry: searchQuery.industry,
            location_country: searchQuery.location_country
          },
          size: 50
        });
        if (response.status === 200 && response.data) {
          setCompanyResults(response.data);
          setCreditsUsed(response.data.length);
        } else {
          throw new Error(response.error?.message || 'Company search failed');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setPersonParams({ name: '', first_name: '', last_name: '', email: '', phone: '', linkedin_url: '', company: '', location: '', min_likelihood: 0.7 });
    setCompanyParams({ name: '', website: '', linkedin_url: '', location: '', min_likelihood: 0.7 });
    setSearchQuery({ job_title: [], job_company_name: [], location_country: [], skills: [], industry: [], education_school: [] });
    setPersonResults(null);
    setCompanyResults(null);
    setError(null);
    setCreditsUsed(null);
    setLikelihood(null);
    onClose();
  };

  const getDialogTitle = () => {
    switch (type) {
      case 'enrich-person': return 'Enrich Person';
      case 'search-people': return 'Search People';
      case 'enrich-company': return 'Enrich Company';
      case 'search-companies': return 'Search Companies';
    }
  };

  const getDialogIcon = () => {
    switch (type) {
      case 'enrich-person': return <PersonIcon sx={{ mr: 1 }} />;
      case 'search-people': return <SearchIcon sx={{ mr: 1 }} />;
      case 'enrich-company': return <BusinessIcon sx={{ mr: 1 }} />;
      case 'search-companies': return <WorkIcon sx={{ mr: 1 }} />;
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="lg" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {getDialogIcon()}
          {getDialogTitle()}
        </Box>
      </DialogTitle>
      <DialogContent>
        {(type === 'enrich-person') && (
          <Box sx={{ mt: 1 }}>
            <Typography variant="h6" gutterBottom>Person Enrichment</Typography>
            <Grid container spacing={2}>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Full Name"
                  value={personParams.name}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="John Doe"
                />
              </Grid>
              <Grid size={12} sm={3}>
                <TextField
                  fullWidth
                  label="First Name"
                  value={personParams.first_name}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, first_name: e.target.value }))}
                />
              </Grid>
              <Grid size={12} sm={3}>
                <TextField
                  fullWidth
                  label="Last Name"
                  value={personParams.last_name}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, last_name: e.target.value }))}
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={personParams.email}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, email: e.target.value }))}
                  placeholder="john@company.com"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  value={personParams.phone}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, phone: e.target.value }))}
                  placeholder="+1-555-123-4567"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="LinkedIn URL"
                  value={personParams.linkedin_url}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, linkedin_url: e.target.value }))}
                  placeholder="https://linkedin.com/in/johndoe"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Company"
                  value={personParams.company}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, company: e.target.value }))}
                  placeholder="Acme Inc"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Location"
                  value={personParams.location}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, location: e.target.value }))}
                  placeholder="San Francisco, CA"
                />
              </Grid>
              <Grid size={12} sm={4}>
                <TextField
                  fullWidth
                  label="Min Likelihood"
                  type="number"
                  inputProps={{ min: 0, max: 1, step: 0.1 }}
                  value={personParams.min_likelihood}
                  onChange={(e) => setPersonParams(prev => ({ ...prev, min_likelihood: parseFloat(e.target.value) }))}
                />
              </Grid>
              <Grid size={12} sm={2}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  onClick={handleEnrich}
                  disabled={loading}
                  sx={{ height: '56px' }}
                >
                  {loading ? 'Enriching...' : 'Enrich'}
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}

        {(type === 'search-people') && (
          <Box sx={{ mt: 1 }}>
            <Typography variant="h6" gutterBottom>People Search</Typography>
            <Grid container spacing={2}>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Job Titles (comma-separated)"
                  value={searchQuery.job_title.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    job_title: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="CEO, CTO, Software Engineer"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Companies (comma-separated)"
                  value={searchQuery.job_company_name.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    job_company_name: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Google, Microsoft, Apple"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Countries (comma-separated)"
                  value={searchQuery.location_country.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    location_country: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="United States, Canada, United Kingdom"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Skills (comma-separated)"
                  value={searchQuery.skills.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    skills: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Python, JavaScript, Machine Learning"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Industries (comma-separated)"
                  value={searchQuery.industry.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    industry: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Technology, Healthcare, Finance"
                />
              </Grid>
              <Grid size={12} sm={4}>
                <TextField
                  fullWidth
                  label="Schools (comma-separated)"
                  value={searchQuery.education_school.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    education_school: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Stanford, MIT, Harvard"
                />
              </Grid>
              <Grid size={12} sm={2}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  onClick={handleEnrich}
                  disabled={loading}
                  sx={{ height: '56px' }}
                >
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}

        {(type === 'enrich-company') && (
          <Box sx={{ mt: 1 }}>
            <Typography variant="h6" gutterBottom>Company Enrichment</Typography>
            <Grid container spacing={2}>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Company Name"
                  value={companyParams.name}
                  onChange={(e) => setCompanyParams(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Acme Corporation"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Website"
                  value={companyParams.website}
                  onChange={(e) => setCompanyParams(prev => ({ ...prev, website: e.target.value }))}
                  placeholder="https://acme.com"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="LinkedIn URL"
                  value={companyParams.linkedin_url}
                  onChange={(e) => setCompanyParams(prev => ({ ...prev, linkedin_url: e.target.value }))}
                  placeholder="https://linkedin.com/company/acme"
                />
              </Grid>
              <Grid size={12} sm={4}>
                <TextField
                  fullWidth
                  label="Location"
                  value={companyParams.location}
                  onChange={(e) => setCompanyParams(prev => ({ ...prev, location: e.target.value }))}
                  placeholder="San Francisco, CA"
                />
              </Grid>
              <Grid size={12} sm={2}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  onClick={handleEnrich}
                  disabled={loading}
                  sx={{ height: '56px' }}
                >
                  {loading ? 'Enriching...' : 'Enrich'}
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}

        {(type === 'search-companies') && (
          <Box sx={{ mt: 1 }}>
            <Typography variant="h6" gutterBottom>Company Search</Typography>
            <Grid container spacing={2}>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Company Names (comma-separated)"
                  value={searchQuery.job_company_name.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    job_company_name: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Google, Microsoft, Apple"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Industries (comma-separated)"
                  value={searchQuery.industry.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    industry: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="Technology, Healthcare, Finance"
                />
              </Grid>
              <Grid size={12} sm={6}>
                <TextField
                  fullWidth
                  label="Countries (comma-separated)"
                  value={searchQuery.location_country.join(', ')}
                  onChange={(e) => setSearchQuery(prev => ({ 
                    ...prev, 
                    location_country: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  }))}
                  placeholder="United States, Canada, United Kingdom"
                />
              </Grid>
              <Grid size={12} sm={4}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  onClick={handleEnrich}
                  disabled={loading}
                  sx={{ height: '56px' }}
                >
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {(creditsUsed !== null || likelihood !== null) && (
          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="body2">
              {creditsUsed && `Credits used: ${creditsUsed}`}
              {creditsUsed && likelihood && ' | '}
              {likelihood && `Likelihood: ${(likelihood * 100).toFixed(1)}%`}
            </Typography>
          </Alert>
        )}

        {personResults && personResults.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Person Results ({personResults.length})
            </Typography>
            <Grid container spacing={2}>
              {personResults.slice(0, 10).map((person, index) => (
                <Grid size={12} sm={6} md={4} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <PDLPersonResultDisplay data={person} />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
            {personResults.length > 10 && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Showing first 10 of {personResults.length} results
              </Typography>
            )}
          </Box>
        )}

        {companyResults && companyResults.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Company Results ({companyResults.length})
            </Typography>
            <Grid container spacing={2}>
              {companyResults.slice(0, 10).map((company, index) => (
                <Grid size={12} sm={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <PDLCompanyResultDisplay data={company} />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
            {companyResults.length > 10 && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Showing first 10 of {companyResults.length} results
              </Typography>
            )}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
        {(personResults?.length || companyResults?.length) && (
          <Button variant="contained">
            Create {type.includes('person') || type.includes('people') ? 'Contacts' : 'Companies'} ({(personResults?.length || companyResults?.length || 0)})
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

const PDLPersonResultDisplay: React.FC<{ data: PDLPersonData }> = ({ data }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{data.full_name}</Typography>
    
    {data.job_title && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Job Title:</strong> {data.job_title}
      </Typography>
    )}
    
    {data.job_company_name && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Company:</strong> {data.job_company_name}
        {data.job_company_industry && ` (${data.job_company_industry})`}
      </Typography>
    )}
    
    {data.location_name && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Location:</strong> {data.location_name}
      </Typography>
    )}
    
    {data.work_email && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Work Email:</strong> {data.work_email}
      </Typography>
    )}
    
    {data.personal_emails && data.personal_emails.length > 0 && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Personal Emails:</strong> {data.personal_emails.slice(0, 2).join(', ')}
      </Typography>
    )}
    
    {data.phone_numbers && data.phone_numbers.length > 0 && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Phone:</strong> {data.phone_numbers[0]}
      </Typography>
    )}
    
    {data.linkedin_url && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>LinkedIn:</strong>{' '}
        <a href={data.linkedin_url} target="_blank" rel="noopener noreferrer">
          Profile
        </a>
      </Typography>
    )}
    
    {data.skills && data.skills.length > 0 && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Skills:</strong> {data.skills.slice(0, 5).join(', ')}
        {data.skills.length > 5 && '...'}
      </Typography>
    )}
    
    {data.education && data.education.length > 0 && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Education:</strong> {data.education[0].school?.name}
        {data.education[0].degrees && data.education[0].degrees.length > 0 && ` (${data.education[0].degrees[0]})`}
      </Typography>
    )}
  </Box>
);

const PDLCompanyResultDisplay: React.FC<{ data: PDLCompanyData }> = ({ data }) => (
  <Box>
    <Typography variant="h6" gutterBottom>{data.name}</Typography>
    
    {data.website && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Website:</strong>{' '}
        <a href={data.website} target="_blank" rel="noopener noreferrer">
          {data.website}
        </a>
      </Typography>
    )}
    
    {data.industry && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Industry:</strong> {data.industry}
      </Typography>
    )}
    
    {data.employee_count && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Employees:</strong> {data.employee_count.toLocaleString()}
      </Typography>
    )}
    
    {data.size && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Size:</strong> {data.size}
      </Typography>
    )}
    
    {data.location && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Location:</strong> {[data.location.locality, data.location.region, data.location.country].filter(Boolean).join(', ')}
      </Typography>
    )}
    
    {data.founded && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Founded:</strong> {data.founded}
      </Typography>
    )}
    
    {data.linkedin_url && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>LinkedIn:</strong>{' '}
        <a href={data.linkedin_url} target="_blank" rel="noopener noreferrer">
          Company Page
        </a>
      </Typography>
    )}
    
    {data.ticker && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Ticker:</strong> {data.ticker}
      </Typography>
    )}
    
    {data.tags && data.tags.length > 0 && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Tags:</strong> {data.tags.slice(0, 3).join(', ')}
        {data.tags.length > 3 && '...'}
      </Typography>
    )}
    
    {data.naics && data.naics.length > 0 && (
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>NAICS:</strong> {data.naics[0].naics_code} - {data.naics[0].industry_group}
      </Typography>
    )}
  </Box>
);

export const Integrations: React.FC = () => {
  const [configDialogOpen, setConfigDialogOpen] = useState(false);
  const [wizaConfigOpen, setWizaConfigOpen] = useState(false);
  const [surfeConfigOpen, setSurfeConfigOpen] = useState(false);
  const [pdlConfigOpen, setPdlConfigOpen] = useState(false);
  const [enrichmentDialogOpen, setEnrichmentDialogOpen] = useState(false);
  const [wizaEnrichmentOpen, setWizaEnrichmentOpen] = useState(false);
  const [surfeEnrichmentOpen, setSurfeEnrichmentOpen] = useState(false);
  const [pdlEnrichmentOpen, setPdlEnrichmentOpen] = useState(false);
  const [enrichmentType, setEnrichmentType] = useState<'cpf' | 'cnpj'>('cpf');
  const [wizaEnrichmentType, setWizaEnrichmentType] = useState<'linkedin' | 'email'>('linkedin');
  const [surfeEnrichmentType, setSurfeEnrichmentType] = useState<'search-people' | 'enrich-people' | 'search-companies' | 'enrich-companies'>('search-people');
  const [pdlEnrichmentType, setPdlEnrichmentType] = useState<'enrich-person' | 'search-people' | 'enrich-company' | 'search-companies'>('enrich-person');
  const [bigDataConnectionStatus, setBigDataConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');
  const [wizaConnectionStatus, setWizaConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');
  const [surfeConnectionStatus, setSurfeConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');
  const [pdlConnectionStatus, setPdlConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');

  const handleConfigureBigData = () => {
    setConfigDialogOpen(true);
  };

  const handleConfigureWiza = () => {
    setWizaConfigOpen(true);
  };

  const handleConfigureSurfe = () => {
    setSurfeConfigOpen(true);
  };

  const handleConfigurePDL = () => {
    setPdlConfigOpen(true);
  };

  const handleSaveBigDataCredentials = async (credentials: BigDataCorpCredentials) => {
    try {
      bigDataCorpService.setCredentials(credentials);
      const isConnected = await bigDataCorpService.testConnection();
      setBigDataConnectionStatus(isConnected ? 'connected' : 'error');
    } catch (error) {
      setBigDataConnectionStatus('error');
    }
  };

  const handleSaveWizaCredentials = async (credentials: WizaCredentials) => {
    try {
      wizaService.setCredentials(credentials);
      const isConnected = await wizaService.testConnection();
      setWizaConnectionStatus(isConnected ? 'connected' : 'error');
    } catch (error) {
      setWizaConnectionStatus('error');
    }
  };

  const handleSaveSurfeCredentials = async (credentials: SurfeCredentials) => {
    try {
      surfeService.setCredentials(credentials);
      const isConnected = await surfeService.testConnection();
      setSurfeConnectionStatus(isConnected ? 'connected' : 'error');
    } catch (error) {
      setSurfeConnectionStatus('error');
    }
  };

  const handleSavePDLCredentials = async (credentials: PDLCredentials) => {
    try {
      peopleDataLabsService.setCredentials(credentials);
      const isConnected = await peopleDataLabsService.testConnection();
      setPdlConnectionStatus(isConnected ? 'connected' : 'error');
    } catch (error) {
      setPdlConnectionStatus('error');
    }
  };

  const handleEnrichCPF = () => {
    setEnrichmentType('cpf');
    setEnrichmentDialogOpen(true);
  };

  const handleEnrichCNPJ = () => {
    setEnrichmentType('cnpj');
    setEnrichmentDialogOpen(true);
  };

  const handleEnrichLinkedIn = () => {
    setWizaEnrichmentType('linkedin');
    setWizaEnrichmentOpen(true);
  };

  const handleFindEmail = () => {
    setWizaEnrichmentType('email');
    setWizaEnrichmentOpen(true);
  };

  const handleSearchPeople = () => {
    setSurfeEnrichmentType('search-people');
    setSurfeEnrichmentOpen(true);
  };

  const handleEnrichPeople = () => {
    setSurfeEnrichmentType('enrich-people');
    setSurfeEnrichmentOpen(true);
  };

  const handleSearchCompanies = () => {
    setSurfeEnrichmentType('search-companies');
    setSurfeEnrichmentOpen(true);
  };

  const handleEnrichSurfeCompanies = () => {
    setSurfeEnrichmentType('enrich-companies');
    setSurfeEnrichmentOpen(true);
  };

  const handleEnrichPerson = () => {
    setPdlEnrichmentType('enrich-person');
    setPdlEnrichmentOpen(true);
  };

  const handleSearchPDLPeople = () => {
    setPdlEnrichmentType('search-people');
    setPdlEnrichmentOpen(true);
  };

  const handleEnrichPDLCompany = () => {
    setPdlEnrichmentType('enrich-company');
    setPdlEnrichmentOpen(true);
  };

  const handleSearchPDLCompanies = () => {
    setPdlEnrichmentType('search-companies');
    setPdlEnrichmentOpen(true);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Data Integrations
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Connect with external data sources to enrich your contacts and companies with additional information.
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={12} md={6}>
          <IntegrationCard
            title="BigData Corp"
            description="Enrich contacts with CPF data and companies with CNPJ data using BigData Corp's comprehensive Brazilian database."
            icon={<ApiIcon color="primary" />}
            status={bigDataConnectionStatus}
            onConfigure={handleConfigureBigData}
          />
        </Grid>
        <Grid size={12} md={6}>
          <IntegrationCard
            title="Wiza"
            description="Enrich LinkedIn profiles with professional data and find verified email addresses for lead generation."
            icon={<LinkedInIcon color="primary" />}
            status={wizaConnectionStatus}
            onConfigure={handleConfigureWiza}
          />
        </Grid>
        <Grid size={12} md={6}>
          <IntegrationCard
            title="Surfe"
            description="Search and enrich people and companies with email, mobile, and professional data using advanced filters."
            icon={<GroupsIcon color="primary" />}
            status={surfeConnectionStatus}
            onConfigure={handleConfigureSurfe}
          />
        </Grid>
        <Grid size={12} md={6}>
          <IntegrationCard
            title="People Data Labs"
            description="Access comprehensive person and company data with advanced search capabilities, education history, and professional profiles."
            icon={<DatabaseIcon color="primary" />}
            status={pdlConnectionStatus}
            onConfigure={handleConfigurePDL}
          />
        </Grid>
      </Grid>

      {(bigDataConnectionStatus === 'connected' || wizaConnectionStatus === 'connected' || surfeConnectionStatus === 'connected' || pdlConnectionStatus === 'connected') && (
        <Box sx={{ mt: 4 }}>
          <Divider sx={{ mb: 3 }} />
          
          <Typography variant="h5" gutterBottom>
            Data Enrichment Tools
          </Typography>

          <Grid container spacing={3}>
            {bigDataConnectionStatus === 'connected' && (
              <>
                <Grid size={12} sm={6} md={4}>
                  <Card>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <PersonIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        Enrich Contacts (CPF)
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Use CPF to enrich contact information with emails, phones, and professional data.
                      </Typography>
                      <Button 
                        variant="contained" 
                        onClick={handleEnrichCPF}
                        fullWidth
                      >
                        Enrich by CPF
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid size={12} sm={6} md={4}>
                  <Card>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        Enrich Companies (CNPJ)
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Use CNPJ to enrich company information with shareholders, contacts, and business data.
                      </Typography>
                      <Button 
                        variant="contained" 
                        onClick={handleEnrichCNPJ}
                        fullWidth
                      >
                        Enrich by CNPJ
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </>
            )}

            {wizaConnectionStatus === 'connected' && (
              <>
                <Grid size={12} sm={6} md={4}>
                  <Card>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <LinkedInIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        LinkedIn Enrichment
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Enrich LinkedIn profiles with professional data, emails, and contact information.
                      </Typography>
                      <Button 
                        variant="contained" 
                        onClick={handleEnrichLinkedIn}
                        fullWidth
                      >
                        Enrich LinkedIn Profile
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid size={12} sm={6} md={4}>
                  <Card>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <EmailIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        Email Finder
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Find verified email addresses using name and company domain information.
                      </Typography>
                      <Button 
                        variant="contained" 
                        onClick={handleFindEmail}
                        fullWidth
                      >
                        Find Email
                      </Button>
                    </CardContent>
                  </Card>
                                 </Grid>
               </>
             )}

             {surfeConnectionStatus === 'connected' && (
               <>
                 <Grid size={12} sm={6} md={3}>
                   <Card>
                     <CardContent sx={{ textAlign: 'center' }}>
                       <SearchIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                       <Typography variant="h6" gutterBottom>
                         Search People
                       </Typography>
                       <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                         Find people using advanced filters like industry, location, job title, and seniority.
                       </Typography>
                       <Button 
                         variant="contained" 
                         onClick={handleSearchPeople}
                         fullWidth
                       >
                         Search People
                       </Button>
                     </CardContent>
                   </Card>
                 </Grid>

                 <Grid size={12} sm={6} md={3}>
                   <Card>
                     <CardContent sx={{ textAlign: 'center' }}>
                       <PersonIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                       <Typography variant="h6" gutterBottom>
                         Enrich People
                       </Typography>
                       <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                         Enrich existing contact data with verified emails, mobile numbers, and LinkedIn profiles.
                       </Typography>
                       <Button 
                         variant="contained" 
                         onClick={handleEnrichPeople}
                         fullWidth
                       >
                         Enrich People
                       </Button>
                     </CardContent>
                   </Card>
                 </Grid>

                 <Grid size={12} sm={6} md={3}>
                   <Card>
                     <CardContent sx={{ textAlign: 'center' }}>
                       <FilterIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                       <Typography variant="h6" gutterBottom>
                         Search Companies
                       </Typography>
                       <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                         Discover companies using filters like industry, size, revenue, and technologies.
                       </Typography>
                       <Button 
                         variant="contained" 
                         onClick={handleSearchCompanies}
                         fullWidth
                       >
                         Search Companies
                       </Button>
                     </CardContent>
                   </Card>
                 </Grid>

                 <Grid size={12} sm={6} md={3}>
                   <Card>
                     <CardContent sx={{ textAlign: 'center' }}>
                       <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                       <Typography variant="h6" gutterBottom>
                         Enrich Companies
                       </Typography>
                       <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                         Get detailed company information including size, revenue, location, and key people.
                       </Typography>
                       <Button 
                         variant="contained" 
                         onClick={handleEnrichSurfeCompanies}
                         fullWidth
                       >
                         Enrich Companies
                       </Button>
                     </CardContent>
                   </Card>
                                   </Grid>
                </>
              )}

              {pdlConnectionStatus === 'connected' && (
                <>
                  <Grid size={12} sm={6} md={3}>
                    <Card>
                      <CardContent sx={{ textAlign: 'center' }}>
                        <PersonIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h6" gutterBottom>
                          Enrich Person
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          Comprehensive person enrichment with education, experience, skills, and contact information.
                        </Typography>
                        <Button 
                          variant="contained" 
                          onClick={handleEnrichPerson}
                          fullWidth
                        >
                          Enrich Person
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid size={12} sm={6} md={3}>
                    <Card>
                      <CardContent sx={{ textAlign: 'center' }}>
                        <SearchIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h6" gutterBottom>
                          Search People
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          Advanced people search with detailed filters for job titles, education, skills, and experience.
                        </Typography>
                        <Button 
                          variant="contained" 
                          onClick={handleSearchPDLPeople}
                          fullWidth
                        >
                          Search People
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid size={12} sm={6} md={3}>
                    <Card>
                      <CardContent sx={{ textAlign: 'center' }}>
                        <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h6" gutterBottom>
                          Enrich Company
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          Detailed company information including industry codes, employee count, and business data.
                        </Typography>
                        <Button 
                          variant="contained" 
                          onClick={handleEnrichPDLCompany}
                          fullWidth
                        >
                          Enrich Company
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid size={12} sm={6} md={3}>
                    <Card>
                      <CardContent sx={{ textAlign: 'center' }}>
                        <WorkIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h6" gutterBottom>
                          Search Companies
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          Find companies by industry, size, location, and business characteristics with comprehensive data.
                        </Typography>
                        <Button 
                          variant="contained" 
                          onClick={handleSearchPDLCompanies}
                          fullWidth
                        >
                          Search Companies
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>
                </>
              )}
            </Grid>

          <Box sx={{ mt: 4 }}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">API Documentation</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body2" paragraph>
                  The BigData Corp integration provides access to comprehensive Brazilian business and personal data.
                </Typography>
                                 <Typography variant="subtitle2" gutterBottom>Available Datasets:</Typography>
                <List dense>
                  {bigDataConnectionStatus === 'connected' && (
                    <>
                      <ListItem>
                        <ListItemIcon><PersonIcon /></ListItemIcon>
                        <ListItemText 
                          primary="CPF Data (BigData Corp)" 
                          secondary="Basic personal data, contact information, addresses, professional data"
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><BusinessIcon /></ListItemIcon>
                        <ListItemText 
                          primary="CNPJ Data (BigData Corp)" 
                          secondary="Company registration, shareholders, business contacts, financial data"
                        />
                      </ListItem>
                    </>
                  )}
                                     {wizaConnectionStatus === 'connected' && (
                     <>
                       <ListItem>
                         <ListItemIcon><LinkedInIcon /></ListItemIcon>
                         <ListItemText 
                           primary="LinkedIn Profiles (Wiza)" 
                           secondary="Professional data, work history, education, skills, contact information"
                         />
                       </ListItem>
                       <ListItem>
                         <ListItemIcon><EmailIcon /></ListItemIcon>
                         <ListItemText 
                           primary="Email Finding (Wiza)" 
                           secondary="Verified email addresses with confidence scores and validation status"
                         />
                       </ListItem>
                     </>
                   )}
                                       {surfeConnectionStatus === 'connected' && (
                      <>
                        <ListItem>
                          <ListItemIcon><SearchIcon /></ListItemIcon>
                          <ListItemText 
                            primary="People Search (Surfe)" 
                            secondary="Advanced search with industry, location, job title, and seniority filters"
                          />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon><PersonIcon /></ListItemIcon>
                          <ListItemText 
                            primary="People Enrichment (Surfe)" 
                            secondary="Email, mobile, LinkedIn data with high confidence scores"
                          />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon><BusinessIcon /></ListItemIcon>
                          <ListItemText 
                            primary="Company Search & Enrichment (Surfe)" 
                            secondary="Company data, size, revenue, technologies, and key personnel"
                          />
                        </ListItem>
                      </>
                    )}
                    {pdlConnectionStatus === 'connected' && (
                      <>
                        <ListItem>
                          <ListItemIcon><DatabaseIcon /></ListItemIcon>
                          <ListItemText 
                            primary="Person Enrichment (People Data Labs)" 
                            secondary="Comprehensive profiles with education, experience, skills, and detailed contact information"
                          />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon><WorkIcon /></ListItemIcon>
                          <ListItemText 
                            primary="People Search (People Data Labs)" 
                            secondary="Advanced search with detailed filters for professional experience and education"
                          />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon><BusinessIcon /></ListItemIcon>
                          <ListItemText 
                            primary="Company Data (People Data Labs)" 
                            secondary="Business information with NAICS/SIC codes, employee data, and industry classification"
                          />
                        </ListItem>
                      </>
                    )}
                </List>
                <Typography variant="body2" sx={{ mt: 2 }}>
                  API Documentation: {' '}
                  {bigDataConnectionStatus === 'connected' && (
                    <a 
                      href="https://docs.bigdatacorp.com.br/plataforma/reference/api-de-views" 
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      BigData Corp
                    </a>
                  )}
                                     {(bigDataConnectionStatus === 'connected' && (wizaConnectionStatus === 'connected' || surfeConnectionStatus === 'connected' || pdlConnectionStatus === 'connected')) && ' | '}
                   {wizaConnectionStatus === 'connected' && (
                     <a 
                       href="https://wiza.co/api-docs" 
                       target="_blank" 
                       rel="noopener noreferrer"
                     >
                       Wiza
                     </a>
                   )}
                   {(wizaConnectionStatus === 'connected' && (surfeConnectionStatus === 'connected' || pdlConnectionStatus === 'connected')) && ' | '}
                   {surfeConnectionStatus === 'connected' && (
                     <a 
                       href="https://developers.surfe.com/" 
                       target="_blank" 
                       rel="noopener noreferrer"
                     >
                       Surfe
                     </a>
                   )}
                   {(surfeConnectionStatus === 'connected' && pdlConnectionStatus === 'connected') && ' | '}
                   {pdlConnectionStatus === 'connected' && (
                     <a 
                       href="https://www.peopledatalabs.com/pricing/person" 
                       target="_blank" 
                       rel="noopener noreferrer"
                     >
                       People Data Labs
                     </a>
                   )}
                </Typography>
              </AccordionDetails>
            </Accordion>
          </Box>
        </Box>
      )}

      <BigDataCorpConfigDialog
        open={configDialogOpen}
        onClose={() => setConfigDialogOpen(false)}
        onSave={handleSaveBigDataCredentials}
      />

      <WizaConfigDialog
        open={wizaConfigOpen}
        onClose={() => setWizaConfigOpen(false)}
        onSave={handleSaveWizaCredentials}
      />

      <SurfeConfigDialog
        open={surfeConfigOpen}
        onClose={() => setSurfeConfigOpen(false)}
        onSave={handleSaveSurfeCredentials}
      />

      <PDLConfigDialog
        open={pdlConfigOpen}
        onClose={() => setPdlConfigOpen(false)}
        onSave={handleSavePDLCredentials}
      />

      <EnrichmentDialog
        open={enrichmentDialogOpen}
        onClose={() => setEnrichmentDialogOpen(false)}
        type={enrichmentType}
      />

      <WizaEnrichmentDialog
        open={wizaEnrichmentOpen}
        onClose={() => setWizaEnrichmentOpen(false)}
        type={wizaEnrichmentType}
      />

      <SurfeEnrichmentDialog
        open={surfeEnrichmentOpen}
        onClose={() => setSurfeEnrichmentOpen(false)}
        type={surfeEnrichmentType}
      />

      <PDLEnrichmentDialog
        open={pdlEnrichmentOpen}
        onClose={() => setPdlEnrichmentOpen(false)}
        type={pdlEnrichmentType}
      />
    </Box>
  );
}; 