# React + Vite Frontend Implementation Plan - Enrich DDF Floor 2

## Overview

Create a modern, responsive frontend using React + Vite to provide a user-friendly interface for the Enrich DDF Floor 2 API backend.

## Technology Stack

### Core Framework
- **React 18+** - Modern React with hooks and concurrent features
- **Vite** - Fast build tool and dev server
- **TypeScript** - Type safety and better developer experience

### UI Framework & Styling
- **Material-UI (MUI)** - Comprehensive React component library
- **Emotion** - CSS-in-JS styling (comes with MUI)
- **Material Icons** - Icon set for consistent UI

### State Management
- **React Query (TanStack Query)** - Server state management and caching
- **Zustand** - Lightweight global state management

### Routing & Navigation
- **React Router v6** - Client-side routing
- **React Router DOM** - Browser routing utilities

### HTTP Client
- **Axios** - HTTP client with interceptors and request/response handling

### Form Management
- **React Hook Form** - Performant form library
- **Zod** - Schema validation for forms

### Development Tools
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Husky** - Git hooks
- **TypeScript** - Static type checking

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── companies/
│   │   │   ├── CompanyList.tsx
│   │   │   ├── CompanyForm.tsx
│   │   │   └── CompanyCard.tsx
│   │   ├── contacts/
│   │   │   ├── ContactList.tsx
│   │   │   ├── ContactForm.tsx
│   │   │   └── ContactCard.tsx
│   │   └── products/
│   │       ├── ProductList.tsx
│   │       ├── ProductForm.tsx
│   │       └── ProductCard.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Companies.tsx
│   │   ├── Contacts.tsx
│   │   ├── Products.tsx
│   │   └── Settings.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── companies.ts
│   │   ├── contacts.ts
│   │   └── products.ts
│   ├── hooks/
│   │   ├── useCompanies.ts
│   │   ├── useContacts.ts
│   │   └── useProducts.ts
│   ├── types/
│   │   ├── company.ts
│   │   ├── contact.ts
│   │   └── product.ts
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   └── validation.ts
│   ├── store/
│   │   └── appStore.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .eslintrc.js
├── .prettierrc
└── README.md
```

## Implementation Phases

### Phase 1: Project Setup & Configuration (2-3 hours)

#### 1.1 Initialize Vite React Project
```bash
cd /Users/luismartins/local_repos/enrich-ddf-floor-2
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

#### 1.2 Install Core Dependencies
```bash
# UI Framework
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material

# State Management & HTTP
npm install @tanstack/react-query axios zustand

# Routing
npm install react-router-dom

# Forms & Validation
npm install react-hook-form @hookform/resolvers zod

# Development Tools
npm install -D eslint prettier husky lint-staged
npm install -D @types/node
```

#### 1.3 Configure Development Tools
- Set up ESLint configuration
- Configure Prettier
- Set up Husky for pre-commit hooks
- Configure TypeScript paths

### Phase 2: Core Infrastructure (3-4 hours)

#### 2.1 API Service Layer
```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8247';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request/Response interceptors for error handling
```

#### 2.2 Type Definitions
```typescript
// src/types/company.ts
export interface Company {
  id: number;
  name: string;
  industry?: string;
  website?: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateCompanyRequest {
  name: string;
  industry?: string;
  website?: string;
  description?: string;
}
```

#### 2.3 React Query Setup
```typescript
// src/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});
```

### Phase 3: Basic Layout & Navigation (2-3 hours)

#### 3.1 App Layout Component
```typescript
// src/components/common/Layout.tsx
import { AppBar, Drawer, Toolbar, Typography } from '@mui/material';

export const Layout = ({ children }) => {
  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6">
            Enrich DDF Floor 2
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent">
        {/* Navigation items */}
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
    </Box>
  );
};
```

#### 3.2 Routing Setup
```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/companies" element={<Companies />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/products" element={<Products />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
```

### Phase 4: Companies Module (4-5 hours)

#### 4.1 Company Service
```typescript
// src/services/companies.ts
export const companiesService = {
  getAll: async (): Promise<Company[]> => {
    const response = await apiClient.get('/api/v1/companies');
    return response.data;
  },

  create: async (data: CreateCompanyRequest): Promise<Company> => {
    const response = await apiClient.post('/api/v1/companies', data);
    return response.data.data;
  },
};
```

#### 4.2 Custom Hooks
```typescript
// src/hooks/useCompanies.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export const useCompanies = () => {
  return useQuery({
    queryKey: ['companies'],
    queryFn: companiesService.getAll,
  });
};

export const useCreateCompany = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: companiesService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['companies'] });
    },
  });
};
```

#### 4.3 Company Components
```typescript
// src/components/companies/CompanyList.tsx
export const CompanyList = () => {
  const { data: companies, isLoading, error } = useCompanies();

  if (isLoading) return <CircularProgress />;
  if (error) return <Alert severity="error">Error loading companies</Alert>;

  return (
    <Grid container spacing={2}>
      {companies?.map((company) => (
        <Grid item xs={12} md={6} lg={4} key={company.id}>
          <CompanyCard company={company} />
        </Grid>
      ))}
    </Grid>
  );
};
```

### Phase 5: Contacts Module (3-4 hours)

#### 5.1 Contact Service & Hooks
- Similar structure to companies
- Contact-specific API endpoints
- CRUD operations with React Query

#### 5.2 Contact Components
- ContactList with search and filtering
- ContactForm with validation
- ContactCard with contact details

### Phase 6: Products Module (3-4 hours)

#### 6.1 Product Service & Hooks
- Product-specific API endpoints
- Product CRUD operations
- Search and categorization

#### 6.2 Product Components
- ProductList with grid/list view toggle
- ProductForm with category selection
- ProductCard with pricing display

### Phase 7: Dashboard & Analytics (2-3 hours)

#### 7.1 Dashboard Overview
```typescript
// src/pages/Dashboard.tsx
export const Dashboard = () => {
  const { data: companies } = useCompanies();
  const { data: contacts } = useContacts();
  const { data: products } = useProducts();

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <StatCard
          title="Companies"
          value={companies?.length || 0}
          icon={<BusinessIcon />}
        />
      </Grid>
      {/* More stat cards */}
    </Grid>
  );
};
```

#### 7.2 Statistics Cards
- Total counts for each entity
- Recent activity feed
- Quick action buttons

### Phase 8: Advanced Features (4-5 hours)

#### 8.1 Search & Filtering
```typescript
// src/components/common/SearchFilter.tsx
export const SearchFilter = ({ onSearch, onFilter }) => {
  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <TextField
        placeholder="Search..."
        onChange={(e) => onSearch(e.target.value)}
        InputProps={{
          startAdornment: <SearchIcon />,
        }}
      />
      <FormControl sx={{ ml: 2, minWidth: 120 }}>
        <Select onChange={(e) => onFilter(e.target.value)}>
          <MenuItem value="">All</MenuItem>
          {/* Filter options */}
        </Select>
      </FormControl>
    </Paper>
  );
};
```

#### 8.2 Data Export
- Export to CSV functionality
- Print-friendly views
- Data visualization charts

#### 8.3 Responsive Design
- Mobile-first approach
- Responsive grid layouts
- Touch-friendly interactions

### Phase 9: Testing & Optimization (3-4 hours)

#### 9.1 Unit Testing
```bash
npm install -D @testing-library/react @testing-library/jest-dom vitest
```

#### 9.2 Performance Optimization
- Code splitting with React.lazy
- Image optimization
- Bundle size analysis

#### 9.3 Error Handling
- Global error boundary
- Toast notifications
- Retry mechanisms

### Phase 10: Deployment & Integration (2-3 hours)

#### 10.1 Build Configuration
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8247',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../static/frontend',
  },
});
```

#### 10.2 FastAPI Integration
```python
# main.py updates
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static/frontend", html=True), name="frontend")
```

## Development Workflow

### 1. Development Setup
```bash
# Terminal 1: Start FastAPI backend
cd /Users/luismartins/local_repos/enrich-ddf-floor-2
source venv/bin/activate
python main.py

# Terminal 2: Start Vite dev server
cd frontend
npm run dev
```

### 2. Development URLs
- **Frontend**: `http://localhost:5173` (Vite dev server)
- **Backend API**: `http://127.0.0.1:8247`
- **API Docs**: `http://127.0.0.1:8247/docs`

### 3. Production Build
```bash
cd frontend
npm run build
# Files will be built to ../static/frontend/
```

## Key Features to Implement

### Core Functionality
- ✅ CRUD operations for Companies, Contacts, Products
- ✅ Real-time data synchronization
- ✅ Search and filtering
- ✅ Responsive design
- ✅ Form validation
- ✅ Error handling

### Enhanced UX
- ✅ Loading states and skeletons
- ✅ Toast notifications
- ✅ Confirmation dialogs
- ✅ Bulk operations
- ✅ Data export
- ✅ Keyboard shortcuts

### Technical Features
- ✅ TypeScript throughout
- ✅ Performance optimization
- ✅ Accessibility compliance
- ✅ SEO optimization
- ✅ Progressive Web App features

## Estimated Timeline

- **Total Development Time**: 25-35 hours
- **Sprint Duration**: 2-3 weeks (part-time)
- **MVP Delivery**: 1 week (basic CRUD + layout)
- **Full Feature Set**: 2-3 weeks

## Success Criteria

1. **Functional Requirements**
   - All API endpoints accessible through UI
   - CRUD operations for all entities
   - Responsive design works on mobile/desktop

2. **Technical Requirements**
   - TypeScript coverage > 95%
   - Bundle size < 1MB
   - Lighthouse score > 90
   - No accessibility violations

3. **User Experience**
   - Intuitive navigation
   - Fast load times (< 3s)
   - Clear error messages
   - Consistent design system

## Future Enhancements

### Phase 11: Advanced Features
- Real-time updates with WebSocket
- Advanced charts and analytics
- Data visualization dashboards
- API key management
- User authentication/authorization

### Phase 12: Performance & Scaling
- Service Worker for offline support
- Virtual scrolling for large datasets
- Advanced caching strategies
- Internationalization (i18n)

## Dependencies Summary

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@mui/material": "^5.14.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.0",
    "@tanstack/react-query": "^4.32.0",
    "axios": "^1.5.0",
    "zustand": "^4.4.0",
    "react-router-dom": "^6.15.0",
    "react-hook-form": "^7.45.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^4.4.0",
    "eslint": "^8.45.0",
    "prettier": "^3.0.0",
    "husky": "^8.0.0"
  }
}
```

This plan provides a comprehensive roadmap for implementing a modern, professional React frontend for the Enrich DDF Floor 2 API backend.
