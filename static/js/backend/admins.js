var myapp = angular.module('mainApp',['ngRoute',
                                      'ngImgCrop',
                                      'textAngular',
                                      'youtube-embed'
                                      ]);

var customInterpolationApp = angular.module('customInterpolationApp', []);
myapp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('||');
    $interpolateProvider.endSymbol('||');
});

myapp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';        
}]);
