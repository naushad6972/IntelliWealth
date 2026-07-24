import React, { Suspense, lazy } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Landing } from './pages/Landing';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

const Dashboard = lazy(() => import('./pages/Dashboard').then(m => ({ default: m.Dashboard })));
const Transactions = lazy(() => import('./pages/Transactions').then(m => ({ default: m.Transactions })));
const ConnectBank = lazy(() => import('./pages/ConnectBank').then(m => ({ default: m.ConnectBank })));
const UploadCSV = lazy(() => import('./pages/UploadCSV').then(m => ({ default: m.UploadCSV })));
const BudgetPlanner = lazy(() => import('./pages/BudgetPlanner').then(m => ({ default: m.BudgetPlanner })));
const Analytics = lazy(() => import('./pages/Analytics').then(m => ({ default: m.Analytics })));
const Goals = lazy(() => import('./pages/Goals').then(m => ({ default: m.Goals })));
const Forecast = lazy(() => import('./pages/Forecast').then(m => ({ default: m.Forecast })));
const HealthScore = lazy(() => import('./pages/HealthScore').then(m => ({ default: m.HealthScore })));
const EMICalculator = lazy(() => import('./pages/EMICalculator').then(m => ({ default: m.EMICalculator })));
const InvestmentEducation = lazy(() => import('./pages/InvestmentEducation').then(m => ({ default: m.InvestmentEducation })));
import { ProtectedLayout } from './components/ProtectedLayout';
import { AIChat } from './pages/AIChat';
import { Reports } from './pages/Reports';
import { Notifications } from './pages/Notifications';
import { Profile } from './pages/Profile';
import { Settings } from './pages/Settings';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Suspense fallback={<div className="p-6">Loading...</div>}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route element={<ProtectedLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/connect-bank" element={<ConnectBank />} />
            <Route path="/upload-csv" element={<UploadCSV />} />
            <Route path="/budgets" element={<BudgetPlanner />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/goals" element={<Goals />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/health" element={<HealthScore />} />
            <Route path="/emi" element={<EMICalculator />} />
            <Route path="/education" element={<InvestmentEducation />} />
            <Route path="/ai-chat" element={<AIChat />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Routes>
        </Suspense>
      </BrowserRouter>
    </AuthProvider>
  );
}

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
