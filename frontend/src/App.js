import React from 'react';
import './App.css';

import Navbar from './components/navbar';
import ContentHolder from './components/contentHolder';

function App() {
  return (
    <div className="App">
      <Navbar />
      <ContentHolder />
    </div>
  );
}

export default App;
