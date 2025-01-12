import React, { useState } from 'react';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import PetRegisterForm from './components/pets/RegisterPetForm';
import PetHealthChart from "./components/pets/PetHealthChart";

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentView, setCurrentView] = useState('login'); // 'login', 'register', 'petRegister', 'PetHealthChart'

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setCurrentView('login');
  };

  const renderForm = () => {
    switch (currentView) {
      case 'PetHealthChart':
        return <PetHealthChart onSuccess={() => setIsLoggedIn(true) } />;
      case 'login':
        return <LoginForm onSuccess={() => setIsLoggedIn(true)} />;
      case 'register':
        return <RegisterForm onSuccess={() => setCurrentView('login')} />;
      case 'petRegister':
        return <PetRegisterForm onSuccess={() => {
          alert('반려동물이 등록되었습니다!');
          setCurrentView('login');
        }} />;
      default:
        return <LoginForm onSuccess={() => setIsLoggedIn(true)} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Navigation Bar */}
        <nav className="py-4 border-b border-gray-200 mb-8">
          <div className="flex justify-between items-center">
            <div className="text-xl font-bold text-gray-800">Pet Care</div>
            {isLoggedIn && (
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700"
              >
                Logout
              </button>
            )}
          </div>
        </nav>

        {/* Form Selection Buttons */}
        <div className="flex justify-center space-x-4 mb-8">
          <button
              onClick={() => setCurrentView('login')}
              className={`px-4 py-2 rounded transition-colors duration-200 ${
                  currentView === 'login'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 hover:bg-gray-300'
              }`}
          >
            Login
          </button>
          <button
              onClick={() => setCurrentView('register')}
              className={`px-4 py-2 rounded transition-colors duration-200 ${
                  currentView === 'register'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-200 hover:bg-gray-300'
              }`}
          >
            Register
          </button>
          <button
              onClick={() => setCurrentView('PetHealthChart')}
              className={`px-4 py-2 rounded transition-colors duration-200 ${
                  currentView === 'PetHealthChart'
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-200 hover:bg-gray-300'
              }`}
          >
            PetHealthChart
          </button>
          {isLoggedIn && (
              <button
                  onClick={() => setCurrentView('petRegister')}
                  className={`px-4 py-2 rounded transition-colors duration-200 ${
                      currentView === 'petRegister'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300'
                  }`}
              >
                Pet Register
              </button>
          )}
        </div>

        {/* Main Content Area */}
        <div className="max-w-md mx-auto">
          {renderForm()}
        </div>
      </div>

      {/* Footer */}
      <footer className="py-4 text-center text-gray-600 mt-8">
        <p>&copy; 2024 Pet Care. All rights reserved.</p>
      </footer>
    </div>
  );
}