(function() {

    var chartDiv = document.getElementById("powerSplit_graph");
    var svg = d3.select(chartDiv).append("svg");

    function redraw() {

    document.querySelector( '#powerSplit_graph' ).innerHTML = '';

    var m = {
        top: 70,
        right: 60,
        bottom: 630,
        left: 30
      },
    width_power = chartDiv.clientWidth - m.left - m.right;
    height_power = 2000 - m.top - m.bottom;
      // width_power = 900 - m.left - m.right,
      // height_power = 1600 - m.top - m.bottom,
      pad = 0.2;

    // Functions for offsetting annotations
      // function dy(t) {
      //   return y(t)-y(0);
      // }
      // function dx(t) {
      //   return x(t)-x(0);
      // }

    var y = d3.scaleBand().range([10, height_power]);

    var x = d3.scaleLinear().rangeRound([0, width_power]);
    var y0 = d3.scaleOrdinal();

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var svg = d3.select("#powerSplit_graph").append("svg")
      .attr("width", width_power + m.right + m.left + 100)
      .attr("height", height_power + m.top + m.bottom)
      .append("g")
      .attr("transform",
        "translate(" + m.left + "," + m.top + ")");


    d3.csv("gender_bars_sig_less.csv", function(error, data) {

      data.forEach(function(d) {
        d.diff = +d.diff;
        d.per_males = +d.per_males;
        d.per_females = +d.per_females;
      });

      var barHeight = height_power / (data.length);
      var padBetween = 60;

      y0.domain(data.map(function(d) {
        return d.category;
      }));
      y.domain(data.map(function(d) { return d.power; }));


      
      var y0Range = [0];
      var categoryD = d3.nest()
            .key(function(d) {
              return d.category;
            })
            .rollup(function(d) {
              var barSpace = ( (barHeight+pad) * d.length);
              y0Range.push(y0Range[y0Range.length - 1] + barSpace + padBetween);
              return d3.scaleBand()
                        .domain(d.map(function(c) {
                          return c.power
                        }))
                        .rangeRound([0, barSpace], pad);
              })
            .object(data);


      y0.range(y0Range);

      
      var d3Max = d3.max(data, function(d) { return d.diff });
      var d3Min = d3.min(data, function(d) { return d.diff });

      x.domain([-8,8]);

      var axisX = d3.axisTop(x)
           .tickFormat( function(d){ return (Math.abs(d)); })
           .tickSize(-1900)

      svg.append("g")
        .attr("class", "x axis tk-atlas")
        .attr("transform", "translate(0, -50)")
        .call(axisX)
        .selectAll("text")
        .style("text-anchor", "middle");

      svg.append("g")
        .attr("class", "y axis")
        .attr("class", "tk-atlas")
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + x(0) + ",0)")
        .call(customYAxis)

        function customYAxis(g) {
        g.call(d3.axisLeft(y0));
        g.select(".domain").remove();
        g.selectAll(".tick line").attr("stroke", "#777").attr("opacity", "0");
        g.selectAll(".tick text").attr("dy", -8).attr("class", "label");
        }




const annotation_object = [{
      note: {
        title: "Object—ified",
        label: "Though Wonder Woman has her lasso, and Stargirl has a cosmic staff, it's generally the male characters that like their stuff. Think Thor and his hammer, or Iron Man and his suit.",
        wrap:180
      },
          y: y('Gadgets')+padBetween-15,
          x: 100,
          
    }
  ]

        const makeAnnotation_object = d3.annotation()
    .editMode(false)
    .type(d3.annotationLabel)   
    .annotations(annotation_object)
  svg.append("g")
      .attr("id", "object_anno")
      .attr("class", "annotation-group")
      .attr("class", "tk-atlas")
      .attr("font-size", 12)
      .call(makeAnnotation_object)   



const annotation_mind = [{
      note: {
        title: "Mind your powers",
        label: "There is a clear trend here: Female characters are more often given non-physical, thought-induced abilities.",
        wrap:130
      },
          y: y('Empathy')+10+padBetween*5,
          x: 450,
          
    }
  ]

const makeAnnotation_mind = d3.annotation()
    .editMode(false)
    .type(d3.annotationLabel)   
    .annotations(annotation_mind)
  svg.append("g")
      .attr("id", "mind_anno")
      .attr("class", "annotation-group")
      .attr("class", "tk-atlas")
      .attr("font-size", 12)
      .call(makeAnnotation_mind)

      svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "power_bar")
        .style("fill", function(d, i) {
          if(d.diff>=0) {return colors.male}
          else return colors.female; })
        .attr("x", function(d) { 
          if(d.diff>=0) {return x(0)}
          else return x(d.diff); })
        .attr("y", function(d) {
          return y0(d.category) + categoryD[d.category](d.power);
        })
        .attr("height", function(d) {
          return (1.0-pad)*barHeight;
        })
        .attr("width", function(d) { return x(Math.abs(d.diff))-x(0); })
        .on('mouseover', function (d) {
          var section = d3.select(this);
              section.style("opacity", 0.6)
          d3.select('#tooltip')
          .style("left", (d3.event.pageX + 5) + "px")
          .style("top", (d3.event.pageY - 28) + "px")
          .html("<p class='difference'>Difference: " + Math.abs(d.diff).toFixed(2) + "</p><p class='gender'><span>Males:</span> <span class='number'>" + Math.abs(d.per_males).toFixed(2) + "%</span></p><p class='gender'><span>Females:</span> <span class='number'>" + Math.abs(d.per_females).toFixed(2) + "%</span></p>");
           d3.select('#tooltip').classed('hidden', false);
        })
        .on("click",  function(d){
          $("#textInsert_powers").html(d.definition)
          $("#titleInsert_powers").html(d.power);
        })
        .on('mouseout', function () {
          var section = d3.select(this);
              section.style("opacity", '1')
          d3.select('#tooltip').classed('hidden', true);
        });





      var ls = svg.selectAll(".labels")
        .data(data)
        .enter().append("g");
      
      // bg text 
      ls.append("text")
        .attr("class", "bar__label bar__label--bg tk-atlas")
        .text(function(d) {
          return (d.power);
        })
        .attr('text-anchor', function(d) {
        if (d.diff <= 0) {return 'end'}
          else {return 'start'}
        })
        .attr("x", function(d) {
        if (d.diff <= 0) {return x(d.diff)-5}
          else {return x(d.diff)+5}
        })
        .attr("y", function(d) {
          return y0(d.category) + categoryD[d.category](d.power) + 0.6*barHeight;

        })

      ls.append("text")
        .attr("class", "bar__label tk-atlas")
        .text(function(d) {
          return (d.power);
        })
        .attr('text-anchor', function(d) {
        if (d.diff <= 0) {return 'end'}
          else {return 'start'}
        })
        .attr("x", function(d) {
        if (d.diff <= 0) {return x(d.diff)-5}
          else {return x(d.diff)+5}
        })
        .attr("y", function(d) {
          return y0(d.category) + categoryD[d.category](d.power) + 0.6*barHeight;

        })
        .on('mouseover', function (d) {
          d3.select('#tooltip')
          .style("left", (d3.event.pageX + 5) + "px")
          .style("top", (d3.event.pageY - 28) + "px")
          .html("<p class='difference'>Difference: " + Math.abs(d.diff).toFixed(2) + "</p><p class='gender'><span>Males:</span> <span class='number'>" + Math.abs(d.per_males).toFixed(2) + "%</span></p><p class='gender'><span>Females:</span> <span class='number'>" + Math.abs(d.per_females).toFixed(2) + "%</span></p>");
           d3.select('#tooltip').classed('hidden', false);
        })
        .on("click",  function(d){
          $("#textInsert_powers").html(d.definition)
          $("#titleInsert_powers").html(d.power);
        })
        .on('mouseout', function () {
          d3.select('#tooltip').classed('hidden', true);
        });


    });

 } // End of redraw function

 redraw();

 window.addEventListener("resize", redraw);

// init()
})()
