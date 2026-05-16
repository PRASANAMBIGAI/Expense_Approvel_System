import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import ExpenseTable from '../../components/expenses/ExpenseTable';
import Modal from '../../components/common/Modal';
import { getExpenses, approveExpense, rejectExpense } from '../../services/api';
import './ManagerQueue.css';

const ManagerQueue = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal State
  const [selectedExpense, setSelectedExpense] = useState(null);
  const [comment, setComment] = useState('');
  const [actionError, setActionError] = useState('');

  const fetchExpenses = async () => {
    try {
      setLoading(true);
      const data = await getExpenses();
      setExpenses(Array.isArray(data) ? data : (data.expenses || []));
    } catch (err) {
      setError('Could not load pending approvals. The server might be unreachable.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleRowClick = (expense) => {
    setSelectedExpense(expense);
    setComment('');
    setActionError('');
  };

  const handleAction = async (actionType) => {
    if (actionType === 'reject' && !comment.trim()) {
      setActionError('A comment is required when rejecting an expense.');
      return;
    }

    try {
      if (actionType === 'approve') {
        await approveExpense(selectedExpense.id, comment);
      } else {
        await rejectExpense(selectedExpense.id, comment);
      }
      setSelectedExpense(null);
      fetchExpenses(); // Refresh queue
    } catch (err) {
      setActionError(`Failed to ${actionType} expense.`);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <DashboardLayout role="manager">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Approval Queue</h1>
          <p className="dashboard-subtitle">Review and process team expenses</p>
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {loading ? (
        <div className="loading-state">Loading queue...</div>
      ) : (
        <ExpenseTable 
          expenses={expenses} 
          onRowClick={handleRowClick}
          emptyMessage="You're all caught up! No pending approvals." 
        />
      )}

      <Modal 
        isOpen={!!selectedExpense} 
        onClose={() => setSelectedExpense(null)} 
        title="Review Expense Request"
      >
        {selectedExpense && (
          <div className="expense-details">
            <div className="detail-row">
              <span className="detail-label">Employee</span>
              <span className="detail-value">{selectedExpense.employee_name || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Title</span>
              <span className="detail-value">{selectedExpense.title}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Amount</span>
              <span className="detail-value highlight">{formatCurrency(selectedExpense.amount)}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Category</span>
              <span className="detail-value">{selectedExpense.category}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Description</span>
              <span className="detail-value text-block">{selectedExpense.description || 'No description provided.'}</span>
            </div>

            <hr className="divider" />

            <div className="form-group">
              <label className="form-label" htmlFor="comment">Manager Comment <span className="required">* required for rejection</span></label>
              <textarea 
                id="comment" 
                className="form-control" 
                rows="3" 
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Provide reasoning if rejecting..."
              ></textarea>
            </div>

            {actionError && <div className="action-error">{actionError}</div>}

            <div className="modal-actions">
              <button 
                type="button" 
                className="btn btn-secondary btn-danger-outline" 
                onClick={() => handleAction('reject')}
              >
                Reject Request
              </button>
              <button 
                type="button" 
                className="btn btn-success" 
                onClick={() => handleAction('approve')}
              >
                Approve Request
              </button>
            </div>
          </div>
        )}
      </Modal>
    </DashboardLayout>
  );
};

export default ManagerQueue;
