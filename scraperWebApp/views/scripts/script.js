
function isCurrentEra(date){
    alert("iscurrera");
    var parts = date.split("-");
    var dt = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
    var nextdt = new Date();
    nextdt.setDate(dt.getDate+14); //next era start
    var currentDate = new Date();
    if (dt<currentDate && nextDt > currentDate) return true;
    else return false;
}

function parseDate(date, addDays){
    alert("pd");
    var parts = date.split("-");
    var dt = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
    dt.setDate(dt.getDate()+addDays);
    var month = dt.getMonth() +1;
    var day = dt.getDate();
    if(day<10) day = "0"+day;
    if(month <10) month = "0"+month;
    var dtStr = dt.getFullYear()+"-"+month+"-"+day;
    return dtStr;
}
