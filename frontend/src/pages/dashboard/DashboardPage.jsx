import { ArrowUpRight, BadgeCheck, CircleUserRound, KeyRound, Shield, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();
  return (
    <div className="page-content">
      <div className="page-heading"><div><div className="eyebrow">OVERVIEW</div><h1>Good to have you here, {user?.full_name?.split(" ")[0]}.</h1><p>Your secure SmartERP workspace is ready.</p></div><div className="date-chip"><span className="status-indicator" /> All systems operational</div></div>
      <section className="welcome-banner"><div className="welcome-copy"><div className="banner-kicker"><ShieldCheck size={15} /> AUTHENTICATION MODULE ACTIVE</div><h2>SmartERP Dashboard</h2><p>Authentication module successfully connected.</p><Link to="/profile" className="banner-link">View your profile <ArrowUpRight size={16} /></Link></div><div className="banner-art"><div className="art-orbit orbit-a" /><div className="art-orbit orbit-b" /><div className="art-shield"><ShieldCheck size={42} /></div><span className="art-dot dot-a" /><span className="art-dot dot-b" /></div></section>
      <div className="section-title"><div><h2>Account overview</h2><p>Your identity and access at a glance.</p></div><Link to="/profile" className="text-link">Manage profile <ArrowUpRight size={15} /></Link></div>
      <section className="overview-grid">
        <article className="overview-card"><div className="card-icon blue-icon"><CircleUserRound size={19} /></div><span className="card-label">SIGNED IN AS</span><strong>{user?.full_name}</strong><small>{user?.email}</small></article>
        <article className="overview-card"><div className="card-icon purple-icon"><Shield size={19} /></div><span className="card-label">ACCESS ROLE</span><strong>{user?.roles?.join(", ") || "EMPLOYEE"}</strong><small>Role-based access control enabled</small></article>
        <article className="overview-card"><div className="card-icon green-icon"><KeyRound size={19} /></div><span className="card-label">PERMISSIONS</span><strong>{user?.permissions?.length || 0} assigned</strong><small>{user?.permissions?.slice(0, 3).join(" · ") || "Access assigned by role"}</small></article>
      </section>
      <section className="security-summary"><div className="summary-icon"><BadgeCheck size={20} /></div><div><strong>Protected by SmartERP security</strong><p>Your account is authenticated and access is controlled by assigned roles and permissions.</p></div><span className="summary-status">ACTIVE SESSION</span></section>
      <div className="module-coming"><span>MORE CAPABILITIES ARE ON THE WAY</span><p>Business modules will appear here as they become available.</p></div>
    </div>
  );
}
