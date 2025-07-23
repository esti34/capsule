import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Form, Button, Card, Container, Row, Col, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import authApi, { LoginCredentials, RegisterData, ResetPasswordRequest } from '../services/authApi';
import LanguageSwitcher from './LanguageSwitcher';

enum AuthMode {
  LOGIN = 'login',
  REGISTER = 'register',
  FORGOT_PASSWORD = 'forgot_password'
}

// אובייקט להחזקת הודעות שגיאת ולידציה
interface ValidationErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
  firstName?: string;
  lastName?: string;
  nationalId?: string;
}

interface AuthFormProps {
  onLoginSuccess?: () => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ onLoginSuccess }) => {
  const { t } = useTranslation();
  const [mode, setMode] = useState<AuthMode>(AuthMode.LOGIN);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [nationalId, setNationalId] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});

  // פונקציה לבדיקת תקינות המייל
  const validateEmail = (email: string): boolean => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  // פונקציה לבדיקת תקינות הסיסמה
  const validatePassword = (password: string): boolean => {
    return password.length >= 6;
  };

  // פונקציה לבדיקת תקינות מספר הזהות (9 ספרות)
  const validateNationalId = (id: string): boolean => {
    return /^\d{9}$/.test(id);
  };

  // בדיקת תקינות לטופס התחברות
  const validateLoginForm = (): boolean => {
    const errors: ValidationErrors = {};
    let isValid = true;

    if (!email) {
      errors.email = t('validation.required') as string;
      isValid = false;
    } else if (!validateEmail(email)) {
      errors.email = t('validation.emailInvalid') as string;
      isValid = false;
    }

    if (!password) {
      errors.password = t('validation.required') as string;
      isValid = false;
    }

    setValidationErrors(errors);
    return isValid;
  };

  // בדיקת תקינות לטופס הרשמה
  const validateRegisterForm = (): boolean => {
    const errors: ValidationErrors = {};
    let isValid = true;

    if (!firstName) {
      errors.firstName = t('validation.required') as string;
      isValid = false;
    }

    if (!lastName) {
      errors.lastName = t('validation.required') as string;
      isValid = false;
    }

    if (!email) {
      errors.email = t('validation.required') as string;
      isValid = false;
    } else if (!validateEmail(email)) {
      errors.email = t('validation.emailInvalid') as string;
      isValid = false;
    }

    if (!nationalId) {
      errors.nationalId = t('validation.required') as string;
      isValid = false;
    } else if (!validateNationalId(nationalId)) {
      errors.nationalId = t('validation.idInvalid') as string;
      isValid = false;
    }

    if (!password) {
      errors.password = t('validation.required') as string;
      isValid = false;
    } else if (!validatePassword(password)) {
      errors.password = t('validation.passwordLength') as string;
      isValid = false;
    }

    if (!confirmPassword) {
      errors.confirmPassword = t('validation.required') as string;
      isValid = false;
    } else if (password !== confirmPassword) {
      errors.confirmPassword = t('validation.passwordsNotMatch') as string;
      isValid = false;
    }

    setValidationErrors(errors);
    return isValid;
  };

  // בדיקת תקינות לטופס שכחתי סיסמה
  const validateForgotPasswordForm = (): boolean => {
    const errors: ValidationErrors = {};
    let isValid = true;

    if (!email) {
      errors.email = t('validation.required') as string;
      isValid = false;
    } else if (!validateEmail(email)) {
      errors.email = t('validation.emailInvalid') as string;
      isValid = false;
    }

    setValidationErrors(errors);
    return isValid;
  };

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    if (!validateLoginForm()) return;

    setLoading(true);
    setError(null);

    try {
      const credentials: LoginCredentials = {
        email,
        password,
        remember: rememberMe
      };

      const response = await authApi.login(credentials);
      
      // Store token in local storage
      if (response && response.token) {
        localStorage.setItem('authToken', response.token);
      }
      
      setSuccess(t('success.loginSuccess') as string);
      
      // Call onLoginSuccess callback if provided
      if (onLoginSuccess) {
        onLoginSuccess();
      }
    } catch (err: any) {
      console.error("Login error:", err);
      // טיפול נכון בשגיאה - הצגת הודעת שגיאה ברורה
      setError(err.response?.data?.detail || 
               typeof err.message === 'string' ? err.message : 
               t('errors.loginFailed') as string);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    if (!validateRegisterForm()) return;
    
    setLoading(true);
    setError(null);

    try {
      const userData: RegisterData = {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        national_id: nationalId
        // role_id is assigned automatically on the backend
      };

      await authApi.register(userData);
      setSuccess(t('success.registerSuccess') as string);
      setMode(AuthMode.LOGIN);
    } catch (err: any) {
      console.error("Register error:", err);
      
      // טיפול בתשובות שגיאה מהשרת
      let errorMessage = t('errors.registerFailed') as string;
      
      if (err.response?.data) {
        // אם יש פירוט שגיאה מהשרת
        const serverError = err.response.data;
        if (typeof serverError.detail === 'string') {
          errorMessage = serverError.detail;
        } else if (serverError.detail && Array.isArray(serverError.detail)) {
          // טיפול בשגיאות ולידציה מהשרת
          errorMessage = serverError.detail.map((error: any) => 
            typeof error.msg === 'string' ? error.msg : JSON.stringify(error)
          ).join(', ');
        }
      } else if (typeof err.message === 'string') {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async (e: FormEvent) => {
    e.preventDefault();
    if (!validateForgotPasswordForm()) return;
    
    setLoading(true);
    setError(null);

    try {
      const request: ResetPasswordRequest = { email };
      await authApi.forgotPassword(request);
      setSuccess(t('success.resetSuccess') as string);
    } catch (err: any) {
      console.error("Forgot password error:", err);
      setError(err.response?.data?.detail || 
               typeof err.message === 'string' ? err.message : 
               t('errors.resetFailed') as string);
    } finally {
      setLoading(false);
    }
  };

  // ניקוי שגיאות בעת מעבר בין מצבי טופס
  const switchMode = (newMode: AuthMode) => {
    setMode(newMode);
    setError(null);
    setSuccess(null);
    setValidationErrors({});
  };

  const renderLoginForm = () => (
    <Form onSubmit={handleLogin}>
      <Form.Group className="mb-3" controlId="loginEmail">
        <Form.Label>{t('auth.email')}</Form.Label>
        <Form.Control
          type="email"
          placeholder={t('placeholders.enterEmail') as string}
          value={email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          isInvalid={!!validationErrors.email}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.email}
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3" controlId="loginPassword">
        <Form.Label>{t('auth.password')}</Form.Label>
        <Form.Control
          type="password"
          placeholder={t('placeholders.enterPassword') as string}
          value={password}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          isInvalid={!!validationErrors.password}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.password}
        </Form.Control.Feedback>
      </Form.Group>

      <div className="d-flex justify-content-between align-items-center mb-3">
        <Form.Check
          type="checkbox"
          id="rememberMe"
          label={t('auth.rememberMe')}
          checked={rememberMe}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setRememberMe(e.target.checked)}
        />
        <Button
          variant="link"
          className="p-0"
          onClick={() => switchMode(AuthMode.FORGOT_PASSWORD)}
        >
          {t('auth.forgotPasswordLink')}
        </Button>
      </div>

      <Button variant="primary" type="submit" className="w-100" disabled={loading}>
        {loading ? t('auth.loading') : t('auth.loginButton')}
      </Button>

      <div className="text-center mt-3">
        {t('auth.noAccount')}{' '}
        <Button variant="link" className="p-0" onClick={() => switchMode(AuthMode.REGISTER)}>
          {t('auth.registerNow')}
        </Button>
      </div>
    </Form>
  );

  const renderRegisterForm = () => (
    <Form onSubmit={handleRegister}>
      <Row>
        <Col md={6}>
          <Form.Group className="mb-3" controlId="registerFirstName">
            <Form.Label>{t('auth.firstName')}</Form.Label>
            <Form.Control
              type="text"
              placeholder={t('placeholders.enterFirstName') as string}
              value={firstName}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFirstName(e.target.value)}
              isInvalid={!!validationErrors.firstName}
              required
            />
            <Form.Control.Feedback type="invalid">
              {validationErrors.firstName}
            </Form.Control.Feedback>
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group className="mb-3" controlId="registerLastName">
            <Form.Label>{t('auth.lastName')}</Form.Label>
            <Form.Control
              type="text"
              placeholder={t('placeholders.enterLastName') as string}
              value={lastName}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setLastName(e.target.value)}
              isInvalid={!!validationErrors.lastName}
              required
            />
            <Form.Control.Feedback type="invalid">
              {validationErrors.lastName}
            </Form.Control.Feedback>
          </Form.Group>
        </Col>
      </Row>

      <Form.Group className="mb-3" controlId="registerEmail">
        <Form.Label>{t('auth.email')}</Form.Label>
        <Form.Control
          type="email"
          placeholder={t('placeholders.enterEmail') as string}
          value={email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          isInvalid={!!validationErrors.email}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.email}
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3" controlId="registerNationalId">
        <Form.Label>{t('auth.nationalId')}</Form.Label>
        <Form.Control
          type="text"
          placeholder={t('placeholders.enterId') as string}
          value={nationalId}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setNationalId(e.target.value)}
          isInvalid={!!validationErrors.nationalId}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.nationalId}
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3" controlId="registerPassword">
        <Form.Label>{t('auth.password')}</Form.Label>
        <Form.Control
          type="password"
          placeholder={t('placeholders.enterPasswordHint') as string}
          value={password}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          isInvalid={!!validationErrors.password}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.password}
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3" controlId="registerConfirmPassword">
        <Form.Label>{t('auth.confirmPassword')}</Form.Label>
        <Form.Control
          type="password"
          placeholder={t('placeholders.enterPasswordAgain') as string}
          value={confirmPassword}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setConfirmPassword(e.target.value)}
          isInvalid={!!validationErrors.confirmPassword}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.confirmPassword}
        </Form.Control.Feedback>
      </Form.Group>

      <Button variant="primary" type="submit" className="w-100" disabled={loading}>
        {loading ? t('auth.loading') : t('auth.registerButton')}
      </Button>

      <div className="text-center mt-3">
        {t('auth.hasAccount')}{' '}
        <Button variant="link" className="p-0" onClick={() => switchMode(AuthMode.LOGIN)}>
          {t('auth.loginNow')}
        </Button>
      </div>
    </Form>
  );

  const renderForgotPasswordForm = () => (
    <Form onSubmit={handleForgotPassword}>
      <Form.Group className="mb-3" controlId="forgotEmail">
        <Form.Label>{t('auth.email')}</Form.Label>
        <Form.Control
          type="email"
          placeholder={t('placeholders.enterEmail') as string}
          value={email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          isInvalid={!!validationErrors.email}
          required
        />
        <Form.Control.Feedback type="invalid">
          {validationErrors.email}
        </Form.Control.Feedback>
      </Form.Group>

      <Button variant="primary" type="submit" className="w-100" disabled={loading}>
        {loading ? t('auth.loading') : t('auth.resetPasswordButton')}
      </Button>

      <div className="text-center mt-3">
        <Button variant="link" className="p-0" onClick={() => switchMode(AuthMode.LOGIN)}>
          {t('auth.backToLogin')}
        </Button>
      </div>
    </Form>
  );

  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col xs={12} sm={10} md={8} lg={6} xl={5}>
          <div className="d-flex justify-content-end mb-3">
            <LanguageSwitcher />
          </div>
          <Card className="shadow">
            <Card.Body className="p-4">
              {error && <Alert variant="danger">{error}</Alert>}
              {success && <Alert variant="success">{success}</Alert>}

              <h2 className="text-center mb-4">
                {mode === AuthMode.LOGIN && t('auth.login')}
                {mode === AuthMode.REGISTER && t('auth.register')}
                {mode === AuthMode.FORGOT_PASSWORD && t('auth.forgotPassword')}
              </h2>

              {mode === AuthMode.LOGIN && renderLoginForm()}
              {mode === AuthMode.REGISTER && renderRegisterForm()}
              {mode === AuthMode.FORGOT_PASSWORD && renderForgotPasswordForm()}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AuthForm; 