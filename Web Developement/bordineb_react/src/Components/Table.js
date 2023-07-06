import ExerciseRow from './Row.js'

export default function ExerciseTable({ exercises, onDelete, onEdit }) {
  return (
    <table>
      <thead>
        <tr>
          <th> Name of Exercise </th>
          <th> Number of Reps </th>
          <th> Weight </th>
          <th> Unit in lbs or kgs</th>
          <th> Date </th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {exercises.map((exercise, i) => <ExerciseRow exercise={exercise} onDelete={onDelete} onEdit={onEdit} key={i}/> )}
      </tbody>
    </table>
  );
}