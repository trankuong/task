app.directive('createAccount', ['$http', function($http) {
	return {
		restrict: 'E',
		scope: {
		},
		controller: function($scope) {

			$scope.has_error = false;
			$scope.errors = [];

			$scope.username = "";
			$scope.email = "";
			$scope.firstname = "";
			$scope.lastname = "";
			$scope.password1 = "";
			$scope.password2 = "";

			$scope.create = function() {
				var dataObj = {
					username: String($scope.username),
					email: String($scope.email),
					firstname: String($scope.firstname),
					lastname: String($scope.lastname),
					password1: String($scope.password1),
					password2: String($scope.password2)
				};
				post_data('api/v1/user', dataObj, create_success, create_fail);
			};

			function post_data(url, dataObj, function1, function2){
				$http.post(url, dataObj).then(function1, function2);
			}

			function create_success() {
				$scope.has_error = false;
				$scope.errors = [];
				window.location = '/login';
			}

			function create_fail(response) {
				$scope.has_error = true;
				$scope.errors = response.data['errors'];
			}

		},
		templateUrl: 'static/javascript/directives/createAccount.html',
		link: function(scope, element, attrs) {
		}
	};
}]);