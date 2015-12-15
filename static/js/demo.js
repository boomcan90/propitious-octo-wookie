(function() {
    angular.module('app', []);
    AppController.$inject = [
        '$scope',
        '$http'
    ];
    angular.module('app').controller('MasterController', AppController);
    angular.module('app').config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }]);

    function AppController($scope, $http) {
        $scope.restartGame = function() {
            $http.get("https://intense-caverns-6032.herokuapp.com/restartgame").then(function(result) {
                console.log(result)
            }, function(result) {
                console.log(result)
            });
        }
    };
})();
