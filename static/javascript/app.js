var app = angular.module("Activities", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{*');
  $interpolateProvider.endSymbol('*}');
}]);

app.filter('capitalize', function() {
    return function(input) {
      return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
});

app.controller("ActivityController", ['$scope', '$http', function($scope, $http) {

	$scope.activities = {};
	$scope.login_input_incorrect = false;
	$scope.create_clicked = false;
	$scope.create_error = false;
	$scope.errors = [];

	$scope.create_time = "";
	$scope.create_name = "";
	$scope.create_details = "";

	$http.get("api/v1/activities").
		then(function(response) {
			$scope.activities = response.data.result;
		});

	$http.get("api/v1/user").
		then(function(response) {
			$scope.user_username = response.data.username;
		});

	$scope.start_schedule = function() {
		if ($scope.activities == undefined) {
			return true;
		}
		else {
			return $scope.activities[$scope.user_username] == undefined;
		}
	}

	$scope.clicked_create_button = function() {
		$scope.create_clicked = true;
	}

	$scope.remove_create_schedule = function() {
		$scope.create_clicked = false;
		$scope.create_time = "";
		$scope.create_name = "";
		$scope.create_details = "";
	}

	$scope.create_schedule = function() {
		$scope.create_error = false;
		$scope.errors = [];
		
		check_create_input();
		if(!$scope.create_error){
			var dataObj = {
				username: String($scope.user_username),
				time: String($scope.create_time),
				activity: String($scope.create_name),
				details: String($scope.create_details)
			};
			post_data('api/v1/activities', dataObj, create_success, create_fail);
		}
	}

	$scope.login = function() {
		check_login_input();
		if(!$scope.login_input_incorrect) {
			var dataObj = {username: $scope.username, password: $scope.password};
			post_data('api/v1/login', dataObj, login_success, login_fail);
		}
	};

	$scope.logout = function() {
		post_data('api/v1/logout', "" ,navigate);
	};

	function refresh() {
		$http.get("api/v1/activities").
			then(function(response) {$scope.activities = response.data.result;
			});
	}

	function post_data(url, dataObj, function1, function2){
		$http.post(url, dataObj).then(function1, function2);
	}

	function put_data(url, dataObj, function1, function2){
		$http.put(url, dataObj).then(function1, function2);
	}

	function check_create_input() {
		$scope.errors = [];
		if(!$scope.create_time) {
			$scope.create_error = true;
			$scope.errors.push("Need to include date and time");
		}
		if(!$scope.create_name) {
			$scope.create_error = true;
			$scope.errors.push("Need to include the activity name");
		}
	}

	function create_success() {
		$scope.create_clicked = false;
		refresh();
	}

	function create_fail(response) {
		$scope.create_error = true;
		$scope.errors = response.data['errors'];
		$scope.test = $scope.create_name;
	}

	function check_login_input() {
		$scope.errors = [];
		if(!$scope.username) {
			$scope.login_input_incorrect = true;
			$scope.errors.push("Missing username from login");

		}
		if(!$scope.password) {
			$scope.login_input_incorrect = true;
			$scope.errors.push("Missing password from login");
		}
		if($scope.username && $scope.password){
			$scope.login_input_incorrect = false;
			$scope.errors = [];
		}
	}

	function login_success(response, status) {
		$scope.errors = [];
		window.location = '/';
	}

	function login_fail(response, status) {
		$scope.login_input_incorrect = true;
		$scope.errors = response.data["errors"];
	}

	function navigate() {
		window.location = '/';
	}


}]);
