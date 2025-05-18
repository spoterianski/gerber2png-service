import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Home, Info } from 'lucide-react';
import HomePage from './pages/Home';
import About from './pages/About';

const App: React.FC = () => {
  return (
    <Router>
      <div className="h-screen grid grid-rows-[80px_1fr_60px] bg-gray-100">
        
        {/* Header */}
        <header className="flex items-center justify-between px-6 bg-white border-b border-gray-200">
          <div className="flex items-center gap-4">
            <img
              src="/logo.png"
              alt="Logo"
              className="h-16 w-auto cursor-pointer"
              onClick={() => window.location.href = '/'}
            />
            <nav className="flex gap-4 text-sm font-medium text-gray-700">
              <Link to="/" className="hover:text-blue-600 transition">
              <Home className="w-8 h-8" />
              </Link>
              <Link to="/about" className="hover:text-blue-600 transition">
              <Info className='w-8 h-8' />
              </Link>
            </nav>
          </div>
        </header>

        {/* Content */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<About />} />
        </Routes>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-300 text-center p-4 text-sm text-gray-600">
          © 2025 <a href="https://github.com/spoterianski" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">Sergey Poterianski</a> | <span title="From Russia with love">🇷🇺</span> | License: MIT | Version: 1.0.3
        </footer>
      </div>
    </Router>
  );
};

export default App;
