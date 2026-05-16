import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { getCurrentUser } from '../../services/api';
import './DashboardLayout.css';

const DashboardLayout = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [role, setRole] = useState(null);

  useEffect(() => {
    const fetchRole = async () => {
      try {
        const user = await getCurrentUser();
        setRole(user.role);
      } catch {
        navigate('/login');
      }
    };
    fetchRole();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <nav className="dashboard-navbar">
        <div className="brand">Stitch Expense</div>
        <div className="nav-links">
          {role === 'employee' && (
            <Link 
              to="/employee/dashboard" 
              className={`nav-link ${location.pathname.includes('/employee') ? 'active' : ''}`}
            >
              My Expenses
            </Link>
          )}
          {(role === 'manager' || role === 'admin') && (
            <Link 
              to="/manager/dashboard" 
              className={`nav-link ${location.pathname.includes('/manager') ? 'active' : ''}`}
            >
              Approval Queue
            </Link>
          )}
          {role === 'admin' && (
            <Link 
              to="/admin/dashboard" 
              className={`nav-link ${location.pathname.includes('/admin') ? 'active' : ''}`}
            >
              Category Management
            </Link>
          )}
        </div>
        <div className="nav-actions">
          <button onClick={handleLogout} className="btn btn-secondary btn-sm">Sign Out</button>
        </div>
      </nav>

      <main className="dashboard-main">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;
