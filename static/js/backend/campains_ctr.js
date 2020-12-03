
angular.module("mainApp").directive('filterCats', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
    	console.log(scope,'a');
 		
 		elm.load(function(){
 			console.log(scope);
 		});

    }
  };

}]);






angular.module("mainApp").directive('destacaMe', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
    	elm.click(function(e){

        	if(elm.is(':checked')){

				var http_params = {
					url:'/campains/destaca/',
					method:'get',
					params:{'pk':scope.r.pk,'des':'des'}
				};

        	}
        	else{
				var http_params = {
					url:'/campains/destaca/',
					method:'get',
					params:{'pk':scope.r.pk}
				};


        		
        	}


		    $http(http_params).then(function(response){
		    	toastr('success','Datos guardados con éxito');
		    	

		    });



    	});
 		


    }
  };

}]);






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




angular.module("mainApp").directive('catbySelect', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.change(function(e){
        	
        	console.log(scope,elm.val());
        	scope.$parent.catbyselect(scope.$parent.editando,elm.val());

        });        
    }
  };

}]);







angular.module("mainApp").directive('marcaMisCats', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

		console.log(scope.$parent.editando);        


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




myapp.controller('campsCtr',function($scope,$http,$filter){
    


	//$scope.pendings = [];
	$scope.readys = [];
	//$scope.videos = [];
	$scope.editando = {};
	$scope.punto = 0;
	$scope.grupoedicion = [];
	$scope.cats = [];
	$scope.groupcats = [];
	$scope.noseve = null;
	$scope.pendientes = 0;
	$scope.username = null;
	$scope.meses = [	
	{mes:'Enero',num:1},
        {mes:'Febrero',num:2},
        {mes:'Marzo',num:3},
        {mes:'Abril',num:4},
        {mes:'Mayo',num:5},
        {mes:'Junio',num:6},
        {mes:'Julio',num:7},
        {mes:'Agosto',num:8},
        {mes:'Septiembre',num:9},
        {mes:'Octubre',num:10},
        {mes:'Noviembre',num:11},
        {mes:'Diciembre',num:12},
	];

	var cur_year = new Date().getFullYear();
	first_year = cur_year - 4;
        $scope.years = [];
	for (i = first_year; i < cur_year+5; i++) {
  		$scope.years.push(i);
	}

		var http_params = {
			url:'/campains/cats/',
			method:'get'
		};

	    $http(http_params).then(function(response){
	    	
	        //$scope.pendings = response.data.pens;
	        $scope.cats = response.data.cats;
	        //$scope.videos = response.data.videos;
	    });



$scope.filtrando = function(targetblank,mycats){
			var filtered;
			var valores;
			angular.forEach(targetblank,function(v,k){
				valores = v.valu;
				filtered = v.valu.filter(
				    function(e) {
				      return this.indexOf(e) < 0;
				    },
				    mycats
				);
				angular.forEach(filtered,function(v,k){
					vax = v;
					inx = valores.indexOf(vax);
					valores.splice(inx,1);					
				});
				$('#cat_by_'+v.pk).val(valores[0]);

            });


}




	$scope.getpends = function(){
		$scope.noseve = null;
		


		var http_params = {
			url:'/campains/getpendings/',
			method:'get'
		};

	    $http(http_params).then(function(response){

	    	$scope.pendientes = response.data.pends;
	    	$scope.username = response.data.user;

	        $scope.readys = response.data.readys;
	        if(response.data.readys<1)
	        	$scope.noseve = true;
	    });
	}




	$scope.savesingle = function(){
		data = $('#editandoform').serializeArray();
		data = $.param(data);
		var http_params = {
			url:'/campains/savesingle/',
			method:'POST',
			data:data
		};
	    $http(http_params).then(function(response){
	    	$('#lightbox').modal('hide');
	    });
	}


	$scope.edtopen = function(pkedt){
		$scope.editando = {};
		$scope.punto = this.$index;
		var http_params = {
			url:'/campains/edtsingle/',
			method:'get',
			params:{'pk':pkedt}
		};
	    $http(http_params).then(function(response){
	    	$scope.editando = response.data.pens;
	    	$scope.filtrando(response.data.pens.allcats,response.data.pens.cats);
			if($scope.editando.typofile){
				inx = $scope.editando.typofile.indexOf('video');
				if(inx==-1){
					bol=true;
				}
				else{
				jsplayer.src({ type: "video/mp4", src:'/'+$scope.editando.original});
				}
			}
	    });
	}


	$scope.nextit = function(){
		if($scope.punto<$scope.readys.length-1){
			$('#editandobox').hide().before('<div class="cargando">Cargando, espere porfavor...</div>');
			$scope.punto++;
		}
		edits = $scope.readys[$scope.punto];
		var http_params = {
			url:'/campains/edtsingle/',
			method:'get',
			params:{'pk':edits.pk}
		};
	    $http(http_params).then(function(response){
	    	$scope.editando = response.data.pens;
	    	$('#editandobox').show(100);
	    	$('.cargando').remove();
			$scope.filtrando(response.data.pens.allcats,response.data.pens.cats);
	    });
	}

	$scope.beforeit = function(){
		if($scope.punto>0){
			$('#editandobox').hide().before('<div class="cargando">Cargando, espere porfavor...</div>');
			$scope.punto--;
			edits = $scope.readys[$scope.punto];
			var http_params = {
				url:'/campains/edtsingle/',
				method:'get',
				params:{'pk':edits.pk}
			};
		    $http(http_params).then(function(response){
		    	$scope.editando = response.data.pens;
		    	$('#editandobox').show(100);
		    	$('.cargando').remove();
		    	$scope.filtrando(response.data.pens.allcats,response.data.pens.cats);
		    });
		}
	}

	
	$scope.checartodos=function(){
		$('.checkar').click();
	}

	$scope.getpends();
	function myTimer() {
	  var d = new Date();
	  document.getElementById("demo").innerHTML = d.toLocaleTimeString();
	}

	$scope.delsingle = function(pkedt){

		if(confirm('Este elemento se elimiara permanente mente, ¿está seguro de realizar est aacción?')){
			$('#'+pkedt+'_item').remove();
			$scope.editando = {};
			$scope.readys.splice(this.$index,1);
			var http_params = {
				url:'/campains/delsingle/',
				method:'get',
				params:{'pk':pkedt}
			};
		    $http(http_params).then(function(response){
		    	removedis=null;
		    });
		}
	}


	$scope.addtocats = function(){
		if(this.$parent.editando.cats)
			inx = this.$parent.editando.cats.indexOf(this.c.pk);
		var accion = null;
		if(inx>=0){
			this.$parent.editando.cats.splice(inx,1);
			accion = 'remove';
		}
		else{
			accion = 'add';
		}

			este = this;
			var http_params = {
				url:'/campains/addtocats/',
				method:'get',
				params:{'pk':this.c.pk,'cpk':this.$parent.editando.pk,'action':accion}
			};

		    $http(http_params).then(function(response){
		    	//toastr('success','Se agregó con éxito');
		    	if(accion=='add')
		    	$scope.editando.cats.unshift(este.c.pk);

		    });
		

	}



	$scope.checkcats = function(){
		if(this.$parent.editando.cats){
			inx = this.$parent.editando.cats.indexOf(this.c.pk);
		}
		else{
			inx = -1;
		}
		if(inx>=0)
			return true;
		return false;
	}




	$scope.addtocatgrupo = function(){
		if(this.$parent.groupcats)
			inx = this.$parent.groupcats.indexOf(this.c.pk);
		var accion = null;
		if(inx>=0){
			this.$parent.groupcats.splice(inx,1);
		}
		else{
			this.$parent.groupcats.unshift(this.c.pk);
		}
	}



	$scope.checkcatsgroup = function(){
		if(this.$parent.groupcats){
			inx = this.$parent.groupcats.indexOf(this.c.pk);
		}
		else{
			inx = -1;
		}
		if(inx>=0)
			return true;
		return false;
	}



	$scope.saveall = function(){

		var http_params = {
			url:'/campains/saveall/',
			method:'get'
		};

	    $http(http_params).then(function(response){
	        $scope.cats = response.data.cats;
	    });


		toastr('success','Se publicó con exito con éxito');

	}



	$scope.showimg = function(){


		if($scope.editando.typofile){

			inx = $scope.editando.typofile.indexOf('image');

			

			if(inx==-1)
				return false;
			else
				return true;

		}



	}


	$scope.showvideo = function(){
		if($scope.editando.typofile){
			inx = $scope.editando.typofile.indexOf('video');
			if(inx==-1){
				return false;
			}
			else{
				return true;
			}

		}

	}







		$scope.catbyselect = function(editando,pk){

			inx = editando.cats.indexOf(pk);		
			var accion = null;
			if(inx>=0){
				editando.cats.splice(inx,1);
				accion = 'remove';

			}
			else{
				accion = 'add';
			}

				este = this;
				var http_params = {
					url:'/campains/addtocats/',
					method:'get',
					params:{'pk':pk,'cpk':editando.pk,'action':accion}
				};

				/*
				console.log(http_params);
				return false;

			    $http(http_params).then(function(response){
			    	//toastr('success','Se agregó con éxito');
			    	if(accion=='add')
			    	editando.cats.unshift(este.c.pk);

			    });
			    */
			

		}



		


});
