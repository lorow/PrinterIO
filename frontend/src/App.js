import React from 'react';
import './App.css';

import Navbar from './components/navbar';
import ContentHolder from './components/contentHolder';

function App() {
  return (
    <main className="App">
      <Navbar />
      <ContentHolder />
    </main>
  );
}

export default App;
