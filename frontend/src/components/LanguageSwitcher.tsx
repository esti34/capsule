import React from 'react';
import { useTranslation } from 'react-i18next';
import { Dropdown } from 'react-bootstrap';

const LanguageSwitcher: React.FC = () => {
  const { t, i18n } = useTranslation();
  const currentLanguage = i18n.language;

  // Languages supported by the app
  const languages = [
    { code: 'he', name: 'עברית', dir: 'rtl' },
    { code: 'en', name: 'English', dir: 'ltr' },
    { code: 'ar', name: 'العربية', dir: 'rtl' }
  ];

  // Change language handler
  const changeLanguage = (langCode: string) => {
    // Get the direction for the selected language
    const selectedLang = languages.find(lang => lang.code === langCode);
    
    // Change document direction based on language
    if (selectedLang) {
      document.documentElement.dir = selectedLang.dir;
      document.documentElement.lang = langCode;
    }
    
    // Change language in i18n
    i18n.changeLanguage(langCode);
  };

  // Find current language object
  const currentLangObj = languages.find(lang => lang.code === currentLanguage) || languages[0];

  return (
    <Dropdown className="language-switcher">
      <Dropdown.Toggle variant="outline-secondary" size="sm" id="dropdown-language">
        {currentLangObj.name}
      </Dropdown.Toggle>

      <Dropdown.Menu>
        {languages.map((lang) => (
          <Dropdown.Item 
            key={lang.code} 
            onClick={() => changeLanguage(lang.code)}
            active={currentLanguage === lang.code}
          >
            {lang.name}
          </Dropdown.Item>
        ))}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default LanguageSwitcher; 