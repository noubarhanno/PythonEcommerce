$(document).ready(function(){
     // Contact Form
     var contactForm = $(".contact-form ")
     var contactFormMethod = contactForm.attr("method")
     var conctactFormEndpoint = contactForm.attr("action")
     var contactFormSubmitBtn = contactForm.find("[type='submit']")
     var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

     function displaySubmitting(submitBtn, defaultTxt, doSubmit){
       if (doSubmit){
         submitBtn.addClass="disabled"
         submitBtn.html("<i class= 'fa fa-spin fa-spinner'></i> Submitting  ...")
       } else {
         submitBtn.removeClass="disabled"
         submitBtn.html(defaultTxt)
       }

     }



     contactForm.submit(function(event){
       event.preventDefault()
       contactFormData = contactForm.serialize()
       var thisForm = $(this)
       var contactFormSubmitBtn = contactForm.find("[type='submit']")
       var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
       displaySubmitting(contactFormSubmitBtn,"",true)
       $.ajax({
         method: contactFormMethod,
         url: conctactFormEndpoint,
         data : contactFormData,
         success: function(data){
           thisForm[0].reset()
           $.alert({
             title: "Success!",
             content: data.message, // the data here comming from PythonEcommerceProject -> views.py in contact view "return JsonResponse({"message":"thank you for submission"})
             theme: "modern",
           })
           setTimeout(function(){
             displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
           }, 2000)
         },
         error: function(error){
           console.log(error.responseJSON);
           var JsonData = error.responseJSON
           var msg =""
           $.each(JsonData, function(key, value){
             msg += key + " : "+value[0].message +"</br>"
           })
           $.alert({
             title: "Oops!",
             content: msg,
             theme: "modern",
           })
           setTimeout(function(){
             displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
           }, 2000)
         }
       })
     })




      // Auto Search


      var searchForm = $('.search-form')
      var searchInput = searchForm.find("[name='q']") // input  name='q'
      var typingTimer;
      var typingInterval = 500
      var searchBtn = searchForm.find("[type='submit']")
      searchInput.keyup(function(event){
        // released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
      })
      searchInput.keydown(function(event){
        // pressed
        clearTimeout(typingTimer)
      })

      function displaySearch(){
        searchBtn.addClass="disabled"
        searchBtn.html("<i class= 'fa fa-spin fa-spinner'></i> Searching ...")
      }

      function performSearch(){
        displaySearch()
        var query = searchInput.val()
        setTimeout(function(){
          window.location.href='/search/?q=' + query
        },1000)

      }


      // Cart + Add Products

      var productForm = $(".form-product-ajax") // #form-product-ajax


      function getOwnedProduct(ProductId, submitSpan){
        var actionEndpoint = '/orders/endpoint/verify/ownership/'
        var httpMethod = 'get'
        var data = {
          product_id : ProductId
        }
        var isOwner;
          $.ajax({
              url: actionEndpoint,
              method: httpMethod,
              data: data,
              success: function(data){
                console.log(data)
                console.log(data.owner)
                if (data.owner){
                  isOwner = true
                  submitSpan.html("<a class='btn btn-warning' href='/library/'>In Library</a>")
                } else {
                  isOwner = false
                }
              },
              error: function(error){
                console.log(error)

              }
          })
      }

      $.each(productForm , function(index,object){
        var $this = $(this) // this is just a shortcut instead of using query in each time we want $(this)
        var isUser = $this.attr('data-user')
        var submitSpan = $this.find('.submit-span')
        var ProductInput = $this.find("[name='product_id']")
        var ProductId = ProductInput.attr('value')
        var ProductIsDigital = ProductInput.attr('data_is_digital')

        if (ProductIsDigital && isUser){
          var isOwned = getOwnedProduct(ProductId, submitSpan)
        }
      })



      productForm.submit(function(event){
        event.preventDefault();
        console.log('Form is not sending')
        var thisForm = $(this)
        // var actionEndpoint = thisForm.attr('action');
        var actionEndpoint = thisForm.attr('data-endpoint')
        var httpMethod = thisForm.attr('method');
        var formData = thisForm.serialize();
        $.ajax({
          url: actionEndpoint,
          method : httpMethod,
          data: formData,
          success: function(data){
            var submitSpan = thisForm.find('.submit-span')
            if (data.added){
              submitSpan.html("<div class='btn-group'><a class='btn btn-link' href='/cart/'>In cart</a> <button type='submit' class='btn btn-link'>Remove ?</button></div>")
            } else {
              submitSpan.html("<button class='btn btn-success'>Add to Cart</button>")
            }
            var navbarCount = $(".navbar-cart-count")
            navbarCount.text(data.cartItemCount)
            var currentPath = window.location.href
            if(currentPath.indexOf("cart") != -1){
              refreshCart()
            }
          },
          error : function(errorData){
            $.alert({
              title: "Oops!",
              content: 'Error occured',
              theme: "modern",
            })
          }
        })

      })
      function refreshCart(){
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find('.cart-body')
        // cartBody.html("<h1>Changed</h1>")
        var productsRows = cartBody.find('.cart-product')
        var currenturl = window.location.href
        var refreshCartUrl = '/api/cart/'
        var refreshCartMethod = "GET"
        var data = {};
        $.ajax({
          url: refreshCartUrl,
          method: refreshCartMethod,
          data: data,
          success: function(data){
            var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
            if (data.products.length>0){
              productsRows.html("")
              i= data.products.length
              $.each(data.products, function(index, value){
                var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                newCartItemRemove.css("display","block")
                newCartItemRemove.find(".cart-item-product-id").val(value.id)
                cartBody.prepend("<tr><th scope=\"row\">"+ i + "</th><td><a href='"+value.url+"'>"+value.name+"</a>"+ newCartItemRemove.html()+"</td>"+"<td>"+value.price+"</td></tr>")
                i --
              })

              cartBody.find(".cart-subtotal").text(data.subtotal)
              cartBody.find(".cart-total").text(data.total)
            } else {
              window.location.href = currenturl
            }
          },
          error : function(errorData){
            $.alert({
              title: "Oops!",
              content: 'Error occured',
              theme: "modern",
            })
          }
        })
      }


})
