(function() {
var radius = 8
var chartDiv_names_ex = document.getElementById("genNames_explainer");
var svg_names_ex = d3.select(chartDiv_names_ex).append("svg");

function redraw_names() {

    document.querySelector( '#genNames_explainer' ).innerHTML = '';


    var margin = {top: 50, right: 60, bottom: 0, left: 50},
        width_names_ex = chartDiv_names_ex.clientWidth - margin.left - margin.right;
        height_names_ex = 200 - margin.top - margin.bottom;

    var y = d3.scaleBand()
        .range([10, height_names_ex], 1);

    var x = d3.scaleLinear()
        .range([width_names_ex, 0]);

    // Functions for offsetting annotations
    function dy(t) {
      return y(t)-y(0);
    }
    function dx(t) {
      return x(t)-x(0);
    }

    var svg_names_ex = d3.select("#genNames_explainer").append("svg")
        .attr("width", width_names_ex + margin.left + margin.right)
        .attr("height", height_names_ex + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        d3.csv("genNames_explainer_data.csv", function(error, data) {
          if (error) throw error;

          data.forEach(function(d) {
            d.gen_per = +d.gen_per/100.0;
            d.count = +d.count;
            d.per_fake = +d.per_fake/100.0;
          });

          data.sort(function(a,b) {
            return d3.ascending(a.gen_per,b.gen_per);
          });


          x.domain([d3.max(data, function(d) { return d.gen_per; }), -0.3]);
          y.domain(data.map(function(d) { return d.gen_cat; }));



        //ANNOTATIONS 
          const circleAnnotations_girl = [
            {
              note: {
                // title: "Girls, not women",
                label: "5.7% of female characters with gendered names have 'woman' in their name.",
                wrap:100
              },
              x: x(-.06),         
              y: y('woman'),   
              dx: dx(0),
              dy: 30,
            
            }
          ]
          const makeCircleAnnotations_girl = d3.annotation()
            .editMode(false)
            .type(d3.annotationLabel)   
            .annotations(circleAnnotations_girl)
          svg_names_ex.append("g")
              .attr("id", "girl_anno_ex")
              .attr("class", "tk-atlas annotation-group")
              .attr("font-size", 12)
              .call(makeCircleAnnotations_girl)   


          const circleAnnotations_man = [
            {
              note: {
                // title: "Men, not boys",
                label: "30% of male characters with gendered names have 'man' in their name.",
                wrap:100
              },
              x: x(.31),        
              y: y('woman'), 
              dx: dx(0),
              dy: 30
            }
          ]
          const makeCircleAnnotations_man = d3.annotation()
            .editMode(false)
            .type(d3.annotationLabel)   
            .annotations(circleAnnotations_man)
          svg_names_ex.append("g")
              .attr("id", "man_anno_ex")
              .attr("class", "tk-atlas annotation-group")
              .attr("font-size", 12)
              .call(makeCircleAnnotations_man) 

        // END ANNOTATIONS





          // Make the lines between the dots

          var linesBetween_ex = svg_names_ex.selectAll("lines.between_ex")
            .data(data)
            .enter()
            .append("line");

          linesBetween_ex.attr("class", "between_ex")
            .attr("x1", function(d){return x(d.gen_per)})
            .attr("y1", function(d){return y(d.gen_cat)})
            .attr("x2", function(d){return x(d.per_fake)})
            .attr("y2", function(d){return y(d.gen_cat)})


          // Dots for each gendered name

          var genDots_ex = svg_names_ex.selectAll(".genDot_ex")
            .data(data);

          genDots_ex.enter().append("circle")
              .attr("class", "genDot_ex")
              .attr("r", function(d) {return d.gen_name === 'lady' ? radius * 1.35 : radius})
              .attr("cx", function(d) { return x(d.gen_per); })
              .attr("cy", function(d) { return y(d.gen_cat); })
              .style("opacity", 1)
              .style("fill", function(d){
                  if (d.gen_name === "lady" ) { return colors.female }
                  else if (d.gender == 1) {return colors.male}
                  else {return colors.female}
                })
              .classed("is-active", function(d) {return d.gen_name === 'lady'});
              // .on('mouseover', function (d) {
              //     var section = d3.select(this);
              //         // section.style("opacity", 0.6)
              //     d3.select('#tooltip')
              //     .style("left", (d3.event.pageX + 5) + "px")
              //     .style("top", (d3.event.pageY - 28) + "px")
              //     .html("<p class='difference'>" + Math.abs(d.gen_per*100).toFixed(1) + "%</p>");
              //      d3.select('#tooltip').classed('hidden', false);
              //   })
              // .on('mouseout', function () {
              //     var section = d3.select(this);
              //         section.style("opacity", '1')
              //     d3.select('#tooltip').classed('hidden', true);
              //   });



              // Text for gender names
          var texts_ex = svg_names_ex.selectAll(".dodo_ex")
            .data(data);

          texts_ex.enter().append("text")
              .attr("class", "bar__label dodo_ex tk-atlas")
              .attr("font-size", 10)
              .attr("x", function(d) {
                if (d.gen_per <=0){return x(d.gen_per)-15}
                  else {return x(d.gen_per)+15}
                 })
              .attr("y", function(d) {
                if (d.gen_per <=0){return y(d.gen_cat)+4}
                  else {return y(d.gen_cat)+4}
                 })
              .attr('text-anchor', function(d) {
                if (d.gen_per <= 0) {return 'end'}
                  else {return 'start'}
                })
              .style("fill", function(d) {
                if (d.dim == 1) {return colors.accent}
                  // else {return "black"}
                })
              .text(function(d) { return d.gen_name;});

          var lineEnd_ex = 0;

          // Line at 0
          svg_names_ex.append("line")
            .attr("x1", function(){return x(lineEnd_ex)})
            .attr("y1", -10)
            .attr("x2", function(){return x(lineEnd_ex)})
            .attr("y2", 30)
            .style("stroke-width", 0.3)
            .style("stroke", "black")
            .style("fill", "none");

          svg_names_ex.append("text")
            .attr('text-anchor', 'middle')
            .attr("x", function(){return x(lineEnd_ex)})
            .attr("y", -15)
            .attr("class", "tk-atlas label_axis ")
            .text('0%');


   }) // end d3.csv
    
}; // end redraw function


     redraw_names();

     window.addEventListener("resize", redraw_names);


})()
