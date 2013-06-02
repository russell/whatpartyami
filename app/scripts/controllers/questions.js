'use strict';

var ANSWERS = {};

angular.module('govtHackApp')
  .controller('QuestionsCtrl', function ($scope, $log, $location) {
	$scope.topics = [];

  	angular.forEach(jsonData, function(value){
  		var topic = {};
  		topic['question'] = value.q;
		$scope.topics.push(topic);
	});


	ANSWERS = $scope.topics;

	$scope.submit = function() {
    	$log.info($scope.topics);
    	$location.path( "/results" );
  	};
});
