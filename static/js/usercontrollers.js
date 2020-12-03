myapp.controller('userCtr',function($scope,$http){

	$scope.userprofile=true;
	$scope.perms = false;
	$scope.list = null;
	$scope.user_sections = permisos;
            $http.get("/allsections/").then(function(response){
                $scope.list = response.data;
            });


    $scope.adding = function(idx){
    var searchinx = $scope.user_sections.indexOf(idx);

    // is currently selected
    if (searchinx > -1) {
      $scope.user_sections.splice(searchinx, 1);
    }

    // is newly selected
    else {
      $scope.user_sections.push(idx);
    }

    }


    $scope.toggleSelection = function toggleSelection(elem) {
    	$scope.adding(elem);
  };

  $scope.checkall = function(col){
  	angular.forEach(col.secs, function(value, key){
		$scope.adding(value.pk);
	});
  }

  $scope.checkallsec = function(event,sec){
    event.preventDefault();
    console.log(sec.pk);
  	$scope.adding(sec.pk);
  	angular.forEach(sec.cols, function(cvalue, ckey){
  		$scope.checkall(cvalue);

  	});
  }


  $scope.checkallofall = function(event,secs){
    event.preventDefault();    
    angular.forEach(secs,function(s,sk){
      $scope.adding(s.pk);
      angular.forEach(s.cols,function(col,colk){
        $scope.checkall(col);

      });


    });

    

  }




  $scope.uncheckall=function(){
  	$scope.user_sections = [];
  }


  $scope.saveperms = function(envet,elem)
  {
    data = {};

    if (gpk!='undefined'){
      data['csrfmiddlewaretoken']=csrf_token;
      data['gpk']=gpk;
      data['perms']=$scope.user_sections;
      data = $.param(data);
      uri = '/admin/saveuser/';
      $http({url:uri,method:'POST',data:data}).then(function(response){
            if(response.data.removed=='ok'){
              //toastr('success',response.data.msg);      
              //$scope.rowsSec.splice(elem.$index,1);    
            }
            
      });

    }
    
    else
    {
      toastr('warning','No se esta editando un usuario valido. :(');
    }
    
    



  }




});
