'use strict';


// Declare app level module which depends on filters, and services
angular.module('ka', [
  'ngRoute',
  'ka.filters',
  'ka.services',
  'ka.directives',
  'ka.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: 'MovieCtrl'});
  $routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: 'MyCtrl2'});
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);

document.oncontextmenu = function (evt) {
    evt.preventDefault();
}
