  function toastr(cla,msgs){
  	$('#toastrto').addClass(cla).fadeIn(600).delay(1500).fadeOut(500);
  	$('#toastrto .msg').html(msgs);
  }


  function gohome(){
  	window.location = "/admon/";

  }


function reg_success(response)
{
	toastr('success',response.msg);
	//location.reload();
	window.location = response.liga;
}

function reg_success_user(response)
{
	toastr('success',response.msg);
	//location.reload();
	window.location = '/admin/users/';
}

function sendit(e){
	
	//var data = $(this).serializeArray();
	 toastr('warning','La información se esta procesando espere porfavor ...');
	var url = $(this).attr('action');
	var type = $(this).attr('method');
	forma = $(this).get(0);
	//forma = $('#empresaspt1').get(0);
	
	var data = new FormData(forma);
	$.ajax({url:url,
			type:type,
			data:data,
			cache: false,
	        processData: false,
	        contentType:false,
    	    dataType: 'json',
			success:function(response){
				$('.errr').removeClass('errr');
				$('.alert').remove();
				if(response.errors){
					toastr('warning',response.msg);
					$.each(response.errors,function(err,i){
					$('#id_'+err).addClass('errr').after('<div  class="id_'+err+' alert " rol="alert"><i class="glyphicon glyphicon-fire"></i>   '+i+'</div>');
					$('.errr').change(function(){
						$('.id_'+err+'').remove();
					});

					});
					
					$('.errr:first').focus();

				}
				if(response.saved=='ok'){
					if(response.callback){
						if(typeof(window[response.callback])=='function'){
							window[response.callback](response.datos);
						}
					}

				}
			}

	});

	return false;

}


function Executor(que,conque){
	console.log(que);
	if(typeof(window[que])=='function'){
		window[que](conque);
	}	
}