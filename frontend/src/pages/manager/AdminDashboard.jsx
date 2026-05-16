import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { getCategories, createCategory, deleteCategory } from '../../services/api';
import '../employee/EmployeeDashboard.css';

const AdminDashboard = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newCatName, setNewCatName] = useState('');
  const [newCatDesc, setNewCatDesc] = useState('');

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const data = await getCategories();
      setCategories(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleAddCategory = async (e) => {
    e.preventDefault();
    if (!newCatName) return;
    try {
      await createCategory({ name: newCatName, description: newCatDesc });
      setNewCatName('');
      setNewCatDesc('');
      fetchCategories();
    } catch (err) {
      alert("Failed to add category");
    }
  };

  const handleDeleteCategory = async (id) => {
    if (!window.confirm("Are you sure you want to delete this category?")) return;
    try {
      await deleteCategory(id);
      fetchCategories();
    } catch (err) {
      alert("Failed to delete category");
    }
  };

  return (
    <DashboardLayout role="admin">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Category Management</h1>
          <p className="dashboard-subtitle">Manage system-wide expense categories</p>
        </div>
      </div>

      <div className="admin-section" style={{ background: 'white', padding: '2rem', borderRadius: '12px', marginBottom: '2rem', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
        <h3>Add New Category</h3>
        <form onSubmit={handleAddCategory} style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <input 
            type="text" 
            className="form-control" 
            placeholder="Category Name" 
            value={newCatName}
            onChange={(e) => setNewCatName(e.target.value)}
            required
          />
          <input 
            type="text" 
            className="form-control" 
            placeholder="Description (Optional)" 
            value={newCatDesc}
            onChange={(e) => setNewCatDesc(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">Add Category</button>
        </form>
      </div>

      <div className="admin-section" style={{ background: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
        <h3>Existing Categories</h3>
        {loading ? <p>Loading...</p> : (
          <table className="expense-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(cat => (
                <tr key={cat.id}>
                  <td>{cat.id}</td>
                  <td><strong>{cat.name}</strong></td>
                  <td>{cat.description}</td>
                  <td>
                    <button onClick={() => handleDeleteCategory(cat.id)} className="btn" style={{ background: '#fef2f2', color: '#dc2626', border: '1px solid #fecaca' }}>Delete</button>
                  </td>
                </tr>
              ))}
              {categories.length === 0 && <tr><td colSpan="4">No categories found.</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AdminDashboard;
