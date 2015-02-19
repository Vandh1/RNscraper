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
    var minimal = {
	interrailwest: ["picas", "pikachu"]

    }

    var rowsfetched = 0;
    
    async.auto({
	'dbFetch': function(callback){
	    console.log("b4 db");
	    db.all("SELECT * from starts;", function(err,rows){
		if(err){
		    console.log("err");
		}

		for(var i=0; i< rows.length;i++){
		    
		console.log("FUNCTION CALL "+i);
		startDate = rows[i].startDate
		server = rows[i].server
		announcementDate = rows[i].announcementDate
		poster = rows[i].poster;
		console.log("b4 switch");

		switch(server){
		case "Interrail West":
		   
		    console.log(rowsfetched);
		    rowsfetched+=1;
		    console.log(startDate);
		    starts.interrailwest.push({
			"start" : startDate,
			"announcementDate" : announcementDate,
			"poster" : poster
		    });
		    console.log("Interrail West");
		    break;
		    
		case "Interrail West 2":
		    console.log("iw");
		    rowsfetched+=1;
		    starts.interrailwest2.push({
			"start" : startDate,
			"announcementDate" : announcementDate,
			"poster" : poster
		    });
		    console.log("Interrail West 2");
		    break;
		    
		case "Interrail West 3":


		    rowsfetched+=1;
		    console.log(rowsfetched);
		    starts.interrailwest3.push({
			"start" : startDate,
			"announcementDate" : announcementDate,
			"poster" : poster
		    });
		    console.log("Interrail West 3");
		    break;
		    
		case "Golden Gate":
		    rowsfetched+=1;
		    console.log(rowsfetched);
		    starts.goldengate.push({
			"start" : startDate,
			"announcementDate" : announcementDate,
			"poster" : poster
		    });
		    console.log("Golden Gate");
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
	    var dateutils = require('date-utils');
	    res.render('index', starts);
	    callback();
	    }
	]
    
    
   
    
    });
});
module.exports = router;
