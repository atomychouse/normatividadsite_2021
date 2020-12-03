myapp.controller('secAxCtr',function($scope,$http){

	/*SLAYING SECION*/
	$scope.slayer_sec = function(event,item){
		event.preventDefault();

		if(confirm('¿Esta seguro que desea borrar la sección?')){
		data = {
			'pku':item,
			'step':'1'
		};
		data['csrfmiddlewaretoken'] = tk;
		data = $.param(data);
	    uri = '/admon/remover/';
	    $http({url:uri,method:'POST',data:data}).then(function(response){
	          
	            swal("La sección se eliminó con éxito. (:");
	            window.location = "/admon/";          
	    });
		}
	};

});

myapp.controller('insideCtr',function($scope,$http){

	$scope.rows = initialrows;
	$scope.initer = 1;
	defaultrow = {'rowpk':'',
						 'orden':'',
						 'cat_name':'category name',
						'cols':[{'sec_name':'Section Name','sections':[]}]
					};

	// PArA AGREGAR UN RENGLON AL MENU DE SECCION
	$scope.cat_addrow = function(elem){
		defaultrow = {'rowpk':'',
					  'secpk':sectionpk,
					  'orden':'',
					  'cat_name':'category name',
					  'cols':[{'col_name':'Section Name','sections':[]}]
				};
		
		$scope.rows.push(defaultrow);
		defaultrow.orden = $scope.rows.indexOf(defaultrow);
		defaultrow.step = 3;
		
		datap = {};
		datap['csrfmiddlewaretoken'] = tk;
		datap['step']=3;
		datap['secpk']=defaultrow.secpk;
		datap['orden']=defaultrow.orden;
	    data = $.param(datap);
	    uri = '/admon/savior/';
	    $http({url:uri,method:'POST',data:data}).then(function(response){
	          if(response.data.saved=='ok'){
	            swal("Here's a message!");
	            defaultrow.rowpk=response.data.pk;
	          }   
	    });
	}





	$scope.slayrow = function(event,row){
		event.preventDefault();
		ind = $scope.rows.indexOf(row);
		$scope.rows.splice(ind,1);
		data = {
			'pku':row.rowpk,
			'step':'2'
		};
		data['csrfmiddlewaretoken'] = tk;
		data = $.param(data);
	    uri = '/admon/remover/';
	    $http({url:uri,method:'POST',data:data}).then(function(response){
	            swal("El renglon se eliminó con éxito. (:");
	                    
	    });
	};		

	

	$scope.savecol = function(elem,row){
		elem.preventDefault();
		data = {rowpk:row.row.rowpk,col_name:row.col.col_name,step:4,pkid:row.col.pk};
		data['csrfmiddlewaretoken'] = tk;
		data['orden']=row.row.cols.indexOf(row.col);
		data = $.param(data);
	    uri = '/admon/savior/';
	    $http({url:uri,method:'POST',data:data}).then(function(response){
	          if(response.data.saved=='ok'){
	            swal("Categoria Renombrada con éxito. (:");
	            row.col.pk=response.data.pk;
	          }
	          
	    });
	}



	$scope.slaycol = function(event,elem){
		event.preventDefault();
		ind = elem.row.cols.indexOf(elem.col);
		elem.row.cols.splice(ind,1);
		data = {
			'pku':elem.col.pk,
			'step':'3'
		};
		data['csrfmiddlewaretoken'] = tk;
		data = $.param(data);
	    uri = '/admon/remover/';
	    $http({url:uri,method:'POST',data:data}).then(function(response){
	            swal("La columna se eliminó con éxito. (:");
	                    
	    });
	};		


	$scope.savesec = function(event,elem){
		event.preventDefault();
		data = {
			'pkid':elem.sec.pk,
			'parent':sectionpk,
			'sec_colum_menu':elem.col.pk,
			'sec_name':elem.sec.sec_name,
			'step':'0'
		};
		data['csrfmiddlewaretoken'] = tk;
		data['orden']=elem.row.cols.indexOf(elem.col);
		data = $.param(data);
	    uri = '/admon/savior/';

	    $http({url:uri,method:'POST',data:data}).then(function(response){
	          if(response.data.saved=='ok'){
	            swal("Categoria Renombrada con éxito. (:");
	            elem.sec.pk=response.data.pk;
	          }
	          
	    });
	}



	$scope.cat_addcol = function(elem){
		console.log('add Columns');
		elem.row.cols.push({'sec_list':'Section LIST',
		              		'sections':[{'sec_name':'SECTION'}]
		              		});
	}


	$scope.cat_addsec = function(event,elem){
		event.preventDefault();
		console.log(elem);
		elem.col.sections.push({'sec_name':'SECTION'});
	}




});