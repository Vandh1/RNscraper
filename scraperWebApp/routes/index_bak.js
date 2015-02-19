var express = require('express');
var router = express.Router();



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
    db.each("SELECT * from starts;", function(err,row){
	startDate = row.startDate
	server = row.server
	announcementDate = row.announcementDate
	poster = row.poster;

	switch(server){
	case "Interrail West":
	    console.log(startDate);
	    starts.interrailwest.push({
		"start" : startDate,
		"announcementDate" : announcementDate,
		"poster" : poster
	    });
	    console.log("Interrail West");
	    break;
	case "Interrail West 2":
	    starts.interrailwest2.push({
		"start" : startDate,
		"announcementDate" : announcementDate,
		"poster" : poster
	    });
	    console.log("Interrail West 2");
	    break;
	case "Interrail West 3":
	    starts.interrailwest3.push({
		"start" : startDate,
		"announcementDate" : announcementDate,
		"poster" : poster
	    });
	    console.log("Interrail West 3");
	    break;
	case "Golden Gate":
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
	
	console.log(starts);
	
	
    });
    res.render('index', starts);
    
});

module.exports = router;
