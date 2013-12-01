var app = angular.module('app', ['ngRoute','ngResource','ui.bootstrap'], function($interpolateProvider, $locationProvider, $routeProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $locationProvider.html5Mode(true);
});

app.run(function($rootScope){
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
    $scope.offers = OfferFactory.query(function(){
        console.log($scope.offers)
    });

    $scope.claim = function(offer){
        offer.claimed = true;
        console.log($scope.offers);
        OfferFactory.save(offer);
    };
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

    $('.input-daterange').datepicker()
        .on('changeDate', function(e){
            $scope.$apply(function(){
                $scope[$(e.target).attr('ng-model')]['day'] = e.date.getDate();
                $scope[$(e.target).attr('ng-model')]['month'] = $rootScope.monthNames[e.date.getMonth()];
                $scope[$(e.target).attr('ng-model')]['date'] = e.date

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
});