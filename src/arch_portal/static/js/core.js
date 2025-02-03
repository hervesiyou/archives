$(document).ready(function(){
    const BASEURL = $("body").data('url');
 

    $(".abClass").on('click', function(e){                         
        e.preventDefault();
        let code = $(this).data("code")
        let an = $("select[name='an"+code+"'] option:selected").val()
        alert(code + ", " + an)
    })

    $("#addOrderID").on('click', function(e){                         
        e.preventDefault();
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
                        // alert(JSON.stringify(data))
                    },
                    error: function(error) {
                        console.error(error);
                        alert(JSON.stringify(error))
                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
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
        
                                }).then((result) => {
                                    window.location.reload()
                                    // if (result.isConfirmed) {
                                    //   Swal.fire("Saved!", "", "success")
                                     
                                    // }  
                                  });
                                // 
                            }   
                    }, 
                    // complete    : function(){ 
                    // }

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