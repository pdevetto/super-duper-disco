mandle= {
   data:{
      updateurl:"http://127.0.0.1:8000/update",
      processurl:"http://127.0.0.1:8000/process"
   },
   init:function(){
      mandle.notification.init();
      mandle.moviebase.init();
   },
   notification:{
      init:function(){
         mandle.notification.addNotif("3","<strong>Holy guacamole!</strong> happy to see you !.")
      },
      addNotif:function(type, text){
         $("#notifs").slideDown();
         alert = (type == "1"?"success":
                     (type=="2"?"info":
                        (type=="3"?"warning":"danger")))
         notif = "<div class='alert alert-dismissible fade in alert-" + alert + "' role='alert'>"+
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>"+
            text + "</div>"
         document.getElementById("notifications").innerHTML += notif;
      }
   },
   moviebase:{
      init:function(){
         mandle.moviebase.update()
      },
      update:function(){
         var req = new XMLHttpRequest()
         req.open('GET', mandle.data.updateurl);
         req.onreadystatechange = function () {
            if (req.readyState === 4) {
               if (req.status === 200) {
                  dat = JSON.parse(req.responseText);
                  console.log(dat);
                  text = "<strong>Update:</strong> " + dat["total"] + " movies <br> " + dat["nb"] + " movie added - " + (Math.round(dat["time"]*1000)/1000) + "s"
                  mandle.notification.addNotif("1",text)

                  if(dat["nb"] != 0){
                     setTimeout(mandle.moviebase.update, 2000);
                  }else{
                     setTimeout(mandle.moviebase.process, 1000);
                  }
               } else {
                  text = "<strong>Update:</strong> Error"
                  mandle.notification.addNotif("4",text);
                  setTimeout(mandle.moviebase.update, 2000);
               }
            }
         }
         req.send();
      },
      process:function(){
         text = "<strong>Process:</strong>"
         mandle.notification.addNotif("2",text)
         var req = new XMLHttpRequest()
         req.open('GET', mandle.data.processurl);
         req.onreadystatechange = function () {
            if (req.readyState === 4) {
               if (req.status === 200) {
                  dat = JSON.parse(req.responseText);
                  console.log(dat);
                  text = "<strong>Process:</strong><br>" + dat["nb"] + " movie processed - " + (Math.round(dat["time"]*1000)/1000) + "s"
                  mandle.notification.addNotif("1",text)

                  if(dat["nb"] != 0){
                     setTimeout(mandle.moviebase.process, 500);
                  }
               } else {
                  text = "<strong>Process:</strong> Error"
                  mandle.notification.addNotif("4",text)
                  setTimeout(mandle.moviebase.process, 5000);
               }
            }
         }
         req.send();
      }
   }
};

document.addEventListener( "DOMContentLoaded", function(){
   mandle.init();
});
