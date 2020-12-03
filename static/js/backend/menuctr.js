

$('[data-parente="'+sorpresa+'"] .daddy').addClass('activate');

// SECCION PARA MANEJAR EL REORDENAMIENTO DEL LISTADO


$('.sortable').nestedSortable({
    handle: 'div',
    items: 'li:not(.ui-state-disabled)',
    toleranceElement: '> div',
    maxLevels:'3',

    stop:function(event,ui) { 
        //console.log(ui);
        var papa = null;
        var columna = null;
        

        

        brodas = $(ui.item).siblings();
        brods = [];
        $.each(brodas,function(x,y){
            orden = $(y).index();
            pk = $(y).attr('data-pk');
            papa = $(y).attr('data-parent');
            columna = $(y).attr('data-columne');
            typo = $(y).attr('data-type');
            dato = pk+'|'+orden+'|'+typo;
            if(pk)
                brods.push(dato);

        });



        if(!columna){
            columna = $(ui.item).parents('li:first').attr('data-pk');
        }
        
        if(!papa || papa=='undefined'){
            papa = $(ui.item).parents('li:first').attr('data-parent');
        }
        
        if(!papa && $(ui.item).attr('data-type')=='col')
        return false;

        


        mypk = ui.item.attr('data-pk');
        myorden = ui.item.index();
        mypapa = papa;
        mycolumn = columna;
        mymodeli = ui.item.attr('data-type');
        updateme = {
            id:mypk,
            parent:mypapa,
            column:mycolumn,
            orden:myorden,
            updateme:1,
            mymodeli:mymodeli,
            pks:brods
        };
        myattrs = {
            'data-parent':papa,
            'id-parent':papa
        };
        ui.item.attr(myattrs);
        //console.log(updateme);
        $.ajax({url:'/admin/addsection/',type:'GET',
                data:updateme,
                dataType:'json',
                success:function(response){
                    if(response.fail)
                        clase = 'warning';
                    else
                        clase = 'success';
                     toastr(clase,response.msg);
                }
        });        
    }
});



$('.nombrele').click(function(e){
    url = '/admin/config/'+$(this).attr('data-go')+'/';
    window.location=url;

});

$('.nombrele').dblclick(function(e){
    alert('editar nombre');

});



//END MANAGER SORT





myapp.controller('menuMaster',function($scope,$http){
    $scope.secs = [];


    ruta = window.location.pathname;
    seleccionado = ruta.indexOf('config');
    ruta_pices = ruta.split('/');
    pieza = ruta_pices[ruta_pices.length-2];
    
    if(seleccionado>0)    
        uri = '/admin/section_list/?sel='+pieza;
    else
        uri = '/admin/section_list/';
    
    $http({url:uri,method:'GET'}).then(function(response){
        $scope.secs = response.data;
        
    });


    $http({url:'/admin/chlogo/',method:'GET'}).then(function(response){
        $scope.logofile = response.data.logo;
        
    });


    $scope.chower = function(s){
        if(s.page_type=='bancoimagen' || s.ishome==true)
            return false;
        else 
            return true;
    }


    $scope.addSec = function(event,item){
        orden = item.secs.length+1;
        event.preventDefault();
        $scope.secs.push({'sec_name':'Undefined',
                          'editor':true,
                          'orden':orden,
                          parent:null,
                          sec_colum_menu:null,
                          'rows':[
                                {'onerow':'',
                                 'cols':[{'col_name':'COLUMNA',
                                 'secs':[{'sec_name':'seccion'}]
                                  }]
                                }]
                            });
    }

    $scope.additem = function(event,item,secparent,cual){
        event.preventDefault();
        if(cual=='rows'){
            item.cols.push({'col_name':'Columna',
                               'parent':item.pk,
                               'opened':true,
                            'editor':true
            });
        }
        
        else if(cual=='sb'){
            if(!item.secs) item.secs = [];
            item.secs.push({'sec_name':'Seccion',
                             parent:secparent.pk,
                             opened:false,
                             sec_colum_menu:item.cpk,
                             editor:true
            });
        }
    }

    $scope.edit = 0;
    
    $scope.changeOrEdit = function(event,item){
        event.preventDefault();
        item.editor=true;

    }
    

    $scope.escondeme = function(elemento){
        //console.log(elemento.editor);

        if(!elemento.editor)
            return false;

        if(elemento.editor==true)
          return  true;
        else
          return false;
    }


    $scope.chows = function(event,elemento,quehago){
        event.preventDefault();
        
        if(elemento.pk){
            //console.log(elemento.pk);
            targets = elemento.pk;
            elementos = 'data-sonsof';    
        }
        else{
            //console.log(elemento.cpk);
            targets = elemento.cpk;
            elementos = 'data-sonsofc';
        }

        jQuery("["+elementos+"='"+targets+"']").toggle();
        elemento.shows = quehago;

    }




    $scope.otras = function(s){
        if(s.ishome==false && s.page_type!='bancoimagen')
            return true;
    }




    $scope.saver = function(event,elemento){
        event.preventDefault();
        elemento.editor = false;
        uri = "/admin/addsec";
        data = {pk:elemento.pk,
                sec_name:elemento.sec_name,
                orden:elemento.orden,
                parent:elemento.parent,
                sec_colum_menu:elemento.sec_colum_menu
        };

        $http({url:uri,method:'GET',params:data}).then(function(response){
            
            if(response.data.datos.pk>0){
                elemento.pk = response.data.datos.pk;
                elemento.sec_colum_menu = response.data.datos.sec_colum_menu;

                if(elemento.parent>0)
                    toastr('success',response.data.datos.msg);
                else
                    window.location.reload();
            }
        });


    }



    $scope.saveCol = function(event,elemento){

        event.preventDefault();

        elemento.editor = false;
        uri = "/admin/addcol";
        data = {pk:elemento.cpk,
                col_name:elemento.col_name,
                parent:elemento.parent
        };

        $http({url:uri,method:'GET',params:data}).then(function(response){
            if(response.data.datos.pk>0){
                elemento.cpk = response.data.datos.pk;

                toastr('success',response.data.msg);
            }
        });


    }


    $scope.chlogo = function() {

        jQuery('#logofile').click();
        
    };


    angular.element(jQuery('#logofile')).on('change',function(e){
      
      $scope.chlogoya(e);
    });




  $scope.slaye_colum = function(event,elem){
    event.preventDefault();
    ind = elem.s.cols.indexOf(elem.c);

    
    if(confirm('La columna y todas sus secciones seran eliminadas \\n ¿Desea continuar?')){
    
    if(elem.c.cpk){
      data = {'pku':elem.c.cpk};
      data['csrfmiddlewaretoken']=cfr;
      data['step']=3;
      data = $.param(data);
      uri = '/admin/remover/';

      $http({url:uri,method:'POST',data:data}).then(function(response){
            if(response.data.removed=='ok'){
              toastr('success',response.data.msg);      
              elem.s.cols.splice(ind,1);    
            }
            
      });
    }
    else{
      elem.s.cols.splice(ind,1);
      toastr('success','Se eliminio el pad de edición');
    }


  }

  }



  $scope.slaye_sec = function(event,elem){
    event.preventDefault();
    //console.log(elem);
    ind = elem.secs.indexOf(elem.s);
    if(confirm('La columna y todas sus secciones seran eliminadas \\n ¿Desea continuar?')){
    
    if(elem.s.pk){
      data = {'pku':elem.s.pk};
      data['csrfmiddlewaretoken']=cfr;
      data['step']=1;
      data = $.param(data);
      uri = '/admin/remover/';

      $http({url:uri,method:'POST',data:data}).then(function(response){
            if(response.data.removed=='ok'){
              toastr('success','Sección eliminada con éxito');      
              elem.secs.splice(ind,1);    
            }
            
      });
    }
    else{
      elem.secs.splice(ind,1);
      toastr('success','Se eliminio el pad de edición');
    }


  }

  }



  $scope.slaye_subsec = function(event,elem){
    event.preventDefault();
    ind = elem.c.secs.indexOf(elem.sb);
    if(confirm('La columna y todas sus secciones seran eliminadas \\n ¿Desea continuar?')){
    
    if(elem.sb.pk){
      data = {'pku':elem.sb.pk};
      data['csrfmiddlewaretoken']=cfr;
      data['step']=1;
      data = $.param(data);
      uri = '/admin/remover/';

      $http({url:uri,method:'POST',data:data}).then(function(response){
            if(response.data.removed=='ok'){
              toastr('success','Sección eliminada con éxito');      
              elem.c.secs.splice(ind,1);    
            }
            
      });
    }
    else{
      elem.c.secs.splice(ind,1);
      toastr('success','Se eliminio el pad de edición');
    }


  }

  }






  $scope.chlogoya=function(evt) {
      var file=evt.currentTarget.files[0];
      $scope.filename = file.name;
      var reader = new FileReader();

      reader.onload = function (evt) {
        $scope.logofile = evt.target.result;
        $scope.$apply(function($scope){
            data = {};
            data['logofile'] = $scope.logofile.replace(/^data:image\/(png|jpeg);base64,/, "");
            data['filename'] = $scope.filename;
            data['csrfmiddlewaretoken']=cfr;
            data = $.param(data);
            uri = '/admin/chlogo/';

            $http({url:uri,method:'POST',data:data}).then(function(response){
                  if(response.data){
                    toastr('success','se guardó con éxito');
                    //$scope.elementado.dl.dfile=$scope.filename;
                    //$scope.elementado.dl.pk = response.data.pk;
                    //elem.item.nodeses.splice(ind,1);    
                  }
                  
            });



        });
      };
      reader.readAsDataURL(file);
    };



    $scope.addSecBanco = function(ev,elemento){
      ev.preventDefault();
     
      orden = elemento.secs.length+1;

      uri = "/admin/addsection/";

      data = {sec_name:'banco imagen',                        
                  orden:orden,
                  parent:null,
                  page_type:'bancoimagen',
                  sec_colum_menu:null
                    };
      data['csrfmiddlewaretoken']=cfr;


      data = $.param(data);


      $http({url:uri,method:'POST',data:data}).then(function(response){
          
          if(response.data.datos.pk>0){
              elemento.pk = response.data.datos.pk;
              elemento.sec_colum_menu = response.data.datos.sec_colum_menu;

              if(elemento.parent>0)
                  toastr('success',response.data.datos.msg);
              else
                  window.location.reload();
          }

      });




    }


});