import { BadgeCheck, KeyRound, Mail, ShieldCheck, UserRound } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export default function ProfilePage() {
  const { user } = useAuth();
  return (
    <div className="page-content profile-page">
      <div className="page-heading"><div><div className="eyebrow">ACCOUNT SETTINGS</div><h1>Your profile</h1><p>Review your account details and access.</p></div></div>
      <section className="profile-card">
        <div className="profile-hero"><div className="profile-avatar">{user?.full_name?.slice(0, 1).toUpperCase()}</div><div><h2>{user?.full_name}</h2><p>{user?.email}</p></div><span className="verified-badge"><BadgeCheck size={15} /> Verified account</span></div>
        <div className="profile-details">
          <div className="profile-detail"><span><UserRound size={17} /> Full name</span><strong>{user?.full_name}</strong></div>
          <div className="profile-detail"><span><Mail size={17} /> Email address</span><strong>{user?.email}</strong></div>
          <div className="profile-detail"><span><UserRound size={17} /> Username</span><strong>{user?.username}</strong></div>
          <div className="profile-detail"><span><ShieldCheck size={17} /> Assigned role</span><strong>{user?.roles?.join(", ") || "EMPLOYEE"}</strong></div>
          <div className="profile-detail"><span><KeyRound size={17} /> Permissions</span><strong>{user?.permissions?.length ? user.permissions.join(", ") : "None assigned"}</strong></div>
        </div>
      </section>
      <div className="profile-notice"><ShieldCheck size={18} /><div><strong>Your account is protected</strong><p>Authentication is secured with encrypted passwords, expiring access tokens, and role-based permissions.</p></div></div>
    </div>
  );
}
