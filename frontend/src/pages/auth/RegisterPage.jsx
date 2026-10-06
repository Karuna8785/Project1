import { useState } from "react";
import { Check, Eye, EyeOff, LockKeyhole, Mail, UserRound } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../../components/AuthLayout";
import { useAuth } from "../../context/AuthContext";
import { getApiError } from "../../services/api";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", username: "", password: "", confirm_password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{10,}$/.test(form.password);

  function update(field) {
    return (event) => setForm((current) => ({ ...current, [field]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    if (form.password !== form.confirm_password) {
      setError("Passwords do not match.");
      return;
    }
    setSubmitting(true);
    try {
      await register(form);
      navigate("/login", { replace: true, state: { notice: "Your account is ready. Sign in to continue." } });
    } catch (requestError) {
      setError(getApiError(requestError, "Unable to create your account. Please try again."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthLayout mode="register">
      <form className="auth-form register-form" onSubmit={handleSubmit}>
        {error && <div className="form-alert" role="alert">{error}</div>}
        <label htmlFor="full_name">Full name</label>
        <div className="input-wrap"><UserRound size={17} /><input id="full_name" autoComplete="name" minLength="2" maxLength="120" required value={form.full_name} onChange={update("full_name")} placeholder="Your full name" /></div>
        <label htmlFor="email">Work email</label>
        <div className="input-wrap"><Mail size={17} /><input id="email" type="email" autoComplete="email" required value={form.email} onChange={update("email")} placeholder="you@company.com" /></div>
        <label htmlFor="username">Username</label>
        <div className="input-wrap"><UserRound size={17} /><input id="username" autoComplete="username" minLength="3" maxLength="50" pattern="(?:[A-Za-z0-9_.]|-)+" required value={form.username} onChange={update("username")} placeholder="Choose a username" /></div>
        <label htmlFor="new-password">Password</label>
        <div className="input-wrap"><LockKeyhole size={17} /><input id="new-password" type={showPassword ? "text" : "password"} autoComplete="new-password" minLength="10" required value={form.password} onChange={update("password")} placeholder="Create a strong password" /><button className="password-toggle" type="button" onClick={() => setShowPassword((show) => !show)} aria-label={showPassword ? "Hide password" : "Show password"}>{showPassword ? <EyeOff size={17} /> : <Eye size={17} />}</button></div>
        <div className={`password-hint ${strongPassword ? "hint-valid" : ""}`}><Check size={14} /> 10+ characters, uppercase, lowercase, number and symbol</div>
        <label htmlFor="confirm-password">Confirm password</label>
        <div className="input-wrap"><LockKeyhole size={17} /><input id="confirm-password" type="password" autoComplete="new-password" required value={form.confirm_password} onChange={update("confirm_password")} placeholder="Enter your password again" /></div>
        <button className="primary-button" type="submit" disabled={submitting}>{submitting ? <><span className="spinner" /> Creating account...</> : "Create account"}</button>
        <div className="signup-prompt">Already have an account? <Link to="/login">Sign in</Link></div>
      </form>
    </AuthLayout>
  );
}
