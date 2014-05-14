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

document.addEventListener('DOMContentLoaded', function(event) {
    $.get(
        '/ready'
    );
    /*
    setTimeout(function () {
        $('#app-logo').animate({opacity: 0}, 500, 'linear');
        $('#app-info').animate({opacity: 0}, 500, 'linear');
        $('.spinner').animate({borderRadius: 0, padding: 0, width: '100%', height: '100%'}, 1000, 'linear');
        $('.spinner div').animate({marginLeft: 256, marginRight: 256, opacity: 0}, 1000, 'linear');
        $('.spinner .container').animate({marginTop: 512, opacity: 0}, 1000, 'linear', function () {

        });
    }, 3000); */
});
