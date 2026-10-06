import { useState } from "react";
import { BadgeCheck, ChevronDown, CircleUserRound, LayoutDashboard, LogOut, Menu, ShieldCheck, X } from "lucide-react";
import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const comingSoon = ["Employees", "Customers", "Suppliers", "Products", "Inventory", "Sales", "Purchases", "Expenses", "Reports"];

export default function AppShell() {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  async function handleLogout() {
    let notice = "You have been signed out.";
    try {
      await logout();
    } catch {
      notice = "Signed out on this device, but the server could not confirm token revocation.";
    } finally {
      navigate("/login", { replace: true, state: { notice } });
    }
  }

  return (
    <div className="app-shell">
      {sidebarOpen && <button className="sidebar-scrim" onClick={() => setSidebarOpen(false)} aria-label="Close navigation" />}
      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <Link to="/dashboard" className="brand sidebar-brand"><span className="brand-mark">S</span><span>Smart<span>ERP</span></span></Link>
        <div className="workspace-switcher"><div className="workspace-icon">N</div><div><strong>Northstar Group</strong><small>Workspace</small></div><ChevronDown size={15} /></div>
        <div className="side-label">WORKSPACE</div>
        <nav className="side-nav">
          <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? "nav-active" : ""}`} onClick={() => setSidebarOpen(false)}>
            <LayoutDashboard size={18} /><span>Dashboard</span>
          </NavLink>
        </nav>
        <div className="side-label module-label">MODULES <span>COMING SOON</span></div>
        <nav className="side-nav future-nav">
          {comingSoon.map((item) => <div className="nav-item nav-disabled" key={item} title={`${item} — Coming Soon`}><span className="nav-dot" /><span>{item}</span></div>)}
        </nav>
        <div className="sidebar-bottom">
          <div className="secure-status"><span className="status-indicator" /><div><strong>Secure session</strong><small>Connection protected</small></div><ShieldCheck size={16} /></div>
          <button className="user-menu-trigger" onClick={() => setMenuOpen((open) => !open)}>
            <span className="avatar">{user?.full_name?.slice(0, 1).toUpperCase() || "U"}</span>
            <span className="user-menu-name"><strong>{user?.full_name}</strong><small>{user?.roles?.[0] || "EMPLOYEE"}</small></span>
            <ChevronDown size={15} />
          </button>
          {menuOpen && <div className="user-popover">
            <Link to="/profile" onClick={() => setMenuOpen(false)}><CircleUserRound size={16} /> My profile</Link>
            <button onClick={handleLogout}><LogOut size={16} /> Sign out</button>
          </div>}
        </div>
      </aside>
      <div className="main-column">
        <header className="topbar">
          <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setSidebarOpen(true)}><Menu size={20} /></button>
          <div className="breadcrumb">Workspace <span>/</span> <strong>Dashboard</strong></div>
          <div className="topbar-right"><span className="secure-pill"><BadgeCheck size={15} /> Secure workspace</span><span className="top-avatar">{user?.full_name?.slice(0, 1).toUpperCase()}</span></div>
        </header>
        <main className="content-area"><Outlet /></main>
      </div>
      {menuOpen && <button className="popover-dismiss" onClick={() => setMenuOpen(false)} aria-label="Close menu"><X size={1} /></button>}
    </div>
  );
}
