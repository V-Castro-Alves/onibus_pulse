import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ChevronLeft, Bus } from 'lucide-react';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const isHome = location.pathname === '/';

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          {!isHome && (
            <button 
              className="back-button" 
              onClick={() => navigate(-1)}
              aria-label="Go back"
            >
              <ChevronLeft size={24} />
            </button>
          )}
          <div className="brand" onClick={() => navigate('/')}>
            <Bus className="brand-icon" size={28} />
            <h1>Onibus Pulse</h1>
          </div>
          <div className="status-indicator">
            <span className="pulse-dot"></span>
            <span className="status-text">Live</span>
          </div>
        </div>
      </header>
      <main className="app-main">
        {children}
      </main>
    </div>
  );
};

export default Layout;
