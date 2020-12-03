

var options = [];

$(document).ready(function(){


var UIConfirmations = function () {

    var handleSample = function () {

        $('.pagas').on('confirmed.bs.confirmation', function () {
          t = $('[name="csrfmiddlewaretoken"]').val();
            victim = $(this).attr('data-v');
            data = {'k':'1','pk':victim.replace('id_',''),'csrfmiddlewaretoken':t};
            
            $.ajax({url:'/manager/'+layoutpost+'/',
                    type:'post',
                    data:data,
                    success:function(rdata){
                      console.log(rdata);
                    }
            });
            $(this).parents('tr:first').remove();

        });

        
        $('#bs_confirmation_demo_x').on('confirmed.bs.confirmation', function () {
            alert('You confirmed action #1');
        });

        $('#bs_confirmation_demo_x').on('canceled.bs.confirmation', function () {
            alert('You canceled action #1');
        });   

    }


    return {
        //main function to initiate the module
        init: function () {

           handleSample();

        }

    };

}();

jQuery(document).ready(function() {    
   UIConfirmations.init();
});


});
