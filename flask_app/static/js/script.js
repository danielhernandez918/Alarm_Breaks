const display = document.getElementById('clock'); //save reference to clock div and use this to update to curent time saved into constant
const audio = new Audio('https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3');  //create new audio object saced into constant
audio.loop = true; //loop specifies to keep playing sound until alarm is cleared
//let alarmTime = null;// store alarm user sets. only used when using users inputs alarm manually
let alarmTimeout = null;// store reference to the set alarm so can clear later

function updateTime() {
    const date = new Date(); //new date object holds current data and time
    // const hour = formatTime(date.getHours()); // this method extract hour mnutes second to clock
    // const minutes = formatTime(date.getMinutes());
    // const seconds = formatTime(date.getSeconds());
    // display.innerText=`${hour} : ${minutes} : ${seconds}`
    display.innerText=date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true });
}

// function formatTime(time) { //gives me an extra zero if number is orinally less than 10
//     if ( time < 10 ) {
//         return '0' + time;
//     }
//     return time;
// }

// To set up an alarm with a input
// function setAlarmTime(value) { 
//     alarmTime = value;
//     console.log(alarmTime)
// }


function setAlarm() {
    var h = document.getElementById('h').value;
    h = parseInt(h)
    var m = document.getElementById('m').value;
    const ampm = document.getElementById('ampm').value;
    if(ampm == 'pm') {
    h = h + 12;
    }
    else if(ampm == 'am' && h == 12) {
        console.log('yes')
        h = h - 12;
    }
    h = h.toString()
    // var hm = '2022,03,02,'+h+":"+m
    var hm = h+":"+m;

    if(hm) {
        const current = new Date();// gets current time when set alarm button pressed
        // console.log(current)
        const year = (current.getFullYear());
        const month = (current.getMonth())+1;// console.log(month) need add +1 to get correct month because month comes out as 0-11 normally
        const day = (current.getDate());
        var time = year + ','+ month + ',' + day + ',' + hm;
        // console.log(time)
        const timeToAlarm = new Date(time); //when alarm should go off
        console.log(timeToAlarm)

        if (timeToAlarm > current) {
            const timeout = timeToAlarm.getTime() - current.getTime();
            alarmTimeout = setTimeout(() => audio.play(), timeout);
            alert('Alarm set');
        }
        else if(timeToAlarm < current) {
            const timeout = 86400000-(current.getTime() - timeToAlarm.getTime());// getTime calculate difference in mlliseconds between two dates
            alarmTimeout = setTimeout(() => audio.play(), timeout);// set timeout to variable so user can clear alarm before it goes off if they choose.  Using setTimeout to set alarm. => is a promise. setTimeout is a asynnchorus action that promises to return value in the future
            alert('Alarm set');
        }
    }
}

function clearAlarm() {
    audio.pause(); //pauses the current sound
    if (alarmTimeout) { //if there is alarmTimeout, will clear it
        clearTimeout(alarmTimeout);
        alert('Alarm cleared');
    }
}

setInterval(updateTime, 1000);