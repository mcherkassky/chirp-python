var app = angular.module('app', ['ngRoute','ngResource','ui.bootstrap','ui.router'], function($interpolateProvider, $locationProvider, $stateProvider, $urlRouterProvider, $routeProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $locationProvider.html5Mode(true);

    $urlRouterProvider.otherwise("/home");

    $stateProvider
        .state('home', {
          url: "/home",
          templateUrl: "/static/html/browse/home.html",
            controller: 'OfferCtrl'
        })
        .state('create', {
          url: "/create",
          templateUrl: "/static/html/browse/create.html",
            controller: "CampaignCtrl"
        })
        .state('dashboard',{
            url:'/dashboard',
            templateUrl: "static/html/browse/dashboard.html",
            controller: "OfferCtrl"
        })
        .state('current',{
            url:'/open',
            templateUrl: "static/html/offers/current.html",
            controller: 'OfferCtrl'
        });

//    $routeProvider.when('/home',{
//        templateUrl:'/static/html/browse/home.html',
//        controller: 'OfferCtrl'
//    });
//
//    $routeProvider.when('/create',{
//        templateUrl:'/static/html/browse/create.html',
//        controller:'CampaignCtrl'
//    });

//    $routeProvider.otherwise({
//        controller: "404Ctrl",
//        template: "<div></div>"
//    });
});

app.run(function($rootScope, OfferFactory, UserFactory){
    $rootScope.current_user = UserFactory.get();

    OfferFactory.query(function(data){
        $rootScope.offers = data.filter(function(obj){return obj.claimed == false});
        $rootScope.claimed = data.filter(function(obj){return obj.claimed == true});
        debugger;
    });

    $rootScope.count = function(element, counter){
        var current = parseFloat(element.html());
        current= current + counter;
        element.html(Math.round(current * 100) / 100);
        if(current <= (element.data('count') - counter)){
            setTimeout(function(){$rootScope.count(element, counter)}, 30);
        }
        else{
            element.html(element.data('count'))
        }
    };

    $rootScope.monthNames = [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December" ];
});

app.directive('countUp', function($timeout){
    return{
        link: function(scope, element){
            var value = parseFloat(element.html());
            element.data('count', value);
            element.html('0');

            var count_type = element.data('type');

            var counter = value / 20;
            if(count_type == "int"){
                counter = Math.round(counter)
            }
            else{
                counter = Math.round(counter * 100) / 100
            }

            $timeout(function(){
                scope.count(element, counter);
            }, parseInt(element.data('delay')));

        }
    }
});

app.factory('OfferFactory', function($resource){
    return $resource('/offers/:id',{id: '@id'},
        {
            edit: {method:"PUT"}
        })
});

app.factory('UserFactory', function($resource){
    return $resource('/current_user')
});

app.factory('UrlFactory', function($resource){
    return $resource('/offers/:id/url',{id: '@id'},
        {
            edit: {method:"PUT"}
        })
});

app.factory('CampaignFactory', function($resource){
    return $resource('/campaigns/:id',{id: '@id'},
        {
            edit: {method:"PUT"}
        })
});

app.controller('OfferCtrl', function($scope, OfferFactory){
    $scope.show_actions = false;

    $scope.claim = function(offer){
        offer.claimed = true;
        console.log($scope.offers);
        OfferFactory.save(offer);
    };

    $scope.open_tweet = function(url){
        window.open("https://twitter.com/intent/tweet?source=webclient&text=" + url)
    }
});

app.controller('CollapseCtrl', function($scope, $timeout, OfferFactory, UrlFactory){
    $scope.show_offer = false;
    $scope.offer_ready = false;

    $scope.claim = function(offer, index){

        offer.claimed = true;
        OfferFactory.save(offer);
        $scope.url = UrlFactory.get(offer, function(){
            $scope.offer_ready = true
            $timeout(function(){
                $('.copy-button-' + index).zclip({
                    path:'http://www.steamdev.com/zclip/js/ZeroClipboard.swf',
                    copy: $('.url-text-' + index).text(),
                    afterCopy: function(){}
                })
            },100)

        });
        $scope.show_offer = !$scope.show_offer
    };

    $scope.copy = function(index){
        $('.url-text-' + index).css({'color':'#428bca'});
        $timeout(function(){
            $('.url-text-' + index).css({'color': 'black',
                                    '-webkit-transition':'all 0.75s',
                                    '-moz-transition':'all 0.75s',
                                    '-ms-transition':'all 0.75s',
                                    '-o-transition':'all 0.75s',
                                    'transition':'all 0.75s'});
            $timeout(function(){
                $('.url-text-' + index).css({
                                    '-webkit-transition':'all 0s',
                                    '-moz-transition':'all 0s',
                                    '-ms-transition':'all 0s',
                                    '-o-transition':'all 0s',
                                    'transition':'all 0s'});
            },750)

        },100);


        console.log(index)
    }
});

app.controller('CampaignCtrl', function($scope, $rootScope, CampaignFactory, $timeout){
    $('.input-daterange').datepicker({
        format: "MM dd yy",
        orientation: "top left"
    });

    var currentDate = new Date();
    var oneDay = 24*60*60*1000;
    $scope.days = 0;
    $scope.launching = false;
    $scope.start_date = {month: $rootScope.monthNames[currentDate.getMonth()],
                        day: currentDate.getDate(),
                        date: currentDate};

    $scope.end_date = {month: $rootScope.monthNames[currentDate.getMonth()],
                        day: currentDate.getDate(),
                        date:currentDate};

//    $scope.start_date = currentDate.getDate();
//    console.log($scope.start_date.getDate())
//    $scope.end_date = currentDate;

    $('.input-daterange').datepicker()
        .on('changeDate', function(e){

            $scope.$apply(function(){
                var start_date = $('#start-date').datepicker('getDate')
                var end_date = $('#end-date').datepicker('getDate')

                $scope.start_date = {month: $rootScope.monthNames[start_date.getMonth()],
                                    day: start_date.getDate(),
                                    date:start_date}

                $scope.end_date = {month: $rootScope.monthNames[end_date.getMonth()],
                                    day: end_date.getDate(),
                                    date:end_date};

                $scope.days = Math.round(Math.abs($scope.end_date.date - $scope.start_date.date)/oneDay)
            })
        });



    $scope.new_campaign = function(){
        $scope.launching = true;
        $scope.campaign.start_date = $scope.start_date.date;
        $scope.campaign.end_date = $scope.end_date.date;

        CampaignFactory.save($scope.campaign, function(data){
            $scope.launching = false;
            $scope.campaign = {};
            window.location.href = '/home';
        })
    }

    $(document).ready(function(){
        function drawRegionsMap(data_array) {
            var data = google.visualization.arrayToDataTable(data_array);

            var view = new google.visualization.DataView(data)
            view.setColumns([0, 1])

            var options = { region: 'world', resolution: 'continents', width: 600, height: 450 };
            options['colors'] = [ '#ffffff', '#ccc', '#ffffff', '#eee'];
            options['tooltip'] = {trigger: 'none'};

            var chart = new google.visualization.GeoChart(document.getElementById('map_canvas'));
            chart.draw(data, options)

            google.visualization.events.addListener(
                chart, 'regionClick', function(e) {
                   var value = data_array[lookup[e['region']]][1];
                   if(value == 3){
                       data_array[lookup[e['region']]][1] = 2
                   }
                   else{
                       data_array[lookup[e['region']]][1] = 3
                   }
                   drawRegionsMap(data_array)
            });
        }
        var data_array = [
              ['Country', 'Popularity'],
              ['019', 3], //americas
              ['002', 2], //africa
              ['150', 2], //europe
              ['142', 2], //asia
              ['009', 2] //australia
            ];
        drawRegionsMap(data_array)
    })
});