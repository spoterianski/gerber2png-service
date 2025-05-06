// src/App.tsx
import React from 'react';
import FileUpload from './components/FileUpload';

const App: React.FC = () => {
  return (
    <div className="min-h-screen grid grid-rows-[auto_1fr_auto] bg-gray-100">

    {/* Logo */}
    <header className="flex items-center p-4">
      <img
        src="/logo.png"
        alt="Logo"
        className="h-20 w-auto cursor-pointer transition-transform hover:scale-105"
        onClick={() => window.location.reload()}
      />
    </header>

    {/* Main content */}
    <main className="flex flex-col items-center justify-center p-4 overflow-auto">
      <FileUpload />
    </main>

    {/* Footer */}
    <footer className="bg-white border-t border-gray-300 text-center p-4 text-sm text-gray-600">
      © 2025 Sergey Poterianski | License: MIT | Version: 1.0.0
    </footer>

  </div>

    
  );
};

export default App;

