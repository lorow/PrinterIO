import React from 'react';
import './App.css';

import Navbar from './components/navbar';
import ContentContainer from './containers/contentContainer';

function App() {
  return (
    <div className="App">
      <Navbar />
      <ContentContainer />
    </div>
  );
}

export default App;
