(function() {
    angular.module('app', []);
    AppController.$inject = [
        '$scope',
        '$http'
    ];
    angular.module('app').controller('AppController', AppController);
    angular.module('app').config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }]);

    function AppController($scope, $http) {
        $scope.stuff = "sfafd";
        $scope.tile1 = {
            name: "raptor_zombie",
            deviceToken: "210039000347343337373737",
            value: "1"
        }
        $scope.tile2 = {
            name: "dentist_lawyer",
            deviceToken: "37001c001347343432313031",
            value: "2"
        }
        $scope.tile3 = {
            name: "pirate_bobcat",
            deviceToken: "250040000347343337373737",
            value: "3"
        }

        $scope.getPositions = function() {
            $http.get('https://api.particle.io/v1/devices/' + $scope.tile1.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a').then(function(result) {
                console.log(result)
            }, function(result) {
                console.log(result)
            });
            $http.get('https://api.particle.io/v1/devices/' + $scope.tile2.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a').then(function(result) {
                console.log(result)
            }, function(result) {});
            $http.get('https://api.particle.io/v1/devices/' + $scope.tile3.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a').then(function(result) {
                console.log(result)
            }, function(result) {
                console.log(result)
            });
        };

        $scope.changeTileDisplays = function() {

            $http.post('https://api.particle.io/v1/devices/' + $scope.tile1.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a', {
                "args": $scope.tile1.value
            }).then(function(result) {
                console.log(result)
            }, function(result) {
                console.log(result)
            });
            $http.post('https://api.particle.io/v1/devices/' + $scope.tile2.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a', {
                "args": $scope.tile2.value
            }).then(function(result) {
                console.log(result)
            }, function(result) {
                console.log(result)
            });
            $http.post('https://api.particle.io/v1/devices/' + $scope.tile3.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a', {
                "args": $scope.tile3.value
            }).then(function(result) {
                console.log(result)
            }, function(result) {
                console.log(result)
            });
            // $http.post('https://api.particle.io/v1/devices/' + $scope.tile1.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a', {"args":"1"}).then(function(result) {
            //     console.log(result)
            // }, function(result) {
            //     console.log(result)
            // });
            // https://api.particle.io/v1/devices/37001c001347343432313031/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a
            // https://api.particle.io/v1/devices/37001c001347343432313031/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a
            // $http.post('https://api.particle.io/v1/devices/' + $scope.tile2.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a', {
            //     "args": "2"
            // }).then(function(result) {
            //     console.log(result)
            // }, function(result) {});
            // $http.post('https://api.particle.io/v1/devices/' + $scope.tile3.deviceToken + '/tile?access_token=5fdaa0f2dc84764338a30bebe5d695bbdd458c8a', {
            //     "args": "3"
            // }).then(function(result) {
            //     console.log(result)
            // }, function(result) {
            //     console.log(result)
            // });
        };
    }
})();
