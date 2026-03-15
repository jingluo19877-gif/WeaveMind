(function($) {
    'use strict';


    //Header Search
    if($('.search-box-outer').length) {
        $('.search-box-outer').on('click', function() {
            $('body').addClass('search-active');
        });
        $('.close-search').on('click', function() {
            $('body').removeClass('search-active');
        });
    }

	// Mobile Menu
    $('.mobile-menu nav').meanmenu({
        meanScreenWidth: "991",
        meanMenuContainer: ".mobile-menu",
        meanMenuOpen: "<span></span> <span></span> <span></span>",
        onePage: false,
    });	


    // Sticky
    $(document).ready(function() {

        var wind = $(window);
        var sticky = $('.header-manu-section');
        wind.on('scroll', function () {
            var scroll = wind.scrollTop();
            if (scroll < 100) {
                sticky.removeClass('sticky');
            } else {
                sticky.addClass('sticky');
            }
        });
    });


    // animate
    new WOW().init();


     // Case Study Active
    $('.banner-slider').owlCarousel({
        loop: true,
        autoplay: true,
        smartSpeed:1500,
        autoplayTimeout: 10000,
        dots: false,
        nav: true,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    }) 

    // testimonial Active
    $('.testimonial-slider').owlCarousel({
        loop: true,
        autoplay: true,
        smartSpeed:1000,
        autoplayTimeout: false,
        dots: true,
        nav: false,
        margin:30,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    })  
    
    
    // testimonial Active
    $('.choose-slider').owlCarousel({
        loop: true,
        autoplay: true,
        smartSpeed:1000,
        autoplayTimeout: false,
        dots: false,
        nav: true,
        margin:30,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            1000: {
                items: 3
            },
            1920: {
                items: 3
            }
        }
    })  

    // service Active
    $('.nagibrid-slider').owlCarousel({
        loop: true,
        autoplay: false,
        smartSpeed:1000,
        autoplayTimeout: 10000,
        dots: false,
        nav: true,
        center:false,
        margin: 30,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            1000: {
                items: 4
            },
             1500: {
                items: 4
            },
            1920: {
                items: 4
            }
        }
    })  

    // brand Active
    $('.hero-slider').owlCarousel({
        loop: true,
        autoplay: true,
        smartSpeed:1000,
        autoplayTimeout: 10000,
        dots: false,
        nav: false,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1200: {
                items: 1
            },
             1500: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    })  
    
    
    // clinning Active
    $('.testimonial-inner-slider').owlCarousel({
        loop: true,
        autoplay: true,
        smartSpeed:1000,
        autoplayTimeout: 10000,
        dots: false,
        nav: true,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1200: {
                items: 1
            },
             1500: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    }) 
    
    
    // clinning Active
    $('.image-slider').owlCarousel({
        loop: false,
        autoplay: true,
        smartSpeed:1000,
        autoplayTimeout: 10000,
        dots: false,
        nav: true,
        navText: ["<i class='bi bi-chevron-left'></i>", "<i class='bi bi-chevron-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1200: {
                items: 1
            },
             1500: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    }) 
    
    
    // clinning Active
    $('.fecilities-slider').owlCarousel({
        loop: true,
        autoplay: true,
        smartSpeed:1000,
        autoplayTimeout: 10000,
        dots: false,
        nav: true,
        navText: ["<i class='bi bi-chevron-left'></i>", "<i class='bi bi-chevron-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 2
            },
            1000: {
                items: 2
            },
            1200: {
                items: 2
            },
             1500: {
                items: 2
            },
            1920: {
                items: 2
            }
        }
    })  


	/*---------------------
    WOW active js 
    --------------------- */
    new WOW().init();

    // counterUp
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

    
        //<!--barfiller script -->

        $(document).ready(function(){
            $('#bar1').barfiller({ duration: 7000 });
            $('#bar2').barfiller({ duration: 7000 });
            $('#bar3').barfiller({ duration: 7000 });
            $('#bar4').barfiller({ duration: 7000 });
            $('#bar5').barfiller({ duration: 7000 });
            $('#bar6').barfiller({ duration: 7000 });
            $('#bar7').barfiller({ duration: 7000 });
            $('#bar8').barfiller({ duration: 7000 });
        });
    


    // tabs
    $(document).ready(function() {

    
        const tabs= document.querySelectorAll('.tab-btn');
        const all_content= document.querySelectorAll('.tab-view')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });
    
    
    // Work tab

    $(document).ready(function() {

    
        const tabs= document.querySelectorAll('.best-tab-btn');
        const all_content= document.querySelectorAll('.best-work-tab-content')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });
    
    // Service tab

    $(document).ready(function() {

    
        const tabs= document.querySelectorAll('.service-tab-btn');
        const all_content= document.querySelectorAll('.service-inner-tab-content')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });
    
    $(document).ready(function() {

    
        const tabs= document.querySelectorAll('.service-tab-btn');
        const all_content= document.querySelectorAll('.service-inner-tab-content2')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });    
    
    
    // Shop Tab
    $(document).ready(function() {

    
        const tabs= document.querySelectorAll('.shop-tab-btn');
        const all_content= document.querySelectorAll('.shop-tab-content')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });
    
    
    //Shop Details Thumb Tab

    $(document).ready(function() {

    
        const tabs= document.querySelectorAll('.tab-btn button');
        const all_content= document.querySelectorAll('.tab-content')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });
    
    
    
    //Shop Details Content Tab

    $(document).ready(function() {

        const tabs= document.querySelectorAll('.info-tab-btn button');
        const all_content= document.querySelectorAll('.tab-contents')

        tabs.forEach((tab, index)=>{
            tab.addEventListener('click', ()=>{
                tabs.forEach(tab=>{tab.classList.remove('active')});
                tab.classList.add('active');

                all_content.forEach(content=>{content.classList.remove('active')});
                all_content[index].classList.add('active');
            });
        });
    });



    // increasing and decresing btn
        
    "use strict";
    window.onload = function() {
        const   plus    = document.querySelector(".plus"),
                minus   = document.querySelector(".minus"),
                num     = document.querySelector(".num");

        let     a = 1;

        plus
            if  (a < 999) {
                a++;
                insertingText();
            }
     

        minus
            if (a > 1) {
                a--;
                insertingText();
            }

        function insertingText() {
            a = (a < 10) ? "0" + a : a;
            
        }
    };


	
	 // Venubox

    $('.venobox').venobox({

        numeratio: true,

        infinigall: true

    });
    

    //Curser animation

    $(document).ready(function() {

        var curser = document.querySelector(".curser");
        var curser2 = document.querySelector(".curser2");

        document.addEventListener("mousemove", function(e){
            curser.style.cssText = curser2.style.cssText = "left: " + e.clientX + "px; top: " + e.clientY + "px;";
        });
    });



	/*--------------------------
     scrollUp
    ---------------------------- */
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    })



    // accordion js
        jQuery(document).ready(function($) {
            "use strict";

            $(".accordion > li:eq(0) a").addClass("active").next().slideDown();

            $(".accordion a").click(function (j) {
                var dropDown = $(this).closest("li").find("p");

                $(this).closest(".accordion").find("p").not(dropDown).slideUp();

                if ($(this).hasClass("active")) {
                    $(this).removeClass("active");
                } else {
                    $(this).closest(".accordion").find("a.active").removeClass("active");
                    $(this).addClass("active");
                }

                dropDown.stop(false, true).slideToggle();

                j.preventDefault();
            });

        });



        
            
            // active class & remove class

            $(document).ready(function() {
                let buttons = document.querySelectorAll('.shop-list-left i');

                buttons.forEach(button => {
                    button.addEventListener('click', function () {
                        buttons.forEach(btn => btn.classList.remove('active'));
                        this.classList.add('active');        
                    });
                });
            });




            //Header Search

            $(document).ready(function() {

                if($('.search-box-outer').length) {
                    $('.search-box-outer').on('click', function() {
                        $('body').addClass('search-active');
                    });
                    $('.close-search').on('click', function() {
                        $('body').removeClass('search-active');
                    });
                };
            });


            


            //Progress

        $(document).ready(function() {
            if($('.prgoress_indicator path').length){
                var progressPath = document.querySelector('.prgoress_indicator path');
                var pathLength = progressPath.getTotalLength();
                progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
                progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
                progressPath.style.strokeDashoffset = pathLength;
                progressPath.getBoundingClientRect();
                progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
                var updateProgress = function () {
                var scroll = $(window).scrollTop();
                var height = $(document).height() - $(window).height();
                var progress = pathLength - (scroll * pathLength / height);
                progressPath.style.strokeDashoffset = progress;
                }
                updateProgress();
                $(window).on('scroll', updateProgress);
                var offset = 250;
                var duration = 550;
                jQuery(window).on('scroll', function () {
                if (jQuery(this).scrollTop() > offset) {
                    jQuery('.prgoress_indicator').addClass('active-progress');
                } else {
                    jQuery('.prgoress_indicator').removeClass('active-progress');
                }
                });
                jQuery('.prgoress_indicator').on('click', function (event) {
                event.preventDefault();
                jQuery('html, body').animate({ scrollTop: 0 }, duration);
                return false;
                });
            };
        });



        // Preloader
        $(document).ready(function() {
            setTimeout(function(){
                $('.loader_bg').fadeToggle();
            }, 1000);
        });	

    
})(jQuery);