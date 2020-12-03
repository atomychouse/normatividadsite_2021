
angular.module("mainApp").directive('checGrupo', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){
        	
        	var yo = elm.val();
        	inx = scope.$parent.grupoedicion.indexOf(yo);
        	if(elm.is(':checked')){
        		scope.$parent.grupoedicion.unshift(yo);
        	}
        	else{
        		scope.$parent.grupoedicion.splice(inx,1);
        	}
        	try{
        	scope.$apply();
        	}
        	catch(err){
        		noerror = null;
        	}
        });        
    }
  };

}]);




angular.module("mainApp").directive('rmGrupo', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){
        	

        	if($('[name="keyg[]"]').length>0){


				angular.forEach(scope.grupoedicion, function(value, key) {
				  

				        visibles = scope.readys.filter(function (elm) {
				            if(elm.pk==value){
				            	inx = scope.readys.indexOf(elm);
				            	scope.readys.splice(inx,1);
				            	scope.$apply();
				            }
				            return (elm.visible ==='1');
				        });



				});


			    if(confirm('La información se borrara permanentemente, ¿esta seguro de realizar esta acción?')){
			      $('#rmgrupo').submit();
			    }

			}
			else{
				alert('Seleccione algunos elemenytos de la lista');
			}

        	
        });        
    }
  };

}]);




myapp.controller('catsCtr',function($scope,$http,$filter){
   


	$scope.cats = [];
	$scope.newcatname = '';
	$scope.newsubc = '';
	$scope.portada = null;
	
	$scope.reloadcats = function(){

		var http_params = {
			url:'/admin/catlist/',
			method:'get'
		};

	    $http(http_params).then(function(response){
	        $scope.cats = response.data.cats;
	    });


	}


	$scope.reloadcats();


    $scope.addcat = function(){
    	if($scope.newcatname.length>2){
    		data = {
				'catname':$scope.newcatname
    		};
    		data = $.param(data);
			var http_params = {
				url:'/admin/addcampaincat/',
				method:'post',
				data:data
			};
		    $http(http_params).then(function(response){
		        $scope.reloadcats();
		        toastr('success','Información guardada con éxito');
		    });
    	}
    	else{
    		toastr('warning','El nombre d ela categoría es incorrecto');
    	}
    }



    $scope.addsub = function(){


    	if(this.newsubc.length>2){
	    	var data = {
					'catname':this.newsubc,
					'parentcat':this.c.pk

			};
			data = $.param(data);
			var http_params = {
				url:'/admin/addcampaincat/',
				method:'post',
				data:data
			};
		    $http(http_params).then(function(response){
		        $scope.reloadcats();
		        
		        toastr('success','Información guardada con éxito');
		    });

		}
		else{
			toastr('warning','El nombre d ela categoría es incorrecto');
		}

    }



    $scope.kicat = function(){

	    	var data = {
					'pk':this.c.pk

			};
			data = $.param(data);
			var http_params = {
				url:'/admin/rmcampaincat/',
				method:'post',
				data:data
			};
		    $http(http_params).then(function(response){
		        $scope.reloadcats();		        
		        toastr('success','Se eliminó con éxito');
		    });    	

    }



    $scope.subkicat = function(){

	    	var data = {
					'pk':this.sc.pk

			};
			data = $.param(data);
			var http_params = {
				url:'/admin/rmcampaincat/',
				method:'post',
				data:data
			};
		    $http(http_params).then(function(response){
		        $scope.reloadcats();		        
		        toastr('success','Se eliminó con éxito');
		    });    	

    }



});