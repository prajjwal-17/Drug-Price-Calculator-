import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Ruler } from "lucide-react";
import "./App.css";
import "./Navbar.css";
import SignInPage from "./Page/SignInPage";

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        {/* Logo and Company Name */}
        <div className="logo-container">
          <Link to="/" className="logo-link">
            <Ruler className="logo" />
            <h1 className="site-title">Random Company</h1>
          </Link>
        </div>

        {/* Navigation Links */}
        <div className="nav-links">
          <Link to="/product">Product</Link>
          <Link to="/customers">Customers</Link>
          <Link to="/company">Company</Link>
          <Link to="/pricing">Pricing</Link>
          <Link to="/changelog">Changelog</Link>
        </div>

        {/* Buttons (Sign In & Get Started) */}
        <div className="auth-buttons">
          <Link to="/signin" className="btn signin-btn">Sign In</Link>
          <Link to="/get-started" className="btn get-started-btn">Get Started</Link>
        </div>
      </nav>

      {/* Routes */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/product" element={<ProductPage />} />
        <Route path="/customers" element={<CustomersPage />} />
        <Route path="/company" element={<CompanyPage />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/changelog" element={<ChangelogPage />} />
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/get-started" element={<GetStartedPage />} />
      </Routes>
    </BrowserRouter>
  );
}

// Dummy Pages
function HomePage() {
  return <div>Welcome to Random Company</div>;
}
function ProductPage() {
  return <div>Product Information</div>;
}
function CustomersPage() {
  return <div>Customers</div>;
}
function CompanyPage() {
  return <div>Company Info</div>;
}
function PricingPage() {
  return <div>Pricing Details</div>;
}
function ChangelogPage() {
  return <div>Changelog</div>;
}

function GetStartedPage() {
  return <div>Get Started Page</div>;
}

export default App;
