/*
  dateFormatter: str -> str

  This function takes in a time in the format ex. "24 May 2019 00:00:00 UTC"
  and returns a string that is one of the following:
  str ::= | 12:00 am
          | <Weekday> 12:00 am
          | <Month> <Day>, <Year> 12:00AM if time - timeNow > 7 days
*/

function dateFormatter (string) {
  inputTime = new Date(Date.parse(string));
  timeNow = new Date(Date.now());
  difference = convertMS(timeNow - inputTime);
  var options = {};
  if (difference["days"] > 7) {
    // days > 7
    options = {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "numeric",
      hour12: true
    };
    return inputTime.toLocaleDateString('en-US', options);
  }
  else {
    if (sameDay(inputTime, timeNow)) {
      // "same day"
      options = {
        hour: "numeric",
        minute: "numeric",
        hour12: true
      };
      return inputTime.toLocaleTimeString('en-US', options);
    }
    else {
      // "0 < days < 7"
      options = {
        weekday: "short",
        hour: "numeric",
        minute: "numeric",
        hour12: true
      }
      return inputTime.toLocaleTimeString('en-US', options);
    }
  }
}


//Converts milliseconds to days, hours, minutes and seconds and returns a dict.
function convertMS(ms) {
    var d, h, m, s;
    s = Math.floor(ms / 1000);
    m = Math.floor(s / 60);
    s = s % 60;
    h = Math.floor(m / 60);
    m = m % 60;
    d = Math.floor(h / 24);
    h = h % 24;
    return { days: d, hours: h, minutes: m, seconds: s };
};

// Taken from https://stackoverflow.com/questions/43855166/how-to-tell-if-two-dates-are-in-the-same-day
function sameDay(d1, d2) {
  return d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate();
}
