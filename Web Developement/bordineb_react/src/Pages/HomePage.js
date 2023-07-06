import React from 'react';
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ExerciseTable from '../Components/Table';

export default function HomePage({ setExerciseToEdit }) {

  const history = useNavigate();

  const [exercises, setExercises] = useState([]);

  const loadExercises = async () => {
    const response = await fetch('/exercises');
    const data = await response.json();
    setExercises(data);
  }
  useEffect(() => {
    loadExercises();
}, []);

  const onDelete = async _id => {

    const confirmation = window.confirm("Are you sure you want to delete this?");
    if (!confirmation){
      console.log('User decided not to delete the row.')
      return
    }

    const response = await fetch(`/exercises/${_id}`, {method: 'DELETE'});
    if (response.status === 204) {
      const newExercise = exercises.filter(e => e._id !== _id);
      setExercises(newExercise);
    } else {
      console.error(`Failed to delete exercise with _id ${_id} with status \
        code = ${response.status}`)
    }
  };

  const onEdit = exercise => {
    setExerciseToEdit(exercise);
     history('/edit');
  };

  return (
    <>
      <h1>Exercise App</h1>

      <ExerciseTable exercises={exercises} onDelete={onDelete} onEdit={onEdit}/>

      <br/>

      <Link to='/create'>Create</Link>
    </>
  )
}
