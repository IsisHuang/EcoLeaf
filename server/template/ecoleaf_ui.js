document.addEventListener("DOMContentLoaded", (event) => {

  var dataURL="/get_biometric";
  document.getElementById("button").addEventListener("click", clicked);
  document.getElementById("mode1").addEventListener("click", toggled);
  document.getElementById("mode2").addEventListener("click", toggled);
  
  function update(data) {
    let img=document.createElement("img");
    img.src="result.jpeg";
    document.getElementById("idx").innerHTML=data[0];
    document.getElementById("ecoleaf").appendChild(img);
    document.getElementById("ecoleaf").value="Low in magnesium, whole grains and leafy greens recommended, see suggested recipe!";
  }

  function clicked() {
    document.getElementById("value").value="-";
    document.getElementById("diet").value="";
    document.getElementById("sleep").value="";
    document.getElementById("wake").value="";
    setInterval(function() {
      fetch(dataURL)
      .then(response=>response.json())
      .then(update)
    }, 3000)
  }

  function toggled(event) {
    let interactive=document.getElementById("metric");
    let flightplan=document.getElementById("index");
    if(event.target.value=="metric") {
      flightplan.style.display="none";
      interactive.style.display="inline";
    }
    if(event.target.value=="index") {
      interactive.style.display="none";
      flightplan.style.display="inline";
    }
  }

});