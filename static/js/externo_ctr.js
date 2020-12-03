



myapp.controller('externoCtr',function($scope,$http,$filter){
    $scope.filex = [];
    $scope.externos = [];
    $scope.rowpk = $('#rowpkexterno').val();

    $scope.addfilefield = function(){
    	var newfile = {
    		name:'',
    		pk:0,
    		order:1
    	};
    	$scope.filex.unshift(newfile);
    	
    	
    }

    $scope.getexts = function(){

        var http_params = {
            url:'/admin/getexts/',
            method:'get',
            params:{'rowpk':$scope.$parent.item.pk}
        };

        $http(http_params).then(function(response){
            
            //$scope.pendings = response.data.pens;
            $scope.externos = response.data;
            //$scope.videos = response.data.videos;
        });

        

    }


    $scope.rmmodulo = function(){

        if(confirm('El elemento se eliminara permanentemene, ¿esta seguro que desea realizar esta acción?')){
        var http_params = {
            url:'/admin/rmmoduloexterno/',
            method:'get',
            params:{'pk':$scope.$parent.item.pk}
        };
        $http(http_params).then(function(response){
            //$scope.pendings = response.data.pens;
            echoo = true;
            window.location.replace(window.location.pathname);
            //$scope.videos = response.data.videos;
        });
    }
    }



    $scope.rmext = function(pk){
        if(confirm('El elemento se eliminara permanentemene, ¿esta seguro que desea realizar esta acción?')){
        var http_params = {
            url:'/admin/rmexterno/',
            method:'get',
            params:{'pk':pk}
        };
        $http(http_params).then(function(response){
            $scope.getexts();
        });

    }

    }



    $scope.getexts();


});