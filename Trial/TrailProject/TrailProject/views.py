from django.shortcuts import render
from django.http import JsonResponse
import json

def facts(request):
    import cx_Oracle
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''
select 'Customers' as name , count(*) as tuple_count from vvarma.customers union
select 'Delivery' as name, count(*) as a from vvarma.delivery union
select 'Geolocation' , count(*) as a from vvarma.geolocation union
select 'Orders', count(*) as a from vvarma.orders union
select 'Payments',count(*) as a from vvarma.payments union
select 'Product',count(*) as a from vvarma.product union
select 'Product Category',count(*) as a from vvarma.productcategory union
select 'Product SuperCategory',count(*) as a from vvarma.productsupercategory union
select 'Products Ordered',count(*) as a from vvarma.productsordered union
select 'Reviews',count(*) as a from vvarma.reviews union
select 'Sellers',count(*) as a from vvarma.sellers union
select 'Total', sum(a) tuple_count from 
(
select 'Customers' as name , count(*) as a from vvarma.customers union
select 'Delivery' as name, count(*) as a from vvarma.delivery union
select 'Geolocation' , count(*) as a from vvarma.geolocation union
select 'Orders', count(*) as a from vvarma.orders union
select 'Payments',count(*) as a from vvarma.payments union
select 'Product',count(*) as a from vvarma.product union
select 'Product_Category',count(*) as a from vvarma.productcategory union
select 'Product_SuperCategory',count(*) as a from vvarma.productsupercategory union
select 'Products_Ordered',count(*) as a from vvarma.productsordered union
select 'Reviews',count(*) as a from vvarma.reviews union
select 'Sellers',count(*) as a from vvarma.sellers
)''')
    Customers=0;Delivery=0;Geolocation=0;Orders=0;Payments=0;Product=0;Product_Category=0;
    Product_SuperCategory=0;Products_Ordered=0;Reviews=0;Sellers=0;Total=0
    for row in c:
        if(row[0]=='Customers'):
            Customers=row[1]
        elif(row[0]=='Delivery'):
            Delivery=row[1]
        elif (row[0] == 'Geolocation'):
            Geolocation = row[1]
        elif (row[0] == 'Orders'):
            Orders = row[1]
        elif (row[0] == 'Payments'):
            Payments = row[1]
        elif (row[0] == 'Product'):
            Product = row[1]
        elif (row[0] == 'Product Category'):
            Product_Category = row[1]
        elif (row[0] == 'Product SuperCategory'):
            Product_SuperCategory = row[1]
        elif (row[0] == 'Products Ordered'):
            Products_Ordered = row[1]
        elif (row[0] == 'Reviews'):
            Reviews = row[1]
        elif (row[0] == 'Sellers'):
            Sellers = row[1]
        elif (row[0] == 'Total'):
            Total = row[1]

    c.execute('''select c.customer_state,count(o.order_id)as orders from orders o
    join stg_customers c on o.customer_id=c.customer_id
    group by c.customer_state
    order by 2 desc''')
    x1 = []
    x1.append(['State', 'Orders'])
    for row in c:
        x1.append([row[0], row[1]])

    return render(request, 'Facts.html', {'Customers': Customers,'Delivery': Delivery,
                                          'Geolocation': Geolocation,'Orders': Orders,'Payments': Payments,
                                          'Product': Product,'Product_Category': Product_Category,
    'Product_SuperCategory': Product_SuperCategory,'Products_Ordered': Products_Ordered,'Reviews': Reviews,
                                          'Sellers': Sellers,'Total': Total,
                                          'data': x1})


def olisthome(request):
    import cx_Oracle
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''select c.customer_state,count(o.order_id)as orders from orders o
join stg_customers c on o.customer_id=c.customer_id
group by c.customer_state
order by 2 desc''')
    x1 = []
    x1.append(['State', 'Orders'])
    for row in c:
        x1.append([row[0], row[1]])
    c.execute('''select sum(a) tuple_count from 
    (
    select count(*) as a from vvarma.customers union
    select count(*) as a from vvarma.delivery union
    select count(*) as a from vvarma.geolocation union
    select count(*) as a from vvarma.orders union
    select count(*) as a from vvarma.payments union
    select count(*) as a from vvarma.product union
    select count(*) as a from vvarma.productcategory union
    select count(*) as a from vvarma.productsupercategory union
    select count(*) as a from vvarma.productsordered union
    select count(*) as a from vvarma.reviews union
    select count(*) as a from vvarma.sellers
    )''')
    tuple_count = 0
    for row in c:
        tuple_count = row[0]
    return render(request, 'OlistHome.html', {'data': x1,'tuple_count': tuple_count})
def olistexe(request):
    print('hi from olistexe')
    import cx_Oracle
    import plotly.graph_objects as go
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''
        select substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year, count(customer_id) as customers
    from vvarma.orders
    group by substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4)
    order by 1 asc''')
    customer_year = []
    customer_count = []
    for row in c:
        customer_year.append(row[0])
        customer_count.append(row[1])
    c.execute('''select total, ontime, round((ontime/total)*100,2) as deliveredontimepercentage from (select count(*) as total from  vvarma.delivery),
(select count(*) as ontime
from vvarma.delivery where order_delivered_customer_date <= order_estimated_delivery_date)''')
    total_orders=0
    total_orders_ontime=0
    for row in c:
        total_orders=row[0]
        total_orders_ontime=row[1]

    c.execute('''select last1.MonthYear,deliveredontimepercentage,sales from 
(
select substr(d.month,0,3)||d.year as MonthYear,deliveredontimepercentage from
(
select a.month,a.monthnumber,a.year,ontime,total,round((ontime/total)*100,2) as deliveredontimepercentage from (
select trim(substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),0,4) as year,count(*) as ontime
from vvarma.delivery where order_delivered_customer_date <= order_estimated_delivery_date
group by 
trim(substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),9)),
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/mm'),9),
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),0,4)
) a 
join
(
select trim(substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),0,4) as year,count(*) as total from  vvarma.delivery
group by 
trim(substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),9)),
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/mm'),9),
substr(TO_CHAR(order_delivered_customer_date,'yyyy/dd/Month'),0,4)
) b
on a.month=b.month and a.year=b.year
order by 3 asc, 2 asc
) d
) last1 
join
(
select substr(d.month,0,3)||d.year as MonthYear, sales from
(
select
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year,
sum(item_price+order_freight_value) as sales from vvarma.productsordered po
join vvarma.orders o on po.order_id=o.order_id
group by 
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)),
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9),
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by 3 asc, 2 asc
)d
) last2 
on last1.monthyear=last2.monthyear''')
    month_year=[]
    ontime_delivery_rate=[]
    sales_month_year=[]
    for row in c:
        month_year.append(row[0])
        ontime_delivery_rate.append(row[1])
        sales_month_year.append(row[2])

    c.execute('''select payment_type, count(payment_type) from vvarma.payments where payment_type<>'not_defined'
group by payment_type order by 2 desc''')
    payment_methods=[]
    number_of_payments=[]
    for row in c:
        payment_methods.append(row[0])
        number_of_payments.append(row[1])
    c.execute('''
    select a.product_super_category,a.month,a.monthnumber,a.year,nvl(b.sales,0) as sales from
(select * from (
select distinct(product_super_category) from vvarma.productsupercategory)
cross join (select * from datelookup where year='2017') )a
left join
(select sum(po.item_price+po.order_freight_value) as sales, psc.product_super_category,
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year
from vvarma.productsordered po
join vvarma.product p 
on po.product_id=p.product_id
join vvarma.productcategory pc
on p.product_category_id=pc.product_category_id
join orders o
on po.order_id=o.order_id
join (select * from vvarma.delivery d where d.order_status='delivered') d 
on o.order_id=d.order_id
join vvarma.productsupercategory psc
on pc.product_category_id=psc.product_category_id
group by  psc.product_super_category,
trim(substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),9)),
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm'),9),
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm'),9) asc,
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4) asc) b
on a.product_super_category=b.product_super_category
and a.month=b.month
and a.monthnumber=b.monthnumber
and a.year=b.year
order by a.monthnumber,a.year,a.product_super_category''')
    product_super_category=[]
    Electronic_Sales=[]
    Household_Sales=[]
    Others_Sales=[]
    PersonalCare_Sales=[]
    Sports_Sales=[]
    Month=[]
    for row in c:
        if(row[0]=='Electronics'):
            Electronic_Sales.append(row[4])
        elif(row[0]=='Household'):
            Household_Sales.append(row[4])
        elif(row[0]=='Others'):
            Others_Sales.append(row[4])
        elif(row[0]=='Personal Care'):
            PersonalCare_Sales.append(row[4])
        else:
            Sports_Sales.append(row[4])
    c.execute('''select month from datelookup where rownum<=12''')
    for row in c:
        Month.append(row[0])

    data1 = { 'customer_year': customer_year, 'customer_count': customer_count, 'total_orders': total_orders, 'total_orders_ontime': total_orders_ontime,
              'payment_methods': payment_methods, 'number_of_payments': number_of_payments, 'Month': Month,
              'Electronic_Sales': Electronic_Sales, 'Household_Sales': Household_Sales,
              'Others_Sales': Others_Sales, 'PersonalCare_Sales': PersonalCare_Sales,
              'Sports_Sales': Sports_Sales,
              'month_year': month_year, 'ontime_delivery_rate': ontime_delivery_rate,'sales_month_year': sales_month_year}
    return render(request, 'OlistExe.html', {'data2': json.dumps(data1)})
def customer(request):
    print('hi from customer')
    product_super_category = ''
    view_by=''
    if request.method == 'POST':
        product_super_category = request.POST['product_super_category']
        view_by = request.POST['view_by']
        print(product_super_category)
        print(view_by)
    import cx_Oracle
    import plotly.graph_objects as go
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''select psc.product_super_category, count(distinct(order_id)) no_of_orders from vvarma.productsordered po
join vvarma.product p on po.product_id=p.product_id
join vvarma.productsupercategory psc on p.product_category_id=psc.product_category_id
group by psc.product_super_category
order by 2 desc''')
    product_category = []
    no_of_orders = []
    for row in c:
        product_category.append(row[0])
        no_of_orders.append(row[1])
    c.execute('''
    select substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year, count(customer_id) as customers
from vvarma.orders
group by substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by 1 asc''')
    customer_year=[]
    customer_count=[]
    for row in c:
        customer_year.append(row[0])
        customer_count.append(row[1])

    c.execute('''select distinct product_super_category from vvarma.productsupercategory order by 1 asc''')
    pc = []
    for row in c:
        pc.append(row[0])
    d = {'val': product_super_category}
    if(view_by=='Delivery Rate' or view_by==''):
        if (product_super_category == '' or product_super_category == 'All'):
            c.execute('''select a.seller_id ,a.total, b.ontime,round((b.ontime/a.total) *100,2) as percent, rank() over (order by round((b.ontime/a.total) *100,2) desc) 
            as rank from (select seller_id, count(*) as total 
            from vvarma.productsordered po , vvarma.delivery d where d.order_id=po.order_id  group by seller_id) a,
            (select seller_id, count(*) as ontime
            from vvarma.productsordered  po , vvarma.delivery d where d.order_id=po.order_id and 
            order_delivered_customer_date <= order_estimated_delivery_date group by seller_id) b where a.seller_id=b.seller_id 
            and a.total>=100 
            and rownum<=10
            order by 5 asc''')
        else:
            c.execute('''select seller_id,total,ontime,percent,rank,product_super_category from 
            (
            select * from (select a.product_super_category,a.seller_id ,a.total, b.ontime,round((b.ontime/a.total) *100,2) as percent, rank() over 
            (partition by a.product_super_category order by round((b.ontime/a.total) *100,2) desc) 
            as rank from (select ps.product_super_category, seller_id, count(*) as total 
            from vvarma.productsordered po ,vvarma.product p, vvarma.productsupercategory ps, vvarma.delivery d where d.order_id=po.order_id and 
            po.product_id=p.product_id and p.product_category_id=ps.product_category_id group by ps.product_super_category,seller_id) a,
            (select ps1.product_super_category,seller_id, count(*) as ontime
            from vvarma.productsordered po1 , vvarma.delivery d1, vvarma.product p1, vvarma.productsupercategory ps1 where d1.order_id=po1.order_id and  
            po1.product_id=p1.product_id and p1.product_category_id=ps1.product_category_id and 
            order_delivered_customer_date <= order_estimated_delivery_date group by ps1.product_super_category,seller_id) b 
            where a.seller_id=b.seller_id 
            and a.total>=100 and a.product_super_category=b.product_super_category order by 5 asc) where rank<=10 order by 1,6 asc
            ) where product_super_category=:val''', d)
    else:
        if (product_super_category == '' or product_super_category == 'All'):
            c.execute('''select seller_id,product_super_category,product_super_category_id,average,"rank1" from
(
select * from (select ps.product_super_category,ps.product_super_category_id,s.seller_id,round(avg(r.review_score),2) as average, rank() over(
 order by avg(review_score) desc) "rank1" from vvarma.orders o, vvarma.reviews r, vvarma.sellers s, vvarma.productsordered po, vvarma.productsupercategory ps, vvarma.product p
where r.order_id=o.order_id and po.seller_id=s.seller_id and
po.order_id=o.order_id and ps.product_category_id=p.product_category_id and  p.product_id=po.product_id  group by 
ps.product_super_category,ps.product_super_category_id, s.seller_id having count(*)>30) where "rank1"<=10 order by 5 asc
)''')
        else:
            c.execute('''select seller_id,product_super_category,product_super_category_id,average,"rank1" from
(
select * from (select ps.product_super_category,ps.product_super_category_id,s.seller_id,round(avg(r.review_score),2) as average, rank() over(partition by ps.product_super_category
 order by avg(review_score) desc) "rank1" from vvarma.orders o, vvarma.reviews r, vvarma.sellers s, vvarma.productsordered po, vvarma.productsupercategory ps, vvarma.product p
where r.order_id=o.order_id and po.seller_id=s.seller_id and
po.order_id=o.order_id and ps.product_category_id=p.product_category_id and  p.product_id=po.product_id  group by 
ps.product_super_category,ps.product_super_category_id, s.seller_id having count(*)>30) where "rank1"<=10 order by 1,5 asc
) where product_super_category=:val''',d)

    seller_id = []
    rating = []
    for row in c:
        seller_id.append(row[0])
        rating.append(row[3])


    data1 = {'product_category': product_category, 'no_of_orders': no_of_orders, 'customer_year': customer_year, 'customer_count': customer_count
             , 'pc': pc, 'seller_id': seller_id, 'rating': rating, 'selected_category':product_super_category ,'view_by': view_by}
    # return render(request, 'Customer.html', {'data2': json.dumps(data1)})
    return render(request, 'Customer.html', {'data2': data1})
def customer_products(request):
    print("hiiiiiiiiii")
    print(request.GET['label1'])
    val1=request.GET['label1']
    import cx_Oracle
    import plotly.graph_objects as go
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    d = {'val': val1}
    if(len(val1)<20):
        c.execute('''select * from(
select p.product_id, count(distinct(order_id)) as no_of_orders from vvarma.productsordered po
join vvarma.product p on po.product_id=p.product_id
join vvarma.productsupercategory psc on p.product_category_id=psc.product_category_id
and psc.product_super_category=:val
group by p.product_id
order by 2 desc)
where rownum<=10''', d)
    else:
        c.execute('''
        select psc.product_super_category, count(distinct(order_id)) no_of_orders from vvarma.productsordered po
join vvarma.product p on po.product_id=p.product_id
join vvarma.productsupercategory psc on p.product_category_id=psc.product_category_id
group by psc.product_super_category
order by 2 desc''')

    product_id = []
    product_count = []
    for row in c:
        product_id.append(row[0])
        product_count.append(row[1])
    data1 = {'products': product_id, 'products_count': product_count, 'category': val1}
    return JsonResponse(data1)
def customer_next(request):
    print('hi from next')
    product_super_category=''
    if request.method=='POST':
        product_super_category=request.POST['product_super_category']
        print(product_super_category)
    import cx_Oracle
    import plotly.graph_objects as go
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''select distinct product_super_category from vvarma.productsupercategory order by 1 asc''')
    pc = []
    pc.append('All')
    for row in c:
        pc.append(row[0])
    d = {'val': product_super_category}
    if (product_super_category == '' or product_super_category == 'All'):
        c.execute('''select a.seller_id ,a.total, b.ontime,round((b.ontime/a.total) *100,2) as percent, rank() over (order by round((b.ontime/a.total) *100,2) desc) 
    as rank from (select seller_id, count(*) as total 
    from vvarma.productsordered po , vvarma.delivery d where d.order_id=po.order_id  group by seller_id) a,
    (select seller_id, count(*) as ontime
    from vvarma.productsordered  po , vvarma.delivery d where d.order_id=po.order_id and 
    order_delivered_customer_date <= order_estimated_delivery_date group by seller_id) b where a.seller_id=b.seller_id 
    and a.total>=100 
    and rownum<=10
    order by 5 asc''')
    else:
        c.execute('''select seller_id,total,ontime,percent,rank,product_super_category from 
    (
    select * from (select a.product_super_category,a.seller_id ,a.total, b.ontime,round((b.ontime/a.total) *100,2) as percent, rank() over 
    (partition by a.product_super_category order by round((b.ontime/a.total) *100,2) desc) 
    as rank from (select ps.product_super_category, seller_id, count(*) as total 
    from vvarma.productsordered po ,vvarma.product p, vvarma.productsupercategory ps, vvarma.delivery d where d.order_id=po.order_id and 
    po.product_id=p.product_id and p.product_category_id=ps.product_category_id group by ps.product_super_category,seller_id) a,
    (select ps1.product_super_category,seller_id, count(*) as ontime
    from vvarma.productsordered po1 , vvarma.delivery d1, vvarma.product p1, vvarma.productsupercategory ps1 where d1.order_id=po1.order_id and  
    po1.product_id=p1.product_id and p1.product_category_id=ps1.product_category_id and 
    order_delivered_customer_date <= order_estimated_delivery_date group by ps1.product_super_category,seller_id) b 
    where a.seller_id=b.seller_id 
    and a.total>=100 and a.product_super_category=b.product_super_category order by 5 asc) where rank<=10 order by 1,6 asc
    ) where product_super_category=:val''', d)
    seller_id=[]
    rating=[]
    for row in c:
        seller_id.append(row[0])
        rating.append(row[3])
    data1= {'pc': pc, 'seller_id': seller_id, 'rating': rating, 'selected_category':product_super_category}
    return render(request, 'CustomerNext.html', {'data2': data1})
def customer_count_monthly(request):
    print(request.GET['label1'])
    val1 = request.GET['label1']
    import cx_Oracle
    import plotly.graph_objects as go
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    d = {'val': val1}
    customer_month = []
    customer_count = []
    customer_count_2016 = []
    customer_count_2017 = []
    customer_count_2018 = []
    if(val1 in ('2016','2017','2018')):
        c.execute('''
        select month,year,customers from (
select d.month,d.monthnumber,d.year,nvl(c.customers,0) as customers from datelookup d 
left outer join
(select Month,monthnumber,year,customers from(
select trim(substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year,
count(customer_id) as customers
from vvarma.orders
group by substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),9)
,substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm'),9)
,substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by 2 asc)) c 
on d.month=c.month and c.year=d.year and c.monthnumber=d.monthnumber
order by d.monthnumber,d.year) where year=:val''',d)
        for row in c:
            if(row[1]=='2018'):
                customer_count_2018.append(row[2])
            elif(row[1]=='2017'):
                customer_count_2017.append(row[2])
            else:
                customer_count_2016.append(row[2])
        c.execute('''select month from datelookup where rownum<=12''')
        for row in c:
            customer_month.append(row[0])
    else:
        c.execute('''
        select substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year, count(customer_id) as customers
    from vvarma.orders
    group by substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/Month'),0,4)
    order by 1 asc
        ''')
        for row in c:
            customer_count.append(row[1])
    data1 = {'customer_month': customer_month, 'customer_count_2018': customer_count_2018, 'customer_count_2017': customer_count_2017, 'customer_count_2016': customer_count_2016,
             'customer_count': customer_count}
    return JsonResponse(data1)

def seller(request):
    print('hi from seller')
    seller_id = '4a3ca9315b744ce9f8e9374361493884'
    if request.method == 'POST':
        seller_id = request.POST['seller_id']
    import cx_Oracle
    dsn_tns = cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
    conn = cx_Oracle.connect(user='prajan', password='Sangeetha28', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''select count(order_id) number_of_orders,substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm hh24:mm:ss'),12,2) as hour,
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm hh24:mm:ss'),0,4) as year
from orders
group by substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm hh24:mm:ss'),12,2),
substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm hh24:mm:ss'),0,4)
order by 2 asc''')
    number_of_orders_2016=[]
    number_of_orders_2017 = []
    number_of_orders_2018 = []
    hour=[]
    for row in c:
        if(row[2]=='2018'):
            number_of_orders_2018.append(row[0])
        elif (row[2] == '2017'):
            number_of_orders_2017.append(row[0])
        else:
            number_of_orders_2016.append(row[0])
    c.execute('''select distinct(substr(TO_CHAR(order_purchase_timestamp,'yyyy/dd/mm hh24:mm:ss'),12,2)) as hour
from orders
order by 1 asc''')
    for row in c:
        hour.append(row[0])
    c.execute('''select c.customer_state,count(o.order_id)as orders from orders o
    join stg_customers c on o.customer_id=c.customer_id
    group by c.customer_state
    order by 2 desc''')
    x1 = []
    x2=[]
    x1.append(['State', 'Orders'])
    for row in c:
        x1.append([row[0], row[1]])
        x2.append([row[0], row[1]])
    c.execute('''
    select e.seller_id,d.month,d.monthnumber, substr(d.month,0,3)||d.year as MonthYear,d.year,nvl(e.sales,0) as sales
from (select * from datelookup where year!='2016') d 
left join
(
select * from(
select seller_id,
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year,
sum(item_price+order_freight_value) as sales from vvarma.productsordered po
join vvarma.orders o on po.order_id=o.order_id
group by seller_id,
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)),
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9),
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by 5 desc
)
where seller_id=(
select seller_id
from vvarma.productsordered po
join vvarma.orders o on po.order_id=o.order_id
group by seller_id
having sum(item_price+order_freight_value)=
(
select max(sum(item_price+order_freight_value))
from vvarma.productsordered po
join vvarma.orders o on po.order_id=o.order_id
group by seller_id))
order by year asc,monthnumber asc
) e
on d.month=e.month and d.year=e.year
order by year asc,monthnumber asc''')
    month_year=[]
    sales=[]
    top_seller='4869f7a5dfa277a7dca6462dcf3b52b2'
    for row in c:
        month_year.append(row[3])
        sales.append(row[5])
    d={'val': seller_id}
    # c.execute('''
    # select * from vvarma.sellers where seller_id=:val''',d)
    # for row in c:
    #     if row[0]:
    #         flag=True
    #         break
    # if(flag==False):
    #     seller_id='4a3ca9315b744ce9f8e9374361493884'
    c.execute('''
    select e.seller_id,d.month,d.monthnumber, substr(d.month,0,3)||d.year as MonthYear,d.year,nvl(e.sales,0) as sales
from (select * from datelookup where year!='2016') d 
left join
(
select * from(
select seller_id,
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)) as month,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9) as monthnumber,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year,
sum(item_price+order_freight_value) as sales from vvarma.productsordered po
join vvarma.orders o on po.order_id=o.order_id
group by seller_id,
trim(substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),9)),
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/mm'),9),
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by 5 desc
)
where seller_id=:val
order by year asc,monthnumber asc
) e
on d.month=e.month and d.year=e.year
order by year asc,monthnumber asc''',d)
    sales_2nd = []

    for row in c:
        sales_2nd.append(row[5])

    c.execute('''select distinct seller_id from vvarma.sellers''')
    seller_id_list = []
    for row in c:
        seller_id_list.append(row[0])

    c.execute('''select * from
(
select seller_id,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4) as year,
sum(item_price+order_freight_value) as sales from vvarma.productsordered po
join vvarma.orders o on po.order_id=o.order_id
group by seller_id,
substr(TO_CHAR(o.order_purchase_timestamp,'yyyy/dd/Month'),0,4)
order by 2 desc, 3 desc
) where rownum=1''')
    top_seller = ''
    for row in c:
        top_seller=row[0]



    data1={'hour': hour, 'number_of_orders_2016': number_of_orders_2016, 'number_of_orders_2017': number_of_orders_2017, 'number_of_orders_2018': number_of_orders_2018
           ,'data': x1, 'state_sales': x2, 'month_year': month_year, 'sales': sales,
           'sales_2nd': sales_2nd, 'seller_id_list': seller_id_list }
    # return render(request, 'Seller.html', {'data2': json.dumps(data1)})
    return render(request, 'Seller.html', {'data2': data1, 'top_seller': top_seller})

