import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import CreatePage from './Pages/CreatePage';
import EditPage from './Pages/EditPage';
import { useState } from 'react';

function App() {
  const[exerciseToEdit, setExerciseToEdit] = useState();

  return (
    <div className="App">
      <Router>

        <div className="App-header">
          <Routes>
            <Route path="/" exact element={<HomePage setExerciseToEdit={setExerciseToEdit}/>}>
            </Route>
            <Route path="/create" element={<CreatePage />}>
            </Route>
            <Route path="/edit" element={<EditPage exerciseToEdit={exerciseToEdit}/>}>
            </Route>
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;