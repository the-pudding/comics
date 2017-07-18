(function() {
  $(window).scroll(function() {
    var middle = window.innerHeight / 2
    var bbox1 = d3.select('#powerSplit_graph').node().getBoundingClientRect()
    var stick1 = bbox1.top < middle && bbox1.bottom > 0
    d3.select('#stick').classed('is-visible', stick1)

    var bbox2 = d3.select('#genNames_graph').node().getBoundingClientRect()
    var stick2 = bbox2.top < middle && bbox2.bottom > 0
    d3.select('#stick2').classed('is-visible', stick2)
  });

})()
