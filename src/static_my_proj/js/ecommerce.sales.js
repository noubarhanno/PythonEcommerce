$(document).ready(function(){

  function renderChart(id, data, labels){
    // var ctx = document.getElementById("myChart").getContext('2d');

    var ctx = $('#' + id)
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sales',
                data: data,
                backgroundColor: 'rgba(104, 162, 115, 0.3)',
                borderColor: 'rgba(104, 162, 115, 1)',
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
  }

  function getSalesData(id, type){
    var url = '/analytics/sales/data/'
    var method = 'GET'
    var data = {"type": type}

    $.ajax({
      url: url,
      method: method,
      data: data,
      success: function(responseData){
        renderChart(id, responseData.data, responseData.labels)
      },
      error: function(error){
        $.alert(error)
      }
    })
  }

  // getSalesData('thisWeekSales', 'week')
  // getSalesData('FourWeekSales', '4weeks')
  var chartToRender = $('.ecommerce-render-chart')
  $.each(chartToRender, function(index, html){
    var $this = $(this)
    if ($this.attr('id') && $this.attr('data-type'))
    {
      getSalesData($this.attr('id'), $this.attr('data-type'))
    }
  })

})
