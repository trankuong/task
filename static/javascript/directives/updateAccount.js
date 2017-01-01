app.directive('updateAccount', ['$http', function($http) {
	return {
		restrict: 'E',
		scope: {
		},
		controller: function($scope) {

			//$scope.updated = false;
			$scope.has_error = false;
			$scope.errors = [];

			$scope.email = "";
			$scope.firstname = "";
			$scope.lastname = "";
			$scope.password1 = "";
			$scope.password2 = "";

			$scope.update = function() {
				$scope.updated = false;
				var dataObj = {
					email: String($scope.email),
					firstname: String($scope.firstname),
					lastname: String($scope.lastname),
					password1: String($scope.password1),
					password2: String($scope.password2)
				};
				put_data('api/v1/user', dataObj, update_success, update_fail);
			}

			function put_data(url, dataObj, function1, function2){
				$http.put(url, dataObj).then(function1, function2);
			}

			function update_success() {
				$scope.updated = true;
				$scope.has_error = false;
				$scope.errors = [];
				setTimeout(load, 1000);
			}

			function update_fail(response) {
				$scope.has_error = true;
				$scope.errors = response.data['errors'];
			}

			function load() {
				window.location = "/edit";
			}

		},
		templateUrl: 'static/javascript/directives/updateAccount.html',
		link: function(scope, element, attrs) {
		}
	};
}]);