import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-container">
      <nav className="landing-navbar">
        <div className="brand">Stitch Expense</div>
        <div className="nav-actions">
          <Link to="/login" className="btn btn-secondary">Log In</Link>
          <Link to="/register" className="btn btn-primary">Sign Up</Link>
        </div>
      </nav>

      <main className="hero-section">
        <h1 className="hero-title">Enterprise Expense Approval, Simplified.</h1>
        <p className="hero-subtitle">
          Submit, track, and approve expenses seamlessly with our sleek, high-efficiency platform designed for modern enterprises.
        </p>
        <div className="cta-group">
          <Link to="/register" className="btn btn-primary btn-large">Get Started Now</Link>
        </div>
      </main>

      <section className="features-section">
        <div className="feature-card">
          <h3>Fast Approvals</h3>
          <p>Manager queues designed for high-density data and one-click decisions.</p>
        </div>
        <div className="feature-card">
          <h3>Real-time Tracking</h3>
          <p>Employees can see exactly where their reimbursements are in the pipeline.</p>
        </div>
        <div className="feature-card">
          <h3>Secure & Compliant</h3>
          <p>Role-based access ensuring data stays visible only to the right people.</p>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
