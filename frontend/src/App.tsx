import LandingPage from './pages/common/LandingPage/landing-page';
import DiscoverPage from './pages/customer/DiscoverPage/discover-page';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUpPage from './pages/customer/SignUpPage/sign-up-page';
import CompanyDashboardPage from './pages/customer/CompanyDashboardPage/company-dashboard-page';
import HubPage from './pages/customer/HubPage/hub-page';
import 'bootstrap/dist/css/bootstrap.min.css'
import CustomerDashboardPage from './pages/customer/CustomerDashboardPage/customer-dashboard-page'

import AdminDashboardPage from './pages/admin/AdminDashboardPage/admin-dashboard-page';

import SignInPage from './pages/common/SignInPage/sign-in-page';
import { AuthContext, AuthProvider } from './contexts/authContext';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AboutUsPage from './pages/common/AboutUsPage/aboutus-page';
import CustomerProfilePage from './pages/customer/CustomerProfilePage/customer-profile-page';

function App() {

  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <header className="App-header">
            <Routes>
              <Route path="/customers/:customerId/discover" Component={DiscoverPage}/>
              <Route path="/" Component={LandingPage} />
              <Route path="/signup" Component={SignUpPage} />
              <Route path="/login" Component={SignInPage} />
              <Route path="/hub" Component={HubPage} />
              <Route path="/customers/:customerId/companies" Component={CompanyDashboardPage} />
              <Route path="/customers/:customerId/dashboard" Component={CustomerDashboardPage}/>
              <Route path="/admins/:adminId/train" Component={AdminDashboardPage}/>
              <Route path='/customers/:customerId/profile' Component={CustomerProfilePage} />
              <Route path='/aboutus' Component={AboutUsPage} />
            </Routes>
          </header>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;