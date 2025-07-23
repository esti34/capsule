import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import all language files
import en from './locales/en.json';
import he from './locales/he.json';
import ar from './locales/ar.json';

// Set up i18next with configuration
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      he: { translation: he },
      ar: { translation: ar },
    },
    fallbackLng: 'he', // Default language
    debug: process.env.NODE_ENV === 'development',
    
    interpolation: {
      escapeValue: false, // React already handles XSS
    },

    // Detect user language preference
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
    },
  });

export default i18n; 