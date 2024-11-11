import React, { useState } from 'react';
import { AlertCircle, Check } from 'lucide-react';

const LoginForm = ({ onSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        onSuccess();
      } else {
        setError(data.detail);
      }
    } catch (err) {
      setError('Failed to login');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Login</h2>
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md flex items-center">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

const RegisterForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: ''
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

const UserProfile = ({ onLogout }) => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState('');

  React.useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          onLogout();
          return;
        }

        const response = await fetch('http://localhost:8000/api/v1/user/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        } else {
          throw new Error('Failed to fetch user data');
        }
      } catch (err) {
        setError('Failed to load user data');
        onLogout();
      }
    };

    fetchUserData();
  }, [onLogout]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <div className="p-8 bg-white rounded-lg shadow-md">
          <div className="text-red-600">{error}</div>
        </div>
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <div className="p-8 bg-white rounded-lg shadow-md">
          <div className="text-gray-600">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Profile</h2>
          <button
            onClick={onLogout}
            className="px-4 py-2 text-sm text-red-600 hover:text-red-700"
          >
            Logout
          </button>
        </div>
        <div className="space-y-4">
          <div className="flex items-center text-green-600 mb-4">
            <Check className="w-5 h-5 mr-2" />
            Successfully logged in!
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600">Email</label>
            <div className="mt-1 text-gray-900">{userData.email}</div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600">Username</label>
            <div className="mt-1 text-gray-900">{userData.username}</div>
          </div>
          {userData.full_name && (
            <div>
              <label className="block text-sm font-medium text-gray-600">Full Name</label>
              <div className="mt-1 text-gray-900">{userData.full_name}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLogin, setShowLogin] = useState(true);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  if (isLoggedIn) {
    return <UserProfile onLogout={handleLogout} />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center space-x-4 py-4">
          <button
            onClick={() => setShowLogin(true)}
            className={`px-4 py-2 rounded ${showLogin ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            Login
          </button>
          <button
            onClick={() => setShowLogin(false)}
            className={`px-4 py-2 rounded ${!showLogin ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
          >
            Register
          </button>
        </div>
        {showLogin ? (
          <LoginForm onSuccess={() => setIsLoggedIn(true)} />
        ) : (
          <RegisterForm onSuccess={() => setShowLogin(true)} />
        )}
      </div>
    </div>
  );
}