'use strict';

var parties = {
	"Australian Greens"     : {"color": "#10c25b" },
	"Australian Labor Party": {"color": "#F00011" }, 
	"National Party"        : {"color": "#00800f" }, 
	"Independent"           : {"color": "#b3b3b3" }, 
	"Liberal Party"         : {"color": "#080cab" }
};

angular.module('govtHackApp')
  .controller('ResultsCtrl', function ($scope, $log) {
  	var numQ = 0;
  	// if we don't have answers go back to landing page, DEV_MODE use defaults
	if (!ANSWERS || !ANSWERS.length) ANSWERS = [{"question":"I believe in same sex marriage.","$$hashKey":"01O","answer":true},{"question":"I am concerned about the number of asylum seekers.","$$hashKey":"01P","answer":true},{"question":"I believe the government should improve the public heath system.","$$hashKey":"01Q","answer":true},{"question":"I am concerned about my Superannuation.","$$hashKey":"01R","answer":""},{"question":"I think the government should increased taxes on non-renewable resource based companies.","$$hashKey":"01S","answer":false},{"question":"I am concerned about climate change.","$$hashKey":"01T","answer":false}];
  	$scope.answers = ANSWERS;
  	$scope.results = parties;

  	var chartData = [];
  	angular.forEach(ANSWERS, function(answer, i){
  		if (answer.answer === undefined || answer.answer === '' || !jsonData[i]) return;
  		var myVotes = jsonData[i].votes;
  		if (!myVotes) return;

  		var chartRow = [];
  		chartRow.push(jsonData[i].theme);
		angular.forEach(myVotes, function(ayesNoes, key) {
			var p = $scope.results[key],
			totalVotes = ayesNoes[0] + ayesNoes[1],
			myPct = ayesNoes[ answer.answer ? 0 : 1 ] / totalVotes;
			if (numQ === 0)  { p['sum'] = 0; }
			p[i] = myPct;
			p['sum'] += myPct;

			// build chart [question#][party-ix]
			chartRow.push(Math.round(myPct === 0 ? 1 : myPct * 100)); 
	  	});

	  	chartData.push(chartRow);
		numQ++;
  	});

  	// calc matching pct
  	angular.forEach($scope.results, function(value, key){
  		value['pct'] = (!value['sum'] ? 0 : value['sum']) / numQ;
  	});

	$scope.view = [];
  	angular.forEach($scope.results, function(value, key){
  		value['name'] = key;
  		$scope.view.push(value);
  	});

    var header = _.pluck($scope.results, 'name');
    header.unshift("Themes");
    chartData.unshift(header);

    $scope.chartData = chartData;
    $scope.scoreHistory = chartData;
  	$scope.view.sort(function (a,b) { return b.pct - a.pct;})

    $scope.loadDataFromServer = function() {
        $scope.scoreHistory = $scope.chartData;
    };
});

google.setOnLoadCallback(function() {
    angular.bootstrap(document, ['govtHackApp']);
});

google.load('visualization', '1', {packages: ['corechart']});