import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function CreatePage() {

  const history = useNavigate();

  const [name, setName] = useState('');
  const [reps, setReps] = useState('');
  const [weight, setWeight] = useState('');
  const [unit, setUnit] = useState('');
  const [date, setDate] = useState('');

  const addExercise = async () => {
    const newExercise = {name, reps, weight, unit, date};

    const response = await fetch('/exercises', {
      method: 'POST',
      body: JSON.stringify(newExercise),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 201) {
      alert("Exercise has been added!");
    } 
    else {
      alert(`Failed to add, status code = ${response.status}`);
    }
    history('/');
  }

  return (
    <div>
      <h1>Create an Exercise</h1>

        <fieldset>

          <label for="name">Name of Exercise</label> 
          <input id="name"
            type="text"
            placeholder="curl"
            value={name}
            onChange={e => setName(e.target.value)}
          /> <br/>

          <label for="reps">Number of Reps</label> 
          <input id="reps"
            type="number"
            min="0"
            placeholder="0"
            value={reps}
            onChange={e => setReps(e.target.value)}
          /> <br/>

          <label for="weight">Weight</label> 
          <input id="weight"
            type="number"
            min="0"
            placeholder="000"
            value={weight}
            onChange={e => setWeight(e.target.value)}
          /> <br/>

          <label for="unit">Unit in lbs or kgs</label> 
          <input id="unit"
            type="text"
            placeholder="lbs/kgs"
            value={unit}
            onChange={e => setUnit(e.target.value)}
          /> <br/>


          <label for="date">Date</label> 
          <input id="date"
            type="text"
            placeholder="00-00-0000"
            value={date}
            onChange={e => setDate(e.target.value)}
          /> <br/>

          <button onClick={addExercise}> Create </button>

        </fieldset>

    </div>
  )

}