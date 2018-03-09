              $("#syn").click( function() {
              var csrftoken = getCookie('csrftoken');
              console.log(csrftoken);
              // console.log(typeof($('#string').html()));
              var datas = {string: $('#temp').html()};
              console.log(datas);
              // set csrf header
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            // Ajax call here
            $.ajax({
                url:"../api/syn/",
                data: JSON.stringify(datas),
                processData: false,
                contentType: 'application/json',
                type: 'POST',
                success: function(data) {

                    console.log(data);
                    }
                });


});