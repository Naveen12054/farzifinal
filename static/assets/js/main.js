(function ($) {
    "use strict";

/*--
    Menu Sticky
-----------------------------------*/
var windows = $(window);
var sticky = $('.header-sticky');

windows.on('scroll', function() {
    var scroll = windows.scrollTop();
    if (scroll < 300) {
        sticky.removeClass('is-sticky');
    }else{
        sticky.addClass('is-sticky');
    }
});

/*--
    Mobile Menu
------------------------*/
var menuNav = $('nav.main-navigation');
menuNav.meanmenu({
    meanScreenWidth: '991',
    meanMenuContainer: '.mobile-menu',
    meanMenuClose: '<span class="menu-close"></span>',
    meanMenuOpen: '<span class="menu-bar"></span>',
    meanRevealPosition: 'right',
    meanMenuCloseSize: '0',
});
 
/*--
   Sidebar Search Active
-----------------------------*/
function sidebarSearch() {
    var searchTrigger = $('.trigger-search'),
        endTriggersearch = $('button.search-close'),
        container = $('.main-search-active');

    searchTrigger.on('click', function() {
        container.addClass('inside');
    });

    endTriggersearch.on('click', function() {
        container.removeClass('inside');
    });

};
sidebarSearch();

/*--
    Hero Slider
--------------------------------------------*/
var heroSlider = $('.hero-slider');
heroSlider.slick({
    arrows: true,
    autoplay: false,
    autoplaySpeed: 5000,
    dots: false,
    pauseOnFocus: false,
    pauseOnHover: false,
    fade: true,
    infinite: true,
    slidesToShow: 1,
    prevArrow: '<button type="button" class="slick-prev"> <i class="icon-arrow-left"></i> </button>',
    nextArrow: '<button type="button" class="slick-next"><i class="icon-arrow-right"></i></button>',
    responsive: [
        {
          breakpoint: 767,
          settings: {
            dots: false,
          }
        }
    ]
});

/*--
	Product Slider
-----------------------------------*/
$('.product-slider').slick({
    dots: false,
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: false,
    prevArrow:false,
    nextArrow: false,
    responsive: [
        {
            breakpoint: 1199,
            settings: {
                slidesToShow: 3,
            }
        },
        {
            breakpoint: 991,
            settings: {
                slidesToShow: 2,
            }
        },
        {
            breakpoint: 767,
            settings: {
                slidesToShow: 2,
            }
        },
        {
            breakpoint: 479,
            settings: {
                slidesToShow: 1,
            }
        }
    ]
});
    
 
/*--
    Instagram Slider
--------------------------------------------*/
    
var instagramSlider = $('.instagram-slider');
instagramSlider.slick({
    dots: false,
    infinite: true,
    slidesToShow: 2,
    slidesToScroll: 1,
    autoplay: false,
    prevArrow:false,
    nextArrow: false,
    responsive: [
        {
          breakpoint: 991,
          settings: {
            slidesToShow: 2,
          }
        },
        {
          breakpoint: 767,
          settings: {
            slidesToShow: 1,
          }
        },
        {
          breakpoint: 479,
          settings: {
            slidesToShow: 1,
          }
        }
    ]
});
/*-- 
    Testimonial Slider 
-----------------------------*/
var testimonialSlider = $('.testimonial-slider');
testimonialSlider.slick({
    arrows: false,
    autoplay: true,
    autoplaySpeed: 7000,
    dots: false,
    pauseOnFocus: false,
    pauseOnHover: false,
    infinite: true,
    slidesToShow: 1,
    slidesToScoll: 1,
});
    
/*-- 
    Brand Slider 
------------------------------------*/
var ourBrandActive = $('.our-brand-active');
ourBrandActive.slick({
    arrows: false,
    autoplay: false,
    dots: false,
    pauseOnFocus: true,
    pauseOnHover: true,
    infinite: true,
    slidesToShow: 5,
    slidesToScoll: 2,
    responsive: [
        {
          breakpoint: 991,
          settings: {
            slidesToShow: 4,
          }
        },
        {
          breakpoint: 767,
          settings: {
            slidesToShow: 3,
          }
        },
        {
          breakpoint: 479,
          settings: {
            slidesToShow: 2,
          }
        }
    ]
});
    
/*-- Brand Slider --*/
var blogSlider = $('.blog-image-slider');
blogSlider.slick({
    arrows: true,
    autoplay: false,
    dots: false,
    pauseOnFocus: true,
    pauseOnHover: true,
    infinite: true,
    slidesToShow: 1,
    slidesToScoll: 1,
    prevArrow: '<button type="button" class="slick-prev"> <i class="icon-arrow-left"></i> </button>',
    nextArrow: '<button type="button" class="slick-next"><i class="icon-arrow-right"></i></button>',
});
    

/* Product Details Images Slider */
$('.product-details-images').each(function(){
    var $this = $(this);
    var $thumb = $this.siblings('.horizantal-product-active');
    $this.slick({
        arrows: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: false,
        autoplaySpeed: 5000,
        dots: false,
        infinite: true,
        centerMode: false,
        centerPadding: 0,
        asNavFor: $thumb,
    });
});
$('.horizantal-product-active').each(function(){
    var $this = $(this);
    var $details = $this.siblings('.product-details-images');
    $this.slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: false,
        autoplaySpeed: 5000,
        dots: false,
        infinite: true,
        focusOnSelect: true,
        centerMode: true,
        centerPadding: 0,
        prevArrow: '<button type="button" class="arrow-prv slick-prev"> <i class="ion-ios-arrow-left"></i> </button>',
        nextArrow: '<button type="button" class="arrow-next slick-next"><i class="ion-ios-arrow-right"></i></button>',
        asNavFor: $details,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                slidesToShow: 3,
                }
            },
            {
                breakpoint: 991,
                settings: {
                slidesToShow: 3,
                }
            },
            {
                breakpoint: 767,
                settings: {
                slidesToShow: 2,
                }
            },
            {
                breakpoint: 479,
                settings: {
                slidesToShow: 2,
                }
            }
        ]
    });
});



/* Product Details 2 Images Slider */
$('.product-details-images-2').each(function(){
    var $this = $(this);
    var $thumb = $this.siblings('.vartical-product-active');
    $this.slick({
        arrows: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: false,
        autoplaySpeed: 5000,
        dots: false,
        infinite: true,
        centerMode: false,
        centerPadding: 0,
        asNavFor: $thumb,
    });
});
$('.vartical-product-active').each(function(){
    var $this = $(this);
    var $details = $this.siblings('.product-details-images-2');
    $this.slick({
        arrows: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: false,
        autoplaySpeed: 5000,
        vertical:true,
        verticalSwiping:true,
        dots: false,
        infinite: true,
        focusOnSelect: true,
        centerMode: false,
        centerPadding: 0,
        prevArrow: '<button type="button" class="arrow-prv slick-prev"> <i class="ion-ios-arrow-up"></i> </button>',
        nextArrow: '<button type="button" class="arrow-next slick-next"><i class="ion-ios-arrow-down"></i></button>',
        asNavFor: $details,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                slidesToShow: 3,
                }
            },
            {
                breakpoint: 991,
                settings: {
                slidesToShow: 3,
                }
            },
            {
                breakpoint: 767,
                settings: {
                slidesToShow: 2,
                }
            },
            {
                breakpoint: 479,
                settings: {
                slidesToShow: 2,
                }
            }
        ]
    });
});
    
/*----------
    price-slider active
-------------------------------*/  
$( "#price-slider" ).slider({
   range: true,
   min: 0,
   max: 120,
   values: [ 20, 115 ],
   slide: function( event, ui ) {
        $( "#min-price" ).val('$' + ui.values[ 0 ] );
        $( "#max-price" ).val('$' + ui.values[ 1 ] );
     }
  });
  $( "#min-price" ).val('$' + $( "#price-slider" ).slider( "values", 0 ));   
  $( "#max-price" ).val('$' + $( "#price-slider" ).slider( "values", 1 )); 
    
    
    
 /*--
    Magnific Popup
------------------------*/
$('.img-poppu').magnificPopup({
    type: 'image',
    gallery:{
        enabled:true
    }
});
    
/*--
    showlogin toggle function
--------------------------*/
$( '#showlogin' ).on('click', function() {
    $('#checkout-login' ).slideToggle(500);
}); 
    
/*--
    showcoupon toggle function
--------------------------*/
$( '#showcoupon' ).on('click', function() {
    $('#checkout-coupon' ).slideToggle(500);
});
    
/*--
    Checkout 
--------------------------*/
$("#chekout-box").on("change",function(){
    $(".account-create").slideToggle("100");
});
    
/*-- 
    Checkout 
---------------------------*/
$("#chekout-box-2").on("change",function(){
    $(".ship-box-info").slideToggle("100");
});    
/* ---
   payment-accordion
* --------------------------------*/ 
	$(".payment-accordion").collapse({
		accordion:true,
	  open: function() {
		this.slideDown(550);
	  },
	  close: function() {
		this.slideUp(550);
	  }		
	}); 
/*--
    Accordion
-------------------------*/
$(".faequently-accordion").collapse({
    accordion:true,
  open: function() {
    this.slideDown(300);
  },
  close: function() {
    this.slideUp(300);
  }		
});	 
   
    
/* --
    counterUp 
-----------------------------*/
$('.count').counterUp({
    delay: 10,
    time: 1000
});
   
/*--
    ScrollUp Active
-----------------------------------*/
$.scrollUp({
    scrollText: '<i class="ion-chevron-up"></i>',
    easingType: 'linear',
    scrollSpeed: 900,
    animation: 'fade'
});   
    
})(jQuery);	
