import mongoose from 'mongoose';

mongoose.connect(
    "mongodb://localhost:27017/exercises_db",
    { useNewUrlParser: true, useUnifiedTopology: true }
);

const db = mongoose.connection;
db.once("open", () => {
    console.log("Successfully connected to MongoDB using Mongoose!");
});

const exerciseSchema = mongoose.Schema({
    name: {type: String, required: true},
    reps: {type: Number, required: true},
    weight: {type: Number, required: true},
    unit: {type: String, enum: ['kgs', 'lbs'], required: true}, 
    date: {type: String, required: true}
});

const Exercises = mongoose.model("Exercises", exerciseSchema);

const createExercises = async (name, reps, weight, unit, date) => {
    const exercise = new Exercises({name:name, reps:reps, weight:weight, unit:unit, date:date});
    return exercise.save();
}

/**
 * @param {String} _id 
 * @returns 
 */

const findExercisesById = async (_id) => {
    const query = Exercises.findById(_id);
    return query.exec();
}

const findExercises = async (filter, projection, limit) => {
    const query = Exercises.find(filter)
        .select(projection)
        .limit(limit);
    return query.exec();
}

const replaceExercise = async(_id, name, reps, weight, unit, date) => {
    const result = await Exercises.updateOne({ _id:_id }, { name: name, reps: reps, weight: weight, unit: unit, date: date });
    console.log(result);
    console.log(result.modifiedCount);
    return result.modifiedCount;
}

const deleteById = async(_id) => {
    const result = await Exercises.deleteOne({ _id: _id });
    return result.deletedCount;
}

export {createExercises, findExercisesById, findExercises, replaceExercise, deleteById}