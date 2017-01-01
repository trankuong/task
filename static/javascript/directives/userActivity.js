app.directive('userActivity', ['$http', function($http) {
	return {
		restrict: 'E',
		scope: {
			username: '=',
			activity: '='
		},
		controller:function($scope) {
			$scope.has_error = false;
			$scope.errors = [];
			$scope.check = "hi";

			$scope.activity_name =  $scope.activity.activity;
			$scope.activity_detail =  $scope.activity.details;

			$scope.update_activity = function(id) {
				clear_errors();
				check_update_input();
				if(!$scope.has_error) {
					var dataObj = {activityid: id, username: $scope.username, time: $scope.activity_time, activity: $scope.activity_name, details: $scope.activity_detail};
					put_data('api/v1/activities', dataObj, update_success, update_fail);
				}
			};

			$scope.delete_activity = function(id) {
				$scope.has_error = false;
				$scope.errors = [];
				var dataObj = {activityid: id.toString()};
				delete_data('api/v1/activities', dataObj, delete_success, delete_fail);
			};

			$scope.remove_update_activity = function() {
				clear_errors();
			};

			function clear_errors() {
				$scope.has_error = false;
				$scope.errors = [];
			}

			function put_data(url, dataObj, function1, function2){
				$http.put(url, dataObj).then(function1, function2);
			}

			function check_update_input() {
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

			function update_success(response) {
				$scope.showUpdate = false;
				$scope.activity.time = response.data.result;
				$scope.activity.activity = $scope.activity_name;
				$scope.activity.details = $scope.activity_detail;
			}

			function update_fail(response) {
				$scope.has_error = true;
				$scope.errors = response.data["errors"];
			}

			function delete_data(url, dataObj, function1, function2) {
				$http.delete(url, {params: dataObj}).then(function1, function2);
			}

			function delete_success(response) {
				$scope.errors = [];
				$scope.has_error = false;
			}

			function delete_fail(response) {
				$scope.delete_input_incorrect = true;
				$scope.errors = response.data["errors"];
			}

		},
		templateUrl: 'static/javascript/directives/userActivity.html',
		link: function(scope, element, attrs) {
		}
	};
}]);




