myapp.config(['$routeProvider', '$compileProvider', function ($routeProvider, $compileProvider) {
      $routeProvider
        .when('/intern', {
          controller: 'configCtr',
          templateUrl: '/static/views/intern.html'
        })
        .when('/links', {
          controller: 'configCtr',
          templateUrl: '/static/views/links.html'
        })
        .when('/homepage', {
          controller: 'homeCtr',
          templateUrl: '/static/views/homepage.html'
        })
        .otherwise({
          controller: 'treeCtr',
          templateUrl: '/static/frontviews/links.html'
   		});
        

      // testing issue #521
      $compileProvider.debugInfoEnabled(false);
    }]);
