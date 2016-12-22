mandle= {
   data:{
      updateurl:"http://127.0.0.1:8000/update",
      processurl:"http://127.0.0.1:8000/process?format=json",
      jsonurl:"http://127.0.0.1:8000/jsondata",
      query:"",
      total:0,todo:0,action:"no"
   },
   init:function(){
      mandle.data.query = window.location.href.toString().split(window.location.host)[1];
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
         mandle.moviebase.collection();
         if(mandle.data.query.length <= 1){
            mandle.moviebase.update()
         }else{
            "No update cause long"
         }
      },
      progress:function(){
         perc = Math.floor((mandle.data.total - mandle.data.todo) / mandle.data.total * 100);
         console.log(mandle.data.total + " et " + mandle.data.todo + " et " + perc)
         document.getElementById("collectionbar").style.width = perc +"%";
         document.getElementById("collectionbar").innerHTML = perc +"%";
         action = (mandle.data.action!="no")?'<span class="glyphicon glyphicon-refresh" ></span>  ' + mandle.data.action  + " )":'';
         // aria-hidden="true"
         document.getElementById("progresslabel").innerHTML = perc + " % ( " + (mandle.data.total - mandle.data.todo) + " / " + mandle.data.total + ")";
      },
      collection:function(){
         if(document.getElementById("collection")){
            var req = new XMLHttpRequest()
            req.open('GET', mandle.data.jsonurl);
            req.onreadystatechange = function () {
               if (req.readyState === 4) {
                  if (req.status === 200) {
                     dat = JSON.parse(req.responseText);
                     console.log(dat);
                     mandle.data.total = dat["total"];
                     mandle.data.todo = dat["todo"];
                     mandle.moviebase.progress();
                  }
               }
            }
            req.send();
         }
      },
      update:function(){
         mandle.data.action = "update";
         mandle.moviebase.progress();
         var req = new XMLHttpRequest()
         req.open('GET', mandle.data.updateurl);
         req.onreadystatechange = function () {
            if (req.readyState === 4) {
               mandle.data.action = "no";
               if (req.status === 200) {
                  dat = JSON.parse(req.responseText);
                  console.log(dat);
                  //text = "<strong>Update:</strong> " + dat["total"] + " movies <br> " + dat["nb"] + " movie added - " + (Math.round(dat["time"]*1000)/1000) + "s"
                  //mandle.notification.addNotif("1",text)

                  mandle.data.total = dat["total"];
                  if(dat["nb"] != 0){
                     mandle.moviebase.update()
                  }else{
                     mandle.moviebase.process()
                  }
               } else {
                  text = "<strong>Update:</strong> Error"
                  mandle.notification.addNotif("4",text);
                  setTimeout(mandle.moviebase.update, 2000);
               }
               mandle.moviebase.progress();
            }
         }
         req.send();
      },
      process:function(){
         mandle.data.action = "process";
         mandle.moviebase.progress();
         //text = "<strong>Process:</strong>"
         //mandle.notification.addNotif("2",text)
         var req = new XMLHttpRequest()
         req.open('GET', mandle.data.processurl);
         req.onreadystatechange = function () {
            if (req.readyState === 4) {
               if (req.status === 200) {
                  dat = JSON.parse(req.responseText);
                  console.log(dat);
                  text = "<strong>Process:</strong><br>" + dat["nb"] + " movie processed - " + (Math.round(dat["time"]*1000)/1000) + "s"
                  mandle.notification.addNotif("1",text)
                  mandle.data.todo = dat["todo"];
                  if(dat["nb"] != 0){
                     mandle.moviebase.process()
                  }
               } else {
                  text = "<strong>Process:</strong> Error - action stopped";
                  mandle.notification.addNotif("4",text);
               }
               mandle.moviebase.progress();
            }
         }
         req.send();
      }
   }
};

document.addEventListener( "DOMContentLoaded", function(){
   mandle.init();
});
