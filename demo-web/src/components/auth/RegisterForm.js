import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
const RegisterForm = ({ onSuccess }) => {
    const [formData, setFormData] = useState({
      email: '',
      password: '',
      username: '',
      cell_number: '',
      birth_date: '',
      sns_type: ''
    });
    const [error, setError] = useState('');
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        const response = await fetch('http://localhost:8000/api/v1/user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData)
        });
  
        const data = await response.json();
        if (response.ok) {
          onSuccess();
        } else {
          setError(data.detail);
        }
      } catch (err) {
        setError('Failed to register');
      }
    };
  
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <div className="p-8 bg-white rounded-lg shadow-md w-96">
          <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Register</h2>
          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md flex items-center">
              <AlertCircle className="w-5 h-5 mr-2" />
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            {Object.entries(formData).map(([key, value]) => (
              <div key={key}>
                <label className="block text-sm font-medium text-gray-700">
                  {key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')}
                </label>
                <input
                  type={key === 'password' ? 'password' : 'text'}
                  value={value}
                  onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
                  required={key !== 'full_name'}
                />
              </div>
            ))}
            <button
              type="submit"
              className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
            >
              Register
            </button>
          </form>
        </div>
      </div>
    );
  };

  export default RegisterForm;