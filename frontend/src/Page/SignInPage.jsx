import { useState } from "react";
import { Link } from "react-router-dom";
import { Eye, EyeOff, Lock, Mail, MessagesSquare } from "lucide-react";
import "./SignInPage.css"; // Ensure you have a separate CSS file for styling

const SignInPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });

  const [login, isLoggingIn] = [() => {}, false];

  const handleSubmit = async (e) => {
    e.preventDefault();
    login(formData);
  };

  return (
    <div className="signin-page-container">
      {/* Left Side: Advertisement Section */}
      <div className="signin-ad-section">
        <h1>Welcome to Random Company</h1>
        <p>Join us to experience the best solutions for your business.</p>
        <p>Innovate. Collaborate. Succeed.</p>
      </div>

      {/* Right Side: Login Section */}
      <div className="signin-form-container">
        <div className="signin-card">
          <div className="text-center">
            <div className="icon-container">
              <MessagesSquare className="icon" />
            </div>
            <h2>Welcome Back</h2>
            <p>Sign in to your account</p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Email</label>
              <div className="input-wrapper">
                <Mail className="input-icon" />
                <input
                  type="email"
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Password</label>
              <div className="input-wrapper">
                <Lock className="input-icon" />
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff /> : <Eye />}
                </button>
              </div>
            </div>

            <button type="submit" className="signin-btn" disabled={isLoggingIn}>
              {isLoggingIn ? "Loading..." : "Sign in"}
            </button>
          </form>

          <p className="signup-link">
            Don't have an account? <Link to="/signup">Create account</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignInPage;
