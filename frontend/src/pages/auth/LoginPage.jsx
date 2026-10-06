import { useState } from "react";
import { Eye, EyeOff, LockKeyhole, Mail, ShieldCheck } from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import AuthLayout from "../../components/AuthLayout";
import { useAuth } from "../../context/AuthContext";
import { getApiError } from "../../services/api";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(identifier.trim(), password);
      navigate(location.state?.from?.pathname || "/dashboard", { replace: true });
    } catch (requestError) {
      setError(getApiError(requestError, "Unable to sign in. Check your connection and try again."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthLayout mode="login">
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="form-alert" role="alert">{error}</div>}
        {location.state?.notice && <div className="form-notice" role="status">{location.state.notice}</div>}
        <label htmlFor="identifier">Email or username</label>
        <div className="input-wrap"><Mail size={17} /><input id="identifier" autoComplete="username" required value={identifier} onChange={(event) => setIdentifier(event.target.value)} placeholder="you@company.com" /></div>
        <div className="label-row"><label htmlFor="password">Password</label><span>Protected with encryption</span></div>
        <div className="input-wrap"><LockKeyhole size={17} /><input id="password" type={showPassword ? "text" : "password"} autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Enter your password" /><button className="password-toggle" type="button" onClick={() => setShowPassword((show) => !show)} aria-label={showPassword ? "Hide password" : "Show password"}>{showPassword ? <EyeOff size={17} /> : <Eye size={17} />}</button></div>
        <button className="primary-button" type="submit" disabled={submitting}>{submitting ? <><span className="spinner" /> Signing in...</> : "Sign in"}</button>
        <div className="signup-prompt">New to SmartERP? <Link to="/register">Create an account</Link></div>
        <div className="form-security"><ShieldCheck size={15} /> Your account is protected with secure authentication.</div>
      </form>
    </AuthLayout>
  );
}
