import React, { useState } from 'react';
import { Container, Row, Col, Nav, Button, Offcanvas } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';
import { Bars3Icon, UserIcon, DocumentTextIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';

interface DashboardProps {
  onLogout?: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onLogout }) => {
  const { t } = useTranslation();
  const [showSidebar, setShowSidebar] = useState(false);
  const [activePage, setActivePage] = useState<'profile' | 'citizenInfo'>('profile');

  const handleCloseSidebar = () => setShowSidebar(false);
  const handleShowSidebar = () => setShowSidebar(true);
  
  const handleLogout = () => {
    if (onLogout) {
      onLogout();
    }
  };
  
  const handleNavigation = (page: 'profile' | 'citizenInfo') => {
    setActivePage(page);
    handleCloseSidebar();
  };

  // Navigation menu content - reused in both desktop and mobile views
  const renderNavLinks = () => (
    <Nav className="flex-column">
      <Nav.Link 
        className={`sidebar-link ${activePage === 'profile' ? 'active' : ''}`} 
        onClick={() => handleNavigation('profile')}
      >
        <UserIcon className="me-2" width={20} height={20} /> {t('dashboard.menu.profile')}
      </Nav.Link>
      <Nav.Link 
        className={`sidebar-link ${activePage === 'citizenInfo' ? 'active' : ''}`}
        onClick={() => handleNavigation('citizenInfo')}
      >
        <DocumentTextIcon className="me-2" width={20} height={20} /> {t('dashboard.menu.citizenInfo')}
      </Nav.Link>
      <hr />
      <Nav.Link className="text-danger" onClick={handleLogout}>
        <ArrowRightOnRectangleIcon className="me-2" width={20} height={20} /> {t('dashboard.menu.logout')}
      </Nav.Link>
    </Nav>
  );

  const renderProfileContent = () => (
    <div className="p-3">
      <h3>{t('dashboard.profile.title')}</h3>
      <p>{t('dashboard.profile.description')}</p>
      {/* Profile content would go here */}
    </div>
  );

  const renderCitizenInfoContent = () => (
    <div className="p-3">
      <h3>{t('dashboard.citizenInfo.title')}</h3>
      <p>{t('dashboard.citizenInfo.description')}</p>
      {/* Citizen information management content would go here */}
    </div>
  );

  return (
    <Container fluid className="p-0 dashboard-container">
      {/* Header */}
      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <Button 
          variant="outline-light" 
          className="d-md-none" 
          onClick={handleShowSidebar}
          aria-label={t('dashboard.openMenu') as string}
        >
          <Bars3Icon width={24} height={24} />
        </Button>
        <h3 className="m-0">{t('dashboard.title')}</h3>
        <div className="d-flex align-items-center">
          <LanguageSwitcher />
        </div>
      </div>

      <Row className="g-0 flex-nowrap">
        {/* Sidebar for medium and up screens */}
        <Col md={3} lg={2} className="d-none d-md-block bg-light sidebar">
          <div className="p-3">
            {renderNavLinks()}
          </div>
        </Col>
        
        {/* Mobile Sidebar (Offcanvas) - only shown on small screens */}
        <Offcanvas show={showSidebar} onHide={handleCloseSidebar} className="d-md-none">
          <Offcanvas.Header closeButton>
            <Offcanvas.Title>{t('dashboard.menu.title')}</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
            {renderNavLinks()}
          </Offcanvas.Body>
        </Offcanvas>

        {/* Main Content Area */}
        <Col md={9} lg={10} className="main-content">
          {activePage === 'profile' && renderProfileContent()}
          {activePage === 'citizenInfo' && renderCitizenInfoContent()}
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard; 