/**
 
 * Send the vals to be loaded
 * @param {string} componies and stock prices
 */
 function fix_box(vals) {
    console.log("Function called");
    console.log(vals)
    var list = vals.split(",")
    var names = new Array()
    var prices =  new Array()
    for (var i = 0 ; i < list.length / 2; i++){
        var k = i * 2
        names.push(list[k]);
        prices.push(list[k+1])
        console.log(list[k])
    }
    var cols =  document.getElementsByClassName("col");
    console.log(cols)
    for (var i = 0; i < 3; i ++){
        console.log("trying to change values")
        cols[i].getElementsByClassName("StockLabel")[0].getElementsByTagName("text")[0].innerHTML = "gme"
        cols[i].getElementsByClassName("card-body")[0].innerHTML = "Stock Price is: "
        console.log(names[i])
    }


}
function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
    console.log(selector);
    // Use the list of sample names to populate the select options
    d3.json("samples.json").then((data) => {
      var sampleNames = data.names;
      console.log(sampleNames);
      sampleNames.forEach((sample) => {
        selector
          .append("option")
          .text(sample)
          .property("value", sample);
      });
      // Use the first sample from the list to build the initial plots
      var firstSample = sampleNames[0];
      buildCharts(firstSample);
      buildMetadata(firstSample);
    });
   }