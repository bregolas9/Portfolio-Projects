import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import RandomAppearance from './Pages/RandomAppearance';
import Stats from './Pages/StatsPage';
import SavedCharactersPage from './Pages/SavedCharacters';
import ClassAndEquipment from './Pages/ClassAndEquipment';
import OldCharacter from './Pages/OldCharacter';

function App() {

  return (
    <div className="App">
      <Router>

        <div className="App-header">
          <Routes>
            <Route path="/" element={<HomePage/>}>
            </Route>
            <Route path="/randomappearance" element={<RandomAppearance />}>
            </Route>
            <Route path="/stats" element={<Stats />}>
            </Route>
            <Route path="/classandequipment" element={<ClassAndEquipment />}>
            </Route>
            <Route path="/savedcharacterspage" element={<SavedCharactersPage />}>
            </Route>
            <Route path="/oldcharacter" element={<OldCharacter />}>
            </Route>
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;