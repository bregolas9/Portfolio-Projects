var mysql = require('mysql');
var pool = mysql.createPool({
    connectionLimit : 10,
    host            : 'classmysql.engr.oregonstate.edu',
    user            : 'cs340_sheent',
    password        : '6331',
    database        : 'cs340_sheent'
});
module.exports.pool = pool;