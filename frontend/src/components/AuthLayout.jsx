import { ArrowUpRight, LockKeyhole, ShieldCheck } from "lucide-react";

export default function AuthLayout({ children, mode }) {
  return (
    <main className="auth-shell">
      <section className="auth-brand-panel">
        <a className="brand brand-light" href="/login" aria-label="SmartERP home">
          <span className="brand-mark">S</span>
          <span>Smart<span>ERP</span></span>
        </a>
        <div className="brand-copy">
          <div className="eyebrow"><ShieldCheck size={15} /> BUSINESS OPERATIONS PLATFORM</div>
          <h1>Clarity for every part of your business.</h1>
          <p>A secure foundation for the teams, workflows, and decisions that move your organization forward.</p>
        </div>
        <div className="security-note"><LockKeyhole size={17} /><span>Secure access protected by encrypted credentials and session controls.</span></div>
        <div className="brand-decoration decoration-one" />
        <div className="brand-decoration decoration-two" />
      </section>
      <section className="auth-form-panel">
        <div className="auth-mobile-brand"><span className="brand-mark">S</span><strong>SmartERP</strong></div>
        <div className="auth-card">
          <div className="auth-heading">
            <div className="eyebrow">{mode === "login" ? "WELCOME BACK" : "GET STARTED"}</div>
            <h2>{mode === "login" ? "Sign in to your account" : "Create your account"}</h2>
            <p>{mode === "login" ? "Enter your details to access your workspace." : "Set up your secure access to SmartERP."}</p>
          </div>
          {children}
          <div className="auth-footnote">Protected workspace <ArrowUpRight size={14} /></div>
        </div>
        <div className="copyright">© 2026 SmartERP · Secure enterprise access</div>
      </section>
    </main>
  );
}
