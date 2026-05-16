const BASE_URL = 'http://localhost:8000';

export const apiFetch = async (endpoint, options = {}) => {
  const token = localStorage.getItem('jwt_token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`);
  }

  return response.json();
};

// --- Auth Endpoints ---
export const registerUser = (userData) => {
  return apiFetch('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
};

export const loginUser = async (email, password) => {
  // OAuth2 expects form data, not JSON
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }
  return response.json();
};

export const getCurrentUser = () => {
  return apiFetch('/auth/me');
};

// --- Expenses Endpoints ---
export const getExpenses = () => {
  return apiFetch('/expenses/');
};

export const getExpense = (id) => {
  return apiFetch(`/expenses/${id}`);
};

export const submitExpense = (expenseData) => {
  return apiFetch('/expenses/', {
    method: 'POST',
    body: JSON.stringify(expenseData),
  });
};

export const updateExpense = (id, expenseData) => {
  return apiFetch(`/expenses/${id}`, {
    method: 'PUT',
    body: JSON.stringify(expenseData),
  });
};

export const deleteExpense = (id) => {
  return apiFetch(`/expenses/${id}`, {
    method: 'DELETE',
  });
};

export const approveExpense = (id, comment = '') => {
  return apiFetch(`/expenses/${id}/approve`, {
    method: 'POST',
    body: JSON.stringify({ comment }),
  });
};

export const rejectExpense = (id, comment = '') => {
  return apiFetch(`/expenses/${id}/reject`, {
    method: 'POST',
    body: JSON.stringify({ comment }),
  });
};

// --- Categories Endpoints ---
export const getCategories = () => {
  return apiFetch('/categories/');
};

export const createCategory = (categoryData) => {
  return apiFetch('/categories/', {
    method: 'POST',
    body: JSON.stringify(categoryData),
  });
};

export const updateCategory = (id, categoryData) => {
  return apiFetch(`/categories/${id}`, {
    method: 'PUT',
    body: JSON.stringify(categoryData),
  });
};

export const deleteCategory = (id) => {
  return apiFetch(`/categories/${id}`, {
    method: 'DELETE',
  });
};
