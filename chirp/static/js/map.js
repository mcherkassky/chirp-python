var width = 960,
    height = 500;

var projection = d3.geo.mercator();
//    .center([0, 5 ])
//    .scale(900)
//    .rotate([-180,0]);

var svg = d3.select("#map").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "svg-map");

var path = d3.geo.path()
    .projection(projection);

var g = svg.append("g");
d3.json("/static/lib/topojson/world-110.json", function(error, topology) {
    svg.append("path")
      .datum(topojson.feature(topology, topology.objects.countries))
      .attr("d", path);

    var coordinates = projection([10,20]);
    svg.append('svg:circle')
        .attr('cx', coordinates[0])
        .attr('cy', coordinates[1])
        .attr('r', 5)
        .style('fill','red');
});