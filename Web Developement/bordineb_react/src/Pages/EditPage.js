import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function EditPage({ exerciseToEdit }) {

  const history = useNavigate();

  const [name, setName] = useState(exerciseToEdit.name);
  const [reps, setReps] = useState(exerciseToEdit.reps);
  const [weight, setWeight] = useState(exerciseToEdit.weight);
  const [unit, setUnit] = useState(exerciseToEdit.unit);
  const [date, setDate] = useState(exerciseToEdit.date);

  const editExercise = async () => {
    const editedExercise = {name, reps, weight, unit, date};

    const response = await fetch(`/exercises/${exerciseToEdit._id}`, {
      method: 'PUT',
      body: JSON.stringify(editedExercise),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 200) {
      alert("Exercise has been edited!");
    } else {
      alert(`Failed to edit, status code = ${response.status}`);
    }
    history('/');
  };

  return (
    <div>
      <h1>Edit an Exercise</h1>

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

          <button onClick={editExercise}> Save </button>

        </fieldset>

    </div>
  )

};