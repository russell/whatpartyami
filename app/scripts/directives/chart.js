'use strict';

angular.module('govtHackApp')
  .directive('chart', function () {
       return {
        restrict: 'E',
        scope: {
            data: '=data'
        },
        template: '<div class="chart"></div>',
        link: function(scope, element, attrs) {

            var chart = new google.visualization.BarChart(element[0]);


            scope.$watch('data', function(v) {

                var options = {
                  width: 850,
                  height: (v.length-1)*120 + 100,
                  colors: _.pluck(parties,'color'),
                  reverseCategories: false,
                  legend : {position: 'bottom', textStyle: {fontSize: 11}},
                  backgroundColor: '#eeeeee',
                  title: 'Party\'s agreement with you',
                  tooltip : {trigger :'none'},
                  chartArea:{width:"67%", height: "80%"}
                  
                };


                var data = google.visualization.arrayToDataTable(v);
                chart.draw(data, options);

            });

        }
    };
  });
