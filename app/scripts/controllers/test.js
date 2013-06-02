'use strict';

// angular.module('govtHackApp')
//   .controller('TestCtrl', function ($scope) {
//     $scope.awesomeThings = [
//       'HTML5 Boilerplate',
//       'AngularJS',
//       'Karma'
//     ];
//       $scope.radioModel = 'Middle';

//   });

google.setOnLoadCallback(function() {
    angular.bootstrap(document, ['govtHackApp']);
});

google.load('visualization', '1', {packages: ['corechart']});

angular.module('govtHackApp')
	.controller('TestCtrl', function($scope) {

    $scope.scoreHistory = [];
    $scope.loadDataFromServer = function() {
        var x = [
            ['interval', 'count']
        ];
        var scoreHistory = [
            {
                intervalStart: 12,
                count: 20
            },
            {
                intervalStart: 100,
                count: 200
            },
            {
                intervalStart: 200,
                count: 50
            },
            {
                intervalStart: 250,
                count: 150
            }
        ];

        angular.forEach(scoreHistory, function(record, key) {
            x.push([
                record.intervalStart,
                record.count
            ]);
        });
        $scope.scoreHistory = x;
    };

});