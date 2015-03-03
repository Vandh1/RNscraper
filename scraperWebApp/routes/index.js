var express = require('express');
var router = express.Router();
var async = require("async");

/* GET home page. */
router.get('/', function(req, res) {
    var sqlite3 = require('sqlite3').verbose();
    var db = new sqlite3.Database('/home/pedro/RNScraper/serverStarts.db');
    
    var starts = {
	interrailwest : [],
	interrailwest2 : [],
	interrailwest3 : [],
	goldengate : [] 
    }
    
    
    
    async.auto({
	'dbFetch': function(callback){
	    db.all("SELECT * from starts;", function(err,rows){
		if(err){
		    console.log("err");
		}

		for(var i=0; i< rows.length;i++){
		    
		    startDate = rows[i].startDate
		    server = rows[i].server
		    announcementDate = rows[i].announcementDate
		    poster = rows[i].poster;
		    
		    switch(server){
		    case "Interrail West":
			starts.interrailwest.push({
			    "start" : startDate,
			    "announcementDate" : announcementDate,
			    "poster" : poster
			});
			console.log("Interrail West data fetched");
			break;
			
		    case "Interrail West 2":
			starts.interrailwest2.push({
			    "start" : startDate,
			    "announcementDate" : announcementDate,
			    "poster" : poster
			});
			console.log("Interrail West 2 data fetched");
			break;
			
		    case "Interrail West 3":
			starts.interrailwest3.push({
			    "start" : startDate,
			    "announcementDate" : announcementDate,
			    "poster" : poster
			});
			console.log("Interrail West 3 data fetched");
			break;
			
		    case "Golden Gate":
			starts.goldengate.push({
			    "start" : startDate,
			    "announcementDate" : announcementDate,
			    "poster" : poster
			});
			console.log("Golden Gate data fetched");
			break;
			
		    default:
			console.log("ERROR: Server string not recognized!");
			break;
		    }
		}
		callback();
		
		
		
	    });
	},
	'sendData': [
	    
	    'dbFetch', function(callback){
		
		console.log(starts);
		res.render('index', starts);
		callback();
	    }
	]
	
	
	
	
    });
});
module.exports = router;
