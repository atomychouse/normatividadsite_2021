
myapp.controller('usersCtr',function($scope,$http){
    $scope.users = [{first_name:'cholo'}];

/*

    $scope.addSec = function(event,item){
        event.preventDefault();
        $scope.sections.push({'sec_name':'Undefined','rows':[
                                {'onerow':'',
                                 'cols':[{'col_name':'COL UNDEFINED',
                                 'secs':[{'sec_name':'Undefined sec'}]
                                  }]
                                }]
                            });
    }

    $scope.additem = function(event,item,cual){
        event.preventDefault();
        console.log(item);
        if(cual=='rows')
            item.cols.push({'col_name':'MATATA'});
        else if(cual=='sb')
            item.secs.push({'sec_name':'Hakuna'});
    }

    $scope.edit = 0;
    
    $scope.changeOrEdit = function(event,item){
        event.preventDefault();
        
        $scope.edit++;
        
        window.setTimeout(function(){
            console.log($scope.edit);
            if($scope.edit==1){
                //item.editor=true;        
                window.location='/admin/config/'+item.pk;
            }
            else{
                item.editor=true;
            }
            $scope.edit = 0;
        }, 500);

    }
    
    $scope.chows = function(event,elemento,quehago){
        event.preventDefault();
        elemento.shows = quehago;
    }



    $scope.saver = function(event,elemento){
        event.preventDefault();
        elemento.editor = false;
        uri = "/admin/addsec";
        data = {pk:elemento.pk,
                sec_name:elemento.sec_name

        };

        $http({url:uri,method:'GET',params:data}).then(function(response){
            if(response.acts=='True'){
                toastr('success',response.msg);
            }
        });


    }



    $scope.saveCol = function(event,elemento){

        event.preventDefault();

        elemento.editor = false;
        uri = "/admin/addcol";
        data = {pk:elemento.cpk,
                col_name:elemento.col_name

        };

        $http({url:uri,method:'GET',params:data}).then(function(response){
            if(response.acts=='True'){
                toastr('success',response.msg);
            }
        });


    }
*/
});