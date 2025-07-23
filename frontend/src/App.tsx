import React, { useEffect, useState } from 'react';
import './App.css';
// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import AuthForm from './components/AuthForm';
import Dashboard from './components/Dashboard';
import { useTranslation } from 'react-i18next';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';

function App() {
  const { i18n, t } = useTranslation();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check if user is logged in (could be expanded with actual token checking)
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  // Set the document direction based on the current language
  useEffect(() => {
    const dir = i18n.language === 'ar' || i18n.language === 'he' ? 'rtl' : 'ltr';
    document.documentElement.dir = dir;
    document.documentElement.lang = i18n.language;
  }, [i18n.language]);

  // Handle successful login
  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsLoggedIn(false);
  };

  const router = createBrowserRouter([
    {
      path: "/login",
      element: isLoggedIn ? <Navigate to="/dashboard" /> : <AuthForm onLoginSuccess={handleLoginSuccess} />
    },
    {
      path: "/dashboard",
      element: isLoggedIn ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" />
    },
    {
      path: "/",
      element: <Navigate to={isLoggedIn ? "/dashboard" : "/login"} />
    }
  ]);

  return (
    <div className="App">
      <Container fluid className="p-0">
        <header className="bg-primary text-white p-3">
          <h1 className="text-center">
            {t('app.title')}
          </h1>
        </header>
      
        <main>
          <RouterProvider router={router} />
        </main>
        
        <footer className="bg-light p-3 text-center mt-5">
          <p>
            © {new Date().getFullYear()} {t('app.footer')}
          </p>
        </footer>
      </Container>
    </div>
  );
}

export default App;
