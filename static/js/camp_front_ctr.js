


myapp.controller('campsCtr',function($scope,$http,$filter){
	$scope.readys = [];
	$scope.imgdesk = '';
	$scope.cats = [];
	$scope.pages = [];
	$scope.page = 1;
	$scope.filtro;
	$scope.orden = "id";
	$scope.noseve = null;
	$scope.destacados = null;
	$scope.destacado = true;

	$scope.getpends = function(){
		$scope.noseve = null;

		var http_params = {
			url:'/listcampanyas/',
			method:'get',
			params:{'cats':$scope.cats,
					'page':$scope.page,
					'orden':$scope.orden,
					'filtro':$scope.filtro,
					'destacado':$scope.destacado
				}
		};
	    $http(http_params).then(function(response){
	    	$scope.pages = [];
	    	
	    	$scope.readys = response.data.readys;

	        if(response.data.readys<1)
	        	$scope.noseve = true;


	    	for(p=0;p<response.data.pages;p++){
	    		$scope.pages.push(p+1);
	    	}

	    });
	}

	$scope.getpends();


	$scope.reordena = function(){
		console.log(this);
	}


	$scope.filtra = function(typofile){

		if(typofile.length<1)
			$scope.destacado = null;
		$scope.filtro = typofile;
		$scope.destacado = null;
		
		$scope.getpends();
	}


	$scope.openbox = function(r){

		$scope.imgdesk = r.desktop;
		inx = r.typofile.indexOf('image');

		hrefdw = '/dw/?f='+r.original;

		if(inx<0)
		jsplayer.src({ type: "video/mp4", src:r.original});


		values = $('#ats_'+r.pk).html();
		console.log(r.pk,values);

		$('#'+r.datatarget).modal('show');

		$('#titboxv').html(r.titulo);
		$('#btndown').attr('href',hrefdw);
		$('#titboxvideo').html(r.titulo);
		$('#btndown_video').attr('href',hrefdw);

		$('#descargaslinks_'+r.datatarget).html(values);


	}


	$scope.pager = function(p){
		
		$scope.page = p;
		$scope.getpends();
	}






$scope.prevp = function(){

	
	if($scope.page>1){
		$scope.page--;
		$scope.getpends();
	}
}



$scope.nextp = function(){

	
	if($scope.page<$scope.pages.length){
		$scope.page++;
		$scope.getpends();
	}
}



$scope.destacados = function(){
	$scope.destacado = true;
	$scope.filtro = null;
	$scope.getpends();

}

});
