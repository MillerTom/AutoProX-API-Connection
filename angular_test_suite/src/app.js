var app = angular.module('AutoProx',[]);

app.factory('AppList', function($http){
  return {
    getApps : function(){
      // Connect API
      return $http.get('http://54.200.162.33/api/pending-list');
    }
  }
});

app.factory('NewApp', function($http){

  return {
    PostApp : function(data){
      // Connect API
      return $http.post('http://54.200.162.33/api/new-app', data);
    }
  }
});

app.controller('MainController', function($scope, AppList, NewApp){
  $scope.loading = "Loading please wait..";
  $scope.button = "Submit";
  $scope.get_apps = AppList.getApps().success(function(response){
    $scope.result = response
    $scope.loading = "Pending Applications";
  });
  $scope.formData = {};

  $scope.submit = function(){
    $scope.button = "Sending app..";
    NewApp.PostApp(this.formData).success(function(response){
      $scope.button = response;
    }).error(function(err){
      $scope.form_result = err;
    })
  }
});