import React from 'react';
import FileUpload from '../components/FileUpload';

const HomePage: React.FC = () => {
  return (
    <main className="flex-1 flex flex-col items-center justify-center p-4">
      <FileUpload />
    </main>
  );
};

export default HomePage;
