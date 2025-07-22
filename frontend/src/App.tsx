import React, { useState, useEffect } from 'react';
import './App.css';
// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Nav } from 'react-bootstrap';
import AuthForm from './components/AuthForm';

function App() {
  return (
    <div className="App" dir="rtl">
      <Container fluid className="p-0">
        <header className="bg-primary text-white p-3">
          <h1 className="text-center">מערכת ניהול משתמשים</h1>
      </header>
      
        <main>
          <AuthForm />
        </main>
        
        <footer className="bg-light p-3 text-center mt-5">
          <p>© {new Date().getFullYear()} כל הזכויות שמורות</p>
        </footer>
      </Container>
    </div>
  );
}

export default App;
