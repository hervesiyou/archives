$(document).ready(function(){
    const BASEURL = $("body").data('url');
 
    $("#addOrderID").on('click', function(){                         

			var data = {                      
				"nom": $("#nom").val(),
				"telephone": $("#telephone").val(),
				"prop_email": $("#email").val(),
				"livre": $("#livre").data("id"),
				"possesseur": $("#possesseur").data("id"),
				"message": $("#message").val(),
			};
// console.log(data)
			if( data.nom.length > 2 && data.telephone.length > 7 && data.message.length > 5 ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_order/",  
                    dataType    : "JSON",
                    beforeSend      : function(){

                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                    
                            if (returnedData.status) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi de Votre Demande, Le proprietaire vous contactera pour la suite " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                });
                                $(".clos").click();

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                });
                                window.location.reload()
                            }
                            
                        
                    }, 
                    complete    : function(){ 
                    }

                });
			}else{

                Swal.fire({
                    icon: "error",
                    title: " Oupps !" ,
                    text:   " Merci de fournir toutes les informations requises!!!" ,
                    timer: 4000,
                    showConfirmButton: false
                });
                console.table( data )
			}

    });
})