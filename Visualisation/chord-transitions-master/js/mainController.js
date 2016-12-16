angular.module('app', []);

angular.module('app').controller('mainCntrl', ['$scope',
function ($scope) {

  $scope.master = {}; // MASTER DATA STORED BY frameworkContract

  $scope.selected_frameworkContract = "FP6";
  $scope.frameworkContracts = ["FP6","FP7","H2020"];//d3.range(2005, 1865, -5);

  $scope.filters = {};
  $scope.hasFilters = false;

  $scope.tooltip = {};

  // FORMATS USED IN TOOLTIP TEMPLATE IN HTML
  $scope.pFormat = d3.format(".1%");  // PERCENT FORMAT
  $scope.qFormat = d3.format(",.0f"); // COMMAS FOR LARGE NUMBERS

  $scope.updateTooltip = function (data) {
    $scope.tooltip = data;
    $scope.$apply();
  }

  $scope.addFilter = function (name) {
    $scope.hasFilters = true;
    $scope.filters[name] = {
      name: name,
      hide: true
    };
    $scope.$apply();
  };

  $scope.update = function () {
    var data = $scope.master[$scope.selected_frameworkContract];

    if (data && $scope.hasFilters) {
      $scope.drawChords(data.filter(function (d) {
        var fl = $scope.filters;
        var v1 = d.country1, v2 = d.country2;

        if ((fl[v1] && fl[v1].hide) || (fl[v2] && fl[v2].hide)) {
          return false;
        }
        return true;
      }));
    } else if (data) {
      $scope.drawChords(data);
    }
  };

  // IMPORT THE CSV DATA
  d3.csv('../data/test.csv', function (err, data) {

    data.forEach(function (d) {
      d.frameworkContract  = + parseFloat(d.id);
      d.nbLinkTmp = + parseFloat(d.nbLinkTmp);
      //d.flow2 = +d.nbLinkTmp;

      if (!$scope.master[d.frameworkContract]) {
        $scope.master[d.frameworkContract] = []; // STORED BY frameworkContract
      }
      $scope.master[d.frameworkContract].push(d);
    })
    $scope.update();
  });

  $scope.$watch('selected_frameworkContract', $scope.update);
  $scope.$watch('filters', $scope.update, true);

}]);
