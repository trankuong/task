app.directive('userSchedule', ['$http', function($http) {
	return {
		restrict: 'E',
		scope: {
			info: '=',
			values: '=',
			refresh: '&'
		},
		controller:function($scope) {
			$scope.has_error = true;
			$scope.errors = [];

			$scope.add_activity = function(name) {
				$scope.has_error = false;
				check_add_input();
				if(!$scope.has_error) {
					var dataObj = {username: name, time: $scope.activity_time, activity: $scope.activity_name, details: $scope.activity_details};
					post_data('api/v1/activities', dataObj, add_success(name), add_fail);
				}
			};

			$scope.remove_add_activity = function() {
				$scope.activity_time = "";
				$scope.activity_name = "";
				$scope.activity_details = "";
				$scope.errors = [];
				$scope.has_error = false;
			};

			function post_data(url, dataObj, function1, function2){
				$http.post(url, dataObj).then(function1, function2);
			}

			function check_add_input() {
				$scope.errors = [];
				if(!$scope.activity_time) {
					$scope.has_error = true;
					$scope.errors.push("Need to include date and time");
				}
				if(!$scope.activity_name) {
					$scope.has_error = true;
					$scope.errors.push("Need to include the activity name");
				}
			}

			function add_success(name) {
				$scope.remove_add_activity(name);
				// added next line later because would not update in browser use
				//window.location = "/";
			}

			function add_fail(response) {
				$scope.add_input_incorrect = true;
				$scope.errors = response.data["errors"];
			}

		},
		templateUrl: 'static/javascript/directives/userSchedule.html',
		link: function(scope, element, attrs) {
		}
	};
}]);