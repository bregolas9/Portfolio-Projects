// App.js
'use strict';

/*
    SETUP
*/
const express = require("express");
const app = express();
app.use(express.json());
app.use(express.urlencoded({extended: true}));
const PORT = 6338;
const handlebars = require('express-handlebars').create({
    defaultLayout: 'index',
});

// database connection
const db = require('./database/dbcon.js');
// Handlebars

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

// Static Files
app.use(express.static('public'));



/*
    ROUTES
*/
app.get('/', function(req, res){
    res.render('main', {layout: 'index'});
});

app.get('/movies', function(req, res){
    var query1 = "SELECT * FROM movies;";
    db.pool.query(query1, function(error, rows, fields){
        res.render('movies', {data: rows});
    })
});

app.get('/members', function(req, res){
    var query1 = "SELECT * FROM members;";
    db.pool.query(query1, function(error, rows, fields){
        res.render('members', {data: rows})
    })
});

app.get('/rentals', function(req, res){
    var query1 = "SELECT * FROM rentals;";
    db.pool.query(query1, function(error, rows, fields){
        res.render('rentals', {data: rows})
    })
});

app.get('/transactions', function(req, res){
    var query1 = "SELECT * FROM transactions;";
    db.pool.query(query1, function(error, rows, fields){
        res.render('transactions', {data: rows})
    })
});

app.get('/movies', function(req, res)
{
    let query1;

    if (req.query.title === undefined)
    {
        query1 = "SELECT * FROM movies;";
    }

    else
    {
        query1 = `SELECT * FROM movies WHERE title LIKE "${req.query.title}%"`;
    }


    // Run the 1st query
    db.pool.query(query1, function(error, rows, fields) {
        
        // Save the people
        let movies = rows;
        return res.render('movies', {data: movies});
        })
    });

// app.js

app.post('/add-movie-form', function(req, res){
    // Capture the incoming data and parse it back to a JS object
    let data = req.body;

    // Capture NULL values
    let itemID = parseInt(data['input-itemID']);
    if (isNaN(itemID))
    {
        itemID = 'NULL'
    }

    // Create the query and run it on the database
    var query1 = `INSERT INTO movies (itemID, title, release_year, in_stock, qty, rental_price) VALUES ('${data['input-itemID']}', '${data['input-title']}', '${data['input-release-year']}',  '1',  '${data['input-quantity']}',  '${data['input-rental-price']}')`
    db.pool.query(query1, function(error, rows, fields){

        // Check to see if there was an error
        if (error) {
            console.log(error)
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/movies');
        }
    })
})

app.delete('/delete-movie-ajax/', function(req,res,next){
    let data = req.body;
    let itemID = parseInt(data.itemID);
    let deleteMovie = `DELETE FROM movies WHERE itemID = ?`;
    let deleteRentals = `DELETE FROM rentals WHERE itemID = ?`;  
  
          // Run the 1st query
          db.pool.query(deleteMovie, [itemID], function(error, rows, fields){
              if (error) {
  
              // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
              console.log(error);
              res.sendStatus(400);
              }
  
              else
              {
                  // Run the second query
                  db.pool.query(deleteRentals, [itemID], function(error, rows, fields) {
  
                      if (error) {
                          console.log(error);
                          res.sendStatus(400);
                      } else {
                          res.sendStatus(204);
                      }
                  })
              }
        })});


app.put('/put-movie-ajax', function(req,res,next){
let data = req.body;

let quantity = parseInt(data.quantity);
let itemID = parseInt(data.itemID);

let queryUpdateQuantity = `UPDATE movies SET qty = ? WHERE movies.itemID = ?`;
let selectQty = `SELECT * FROM movies WHERE qty = ?`

        // Run the 1st query
        db.pool.query(queryUpdateQuantity, [quantity, itemID], function(error, rows, fields){
            if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error);
            res.sendStatus(400);
            }
            else
            {
                // Run the second query
                db.pool.query(selectQty, [quantity], function(error, rows, fields) {

                    if (error) {
                        console.log(error);
                        res.sendStatus(400);
                    } else {
                        res.send(rows)   
                    }
                })
            }
})});


app.post('/transactions', function(req, res){
    res.render('transactions', {layout: 'index'})
});



app.post('/members', function(req, res){
    res.render('members', {layout: 'index'})
});

app.post('/rentals', function(req, res){
    res.render('rentals', {layout: 'index'})
});
    
app.listen(PORT, function(){          
    console.log('Express started on port:' + PORT + '; press Ctrl-C to terminate.')
});

