'use strict';

angular.module('govtHackApp')
  .controller('MainCtrl', function ($scope, $location) {
    $scope.start = function() {
    	$location.path('/questions')
    };
  });
