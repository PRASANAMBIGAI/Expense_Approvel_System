import React from 'react';
import './ExpenseTable.css';

const ExpenseTable = ({ expenses, onRowClick, emptyMessage = "No expenses found." }) => {
  if (!expenses || expenses.length === 0) {
    return (
      <div className="expense-table-empty">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getStatusBadgeClass = (status) => {
    switch(status.toLowerCase()) {
      case 'approved': return 'badge-success';
      case 'rejected': return 'badge-danger';
      default: return 'badge-warning';
    }
  };

  return (
    <div className="expense-table-container">
      <table className="expense-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr 
              key={expense.id} 
              onClick={() => onRowClick && onRowClick(expense)}
              className={onRowClick ? 'clickable-row' : ''}
            >
              <td className="col-id">#{expense.id}</td>
              <td className="col-title">{expense.title}</td>
              <td className="col-category">{expense.category}</td>
              <td className="col-amount">{formatCurrency(expense.amount)}</td>
              <td className="col-status">
                <span className={`status-badge ${getStatusBadgeClass(expense.status)}`}>
                  {expense.status.charAt(0).toUpperCase() + expense.status.slice(1)}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ExpenseTable;
