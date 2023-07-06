import * as exercise from './model.mjs';
import express from 'express';

const PORT = 3000;
const app = express();

app.use(express.json())
   .use(express.urlencoded({ extended: true }))  

app.post('/exercises', (req, res) => {
    exercise.createExercises(req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(exercise => {
            res.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error);
            res.status(400).json({ Error: 'Request failed' });
        });
});

app.get('/exercises/:_id', (req, res) => {
    const exerciseId = req.params._id;
    exercise.findExercisesById(exerciseId)
        .then(exercise => {
            if (exercise !== null) {
                res.json(exercise)
            } 
            else{
                res.status(404).json({Error: 'Resource not found by ID'});
            }
        })
        .catch(error => {
            console.error(error);
            res.status(400).json({ Error: 'Request failed' });
        });
});

app.get('/exercises', (req, res) => {
    const filter = req.query.name === undefined
        ? {}
        : { name: req.query.name };
    if (req.query.reps !== undefined){
        filter.reps=req.query.reps
    };
    if (req.query.weight !== undefined){
        filter.weight=req.query.weight
    };
    if (req.query.unit !== undefined){
        filter.unit=req.query.unit
    };
    if (req.query.date !== undefined){
        filter.date=req.query.date
    };
    if (req.query._id !== undefined){
        filter._id=req.query._id
    };


    exercise.findExercises(filter, '', 0)
        .then(exercise => {
            console.log(exercise)
            res.send(exercise);
        })
        .catch(error => {
            console.error(error);
            res.send({ error: 'Request failed' });
        });
});


app.put('/exercises/:_id', (req, res) => {
    exercise.replaceExercise(req.params._id, req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
    .then(numUpdated => {
        if (numUpdated === 1) {
            res.json({ _id: req.params._id, name: req.body.name, reps: req.body.reps, weight: req.body.weight, unit: req.body.unit, date: req.body.date })
        }
        else {
            res.status(404).json({ Error: 'Resource not found for update'})
        }
    })
    .catch(error => {
        console.error(error);
        res.status(400).json({ "Error" : "Request failed" });
    });
});

app.delete('/exercises/:id', (req, res) => {
    exercise.deleteById(req.params.id)
        .then(deletedCount => {
            if(deletedCount === 1){
                res.status(204).send();
            }
            else {
                res.status(404).json({Error: 'Resource not found. Delete failed.'})
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ error: "Delete request failed" });
        });
});


app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});