(function($) {
    // ton code core.js


$(document).ready(function(){

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const BASEURL = $("body").data('url');

    $(".abClass").on('click', function(e){                         
        e.preventDefault();
        let code = $(this).data("code")
        let an = $("select[name='an"+code+"'] option:selected").val()
       
        var data = {                      
            "code": code,
            "nbannee": an, 
        };

        if( data.code.length > 2 && data.nbannee.length > 0 ){

            $.ajax({
                method      : "POST",
                data        : JSON.stringify(data),
                url         : BASEURL+"/add_abonnement",  
                dataType    : "JSON",
                beforeSend      : function(){
                    // alert(JSON.stringify(data) + ", url: " + this.url)
                },
                error: function(error) {
                    console.error(error);
                    // alert(JSON.stringify(error))
                },
                success  : function(returnedData){
                    // console.log(returnedData); 
            
                    if (returnedData.status) {
                        Swal.fire({
                            icon: "success",
                            title: " Merci !" ,
                            text:   " Ajout Reussi de Votre Abonnement ! " ,
                            timer: 4000,
                            showConfirmButton: false

                        }).then(
                            ()=>{
                                $("#payMessage").html(` <div class="alert alert-info messageDiv">${returnedData.message} </div>`  )
                            }
                        ); 

                    }else{
                        Swal.fire({
                            icon: "error",
                            title: " Oups !" ,
                            text:   " " + returnedData.message ,
                            timer: 4000,
                            showConfirmButton: true

                        }); 
                    }
                }

            })

        }else{

            Swal.fire({
                icon: "error",
                title: " Oupps !" ,
                text:   " Merci de fournir toutes les informations requises pour cet abonnement !!!" ,
                timer: 4000,
                showConfirmButton: false
            });
            // console.table( data )
        }
    })

    $(".partComID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
 				"comid": $(this).data("com"), 
 				"userid": $(this).data("user"), 
			} 
            alert(BASEURL)
            if( parseInt(data.userid) > 0 && data.comid != undefined   ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_ad_comsalleatt",  
                    dataType    : "JSON",
                    beforeSend      : function(){
                        // alert(JSON.stringify(data))
                    },
                    error: function(error) {
                        console.error(error); 
                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.status) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi , votre demande à été pris en compte, un adminitrateur etudiera et vous serez notifié de la validation de votre accès ! " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    $(".clos").click();
                                    window.location.reload()
                                     
                                  });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

                });

			}else{

                Swal.fire({
                    icon: "error",
                    title: " Oupps !" ,
                    text:   " Merci de vous connecter d'abord !!!" ,
                    timer: 4000,
                    showConfirmButton: false
                });
                console.table( data )
			}
    })

    $(".partAssoID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
 				"assoid": $(this).data("asso"), 
 				"userid": $(this).data("user"), 
			} 
            if( parseInt(data.userid) > 0 && data.assoid != undefined   ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_ad_assosalleatt",  
                    dataType    : "JSON",
                    beforeSend      : function(){
                        //alert(JSON.stringify(data))
                    },
                    error: function(error) {
                        console.error(error); 
                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.status) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi , votre demande à été pris en compte, un adminitrateur etudiera et vous serez notifié de la validation de votre accès ! " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    $(".clos").click();
                                    window.location.reload()
                                     
                                  });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

                });

			}else{

                Swal.fire({
                    icon: "error",
                    title: " Oupps !" ,
                    text:   " Merci de vous connecter d'abord !!!" ,
                    timer: 4000,
                    showConfirmButton: false
                });
                console.table( data )
			}
    })

    $(".valideUserID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
 				"salle": $(this).data("salle"), 
 				"direction": $(this).data("dir"), 
			} 
            // alert(JSON.stringify(data))
            if( parseInt(data.salle) > 0 && data.direction != undefined   ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/valsatt",  
                    dataType    : "JSON",
                    beforeSend      : function(){
                        //alert(JSON.stringify(data))
                    },
                    error: function(error) {
                        console.error(error); 
                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.status) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Validation de la demande reussie ! !" ,
                                    text:   "  "+returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    // $(".clos").click();
                                    window.location.reload()
                                     
                                });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

                });

			}else{

                Swal.fire({
                    icon: "error",
                    title: " Oupps !" ,
                    text:   " Merci de vous connecter d'abord !!!" ,
                    timer: 4000,
                    showConfirmButton: false
                });
                console.table( data )
			}
        })

    $(".partFamID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
 				"famid": $(this).data("fam"), 
 				"userid": $(this).data("user"), 
			} 
            if( parseInt(data.userid) > 0 && data.famid != undefined   ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_ad_famsalleatt",  
                    dataType    : "JSON",
                    beforeSend      : function(){
                        // alert(JSON.stringify(data))
                    },
                    error: function(error) {
                        console.error(error); 
                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.status) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi , votre demande à été pris en compte, un adminitrateur etudiera et vous serez notifié de la validation de votre accès ! " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    $(".clos").click();
                                    window.location.reload()
                                     
                                  });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

                });

			}else{

                Swal.fire({
                    icon: "error",
                    title: " Oupps !" ,
                    text:   " Merci de vous connecter d'abord !!!" ,
                    timer: 4000,
                    showConfirmButton: false
                });
                console.table( data )
			}
    })

    $("#addAdminFamID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
				"adminid": $("select[name='adminFam'] option:selected").val(), 
				"famid": $(this).data("fam"), 
			};
            
           
			if( data.adminid.length > 0 && data.famid != undefined   ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_ad_fam",  
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
                                    text:   " Ajout Reussi de ce administrateur " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    $(".clos").click();
                                    window.location.reload()
                                     
                                  });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

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
    $("#addAdminComID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
				"adminid": $("select[name='admin'] option:selected").val(), 
				"comid": $(this).data("com"), 
			};
           
			if( data.adminid.length > 0 && data.comid != undefined   ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_ad_com",  
                    dataType    : "JSON",
                    beforeSend      : function(){
                        //alert(JSON.stringify(data))
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
                                    text:   " Ajout Reussi de ce administrateur " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    $(".clos").click();
                                    window.location.reload()
                                     
                                  });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

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
    $("#addAdminAssoID").on('click', function(e){                         
        e.preventDefault();
       
			var data = {                      
				"adminid": $("select[name='admin'] option:selected").val(), 
				"assoid": $(this).data("asso"), 
			};
           
			if( data.adminid.length > 0 && data.assoid != undefined ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : BASEURL+"/add_ad_asso",  
                    dataType    : "JSON",
                    beforeSend      : function(){
                        alert(JSON.stringify(data))
                    },
                    error: function(error) {
                        console.error(error);
                        // alert(JSON.stringify(error))
                    },
                    success  : function(returnedData){
                            console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.status) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi de ce administrateur " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    $(".clos").click();
                                    window.location.reload()
                                     
                                  });

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload()
                                     
                                  });
                                 
                            }   
                    }, 

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

    $("#addMessageLibID").on('click', function(e){                         
        e.preventDefault();
			var data = {                      
				"nom": $("#username").val(), 
				"id": $("#idlib").val(), 
				"message": $("#message").val(),
			};
            let url =  BASEURL+"/lib/mess/create";
            const csrftoken = getCookie('csrftoken');
            
			if( data.nom.length > 2  && data.message.length > 5 ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : url,  
                    dataType    : "JSON",
                    contentType: "application/json", 
                
                    headers: {                         
                        "X-CSRFToken": csrftoken
                    },
                    beforeSend      : function(){
                        // alert(JSON.stringify(data) + ", " + url)
                    },
                    error: function(error) {
                        console.error(error);
                        // alert(JSON.stringify(error))
                    },
                    success  : function(returnedData){
                            // console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.success) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi de Votre Message, Le proprietaire vous contactera pour la suite " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                });
                                $(".btn-close").click();

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload() 
                                });
                                
                            }   
                    }, 

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

    $("#addMessageComID").on('click', function(e){   
                              
        e.preventDefault();
			var data = {                      
				"nom": $("#username").val(), 
				"id": $("#idcom").val(), 
				"message": $("#message").val(),
			};
            let url =  BASEURL+"/com/mess/create";
            const csrftoken = getCookie('csrftoken');
            
			if( data.nom.length > 2  && data.message.length > 5 ){

                $.ajax({
                    method      : "POST",
                    data        : JSON.stringify(data),
                    url         : url,  
                    dataType    : "JSON",
                    contentType: "application/json", 
                
                    headers: {                         
                        "X-CSRFToken": csrftoken
                    },
                    beforeSend      : function(){
                        // alert(JSON.stringify(data) + ", " + url)
                    },
                    error: function(error) {
                        console.error(error);
                        // alert(JSON.stringify(error))
                    },
                    success  : function(returnedData){
                            // console.log(returnedData);
                            // alert(JSON.stringify(returnedData))
                    
                            if (returnedData.success) {
                                Swal.fire({
                                    icon: "success",
                                    title: " Merci !" ,
                                    text:   " Ajout Reussi de Votre Message, Le gestionnaire vous contactera pour la suite " ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                });
                                $(".btn-close").click();

                            }else{
                                Swal.fire({
                    
                                    icon: "error",
                                    title: " Oupps !" ,
                                    text:   "  " + returnedData.message ,
                                    timer: 4000,
                                    showConfirmButton: false
        
                                }).then((result) => {
                                    window.location.reload() 
                                });
                                
                            }   
                    }, 

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


})(jQuery);