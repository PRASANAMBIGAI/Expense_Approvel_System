import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import ExpenseTable from '../../components/expenses/ExpenseTable';
import Modal from '../../components/common/Modal';
import { getExpenses, submitExpense, getCategories } from '../../services/api';
import './EmployeeDashboard.css';

const EmployeeDashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newExpense, setNewExpense] = useState({
    title: '',
    amount: '',
    category_id: '',
    description: ''
  });

  const fetchExpenses = async () => {
    try {
      setLoading(true);
      const [expensesData, categoriesData] = await Promise.all([
        getExpenses(),
        getCategories()
      ]);
      setExpenses(Array.isArray(expensesData) ? expensesData : (expensesData.expenses || []));
      setCategories(Array.isArray(categoriesData) ? categoriesData : []);
      if (categoriesData.length > 0 && !newExpense.category_id) {
        setNewExpense(prev => ({ ...prev, category_id: categoriesData[0].id }));
      }
    } catch (err) {
      setError('Could not load expenses. The server might be unreachable.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleInputChange = (e) => {
    setNewExpense({
      ...newExpense,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmitExpense = async (e) => {
    e.preventDefault();
    try {
      await submitExpense({
        ...newExpense,
        amount: parseFloat(newExpense.amount),
        category_id: parseInt(newExpense.category_id)
      });
      setIsModalOpen(false);
      setNewExpense({ title: '', amount: '', category_id: categories.length > 0 ? categories[0].id : '', description: '' });
      fetchExpenses(); // Refresh list
    } catch (err) {
      alert('Failed to submit new expense.');
    }
  };

  return (
    <DashboardLayout role="employee">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">My Expenses</h1>
          <p className="dashboard-subtitle">Manage your reimbursement requests</p>
        </div>
        <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
          + New Request
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {loading ? (
        <div className="loading-state">Loading expenses...</div>
      ) : (
        <ExpenseTable expenses={expenses} emptyMessage="You haven't submitted any expenses yet." />
      )}

      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title="Submit New Expense"
      >
        <form onSubmit={handleSubmitExpense} className="expense-form">
          <div className="form-group">
            <label className="form-label" htmlFor="title">Title</label>
            <input 
              type="text" 
              id="title" 
              name="title" 
              className="form-control" 
              required 
              value={newExpense.title}
              onChange={handleInputChange}
              placeholder="e.g. Client Dinner in NYC"
            />
          </div>
          
          <div className="form-row">
            <div className="form-group half">
              <label className="form-label" htmlFor="amount">Amount (₹)</label>
              <input 
                type="number" 
                id="amount" 
                name="amount" 
                className="form-control" 
                required 
                min="0"
                step="0.01"
                value={newExpense.amount}
                onChange={handleInputChange}
                placeholder="15000"
              />
            </div>
            
            <div className="form-group half">
              <label className="form-label" htmlFor="category">Category</label>
              <select 
                id="category_id" 
                name="category_id" 
                className="form-control" 
                required
                value={newExpense.category_id}
                onChange={handleInputChange}
              >
                {categories.length === 0 && <option value="">No categories available</option>}
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="description">Description</label>
            <textarea 
              id="description" 
              name="description" 
              className="form-control" 
              rows="3" 
              value={newExpense.description}
              onChange={handleInputChange}
              placeholder="Provide context for this expense..."
            ></textarea>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Submit Request</button>
          </div>
        </form>
      </Modal>
    </DashboardLayout>
  );
};

export default EmployeeDashboard;
