describe('Angular Test', function(){
  beforeEach(module('AutoProx'));

  describe('Scope Check', function(){
    it('OK', inject(function($controller){
      var scope = {},
      ctrl = $controller('MainController', { $scope: scope });

      expect(scope.loading).toBe("Loading please wait..");

      expect(scope.button).toBe("Submit");

      expect(scope.get_apps).toBeDefined();

      expect(scope.formData).toBeDefined();

      expect(scope.submit).toBeDefined();
    }));
  });
  describe('Ajax Request', function(){
    var $httpBackend, $rootScope;
    beforeEach(inject(function($injector) {
      // Set up the mock http service responses
      $httpBackend = $injector.get('$httpBackend');
      $httpBackend.when('GET', 'http://54.200.162.33/api/pending-list').respond({'apps':[]})
      $httpBackend.when('POST', 'http://54.200.162.33/api/pending-list').respond(500)
      $rootScope = $injector.get('$rootScope');
      var $controller = $injector.get('$controller');

      createController = function() {
        return $controller('MainController', {'$scope' : $rootScope });
      };
    }));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      $httpBackend.verifyNoOutstandingRequest();
    });

    it('OK', function() {
      $httpBackend.expectGET('http://54.200.162.33/api/pending-list');
      var controller = createController();
      $httpBackend.flush();
    });

  });
});