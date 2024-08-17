$(function() {

  var shoreham_g=  Morris.Area({
        element: 'area-example2',
        data: [{
            period: '2010 Q1',
            usart: 2
        }, {
            period: '2010 Q2',
            usart: 3
        }, {
            period: '2010 Q3',
            usart: 4
        }, {
            period: '2010 Q4',
            usart: 5
        }, {
            period: '2011 Q1',
            usart: 6
        }, {
            period: '2011 Q2',
            usart: 7
        }, {
            period: '2011 Q3',
            usart: 8
        }, {
            period: '2011 Q4',
            usart: 11
        }, {
            period: '2012 Q1',
            usart: 12
        }, {
            period: '2012 Q2',
            usart: 13
        }],
        xkey: 'period',
        ykeys: ['usart'],
        labels: ['Usart Data'],
        hideHover: 'auto',
        resize: true
    });
});
   